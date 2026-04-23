"""
Image handler with OCR support for JPG and PNG files.
"""

from pathlib import Path
from typing import Optional

from scripts.handlers.base import BaseHandler


class ImageHandler(BaseHandler):
    """Handles JPG and PNG image files with OCR."""

    def read(self, file_path: str) -> Optional[str]:
        """Extract text from image using OCR."""
        return self.extract_text(file_path)

    def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text using configured OCR engine."""
        ocr_engine = self.settings.get("ocr", "engine", default="pytesseract")
        try:
            if ocr_engine == "pytesseract":
                return self._extract_pytesseract(file_path)
            elif ocr_engine == "paddleocr":
                return self._extract_paddleocr(file_path)
            elif ocr_engine == "rapidocr":
                return self._extract_rapidocr(file_path)
            return self._extract_pytesseract(file_path)
        except Exception:
            return None

    def _extract_pytesseract(self, file_path: str) -> Optional[str]:
        try:
            from PIL import Image
            import pytesseract
            image = Image.open(file_path)
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")
            return pytesseract.image_to_string(
                image,
                lang=self.settings.get("ocr", "language", default="eng+chi_sim"),
            ).strip()
        except Exception:
            return None

    def _extract_paddleocr(self, file_path: str) -> Optional[str]:
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(
                lang=self.settings.get("ocr", "language", default="en"),
                use_angle_cls=True,
            )
            result = ocr.ocr(file_path)
            if result and result[0]:
                lines = []
                for line in result[0]:
                    if len(line) >= 2:
                        text = line[1][0] if isinstance(line[1], tuple) else line[1]
                        lines.append(text)
                return "\n".join(lines)
            return None
        except Exception:
            return None

    def _extract_rapidocr(self, file_path: str) -> Optional[str]:
        try:
            from rapidocr_onnxruntime import RapidOCR
            ocr = RapidOCR()
            result, _, _ = ocr(file_path)
            if result:
                return "\n".join(
                    str(line[1]) if isinstance(line, (list, tuple)) else str(line)
                    for line in result
                )
            return None
        except Exception:
            return None

    def write(self, file_path: str, content: str) -> bool:
        """Save extracted text as .txt alongside image."""
        try:
            base_path = Path(file_path)
            base_path.with_suffix(base_path.suffix + ".txt").write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False
