"""
Redaction module - replaces sensitive data with reversible placeholders.
"""

from typing import TypedDict

from scripts.core.constants import REDACTION_MARKER, PARTIAL_MASK_TYPES
from scripts.core.detector import SensitiveDataDetector, SensitiveMatch


class RedactionMapping(TypedDict):
    """Mapping entry for a redacted item."""
    type: str
    index: int
    original: str
    marker: str


class Redactor:
    """Redacts sensitive data and generates reversible mapping."""

    def __init__(self, settings):
        self.settings = settings
        self.marker_template = settings.get(
            "privacy", "redaction_marker", default=REDACTION_MARKER
        )
        self.detector = SensitiveDataDetector(settings)
        self.partial_types = PARTIAL_MASK_TYPES

    def _mask_value(self, value: str, data_type: str) -> str:
        """Partially mask value: show first + last chars, replace middle with ****."""
        length = len(value)
        if length <= 4:
            return "*" * length
        if data_type == "CREDIT_CARD":
            # Remove separators first to count digits
            digits = "".join(c for c in value if c.isdigit())
            num_digits = len(digits)
            if num_digits <= 8:
                return digits[:4] + "****" + digits[-4:]
            # Format back with original separator style
            return digits[:4] + "****" + digits[-4:]
        else:
            # Default: first 2 + **** + last 2
            return value[:2] + "****" + value[-2:]

    def redact(self, content: str, detections: list[SensitiveMatch] = None) -> tuple[str, list[RedactionMapping]]:
        """Redact sensitive data from content."""
        if detections is None:
            detections = self.detector.detect(content)

        sorted_detections = sorted(detections, key=lambda m: m.start, reverse=True)
        redacted = content
        mapping: list[RedactionMapping] = []
        type_counters: dict[str, int] = {}

        for match in sorted_detections:
            if match.type not in type_counters:
                type_counters[match.type] = 0
            type_counters[match.type] += 1

            if match.type in self.partial_types:
                # Partial mask: show first+last chars, replace middle with ****
                masked = self._mask_value(match.value, match.type)
            else:
                # Full redaction: replace with marker
                masked = self.marker_template.format(type=match.type, index=type_counters[match.type])

            redacted = redacted[:match.start] + masked + redacted[match.end:]
            mapping.insert(0, {
                "type": match.type,
                "index": type_counters[match.type],
                "original": match.value,
                "marker": masked,
            })

        return redacted, mapping
