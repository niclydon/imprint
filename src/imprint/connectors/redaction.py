from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

SECRET_KEY_PATTERN = re.compile(
    r"(api[_-]?key|token|secret|password|credential|dsn|refresh|connection[_-]?string|auth)",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(?:"
    r"(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{12,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"(?:postgres(?:ql)?|mysql|mongodb(?:\\+srv)?|redis|mssql)://[^\s:/@]+:[^\s@]+@[^\s]+|"
    r"(?:[?&](?:api[_-]?key|access[_-]?token|refresh[_-]?token|token|auth|code)=)[^\\s&#]+|"
    r"DefaultEndpointsProtocol=[^;\\s]+;AccountName=[^;\\s]+;"
    r"AccountKey=[^;\\s]+(?:;EndpointSuffix=[^;\\s]+)?|"
    r"(?:refresh[_-]?token|access[_-]?token|api[_-]?key|client[_-]?secret)=[A-Za-z0-9._~+/=-]{12,}|"
    r"[A-Za-z0-9_\\-]{24,}"
    r")"
)
LOCAL_HOME_VALUE_PATTERN = re.compile(
    r"(?:/Users/[^\s\"']+|/home/[^\s\"']+|[A-Za-z]:\\Users\\[^\s\"']+)"
)
PATH_VALUE_PATTERN = re.compile(r"(?:^/|^[A-Za-z]:[\\/]|\.\.|[/\\][^\s]+[/\\]|~[/\\][^\s]+)")

REDACTED = "[REDACTED]"


def redact_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if key_text == "env" and isinstance(item, str) and item.startswith("IMPRINT_"):
                redacted[key_text] = item
            elif SECRET_KEY_PATTERN.search(key_text):
                redacted[REDACTED] = REDACTED
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
    redacted = LOCAL_HOME_VALUE_PATTERN.sub(REDACTED, redacted)
    return PATH_VALUE_PATTERN.sub(REDACTED, redacted)


def safe_error(message: str, context: Mapping[str, Any] | None = None) -> str:
    if not context:
        return redact_text(message)
    return f"{redact_text(message)}: {redact_value(dict(context))}"
