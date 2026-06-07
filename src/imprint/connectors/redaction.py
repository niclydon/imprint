from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

SECRET_KEY_PATTERN = re.compile(r"(api[_-]?key|token|secret|password|credential|dsn)", re.IGNORECASE)
SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(Bearer\s+)?[A-Za-z0-9_\-]{20,}|[a-z][a-z0-9+.-]*://[^\s]+:[^\s@]+@[^\s]+"
)
PATH_VALUE_PATTERN = re.compile(r"(?:^/|^[A-Za-z]:[\\/]|\.\.|[/\\][^\s]+[/\\])")

REDACTED = "[REDACTED]"


def redact_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if key_text == "env":
                redacted[key_text] = item
            elif SECRET_KEY_PATTERN.search(key_text):
                redacted[key_text] = REDACTED
            else:
                redacted[key_text] = redact_value(item)
        return redacted
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_text(value: str) -> str:
    redacted = SECRET_VALUE_PATTERN.sub(REDACTED, value)
    return PATH_VALUE_PATTERN.sub(REDACTED, redacted)


def safe_error(message: str, context: Mapping[str, Any] | None = None) -> str:
    if not context:
        return redact_text(message)
    return f"{redact_text(message)}: {redact_value(dict(context))}"
