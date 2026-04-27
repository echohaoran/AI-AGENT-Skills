"""
Format converter — PDF → DOCX, PDF → Markdown.

Used by the multi-format redaction pipeline (action_redact_multi_format).
Converts original PDF into .docx and .md so each format can be redacted separately.
"""

import os
import re
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────
# Monkey‑patch: PyMuPDF ≥1.24 removed Rect.get_area()
# pdf2docx 0.5.8 still calls it, so we add it back.
# ─────────────────────────────────────────────────
import fitz as _fitz
if not hasattr(_fitz.Rect, "get_area"):
    _fitz.Rect.get_area = lambda self: self.width * self.height


def convert_pdf_to_docx(input_pdf: str, output_docx: str) -> bool:
    """
    Convert PDF to DOCX using pdf2docx (patched for PyMuPDF compatibility).

    If the conversion fails (e.g., complex layout, version mismatch), the
    pipeline continues gracefully without the DOCX output — non-critical.

    Args:
        input_pdf:  Path to the source PDF.
        output_docx: Destination path for the .docx file.

    Returns:
        True if conversion succeeded, False otherwise.
    """
    try:
        from pdf2docx import Converter as PDF2DocxConverter

        os.makedirs(os.path.dirname(output_docx) or ".", exist_ok=True)
        cv = PDF2DocxConverter(input_pdf)
        cv.convert(output_docx, start=0, end=None)
        cv.close()
        return Path(output_docx).exists()
    except Exception as e:
        # Non-critical — pipeline continues without DOCX output
        return False


def convert_pdf_to_markdown(input_pdf: str, output_md: str) -> bool:
    """
    Convert PDF to Markdown using PyMuPDF text extraction.
    
    Preserves:
      - Page breaks (---)
      - Line breaks within paragraphs
      - Headings (approximated from font size heuristics)
      - Image references (in ![page N](image_path) form)
      - Basic list detection (numbered/bullet)
    
    Args:
        input_pdf:  Path to the source PDF.
        output_md:  Destination path for the .md file.
    
    Returns:
        True if conversion succeeded, False otherwise.
    """
    try:
        import fitz

        doc = fitz.open(input_pdf)
        md_lines = []
        last_font_size = 0

        for page_num, page in enumerate(doc, 1):
            # Page separator
            if page_num > 1:
                md_lines.append("\n\n---\n\n")

            blocks = page.get_text("dict").get("blocks", [])

            for block in blocks:
                if block.get("type") != 0:  # Skip images (type 1)
                    continue

                block_lines = block.get("lines", [])
                para_parts = []

                for line in block_lines:
                    spans = line.get("spans", [])
                    if not spans:
                        continue

                    # Font-size heuristic for headings
                    font_sizes = [s.get("size", 12) for s in spans if s.get("size")]
                    avg_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12

                    line_text = "".join(s.get("text", "") for s in spans).strip()

                    if not line_text:
                        continue

                    # Heading detection
                    if avg_size > 18:
                        line_text = f"# {line_text}"
                    elif avg_size > 14:
                        line_text = f"## {line_text}"
                    elif avg_size > 12 and last_font_size > 14:
                        line_text = f"### {line_text}"

                    # Bullet detection
                    if re.match(r'^[\d]+[\.\)]\s', line_text):
                        line_text = f"1. {line_text.split(' ', 1)[1] if ' ' in line_text else line_text}"
                    elif re.match(r'^[•·\-–]\s', line_text):
                        line_text = f"- {line_text[2:]}"

                    last_font_size = avg_size

                    # Bold detection from font flags
                    if spans and any(s.get("flags", 0) & 2 for s in spans if s.get("flags")):
                        line_text = f"**{line_text}**"

                    para_parts.append(line_text)

                if para_parts:
                    md_lines.append(" ".join(para_parts))

            # Render page to image and save as reference
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            img_dir = Path(output_md).parent / f"{Path(output_md).stem}_images"
            img_dir.mkdir(parents=True, exist_ok=True)
            img_path = img_dir / f"page_{page_num}.png"
            pix.save(str(img_path))
            md_lines.append(f"\n![Page {page_num}]({img_path.relative_to(Path(output_md).parent)})\n")

        doc.close()

        md_content = "\n".join(md_lines)
        Path(output_md).parent.mkdir(parents=True, exist_ok=True)
        Path(output_md).write_text(md_content, encoding="utf-8")
        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False
