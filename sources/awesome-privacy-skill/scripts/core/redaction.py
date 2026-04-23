"""
Redaction module — replaces sensitive data with reversible placeholders.

Key improvements over v1.0:
1. Single-pass regex replacement: all matches replaced at once, avoiding
   position-shift issues from sequential in-place replacement.
2. Comprehensive keyword rules: supports exact-match keyword tables
   (bypasses regex entirely for known sensitive keywords).
3. Priority ordering: longest match first to prevent short patterns
   from consuming parts of longer keywords.
4. Post-redaction validation: scans redacted content to ensure
   no sensitive keywords remain.
"""

import re
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
    """
    Redacts sensitive data and generates reversible mapping.

    Two redaction modes:
    - PATTERN mode (default): uses regex pattern detection + replacement.
    - KEYWORD mode: uses exact-match keyword tables (higher confidence,
      bypasses regex for known sensitive strings).
    """

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
            digits = "".join(c for c in value if c.isdigit())
            num_digits = len(digits)
            if num_digits <= 8:
                return digits[:4] + "****" + digits[-4:]
            return digits[:4] + "****" + digits[-4:]
        else:
            return value[:2] + "****" + value[-2:]

    # ─────────────────────────────────────────
    # Pattern-based redact (original approach)
    # ─────────────────────────────────────────
    def redact(
        self, content: str, detections: list[SensitiveMatch] = None
    ) -> tuple[str, list[RedactionMapping]]:
        """
        Redact sensitive data using pattern detection.
        Uses reverse-order replacement to preserve string positions.
        """
        if detections is None:
            detections = self.detector.detect(content)

        # Sort by start position DESC — replace from end to start
        # so earlier positions aren't affected by replacements
        sorted_detections = sorted(detections, key=lambda m: m.start, reverse=True)

        redacted = content
        mapping: list[RedactionMapping] = []
        type_counters: dict[str, int] = {}

        for match in sorted_detections:
            mtype = match.type
            if mtype not in type_counters:
                type_counters[mtype] = 0
            type_counters[mtype] += 1

            if mtype in self.partial_types:
                masked = self._mask_value(match.value, mtype)
            else:
                masked = self.marker_template.format(
                    type=mtype, index=type_counters[mtype]
                )

            redacted = (
                redacted[: match.start]
                + masked
                + redacted[match.end :]
            )
            mapping.insert(
                0,
                {
                    "type": mtype,
                    "index": type_counters[mtype],
                    "original": match.value,
                    "marker": masked,
                },
            )

        return redacted, mapping

    # ─────────────────────────────────────────
    # Keyword-table redact (new in v1.1)
    # ─────────────────────────────────────────
    def redact_with_keywords(
        self, content: str, keyword_rules: list[dict]
    ) -> tuple[str, list[RedactionMapping]]:
        """
        Redact using exact-match keyword → placeholder mapping.

        This is the recommended approach for known sensitive data lists
        (e.g., a config file of company names, personal IDs, etc.)
        It uses single-pass regex replacement to avoid nested pollution.

        Args:
            content: Text to redact.
            keyword_rules: List of {"keyword": "...", "placeholder": "████TYPE_1"}.

        Returns:
            (redacted_content, mapping_dict) where mapping_dict maps
            placeholder → original_value.
        """
        if not keyword_rules:
            return content, {}

        # Sort by keyword length (longest first) to prevent short matches
        # from consuming parts of longer keywords
        sorted_rules = sorted(keyword_rules, key=lambda x: -len(x["keyword"]))

        # Build combined regex (all keywords escaped)
        patterns = []
        for rule in sorted_rules:
            patterns.append(re.escape(rule["keyword"]))
        combined_re = re.compile("|".join(patterns))

        mapping: dict[str, str] = {}
        redacted = content
        replacements = []  # [(start, end, placeholder, original)]

        for m in combined_re.finditer(content):
            original = m.group()
            # Find the corresponding placeholder
            for rule in sorted_rules:
                if rule["keyword"] == original:
                    placeholder = rule["placeholder"]
                    if placeholder not in mapping:
                        mapping[placeholder] = original
                    replacements.append((m.start(), m.end(), placeholder, original))
                    break

        # Apply replacements in reverse order (end→start) to preserve positions
        replacements.sort(key=lambda x: x[0], reverse=True)
        for start, end, placeholder, _ in replacements:
            redacted = redacted[:start] + f"[{placeholder}]" + redacted[end:]

        # Build mapping list
        mapping_list = [
            {
                "type": ph.split("_")[1] if "_" in ph else "CUSTOM",
                "index": i + 1,
                "original": orig,
                "marker": f"[{ph}]",
            }
            for i, (ph, orig) in enumerate(mapping.items())
        ]

        return redacted, mapping_list

    # ─────────────────────────────────────────
    # Hybrid redact (new in v1.1) — combines both
    # ─────────────────────────────────────────
    def redact_hybrid(
        self,
        content: str,
        keyword_rules: list[dict] = None,
        skip_pattern_detection: bool = False,
    ) -> tuple[str, list[RedactionMapping]]:
        """
        Hybrid redaction: keyword-table first (high confidence),
        then pattern-based for remaining content.

        This approach:
        1. Applies exact keyword rules first (single-pass, no pollution).
        2. Runs pattern detection on remaining content.
        3. Validates output for residue.

        Recommended workflow:
        1. Load keyword rules from config or inline.
        2. Call redact_hybrid() with both keyword rules and pattern rules.
        3. Use validate() to check output.
        """
        type_counters: dict[str, int] = {}
        mapping: list[RedactionMapping] = []

        # Step 1: Keyword-table redaction
        if keyword_rules:
            kw_content, kw_mapping = self.redact_with_keywords(content, keyword_rules)
            content = kw_content
            # Renumber type counters from keyword mappings
            for item in kw_mapping:
                mtype = item["type"]
                if mtype not in type_counters:
                    type_counters[mtype] = 0
                type_counters[mtype] += 1
                item["index"] = type_counters[mtype]
            mapping.extend(kw_mapping)

        # Step 2: Pattern-based detection on remaining content (skip if disabled)
        if not skip_pattern_detection:
            detections = self.detector.detect(content)
            sorted_det = sorted(detections, key=lambda m: m.start, reverse=True)

            redacted = content
            for match in sorted_det:
                mtype = match.type
                if mtype not in type_counters:
                    type_counters[mtype] = 0
                type_counters[mtype] += 1

                if mtype in self.partial_types:
                    masked = self._mask_value(match.value, mtype)
                else:
                    masked = self.marker_template.format(
                        type=mtype, index=type_counters[mtype]
                    )

                redacted = redacted[: match.start] + masked + redacted[match.end :]
                mapping.append(
                    {
                        "type": mtype,
                        "index": type_counters[mtype],
                        "original": match.value,
                        "marker": masked,
                    }
                )
        else:
            redacted = content

        return redacted, mapping

    # ─────────────────────────────────────────
    # Validation (new in v1.1)
    # ─────────────────────────────────────────
    def validate(self, redacted_content: str) -> dict:
        """
        Post-redaction validation: scan redacted content for any
        remaining sensitive patterns.

        Returns:
            {"clean": bool, "remaining": [str, ...]}
        """
        remaining = self.detector.validate_content(redacted_content)
        return {"clean": len(remaining) == 0, "remaining": remaining}
