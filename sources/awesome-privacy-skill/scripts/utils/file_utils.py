"""
File utility functions.
"""

import os
from pathlib import Path


def is_file_too_large(file_path: str, max_size_mb: int = 50) -> bool:
    """Check if file exceeds size limit."""
    return os.path.getsize(file_path) / (1024 * 1024) > max_size_mb


def get_file_extension(file_path: str) -> str:
    """Get lowercase file extension."""
    return Path(file_path).suffix.lower()


def ensure_directory(file_path: str) -> bool:
    """Ensure parent directory exists."""
    directory = Path(file_path).parent
    directory.mkdir(parents=True, exist_ok=True)
    return directory.exists()
