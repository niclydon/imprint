from __future__ import annotations

from imprint.exports.json_export import canonical_profile_export
from imprint.schemas import ExpressionProfile


def markdown_profile_export(profile: ExpressionProfile) -> str:
    payload = canonical_profile_export(profile)
    lines = [
        f"# Imprint Profile Summary: `{payload['profile']['profile_id']}`",
        "",
        "## Basis",
        "",
        f"- Subject ID: `{payload['profile']['subject_id']}`",
        f"- Compiler version: `{payload['compatibility']['compiler_version']}`",
        f"- Export schema: `{payload['compatibility']['export_schema_version']}`",
        f"- Profile signals: {payload['source_summary']['profile_signal_count']}",
        f"- Included support count: {payload['source_summary']['included_support_count']}",
        "",
        "## Observed Expression Patterns",
        "",
    ]
    patterns = sorted(
        payload["expression_patterns"],
        key=lambda item: (-item["confidence"]["display"], item["family"], item["name"]),
    )
    if not patterns:
        lines.append("No durable public-safe expression patterns compiled yet.")
    for pattern in patterns:
        lines.extend(
            [
                f"### Observed pattern: {pattern['name']}",
                "",
                f"- Family: `{pattern['family']}`",
                f"- Claim level: `{pattern['claim']['level']}`",
                f"- Summary: {pattern['claim']['text']}",
                f"- Confidence: {pattern['confidence']['display']}",
                f"- Supported by: {pattern['support']['included_count']} included artifacts",
                f"- Source types: {', '.join(pattern['support']['source_types']) or 'none'}",
                f"- Rule IDs: {', '.join(pattern['support']['rule_ids'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## Limitations and Privacy",
            "",
            "- This summary is based on compiled profile metadata, not raw artifacts.",
            "- Confidence summarizes support strength, not truth about a person.",
            (
                "- Public-safe exports exclude raw text, filesystem paths, private "
                "locators, and generation controls."
            ),
        ]
    )
    for limitation in payload["limitations"]:
        lines.append(f"- {limitation}")
    lines.extend(
        [
            "",
            "## Compatibility",
            "",
            (
                "- Classifier versions: "
                f"{', '.join(payload['compatibility']['classifier_versions']) or 'none'}"
            ),
            (
                "- Signal model versions: "
                f"{', '.join(payload['compatibility']['signal_model_versions']) or 'none'}"
            ),
        ]
    )
    for warning in payload["compatibility"]["warnings"]:
        lines.append(f"- Warning: {warning}")
    return "\n".join(lines).rstrip() + "\n"
