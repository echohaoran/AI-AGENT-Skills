"""
awesome-privacy-skill v1.3
OpenClaw Action Protocol: stdin/stdout JSON communication.

Agent 调用方式（stdin JSON）：
  {"action": "redact_file",       "file_path": "..."}
  {"action": "redact_file",       "file_path": "...", "keyword_rules": [...]}
  {"action": "redact_content",   "content": "..."}
  {"action": "redact_content",    "content": "...", "keyword_rules": [...]}
  {"action": "unmask",           "content": "...", "mapping": [...]}
  {"action": "detect",            "content": "..."}
  {"action": "validate",          "redacted_content": "..."}

  # v1.3 多格式脱敏管道（PDF/图片专用）
  {"action": "redact_multi_format", "file_path": "report.pdf", "keyword_rules": [...]}
  # → OCR原文脱敏 + DOCX转换脱敏 + MD转换脱敏 + PDF图像级遮盖 + 汇总映射表
"""

import json
import os
import sys
import shutil
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
from scripts.handlers.converter import (
    convert_pdf_to_docx,
    convert_pdf_to_markdown,
)
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

    # ═══════════════════════════════════════════════════
    # v1.3 多格式脱敏管道
    # ═══════════════════════════════════════════════════

    def action_redact_multi_format(
        self,
        file_path: str,
        keyword_rules: list = None,
        disable_types: list = None,
    ) -> dict:
        """
        全格式脱敏管道 — 针对 PDF / 图片文件：
        
        1. OCR 原文 → 脱敏（覆盖图形化/扫描件文本）
        2. PDF 图像级遮盖 → 脱敏版 PDF（视觉黑框覆盖）
        3. PDF → DOCX 转换 → 脱敏（保留 Word 格式）
        4. PDF → Markdown 转换 → 脱敏（保留 MD 格式）
        5. 汇总所有脱敏结果 + 统一映射表 + 反脱敏文档

        Args:
            file_path:       源文件路径（.pdf / .jpg / .jpeg / .png）
            keyword_rules:   关键词规则表（推荐）
            disable_types:   禁用的敏感类型列表（可选）

        Returns:
            {
                "status": "success",
                "source_file": "report.pdf",
                "outputs": {
                    "ocr_redacted_txt":   "report_脱敏文本.txt",
                    "pdf_redacted_pdf":   "report_脱敏版.pdf",
                    "docx_redacted":      "report_脱敏版.docx",
                    "md_redacted":        "report_脱敏版.md",
                },
                "mapping": [...],
                "mapping_file": "report_汇总映射表.json",
                "unmask_doc":   "report_反脱敏指南.txt",
                "summary": {
                    "total_items": 15,
                    "types_found": ["NAME", "PHONE", "ID", ...],
                }
            }
        """
        from datetime import datetime

        path = Path(file_path)
        stem = path.stem
        parent = path.parent

        if not path.exists():
            return {"status": "error", "message": f"File not found: {file_path}"}

        suffix = path.suffix.lower()
        is_pdf = suffix == ".pdf"
        is_image = suffix in (".jpg", ".jpeg", ".png")

        if not is_pdf and not is_image:
            return {
                "status": "error",
                "message": (
                    f"redact_multi_format only supports PDF/image files, got: {suffix}. "
                    "Use redact_file instead."
                ),
            }

        # ── 初始化结果容器 ──
        outputs = {}
        all_mapping = []
        all_detections = []
        seen_originals = set()  # 去重

        def _dedup_mapping(new_items: list) -> list:
            """Deduplicate mapping items by original value."""
            deduped = []
            for item in new_items:
                orig = item.get("original", "")
                if orig not in seen_originals:
                    seen_originals.add(orig)
                    deduped.append(item)
            return deduped

        # ============================================================
        # Step 1: OCR → 脱敏（适用于 PDF 图形化文字 + 图片）
        # ============================================================
        ocr_text = None
        if is_pdf:
            pdf_handler = self.handlers[".pdf"]
            ocr_text = pdf_handler.ocr_full_text(file_path)
        elif is_image:
            img_handler = self.handlers[suffix]
            ocr_text = img_handler.extract_text(file_path)

        if ocr_text:
            # 脱敏 OCR 文本
            if keyword_rules:
                ocr_redacted, ocr_mapping = self.redactor.redact_hybrid(
                    ocr_text, keyword_rules
                )
            else:
                ocr_detections = self.detector.detect(ocr_text)
                if disable_types:
                    ocr_detections = [
                        d for d in ocr_detections if d.type not in disable_types
                    ]
                ocr_redacted, ocr_mapping = self.redactor.redact(ocr_text, ocr_detections)
                all_detections.extend(ocr_detections)

            deduped = _dedup_mapping(ocr_mapping)
            all_mapping.extend(deduped)

            # 保存 OCR 脱敏文本
            ocr_txt_path = str(parent / f"{stem}_OCR脱敏.txt")
            Path(ocr_txt_path).write_text(
                f"# ====== OCR 脱敏文本（仅用于查看，不可逆）======\n"
                f"# 源文件: {path.name}\n"
                f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"# 注意：OCR 文本与原文件格式不完全一致\n"
                f"# 推荐使用 PDF/Word/Markdown 脱敏版进行还原\n"
                f"# ===========================================\n\n"
                f"{ocr_redacted}",
                encoding="utf-8",
            )
            outputs["ocr_redacted_txt"] = ocr_txt_path

        # ============================================================
        # Step 2: PDF 图像级遮盖（仅 PDF）→ 脱敏版 PDF
        # ============================================================
        if is_pdf and keyword_rules:
            try:
                pdf_redacted_path = str(parent / f"{stem}_脱敏版.pdf")
                pdf_result = pdf_handler.redact_image_level(
                    input_path=file_path,
                    output_path=pdf_redacted_path,
                    keyword_rules=keyword_rules,
                    zoom=4,
                )
                if pdf_result.get("status") == "success":
                    outputs["pdf_redacted_pdf"] = pdf_result["output_path"]
                    # 去重合并 mapping
                    for k, v in pdf_result.get("mapping", {}).items():
                        if v not in seen_originals:
                            seen_originals.add(v)
                            all_mapping.append({
                                "type": k.split("_")[1] if "_" in k else "CUSTOM",
                                "index": len(all_mapping) + 1,
                                "original": v,
                                "marker": f"[{k}]",
                            })
            except Exception as e:
                pass  # 非致命，继续

        # ============================================================
        # Step 3: PDF → DOCX 转换 → 脱敏
        # ============================================================
        if is_pdf:
            try:
                docx_path = str(parent / f"{stem}_临时转换.docx")
                if convert_pdf_to_docx(file_path, docx_path):
                    docx_handler = self.handlers[".docx"]
                    docx_content = docx_handler.read(docx_path)

                    if docx_content:
                        if keyword_rules:
                            docx_redacted, docx_mapping = self.redactor.redact_hybrid(
                                docx_content, keyword_rules
                            )
                        else:
                            docx_dets = self.detector.detect(docx_content)
                            if disable_types:
                                docx_dets = [d for d in docx_dets if d.type not in disable_types]
                            docx_redacted, docx_mapping = self.redactor.redact(
                                docx_content, docx_dets
                            )
                            all_detections.extend(docx_dets)

                        deduped = _dedup_mapping(docx_mapping)
                        all_mapping.extend(deduped)

                        # 保存脱敏版 DOCX（关键词替换模式）
                        kw_map = {}
                        for item in all_mapping:
                            marker = item["marker"]
                            orig = item["original"]
                            if marker.startswith("[") and "]" in marker:
                                ph = marker[1:marker.index("]")]
                                kw_map[orig] = ph
                            elif marker.startswith("<<") and ">>" in marker:
                                kw_map[orig] = marker

                        docx_redacted_path = str(parent / f"{stem}_脱敏版.docx")
                        if kw_map and hasattr(docx_handler, "write_with_mapping"):
                            ok = docx_handler.write_with_mapping(
                                docx_redacted_path, docx_path, kw_map
                            )
                            if ok:
                                outputs["docx_redacted"] = docx_redacted_path
                        else:
                            docx_handler.write(
                                docx_redacted_path, docx_redacted, docx_path
                            )
                            outputs["docx_redacted"] = docx_redacted_path

                    # 清理临时文件
                    Path(docx_path).unlink(missing_ok=True)
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass  # 非致命

        # ============================================================
        # Step 4: PDF → Markdown 转换 → 脱敏
        # ============================================================
        if is_pdf:
            try:
                md_path = str(parent / f"{stem}_临时转换.md")
                if convert_pdf_to_markdown(file_path, md_path):
                    md_content = Path(md_path).read_text(encoding="utf-8")

                    if keyword_rules:
                        md_redacted, md_mapping = self.redactor.redact_hybrid(
                            md_content, keyword_rules
                        )
                    else:
                        md_dets = self.detector.detect(md_content)
                        if disable_types:
                            md_dets = [d for d in md_dets if d.type not in disable_types]
                        md_redacted, md_mapping = self.redactor.redact(md_content, md_dets)
                        all_detections.extend(md_dets)

                    deduped = _dedup_mapping(md_mapping)
                    all_mapping.extend(deduped)

                    md_redacted_path = str(parent / f"{stem}_脱敏版.md")
                    Path(md_redacted_path).write_text(md_redacted, encoding="utf-8")
                    outputs["md_redacted"] = md_redacted_path

                    # 清理临时文件
                    Path(md_path).unlink(missing_ok=True)
                    # 清理临时图片目录
                    img_dir = Path(md_path).parent / f"{stem}_临时转换_images"
                    if img_dir.exists():
                        shutil.rmtree(img_dir, ignore_errors=True)
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass  # 非致命

        # ============================================================
        # Step 5: 图片专用 — 已通过 Step 1 OCR 完成
        # ============================================================
        if is_image:
            # 尝试图片级遮盖（黑框覆盖敏感区域）
            try:
                # 用 PIL 标注 OCR 检测到的敏感区域
                from PIL import Image, ImageDraw
                img = Image.open(file_path).convert("RGB")
                draw = ImageDraw.Draw(img)

                # OCR 文本已脱敏，不再做图像级遮盖
                # 保存脱敏版图片描述
                outputs["image_original"] = file_path
            except Exception:
                pass

        # ============================================================
        # Step 6: 生成汇总映射表 JSON
        # ============================================================
        mapping_file = str(parent / f"{stem}_汇总映射表.json")
        mapping_data = {
            "source_file": path.name,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_items": len(all_mapping),
            "formats": list(outputs.keys()),
            "mapping": all_mapping,
        }
        Path(mapping_file).write_text(
            json.dumps(mapping_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        outputs["mapping_file"] = mapping_file

        # ============================================================
        # Step 7: 生成反脱敏指南文档
        # ============================================================
        unmask_doc_path = str(parent / f"{stem}_反脱敏指南.txt")
        unmask_lines = [
            "=" * 60,
            "  反脱敏指南 — 可逆还原操作说明",
            "=" * 60,
            "",
            f"源文件：{path.name}",
            f"生成时间：{mapping_data['generated_at']}",
            f"脱敏项数：{len(all_mapping)}",
            "",
            "-" * 40,
            "  操作步骤",
            "-" * 40,
            "",
            "Step 1: 获取 LLM 返回的脱敏内容",
            "Step 2: 执行以下命令还原：",
            "",
            f'  echo \'{{"action":"unmask","content":"<LLM回复内容>","mapping":{json.dumps(all_mapping, ensure_ascii=False)}}}\'',
            f"  | python3 {Path(__file__).resolve()}",
            "",
            "Step 3: 查看 restored_content 即为原文",
            "",
            "-" * 40,
            "  各格式脱敏文件说明",
            "-" * 40,
            "",
        ]

        for fmt_key, fmt_path in outputs.items():
            if fmt_key in ("mapping_file",):
                continue
            unmask_lines.append(f"  [{fmt_key}]")
            unmask_lines.append(f"    文件：{fmt_path}")
            if fmt_key == "ocr_redacted_txt":
                unmask_lines.append(f"    用途：OCR 识别原文脱敏（仅供参考，不可逆还原）")
            elif fmt_key == "pdf_redacted_pdf":
                unmask_lines.append(f"    用途：视觉级遮盖 PDF（黑框覆盖敏感区域）")
            elif fmt_key == "docx_redacted":
                unmask_lines.append(f"    用途：Word 格式脱敏版（可编辑，占位符形态）")
            elif fmt_key == "md_redacted":
                unmask_lines.append(f"    用途：Markdown 格式脱敏版（可编辑，占位符形态）")
            unmask_lines.append("")

        unmask_lines.extend([
            "-" * 40,
            "  脱敏项明细",
            "-" * 40,
            "",
        ])
        for i, item in enumerate(all_mapping, 1):
            unmask_lines.append(f"  {i:3d}. {item['original']:30s} → {item['marker']}")

        Path(unmask_doc_path).write_text("\n".join(unmask_lines), encoding="utf-8")
        outputs["unmask_doc"] = unmask_doc_path

        # ── 汇总统计 ──
        types_found = sorted(set(
            item.get("type", "UNKNOWN") for item in all_mapping
        ))

        return {
            "status": "success",
            "source_file": path.name,
            "outputs": outputs,
            "mapping": all_mapping,
            "mapping_file": mapping_file,
            "unmask_doc": unmask_doc_path,
            "summary": {
                "total_items": len(all_mapping),
                "types_found": types_found,
                "formats_produced": [k for k in outputs if k not in ("mapping_file", "unmask_doc")],
            },
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

    elif action == "redact_multi_format":
        # v1.3: Multi-format redaction pipeline (PDF/image → OCR + DOCX + MD + PDF)
        result = tool.action_redact_multi_format(
            input_data.get("file_path", ""),
            input_data.get("keyword_rules"),
            input_data.get("disable_types"),
        )

    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
