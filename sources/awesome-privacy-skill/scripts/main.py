"""
awesome-privacy-skill
OpenClaw Action Protocol: stdin/stdout JSON communication.

Agent 调用方式（stdin JSON）：
  {"action": "redact_file",       "file_path": "..."}
  {"action": "redact_file",       "file_path": "...", "keyword_rules": [...]}
  {"action": "redact_content",   "content": "..."}
  {"action": "redact_content",    "content": "...", "keyword_rules": [...]}
  {"action": "unmask",           "content": "...", "mapping": [...]}
  {"action": "detect",            "content": "..."}
  {"action": "validate",          "redacted_content": "..."}
"""

import json
import os
import sys
from pathlib import Path

# Ensure scripts/ is on the import path
_parent = str(Path(__file__).resolve().parent.parent)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from scripts.core.detector import SensitiveDataDetector
from scripts.core.redaction import Redactor
from scripts.core.unmasker import Unmasker
from scripts.handlers.pdf_handler import PDFHandler
from scripts.handlers.excel_handler import ExcelHandler
from scripts.handlers.word_handler import WordHandler
from scripts.handlers.markdown_handler import MarkdownHandler
from scripts.handlers.image_handler import ImageHandler
from scripts.config.settings import Settings


class PrivacyShield:
    """
    Privacy Shield v1.1 — local sensitive data redaction and unmasking.

    Key improvements in v1.1:
    - WordHandler now supports writing redacted files back to disk.
    - redact_hybrid() combines keyword-table + pattern-based redaction.
    - validate() checks redacted content for remaining sensitive data.
    - keyword_rules: exact-match keyword → placeholder for high-confidence redaction.
    - Output file saved automatically with _redacted suffix.
    """

    def __init__(self):
        self.settings = Settings()
        self.detector = SensitiveDataDetector(self.settings)
        self.redactor = Redactor(self.settings)
        self.unmasker = Unmasker()

        self.handlers = {
            ".pdf": PDFHandler(self.settings),
            ".xlsx": ExcelHandler(self.settings),
            ".xls": ExcelHandler(self.settings),
            ".docx": WordHandler(self.settings),
            ".md": MarkdownHandler(self.settings),
            ".markdown": MarkdownHandler(self.settings),
            ".jpg": ImageHandler(self.settings),
            ".jpeg": ImageHandler(self.settings),
            ".png": ImageHandler(self.settings),
        }

    def _get_output_path(self, original_path: str) -> str:
        """Generate output path: original_name_redacted.ext"""
        path = Path(original_path)
        suffix = self.settings.get("output", "suffix", default="_redacted")
        return str(path.parent / f"{path.stem}{suffix}{path.suffix}")

    def action_redact_file(
        self,
        file_path: str,
        keyword_rules: list = None,
        disable_types: list = None,
        redact_mode: str = None,
    ) -> dict:
        """
        Redact sensitive data from a file.
        Saves redacted file back to disk (with _redacted suffix by default).

        Returns:
            {
                "status": "success",
                "redacted_content": "...",
                "mapping": [...],
                "detections": [...],
                "output_path": "...",   # New in v1.1
                "file_type": ".docx",
                "file_name": "report.docx",
            }
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix not in self.handlers:
            return {
                "status": "error",
                "message": f"Unsupported file format: {suffix}",
            }

        # ── PDF image-level redaction (v1.2 new feature) ──
        # When redact_mode="image" is specified for PDFs, use the image-level
        # redaction method which renders PDF to high-res image, masks sensitive
        # regions with black bars, and embeds back into a new PDF.
        # This is the recommended approach for graphical PDFs.
        if suffix == ".pdf" and redact_mode == "image":
            if not keyword_rules:
                return {
                    "status": "error",
                    "message": "keyword_rules is required for image-level PDF redaction",
                }
            pdf_handler = self.handlers[".pdf"]
            output_path = self._get_output_path(file_path)
            try:
                result = pdf_handler.redact_image_level(
                    input_path=file_path,
                    output_path=output_path,
                    keyword_rules=keyword_rules,
                    custom_patterns=None,
                    zoom=4,
                )
            except Exception as e:
                return {"status": "error", "message": str(e)}

            if result.get("status") == "success":
                return {
                    "status": "success",
                    "output_path": result.get("output_path"),
                    "mapping": [
                        {"type": ph.split("_")[1] if "_" in ph else "CUSTOM",
                         "index": i + 1,
                         "original": orig,
                         "marker": f"[{ph}]"}
                        for i, (ph, orig) in enumerate(result.get("mapping", {}).items())
                    ],
                    "detections": [],
                    "file_type": ".pdf",
                    "file_name": path.name,
                    "redact_mode": "image",
                    "total_rects": result.get("total_rects", 0),
                }
            else:
                return {"status": "error", "message": result.get("details", "Unknown error")}

        handler = self.handlers[suffix]
        content = handler.read(file_path)
        if content is None:
            return {
                "status": "error",
                "message": f"Failed to read file: {file_path}",
            }

        # Keyword rules take precedence; skip pattern detection when disable_types
        # is provided (to avoid false positives from broad patterns like ADDRESS)
        skip_patterns = bool(keyword_rules and disable_types)
        if keyword_rules:
            redacted_content, mapping = self.redactor.redact_hybrid(
                content, keyword_rules,
                skip_pattern_detection=skip_patterns,
            )
            detections_list = [
                {"type": d["type"], "value": d["original"], "start": -1, "end": -1}
                for d in mapping
            ]
        else:
            detections = self.detector.detect(content)
            # Apply disable_types filter
            if disable_types:
                detections = [d for d in detections if d.type not in disable_types]
            redacted_content, mapping = self.redactor.redact(content, detections)
            detections_list = [
                {"type": d.type, "value": d.value, "start": d.start, "end": d.end}
                for d in detections
            ]

        # Save redacted file (v1.1 new feature)
        output_path = None
        if self.settings.get("output", "save_file", default=True):
            try:
                # Build keyword→placeholder map from mapping
                # Supports both marker formats:
                #   - "[████TYPE_1]"     (write_with_mapping format)
                #   - "<<REDACTED_TYPE_1>>" (redact() default format)
                kw_map = {}
                for item in mapping:
                    marker = item["marker"]
                    if marker.startswith("[") and "]" in marker:
                        # Square bracket format: [████TYPE_1]
                        ph = marker[1 : marker.index("]")]
                        kw_map[item["original"]] = ph
                    elif marker.startswith("<<") and ">>" in marker:
                        # Angle bracket format: <<REDACTED_TYPE_1>>
                        # Convert to write format: [████TYPE_1] → keep as <<REDACTED>>
                        # For angle brackets, use the raw marker as-is for replacement
                        ph = marker  # e.g. "<<REDACTED_NAME_1>>"
                        kw_map[item["original"]] = ph

                if hasattr(handler, "write_with_mapping"):
                    output_path = self._get_output_path(file_path)
                    success = handler.write_with_mapping(
                        output_path, file_path, kw_map
                    )
                    if not success:
                        output_path = None
                elif hasattr(handler, "write"):
                    output_path = self._get_output_path(file_path)
                    success = handler.write(output_path, redacted_content, file_path)
                    if not success:
                        output_path = None
            except Exception:
                output_path = None

        result = {
            "status": "success",
            "redacted_content": redacted_content,
            "mapping": mapping,
            "detections": detections_list,
            "file_type": suffix,
            "file_name": path.name,
        }
        if output_path:
            result["output_path"] = output_path

        return result

    def action_redact_content(
        self, content: str, keyword_rules: list = None, disable_types: list = None
    ) -> dict:
        """
        Redact sensitive data from text content.

        New in v1.1: keyword_rules parameter for exact-match redaction.
        """
        if keyword_rules:
            redacted_content, mapping = self.redactor.redact_hybrid(
                content, keyword_rules
            )
            detections_list = [
                {"type": d["type"], "value": d["original"], "start": -1, "end": -1}
                for d in mapping
            ]
        else:
            detections = self.detector.detect(content)
            if disable_types:
                detections = [d for d in detections if d.type not in disable_types]
            redacted_content, mapping = self.redactor.redact(content, detections)
            detections_list = [
                {
                    "type": d.type,
                    "value": d.value,
                    "start": d.start,
                    "end": d.end,
                    "confidence": d.confidence,
                }
                for d in detections
            ]

        return {
            "status": "success",
            "redacted_content": redacted_content,
            "mapping": mapping,
            "detections": detections_list,
        }

    def action_unmask(self, content: str, mapping: list) -> dict:
        """Restore original sensitive data from redaction markers."""
        restored = self.unmasker.restore(content, mapping)
        valid, remaining = self.unmasker.validate(restored)

        return {
            "status": "success" if valid else "partial",
            "restored_content": restored,
            "unmasked_count": len(mapping),
            "remaining_markers": remaining if not valid else [],
        }

    def action_detect(self, content: str) -> dict:
        """Detect sensitive data without redacting."""
        detections = self.detector.detect(content)
        return {
            "status": "success",
            "detections": [
                {
                    "type": d.type,
                    "value": d.value,
                    "start": d.start,
                    "end": d.end,
                    "confidence": d.confidence,
                }
                for d in detections
            ],
        }

    def action_validate(self, redacted_content: str) -> dict:
        """
        New in v1.1: Post-redaction validation.
        Scans redacted content for any remaining sensitive patterns.
        """
        result = self.redactor.validate(redacted_content)
        return {"status": "success", "clean": result["clean"], "remaining": result["remaining"]}


def main():
    """Read stdin JSON, execute action, print stdout JSON."""
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({"status": "error", "message": "Invalid JSON input"}))
        sys.exit(1)

    action = input_data.get("action")
    if not action:
        print(json.dumps({"status": "error", "message": "Missing 'action' field"}))
        sys.exit(1)

    tool = PrivacyShield()

    if action == "redact_file":
        result = tool.action_redact_file(
            input_data.get("file_path", ""),
            input_data.get("keyword_rules"),
            input_data.get("disable_types"),
            input_data.get("redact_mode"),
        )

    elif action == "redact_content":
        result = tool.action_redact_content(
            input_data.get("content", ""),
            input_data.get("keyword_rules"),
            input_data.get("disable_types"),
        )

    elif action == "unmask":
        result = tool.action_unmask(
            input_data.get("content", ""),
            input_data.get("mapping", []),
        )

    elif action == "detect":
        result = tool.action_detect(input_data.get("content", ""))

    elif action == "validate":
        result = tool.action_validate(input_data.get("redacted_content", ""))

    elif action == "verify_pdf":
        # v1.2 new: OCR-based verification for redacted PDF files
        pdf_handler = tool.handlers.get(".pdf")
        if not pdf_handler:
            result = {"status": "error", "message": "PDF handler not available"}
        else:
            result = pdf_handler.verify_redaction(
                pdf_path=input_data.get("pdf_path", ""),
                sensitive_keywords=input_data.get("sensitive_keywords", []),
            )

    elif action == "redact_pdf_image":
        # v1.2: Direct image-level PDF redaction
        result = tool.action_redact_file(
            input_data.get("file_path", ""),
            input_data.get("keyword_rules"),
            None,
            "image",
        )

    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
