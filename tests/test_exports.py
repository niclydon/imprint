from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.adapters import LocalTranscriptJsonAdapter
from imprint.classification import RuleBasedArtifactClassifier
from imprint.cli import app
from imprint.compiler import ProfileCompiler
from imprint.exports import (
    ExportSafetyError,
    canonical_profile_export,
    canonical_profile_json,
    first_run_summary,
    markdown_profile_export,
    mosvera_expression_overlay,
)
from imprint.schemas import ClaimLevel, ClaimValidationMethod
from imprint.signals import RuleBasedSignalExtractor

FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def compiled_profile(path: Path = FIXTURES / "local_transcript_json" / "signal-transcript.json"):
    artifacts = LocalTranscriptJsonAdapter().ingest(path)
    classifications = RuleBasedArtifactClassifier().classify_artifacts(artifacts)
    candidates = RuleBasedSignalExtractor().extract_batch(artifacts, classifications)
    return ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=classifications,
        signal_candidates=candidates,
    )


def test_canonical_json_export_is_deterministic() -> None:
    profile = compiled_profile()

    first = canonical_profile_json(profile)
    second = canonical_profile_json(profile)

    assert first == second
    payload = json.loads(first)
    assert payload["export_type"] == "canonical_json"
    assert payload["profile"]["profile_id"] == profile.profile_id
    assert payload["expression_patterns"]


def test_markdown_export_is_deterministic_and_conservative() -> None:
    profile = compiled_profile()

    first = markdown_profile_export(profile)
    second = markdown_profile_export(profile)

    assert first == second
    assert "Observed pattern" in first
    assert "Supported by" in first
    assert "The subject is" not in first
    assert "Personality" not in first


def test_public_safe_exports_contain_no_raw_text_or_paths() -> None:
    profile = compiled_profile()
    outputs = [
        canonical_profile_json(profile),
        markdown_profile_export(profile),
        first_run_summary(profile),
        json.dumps(mosvera_expression_overlay(profile), sort_keys=True),
    ]

    for output in outputs:
        assert "Start here" not in output
        assert "signal-transcript.json" not in output
        assert "/tests/fixtures/" not in output
        assert "source_path" not in output


def test_prohibited_claims_cannot_export_even_if_profile_is_mutated() -> None:
    profile = compiled_profile()
    bad_claim = profile.claims[0].model_copy(update={"level": ClaimLevel.PROHIBITED})
    bad_profile = profile.model_copy(update={"claims": [bad_claim]})

    with pytest.raises(ExportSafetyError, match="prohibited claim cannot export"):
        canonical_profile_export(bad_profile)


def test_bounded_interpretations_remain_policy_gated_for_exports() -> None:
    profile = compiled_profile()
    bounded_claim = profile.claims[0].model_copy(
        update={"level": ClaimLevel.BOUNDED_INTERPRETATION}
    )
    bounded_signal = profile.signals[0].model_copy(update={"claim": bounded_claim})
    bounded_profile = profile.model_copy(
        update={"claims": [bounded_claim], "signals": [bounded_signal]}
    )

    with pytest.raises(ExportSafetyError, match="bounded interpretation is not export-enabled"):
        canonical_profile_export(bounded_profile)

    payload = canonical_profile_export(bounded_profile, allow_bounded_interpretations=True)
    methods = payload["expression_patterns"][0]["claim"]["validation"]["methods"]
    assert ClaimValidationMethod.REVIEW_BASED not in methods or methods


def test_opaque_source_ids_remain_opaque_in_json_export() -> None:
    payload = canonical_profile_export(compiled_profile())

    source_ids = [
        source_id
        for pattern in payload["expression_patterns"]
        for source_id in pattern["support"]["source_ids"]
    ]

    assert source_ids
    assert all(source_id.startswith("source-") for source_id in source_ids)
    assert all("/" not in source_id and "\\" not in source_id for source_id in source_ids)


def test_incompatible_signal_versions_cannot_export_as_comparable() -> None:
    profile = compiled_profile()
    support = profile.signals[0].support.model_copy(
        update={"signal_model_versions": ["sprint05-rule-v1", "sprint05-rule-v2"]}
    )
    signal = profile.signals[0].model_copy(update={"support": support})
    unsafe_profile = profile.model_copy(update={"signals": [signal]})

    with pytest.raises(ExportSafetyError, match="mixed signal model versions cannot export"):
        canonical_profile_export(unsafe_profile)


def test_first_run_summary_uses_compiled_profile_data_only() -> None:
    output = first_run_summary(compiled_profile())

    assert "What Imprint Learned" in output
    assert "Observed pattern" in output
    assert "raw artifact text" in output
    assert "Start here" not in output
    assert "The subject is" not in output
    assert "diagnose" in output


def test_mosvera_overlay_contains_expression_only_no_provider_prompts() -> None:
    overlay = mosvera_expression_overlay(compiled_profile())
    serialized = json.dumps(overlay, sort_keys=True)

    assert overlay["contract"] == "mosvera_expression_overlay"
    assert overlay["evidence_policy"]["raw_text_included"] is False
    assert overlay["evidence_policy"]["generation_controls_included"] is False
    assert "expression_summaries" in overlay
    assert "prompt" not in serialized
    assert "provider" not in serialized
    assert "Start here" not in serialized


def test_export_cli_smoke_for_all_formats() -> None:
    path = str(FIXTURES / "local_transcript_json" / "signal-transcript.json")
    formats = {
        "json": "canonical_json",
        "markdown": "Observed Expression Patterns",
        "first-run": "What Imprint Learned",
        "mosvera": "mosvera_expression_overlay",
    }

    for export_format, expected in formats.items():
        result = RUNNER.invoke(
            app,
            [
                "export-profile",
                "--source-type",
                "local_transcript_json",
                "--path",
                path,
                "--format",
                export_format,
            ],
        )
        assert result.exit_code == 0
        assert expected in result.output
