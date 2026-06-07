from __future__ import annotations

from imprint.exports.json_export import canonical_profile_export
from imprint.schemas import ExpressionProfile


def first_run_summary(profile: ExpressionProfile) -> str:
    payload = canonical_profile_export(profile)
    patterns = sorted(
        payload["expression_patterns"],
        key=lambda item: (-item["confidence"]["display"], item["name"]),
    )
    lines = [
        "# What Imprint Learned",
        "",
        (
            "Imprint compiled a public-safe expression profile from normalized, "
            "classified, and validated signal metadata."
        ),
        "It did not use raw artifact text for this report.",
        "",
        "## Profile Overview",
        "",
        f"- Profile ID: `{payload['profile']['profile_id']}`",
        f"- Observed pattern count: {len(patterns)}",
        f"- Included support count: {payload['source_summary']['included_support_count']}",
        f"- Artifact storage mode: `{payload['profile']['artifact_storage']['mode']}`",
        "",
        "## Strongest Observed Patterns",
        "",
    ]
    if not patterns:
        lines.append(
            "Imprint did not find enough durable public-safe evidence to summarize "
            "expression patterns yet."
        )
    for pattern in patterns[:5]:
        count = pattern["support"]["included_count"]
        lines.extend(
            [
                f"- Observed pattern `{pattern['name']}`: {pattern['claim']['text']} "
                f"Supported by {_artifact_count(count)} "
                f"with confidence {pattern['confidence']['display']}.",
            ]
        )
    low_confidence = [pattern for pattern in patterns if pattern["confidence"]["display"] < 0.5]
    lines.extend(
        [
            "",
            "## Limits and Cautions",
            "",
            (
                "- Imprint can describe supported expression patterns; it cannot diagnose, "
                "infer intent, or prove identity traits."
            ),
            "- Quarantined and excluded artifacts are not used as durable profile evidence.",
            "- Metadata-only storage limits audit detail in public-safe outputs.",
        ]
    )
    if low_confidence:
        lines.append(
            f"- {len(low_confidence)} patterns have limited confidence and should be "
            "treated cautiously."
        )
    for warning in payload["compatibility"]["warnings"]:
        lines.append(f"- Compatibility warning: {warning}.")
    lines.extend(
        [
            "",
            "## What Imprint Cannot Say",
            "",
            "- It cannot say what the subject is, feels, wants, believes, or intends.",
            (
                "- It cannot treat punctuation, formatting, or source metadata as "
                "psychological ground truth."
            ),
            "- It cannot expose private raw evidence in public-safe exports.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _artifact_count(count: int) -> str:
    label = "artifact" if count == 1 else "artifacts"
    return f"{count} included {label}"
