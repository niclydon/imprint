from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from imprint.adapters import LocalTextAdapter, LocalTranscriptJsonAdapter
from imprint.classification import RuleBasedArtifactClassifier
from imprint.cli import app
from imprint.schemas import ArtifactClassificationLabel, ArtifactSignalFamily, ClaimLevel
from imprint.signals import RuleBasedSignalExtractor


FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def classify_and_extract(path: Path) -> tuple[list, list, list]:
    artifacts = LocalTranscriptJsonAdapter().ingest(path)
    classifications = RuleBasedArtifactClassifier().classify_artifacts(artifacts)
    signals = RuleBasedSignalExtractor().extract_batch(artifacts, classifications)
    return artifacts, classifications, signals


def test_included_artifacts_produce_durable_signals() -> None:
    _, classifications, signals = classify_and_extract(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    assert any(result.classification.label == ArtifactClassificationLabel.INCLUDED for result in classifications)
    assert any(signal.durable for signal in signals)
    assert all(signal.claim_level == ClaimLevel.OBSERVATION for signal in signals if signal.durable)


def test_excluded_artifacts_produce_no_signals() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "assistant-output.txt")[0]
    classification = RuleBasedArtifactClassifier().classify_artifact(artifact)

    signals = RuleBasedSignalExtractor().extract_from_result(artifact, classification)

    assert classification.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert signals == []


def test_quarantined_artifacts_do_not_support_durable_signals() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "forwarded-thread.txt")[0]
    classification = RuleBasedArtifactClassifier().classify_artifact(artifact)

    signals = RuleBasedSignalExtractor().extract_from_result(artifact, classification)

    assert classification.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert signals
    assert all(signal.durable is False for signal in signals)
    assert all(signal.claim_level == ClaimLevel.QUARANTINED for signal in signals)


def test_each_signal_includes_public_safe_evidence_metadata() -> None:
    _, _, signals = classify_and_extract(FIXTURES / "local_transcript_json" / "signal-transcript.json")

    assert signals
    for signal in signals:
        assert signal.evidence.rule_id
        assert signal.evidence.classification_id
        assert signal.evidence.no_raw_text is True
        assert signal.source_id.startswith("source-")
        assert "signal-transcript.json" not in signal.source_id
        assert "transcript" not in signal.observed_feature.lower() or "signal-transcript.json" not in signal.observed_feature


def test_signal_candidates_do_not_contain_personality_or_diagnostic_claims() -> None:
    _, _, signals = classify_and_extract(FIXTURES / "local_transcript_json" / "signal-transcript.json")

    blocked_terms = ("analytical", "introvert", "anxious", "depressed", "bipolar", "adhd")
    for signal in signals:
        haystack = f"{signal.name} {signal.observed_feature}".lower()
        assert not any(term in haystack for term in blocked_terms)


def test_signal_extraction_is_deterministic_and_local_only() -> None:
    artifacts = LocalTranscriptJsonAdapter().ingest(FIXTURES / "local_transcript_json" / "signal-transcript.json")
    classifier = RuleBasedArtifactClassifier()
    classifications = classifier.classify_artifacts(artifacts)
    extractor = RuleBasedSignalExtractor()

    first = [signal.model_dump(mode="json") for signal in extractor.extract_batch(artifacts, classifications)]
    second = [signal.model_dump(mode="json") for signal in extractor.extract_batch(artifacts, classifications)]

    assert first == second
    assert all(signal["evidence"]["classification_model_version"] == "sprint04-rule-v1" for signal in first)


def test_signal_extraction_handles_simple_linear_batch() -> None:
    artifacts = []
    for index in range(120):
        artifact = LocalTranscriptJsonAdapter().ingest(
            FIXTURES / "local_transcript_json" / "signal-transcript.json"
        )[0]
        artifact.artifact_id = f"{artifact.artifact_id}-{index}"  # type: ignore[misc]
        artifacts.append(artifact)
    classifications = RuleBasedArtifactClassifier().classify_artifacts(artifacts)

    signals = RuleBasedSignalExtractor().extract_batch(artifacts, classifications)

    assert len(classifications) == 120
    assert len(signals) >= 120


def test_sprint_5_5_reasoning_narrative_and_anti_pattern_signals_are_emitted() -> None:
    _, classifications, signals = classify_and_extract(
        FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json"
    )

    assert all(result.classification.label == ArtifactClassificationLabel.INCLUDED for result in classifications)
    families = {(signal.family, signal.evidence.rule_id) for signal in signals}
    assert (ArtifactSignalFamily.REASONING, "reasoning_causal_explanation") in families
    assert (ArtifactSignalFamily.REASONING, "reasoning_tradeoff_framing") in families
    assert (ArtifactSignalFamily.NARRATIVE, "narrative_ordered_sequence") in families
    assert (ArtifactSignalFamily.NARRATIVE, "narrative_before_after_transition") in families
    assert (ArtifactSignalFamily.NARRATIVE, "narrative_example_grounding") in families
    assert (ArtifactSignalFamily.ANTI_PATTERN, "anti_pattern_question_burst") in families
    assert (ArtifactSignalFamily.ANTI_PATTERN, "anti_pattern_punctuation_emphasis") in families


def test_anti_pattern_signal_remains_artifact_local_and_public_safe() -> None:
    _, _, signals = classify_and_extract(FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json")

    anti_pattern_signals = [signal for signal in signals if signal.family == ArtifactSignalFamily.ANTI_PATTERN]
    assert anti_pattern_signals
    for signal in anti_pattern_signals:
        assert signal.source_id.startswith("source-")
        assert signal.claim_level == ClaimLevel.OBSERVATION
        lowered = signal.observed_feature.lower()
        assert "profile" not in lowered
        assert "personality" not in lowered
        assert "across artifacts" not in lowered


def test_signal_model_version_is_tracked() -> None:
    _, _, signals = classify_and_extract(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    assert signals
    for signal in signals:
        assert signal.evidence.signal_model_version == "sprint05-rule-v1"
        assert signal.evidence.classification_model_version == "sprint04-rule-v1"


def test_source_id_validation_rejects_paths() -> None:
    from imprint.signals.engine import validate_source_id

    # Valid source IDs
    validate_source_id("source-abc123")
    validate_source_id("source-transcript-001")

    # Invalid: filesystem paths
    try:
        validate_source_id("/home/user/file.txt")
        assert False, "should reject absolute path"
    except ValueError:
        pass

    try:
        validate_source_id("C:\\Users\\file.txt")
        assert False, "should reject Windows path"
    except ValueError:
        pass

    try:
        validate_source_id("../../../etc/passwd")
        assert False, "should reject path traversal"
    except ValueError:
        pass

    try:
        validate_source_id("artifacts/data.json")
        assert False, "should reject file extension"
    except ValueError:
        pass


def test_cli_extract_signals_reports_summary() -> None:
    result = RUNNER.invoke(
        app,
        [
            "extract-signals",
            "--source-type",
            "local_transcript_json",
            "--path",
            str(FIXTURES / "local_transcript_json" / "signal-transcript.json"),
        ],
    )

    assert result.exit_code == 0
    assert "source_type=local_transcript_json" in result.stdout
    assert "signals=" in result.stdout
    assert "durable=" in result.stdout
