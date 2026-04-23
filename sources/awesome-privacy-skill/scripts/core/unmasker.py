"""
Unmasker module - restores original sensitive data from redaction markers.
"""

import re
from typing import TypedDict

from scripts.core.redaction import RedactionMapping


class Unmasker:
    """Restores original sensitive data from redacted content."""

    MARKER_PATTERN = re.compile(r'<<REDACTED_([A-Z_]+)_(\d+)>>')

    def restore(self, content: str, mapping: list[RedactionMapping]) -> str:
        """Restore original sensitive data in content."""
        if not mapping:
            return content

        lookup: dict[tuple[str, int], str] = {}
        for entry in mapping:
            lookup[(entry["type"], entry["index"])] = entry["original"]

        def replacer(match):
            key = (match.group(1), int(match.group(2)))
            return lookup.get(key, match.group(0))

        return self.MARKER_PATTERN.sub(replacer, content)

    def validate(self, content: str) -> tuple[bool, list[str]]:
        """Check if content still contains any unmasked markers."""
        remaining = self.MARKER_PATTERN.findall(content)
        if remaining:
            return False, [f"REDACTED_{t}_{i}" for t, i in remaining]
        return True, []
