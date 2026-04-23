"""
PDF handler with image-level redaction support.

Key techniques learned from实战:
1. PyMuPDF text extraction (text_dict mode) provides precise character coordinates.
2. For graphical/text PDFs: PyMuPDF extracts the text; use its coordinates to draw
   black rectangles on the rendered image, avoiding the "white gap" problem caused
   by font glyphs extending beyond bbox.
3. Resolution: use 4x zoom rendering to minimize coordinate quantization error.
4. Keyword matching: strip spaces — PyMuPDF may not preserve spaces between words.
5. Full-row black bar: always draw the rectangle across the entire page width, not
   just the text bbox, to prevent rendering artifacts from leaking text visually.
6. For verification: render the redacted PDF page and run OCR on it to confirm no
   sensitive content is detectable.
"""

import os
import re
import json
from pathlib import Path
from typing import Optional

from scripts.handlers.base import BaseHandler


class PDFHandler(BaseHandler):
    """
    Handles PDF reading and image-level redaction via PyMuPDF + PIL.

    Supports two redaction modes:
    - TEXT mode (default): uses PyMuPDF text extraction + pattern matching.
      Suitable for text-based PDFs.
    - IMAGE mode: renders PDF to high-resolution image, masks detected regions,
      embeds the image back into a new PDF. Suitable for graphical PDFs where
      PyMuPDF text extraction is incomplete.
    """

    def __init__(self, settings):
        super().__init__(settings)
        self._ocr_available = self._check_ocr()

    def _check_ocr(self) -> bool:
        try:
            import pytesseract
            return True
        except ImportError:
            return False

    def read(self, file_path: str) -> Optional[str]:
        """Extract text from PDF using PyMuPDF."""
        try:
            import fitz
            doc = fitz.open(file_path)
            parts = []
            for page in doc:
                text = page.get_text()
                if text:
                    parts.append(text)
            doc.close()
            return "\n\n".join(parts)
        except Exception:
            return None

    def redact_image_level(
        self,
        input_path: str,
        output_path: str,
        keyword_rules: list,
        custom_patterns: list = None,
        zoom: int = 4,
    ) -> dict:
        """
        Image-level PDF redaction — renders, masks, and re-embeds.

        This is the recommended method for PDFs where text extraction is incomplete
        (e.g., graphical text, non-standard fonts, complex layouts).

        Args:
            input_path: Path to source PDF.
            output_path: Destination path for redacted PDF.
            keyword_rules: List of {"keyword": "...", "placeholder": "████TYPE_A"}
            custom_patterns: List of regex pattern strings (optional).
            zoom: Rendering resolution multiplier (default 4 for 288 DPI).

        Returns:
            {"status": "success"|"error", "mapping": {...}, "details": "..."}
        """
        try:
            import fitz
            from PIL import Image, ImageDraw
        except ImportError as e:
            return {"status": "error", "details": f"Missing dependency: {e}"}

        if not keyword_rules:
            return {"status": "error", "details": "No keyword rules provided"}

        # Sort by length descending (longest first)
        sorted_rules = sorted(keyword_rules, key=lambda x: -len(x.get("keyword", "")))
        combined_re = re.compile(
            "|".join(re.escape(r["keyword"]) for r in sorted_rules if r.get("keyword"))
        )
        placeholder_map = {r["keyword"]: r["placeholder"] for r in sorted_rules if r.get("keyword")}

        # Optional custom patterns
        custom_re = None
        if custom_patterns:
            patterns = [re.escape(p) for p in custom_patterns if isinstance(p, str)]
            if patterns:
                custom_re = re.compile("|".join(patterns))

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Step 1: Open PDF, process each page into redacted images
        doc = fitz.open(input_path)
        page_redacted_images = []  # list of (png_path, pdf_w, pdf_h)
        mapping = {}
        total_rects = 0

        for page_num, page in enumerate(doc, 1):
            pdf_w, pdf_h = page.rect.width, page.rect.height

            # High-resolution render
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_path = f"/tmp/pdf_rl_page_{page_num}.png"
            pix.save(img_path)

            img = Image.open(img_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            px_w, px_h = img.size
            scale_x = px_w / pdf_w
            scale_y = px_h / pdf_h

            sensitive_y_ranges = []
            d = page.get_text("dict")

            for block in d.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    line_text = "".join(
                        span.get("text", "") for span in line.get("spans", [])
                    )
                    if not line_text.strip():
                        continue
                    is_sensitive = bool(combined_re.search(line_text))
                    if not is_sensitive and custom_re:
                        is_sensitive = bool(custom_re.search(line_text))
                    if not is_sensitive:
                        continue

                    bboxes = [
                        span.get("bbox", [])
                        for span in line.get("spans", [])
                        if span.get("bbox")
                    ]
                    if not bboxes:
                        continue

                    iy0 = min(b[1] for b in bboxes) * scale_y
                    iy1 = max(b[3] for b in bboxes) * scale_y
                    sensitive_y_ranges.append((iy0, iy1))

                    for m in combined_re.finditer(line_text):
                        kw = m.group()
                        ph = placeholder_map.get(kw)
                        if ph and ph not in mapping:
                            mapping[ph] = kw

            # Merge adjacent/overlapping Y-ranges
            if sensitive_y_ranges:
                sensitive_y_ranges.sort(key=lambda x: x[0])
                merged = [list(sensitive_y_ranges[0])]
                for y0, y1 in sensitive_y_ranges[1:]:
                    if y0 <= merged[-1][1] + 8:
                        merged[-1][1] = max(merged[-1][1], y1)
                    else:
                        merged.append([y0, y1])
                sensitive_y_ranges = [(y0, y1) for y0, y1 in merged]

            # Draw full-row black bars
            PAD = 10
            for iy0, iy1 in sensitive_y_ranges:
                ry0 = max(0, iy0 - PAD)
                ry1 = min(px_h, iy1 + PAD)
                if ry1 > ry0:
                    draw.rectangle([0, int(ry0), px_w, int(ry1)], fill=(0, 0, 0))
                    total_rects += 1

            img.save(img_path, "PNG")
            page_redacted_images.append((img_path, pdf_w, pdf_h))

        doc.close()

        # Step 2: Build new PDF from redacted images
        doc_out = fitz.open()
        for img_path, pdf_w, pdf_h in page_redacted_images:
            page = doc_out.new_page(width=pdf_w, height=pdf_h)
            page.insert_image(page.rect, filename=img_path)

        doc_out.save(output_path, garbage=4, deflate=True)
        doc_out.close()

        # Save mapping
        mapping_path = output_path.replace(".pdf", "_映射表.json")
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "output_path": output_path,
            "mapping_path": mapping_path,
            "mapping": mapping,
            "total_rects": total_rects,
            "pages": len(page_redacted_images),
        }

    def verify_redaction(
        self, pdf_path: str = "", sensitive_keywords: list = None
    ) -> dict:
        """
        Post-redaction verification: render redacted PDF and run OCR to confirm
        no sensitive keywords remain detectable.

        Args:
            pdf_path: Path to redacted PDF.
            sensitive_keywords: List of keyword strings to check for.

        Returns:
            {"clean": bool, "remaining": [...], "pages": {...}}
        """
        if not self._ocr_available:
            return {
                "status": "skipped",
                "reason": "pytesseract not available",
                "clean": None,
                "remaining": [],
            }

        import fitz
        from PIL import Image
        import pytesseract

        doc = fitz.open(pdf_path)
        all_clean = True
        remaining = []
        page_results = {}

        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            tmp = f"/tmp/pdf_verify_page_{i}.png"
            pix.save(tmp)

            txt = pytesseract.image_to_string(Image.open(tmp)).lower()
            found = [
                kw
                for kw in sensitive_keywords
                if kw.lower() in txt
            ]
            if found:
                all_clean = False
                remaining.extend([(i, kw) for kw in found])
                page_results[i] = {"clean": False, "found": found}
            else:
                page_results[i] = {"clean": True}

        doc.close()
        return {
            "clean": all_clean,
            "remaining": remaining,
            "pages": page_results,
        }
