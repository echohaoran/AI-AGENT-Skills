"""
Base handler interface for file format support.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseHandler(ABC):
    """Abstract base class for file format handlers."""

    def __init__(self, settings):
        self.settings = settings

    @abstractmethod
    def read(self, file_path: str) -> Optional[str]:
        """Read file and return extracted text content."""
        pass
