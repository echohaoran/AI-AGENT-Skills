"""
awesome-privacy-skill
OpenClaw Action Protocol: stdin/stdout JSON communication.

Agent 调用方式（stdin JSON）：
  {"action": "redact_file",   "file_path": "..."}
  {"action": "redact_content","content": "..."}
  {"action": "unmask",        "content": "...", "mapping": [...]}
  {"action": "detect",         "content": "..."}
"""

import json
import sys
from pathlib import Path

# Ensure scripts/ is on the import path
_sys_path = [p for p in sys.path if p and p != ""]
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
    """Privacy Shield - local sensitive data redaction and unmasking tool."""

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

    def action_redact_file(self, file_path: str) -> dict:
        """Redact sensitive data from a file."""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix not in self.handlers:
            return {"status": "error", "message": f"Unsupported file format: {suffix}"}

        handler = self.handlers[suffix]
        content = handler.read(file_path)
        if content is None:
            return {"status": "error", "message": f"Failed to read file: {file_path}"}

        detections = self.detector.detect(content)
        redacted_content, mapping = self.redactor.redact(content, detections)

        return {
            "status": "success",
            "redacted_content": redacted_content,
            "mapping": mapping,
            "detections": [
                {"type": d.type, "value": d.value, "start": d.start, "end": d.end}
                for d in detections
            ],
            "file_type": suffix,
            "file_name": path.name,
        }

    def action_redact_content(self, content: str) -> dict:
        """Redact sensitive data from text content."""
        detections = self.detector.detect(content)
        redacted_content, mapping = self.redactor.redact(content, detections)

        return {
            "status": "success",
            "redacted_content": redacted_content,
            "mapping": mapping,
            "detections": [
                {"type": d.type, "value": d.value, "start": d.start, "end": d.end}
                for d in detections
            ],
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
                {"type": d.type, "value": d.value, "start": d.start, "end": d.end, "confidence": d.confidence}
                for d in detections
            ],
        }


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
        result = tool.action_redact_file(input_data.get("file_path", ""))

    elif action == "redact_content":
        result = tool.action_redact_content(input_data.get("content", ""))

    elif action == "unmask":
        result = tool.action_unmask(
            input_data.get("content", ""),
            input_data.get("mapping", []),
        )

    elif action == "detect":
        result = tool.action_detect(input_data.get("content", ""))

    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
