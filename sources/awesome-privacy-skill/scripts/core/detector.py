"""
Sensitive data detection module.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from scripts.core.constants import SENSITIVE_PATTERNS, SPECIFICITY


@dataclass
class SensitiveMatch:
    """Represents a detected sensitive data match."""
    type: str
    value: str
    start: int
    end: int
    confidence: float = 1.0
    context: Optional[str] = None
    specificity: int = 0

    def __lt__(self, other):
        return self.start < other.start

    def is_overlapping(self, other_start: int, other_end: int) -> bool:
        return self.start < other_end and self.end > other_start


class SensitiveDataDetector:
    """Detects sensitive data patterns in text content."""

    def __init__(self, settings):
        self.settings = settings
        self.enabled_types = {
            k for k, v in settings.get("sensitive_types", default={}).items()
            if v
        }
        self.custom_patterns = self._compile_custom_patterns()

    def _compile_custom_patterns(self) -> list:
        patterns = []
        for item in self.settings.get("custom_patterns", default=[]):
            if isinstance(item, dict) and "pattern" in item:
                try:
                    patterns.append({
                        "type": item.get("type", "CUSTOM"),
                        "pattern": re.compile(item["pattern"]),
                    })
                except re.error:
                    pass
        return patterns

    def _get_specificity(self, data_type: str) -> int:
        return SPECIFICITY.get(data_type, 0)

    def detect(self, content: str) -> list[SensitiveMatch]:
        """
        Detect all sensitive data in content.
        When patterns overlap, keeps the one with higher specificity.
        """
        matches: list[SensitiveMatch] = []
        # Track ranges: range_key -> match_index
        range_map: dict[tuple[int, int], int] = {}

        for data_type, patterns in SENSITIVE_PATTERNS.items():
            if data_type not in self.enabled_types:
                continue
            specificity = self._get_specificity(data_type)
            for pattern in patterns:
                for m in pattern.finditer(content):
                    start, end = m.span()
                    new_match = SensitiveMatch(
                        type=data_type,
                        value=m.group(),
                        start=start,
                        end=end,
                        confidence=self._calculate_confidence(data_type, m.group()),
                        specificity=specificity,
                    )
                    self._add_match(matches, range_map, new_match)

        # Custom patterns (processed last, lower priority than built-in)
        for custom in self.custom_patterns:
            specificity = self._get_specificity("CUSTOM")
            for m in custom["pattern"].finditer(content):
                start, end = m.span()
                new_match = SensitiveMatch(
                    type=custom["type"],
                    value=m.group(),
                    start=start,
                    end=end,
                    confidence=0.9,
                    specificity=specificity,
                )
                self._add_match(matches, range_map, new_match)

        matches.sort()
        return matches

    def _add_match(
        self,
        matches: list[SensitiveMatch],
        range_map: dict[tuple[int, int], int],
        new_match: SensitiveMatch,
    ) -> None:
        """Add match, resolving overlaps by specificity."""
        start, end = new_match.start, new_match.end

        # Find all overlapping ranges
        overlapping_indices: list[int] = []
        for (r_start, r_end), idx in range_map.items():
            if start < r_end and end > r_start:
                overlapping_indices.append(idx)

        if not overlapping_indices:
            # No overlap, add directly
            idx = len(matches)
            matches.append(new_match)
            range_map[(start, end)] = idx
            return

        # Find the highest-specificity existing match among overlaps
        best_existing_idx = max(overlapping_indices, key=lambda i: matches[i].specificity)

        if matches[best_existing_idx].specificity >= new_match.specificity:
            # Existing match is more specific, skip new one
            return

        # New match wins: remove old overlaps, add new
        for idx in overlapping_indices:
            old = matches[idx]
            del range_map[(old.start, old.end)]
            matches[idx] = None  # mark as removed

        # Remove Nones
        matches[:] = [m for m in matches if m is not None]

        # Add new match
        idx = len(matches)
        matches.append(new_match)
        range_map[(start, end)] = idx

    def _calculate_confidence(self, data_type: str, value: str) -> float:
        if data_type == "EMAIL":
            return 0.95
        elif data_type == "PHONE":
            return 0.9
        elif data_type == "CREDIT_CARD":
            return 0.95 if self._luhn_check(value) else 0.5
        elif data_type == "ID":
            return 0.9
        return 0.8

    def _luhn_check(self, number: str) -> bool:
        digits = re.sub(r'\D', '', number)
        if len(digits) < 13 or len(digits) > 19:
            return False
        total = 0
        for i, digit in enumerate(digits[::-1]):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
