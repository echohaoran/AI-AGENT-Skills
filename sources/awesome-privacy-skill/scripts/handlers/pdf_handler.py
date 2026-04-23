"""
PDF file handler with text extraction support.
"""

from typing import Optional

from scripts.handlers.base import BaseHandler


class PDFHandler(BaseHandler):
    """Handles PDF file reading via pypdf."""

    def read(self, file_path: str) -> Optional[str]:
        """Extract text from PDF."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n\n".join(text_parts)
        except Exception:
            return None
