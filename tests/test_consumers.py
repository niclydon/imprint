from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.adapters import LocalTranscriptJsonAdapter
from imprint.classification import RuleBasedArtifactClassifier
from imprint.cli import app
from imprint.compiler import ProfileCompiler
from imprint.consumers import (
    agent_consumer_contract,
    broadside_consumer_contract,
    mosvera_consumer_contract,
    validate_consumer_payload,
)
from imprint.exports import ExportSafetyError
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


def test_mosvera_consumer_payload_is_expression_overlay_only() -> None:
    payload = mosvera_consumer_contract(compiled_profile())
    serialized = json.dumps(payload, sort_keys=True)

    assert payload["contract"] == "mosvera_consumer_contract"
    assert payload["evidence_policy"]["raw_text_included"] is False
    assert payload["evidence_policy"]["generation_controls_included"] is False
    assert payload["compatibility"]["mandatory_in_consumer_projection"] is True
    assert "source_ids" in payload["expression_summaries"][0]
    assert "Start here" not in serialized
    assert "prompt" not in serialized
    assert "provider" not in serialized
    assert "image generation" not in serialized
    assert "runtime adapter" not in serialized


def test_broadside_consumer_payload_contains_constraints_not_publishing_logic() -> None:
    payload = broadside_consumer_contract(compiled_profile())
    serialized = json.dumps(payload, sort_keys=True)

    assert payload["contract"] == "broadside_consumer_contract"
    assert payload["observed_expression_patterns"]
    assert payload["compatibility"]["warnings"]
    assert "publishing workflow" not in serialized
    assert "editorial workflow" not in serialized
    assert "platform-specific" not in serialized
    assert "model parameters" not in serialized
    assert "raw evidence" not in serialized


def test_agent_consumer_payload_preserves_warnings_and_safety_rules() -> None:
    payload = agent_consumer_contract(compiled_profile())

    assert payload["contract"] == "agent_consumer_contract"
    assert payload["compatibility"]["mandatory_in_consumer_projection"] is True
    assert payload["compatibility"]["warnings"]
    assert "do not treat confidence as truth" in payload["usage_rules"]
    assert "safe_pattern_lookup" in payload


def test_consumer_projections_preserve_opaque_ids_and_no_raw_text_policy() -> None:
    contracts = [
        mosvera_consumer_contract(compiled_profile()),
        broadside_consumer_contract(compiled_profile()),
        agent_consumer_contract(compiled_profile()),
    ]

    for contract in contracts:
        serialized = json.dumps(contract, sort_keys=True)
        assert "source-" in serialized
        assert "signal-transcript.json" not in serialized
        assert "/tests/fixtures/" not in serialized
        assert contract["evidence_policy"]["raw_text_included"] is False
        assert contract["evidence_policy"]["source_references"] == "opaque_source_ids_only"


def test_mixed_classifier_version_warning_appears_in_consumer_projection() -> None:
    profile = compiled_profile()
    support = profile.signals[0].support.model_copy(
        update={"classification_model_versions": ["classifier-v1", "classifier-v2"]}
    )
    signal = profile.signals[0].model_copy(update={"support": support})
    mutated = profile.model_copy(update={"signals": [signal, *profile.signals[1:]]})

    payload = agent_consumer_contract(mutated)

    assert "multiple classifier versions are represented in support metadata" in payload[
        "compatibility"
    ]["warnings"]


@pytest.mark.parametrize("field", ["prompt", "temperature", "model_hint", "provider", "system_prompt"])
def test_consumer_validator_rejects_generation_control_fields(field: str) -> None:
    with pytest.raises(ExportSafetyError, match="generation-control fields"):
        validate_consumer_payload({"contract": "bad", field: "not allowed"})


def test_consumer_cli_smoke_for_contract_formats() -> None:
    path = str(FIXTURES / "local_transcript_json" / "signal-transcript.json")
    formats = {
        "mosvera-consumer": "mosvera_consumer_contract",
        "broadside": "broadside_consumer_contract",
        "agent": "agent_consumer_contract",
        "human-cli": "human_cli_consumer_contract",
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
