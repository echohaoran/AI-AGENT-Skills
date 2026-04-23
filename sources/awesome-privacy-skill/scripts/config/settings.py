"""
Configuration management for awesome-privacy-skill.
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
            "CUSTOM": True,
            "API_KEY": True,
            "MONEY": True,
            "COMPANY_NAME": True,
        },
        "custom_patterns": [],
    }

    def __init__(self, config_path: Optional[str] = None):
        self._config = self.DEFAULT_CONFIG.copy()
        self._load_config(config_path)

    def _load_config(self, config_path: Optional[str] = None) -> None:
        env_config_path = os.environ.get("PRIVACY_SKILL_CONFIG")
        if env_config_path and Path(env_config_path).exists():
            config_path = env_config_path

        if config_path is None:
            default_locations = [
                Path.cwd() / "privacy-config.json",
                Path.home() / ".config" / "privacy-skill" / "config.json",
            ]
            for loc in default_locations:
                if loc.exists():
                    config_path = str(loc)
                    break

        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._merge_config(json.load(f))

    def _merge_config(self, user_config: dict) -> None:
        for key, value in user_config.items():
            if key in self._config and isinstance(self._config[key], dict):
                self._config[key].update(value)
            else:
                self._config[key] = value

    def get(self, *keys: str, default: Any = None) -> Any:
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
        return self._config.copy()
