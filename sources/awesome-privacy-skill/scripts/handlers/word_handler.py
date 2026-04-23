"""
Word document handler with text extraction.
"""

from typing import Optional

from scripts.handlers.base import BaseHandler


class WordHandler(BaseHandler):
    """Handles Word .docx file reading via python-docx."""

    def read(self, file_path: str) -> Optional[str]:
        """Extract text from Word document."""
        try:
            from docx import Document
            doc = Document(file_path)
            parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    parts.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        parts.append(" | ".join(row_text))
            return "\n".join(parts)
        except Exception:
            return None
