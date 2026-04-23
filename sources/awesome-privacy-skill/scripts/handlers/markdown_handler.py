"""
Markdown file handler.
"""

from pathlib import Path
from typing import Optional

from scripts.handlers.base import BaseHandler


class MarkdownHandler(BaseHandler):
    """Handles Markdown file reading and writing."""

    def read(self, file_path: str) -> Optional[str]:
        """Read Markdown file content."""
        try:
            return Path(file_path).read_text(encoding="utf-8")
        except Exception:
            return None

    def write(self, file_path: str, content: str) -> bool:
        """Write content to Markdown file."""
        try:
            Path(file_path).write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False
