from __future__ import annotations

from dataclasses import dataclass
import base64
from pathlib import Path
import re

SYNTHETIC_NAME_PATTERN = re.compile(r"(?:synthetic|example|fixture|test|demo)", re.IGNORECASE)
EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@(?!example\.(?:com|org|net)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})")
PRIVATE_URL_PATTERN = re.compile(
    r"https?://(?!example\.(?:com|org|net)\b|localhost\b)[^\s\"')]+",
    re.IGNORECASE,
)
LOCAL_HOME_PATTERN = re.compile(r"(?:/Users/[^\s\"']+|/home/[^\s\"']+|[A-Za-z]:\\Users\\[^\s\"']+)")
ACCOUNT_ID_PATTERN = re.compile(
    r"\b(?:acct|account|tenant|workspace|team|org)[_-]?[0-9A-Za-z]{8,}\b",
    re.IGNORECASE,
)
DSN_PATTERN = re.compile(r"[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s@]+@[^\s]+", re.IGNORECASE)
LEAKAGE_CREDENTIAL_PATTERN = re.compile(
    r"(?i)(?:"
    r"(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{12,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"(?:[?&](?:api[_-]?key|access[_-]?token|refresh[_-]?token|token|auth|code)=)[^\s&#]+|"
    r"DefaultEndpointsProtocol=[^;\s]+;AccountName=[^;\s]+;AccountKey=[^;\s]+|"
    r"(?:refresh[_-]?token|access[_-]?token|api[_-]?key|client[_-]?secret)=[A-Za-z0-9._~+/=-]{12,}"
    r")"
)


@dataclass(frozen=True)
class LeakageFinding:
    path: str
    reason_code: str
    detail: str


def scan_fixture_path(path: Path, *, require_synthetic_name: bool = True) -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    if require_synthetic_name and path.is_file() and not SYNTHETIC_NAME_PATTERN.search(path.name):
        findings.append(
            LeakageFinding(
                path=str(path),
                reason_code="fixture_name_not_synthetic",
                detail="fixture filename must include synthetic, example, fixture, test, or demo",
            )
        )
    if not path.is_file():
        return findings
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append(
            LeakageFinding(
                path=str(path),
                reason_code="binary_fixture_requires_review",
                detail="fixture is not UTF-8 text",
            )
        )
        return findings
    checks = [
        ("real_email", EMAIL_PATTERN),
        ("phone_number", PHONE_PATTERN),
        ("private_url", PRIVATE_URL_PATTERN),
        ("local_home_path", LOCAL_HOME_PATTERN),
        ("account_identifier", ACCOUNT_ID_PATTERN),
        ("credential_or_token", LEAKAGE_CREDENTIAL_PATTERN),
        ("dsn", DSN_PATTERN),
    ]
    for reason_code, pattern in checks:
        if pattern.search(text):
            findings.append(
                LeakageFinding(
                    path=str(path),
                    reason_code=reason_code,
                    detail=f"fixture content matched {reason_code}",
                )
            )
    for decoded in _bounded_decoded_strings(text):
        if LEAKAGE_CREDENTIAL_PATTERN.search(decoded):
            findings.append(
                LeakageFinding(
                    path=str(path),
                    reason_code="encoded_credential_or_token",
                    detail="fixture content decoded to credential-like text",
                )
            )
        if LOCAL_HOME_PATTERN.search(decoded):
            findings.append(
                LeakageFinding(
                    path=str(path),
                    reason_code="encoded_local_home_path",
                    detail="fixture content decoded to a local home path",
                )
            )
    return findings


def scan_fixture_tree(root: Path, *, require_synthetic_name: bool = True) -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        findings.extend(scan_fixture_path(path, require_synthetic_name=require_synthetic_name))
    return findings


def _bounded_decoded_strings(value: str) -> list[str]:
    decoded: list[str] = []
    for match in re.finditer(r"[A-Za-z0-9+/_=-]{16,}", value):
        token = match.group(0)
        padding = "=" * (-len(token) % 4)
        for decoder in (base64.b64decode, base64.urlsafe_b64decode):
            try:
                candidate = decoder(token + padding).decode("utf-8")
            except Exception:
                continue
            if candidate and candidate != token:
                decoded.append(candidate)
    return list(dict.fromkeys(decoded))
