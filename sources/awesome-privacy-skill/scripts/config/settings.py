"""
Configuration management for awesome-privacy-skill.

Supports:
- Default config (built-in patterns).
- JSON config file (privacy-config.json).
- Environment variable: PRIVACY_SKILL_CONFIG.
- keyword_rules: exact-match keyword → placeholder table.
- custom_patterns: user-defined regex patterns.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Settings:
    """Settings management with JSON config file support."""

    DEFAULT_CONFIG = {
        "privacy": {
            "redaction_marker": "<<REDACTED_{type}_{index}>>",
            "marker_style": "angle",  # "angle" → <<REDACTED>>, "bracket" → [████TYPE_1]
            "max_file_size_mb": 50,
            "chunk_size_kb": 1024,
        },
        "ocr": {
            "enabled": True,
            "engine": "pytesseract",
            "language": "eng+chi_sim",
        },
        "sensitive_types": {
            "NAME": True,
            "PHONE": True,
            "EMAIL": True,
            "ID": True,
            "CREDIT_CARD": True,
            "ADDRESS": True,
            "IP": True,
            "API_KEY": True,
            "MONEY": True,
            "COMPANY_NAME": True,
            "CUSTOM": True,
        },
        # User-defined exact-match keyword rules.
        # Format: [{"keyword": "敏感词", "placeholder": "████类型_1"}, ...]
        # These are applied BEFORE regex patterns (highest priority).
        "keyword_rules": [],
        # User-defined regex patterns.
        # Format: [{"type": "CUSTOM", "pattern": "\\bsecret\\d+\\b"}, ...]
        "custom_patterns": [],
        # Output: save redacted file back to disk?
        "output": {
            "save_file": True,
            "suffix": "_redacted",
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        self._config = self._deep_copy(self.DEFAULT_CONFIG)
        self._load_config(config_path)

    def _deep_copy(self, obj: Any) -> Any:
        """Deep copy to avoid mutation of defaults."""
        if isinstance(obj, dict):
            return {k: self._deep_copy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_copy(item) for item in obj]
        return obj

    def _load_config(self, config_path: Optional[str] = None) -> None:
        # Check environment variable first
        env_config_path = os.environ.get("PRIVACY_SKILL_CONFIG")
        if env_config_path and Path(env_config_path).exists():
            config_path = env_config_path

        if config_path is None:
            default_locations = [
                Path.cwd() / "privacy-config.json",
                Path.home() / ".config" / "privacy-skill" / "config.json",
                Path.home() / ".config" / "alma" / "skills" / "awesome-privacy-skill" / "privacy-config.json",
            ]
            for loc in default_locations:
                if loc.exists():
                    config_path = str(loc)
                    break

        if config_path and Path(config_path).exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self._merge_config(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass  # Fall back to defaults

    def _merge_config(self, user_config: dict) -> None:
        """Recursively merge user config into defaults."""
        for key, value in user_config.items():
            if key in self._config and isinstance(self._config[key], dict) and isinstance(value, dict):
                self._config[key].update(value)
            elif key in self._config and isinstance(self._config[key], list) and isinstance(value, list):
                self._config[key] = value  # Replace list entirely
            else:
                self._config[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get nested config value, e.g. settings.get("privacy", "redaction_marker")."""
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def __getitem__(self, key: str) -> dict:
        return self._config.get(key, {})

    def to_dict(self) -> dict:
        return self._deep_copy(self._config)
