from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from imprint.adapters import LocalTextAdapter, LocalTranscriptJsonAdapter
from imprint.classification import RuleBasedArtifactClassifier
from imprint.cli import app
from imprint.compiler import CompilerError, ProfileCompiler
from imprint.schemas import (
    ArtifactClassificationLabel,
    ClaimLevel,
    ClaimValidationMethod,
)
from imprint.signals import RuleBasedSignalExtractor

FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def compile_fixture(path: Path):
    artifacts = LocalTranscriptJsonAdapter().ingest(path)
    classifications = RuleBasedArtifactClassifier().classify_artifacts(artifacts)
    candidates = RuleBasedSignalExtractor().extract_batch(artifacts, classifications)
    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=classifications,
        signal_candidates=candidates,
    )
    return artifacts, classifications, candidates, profile


def test_only_durable_observation_signals_compile() -> None:
    _, classifications, candidates, profile = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    assert any(
        result.classification.label == ArtifactClassificationLabel.INCLUDED
        for result in classifications
    )
    assert profile.signals
    compiled_signal_ids = {
        signal_id for signal in profile.signals for signal_id in signal.support.signal_ids
    }
    assert compiled_signal_ids == {
        candidate.signal_id
        for candidate in candidates
        if candidate.durable and candidate.claim_level == ClaimLevel.OBSERVATION
    }
    assert all(signal.claim.level == ClaimLevel.OBSERVATION for signal in profile.signals)


def test_quarantined_signals_do_not_support_profile_claims() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "forwarded-thread.txt")[0]
    classification = RuleBasedArtifactClassifier().classify_artifact(artifact)
    candidates = RuleBasedSignalExtractor().extract_from_result(artifact, classification)

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=[artifact],
        classifications=[classification],
        signal_candidates=candidates,
    )

    assert candidates
    assert all(not candidate.durable for candidate in candidates)
    assert profile.signals == []
    assert profile.claims == []


def test_excluded_artifacts_produce_no_profile_support() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "assistant-output.txt")[0]
    classification = RuleBasedArtifactClassifier().classify_artifact(artifact)
    candidates = RuleBasedSignalExtractor().extract_from_result(artifact, classification)

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=[artifact],
        classifications=[classification],
        signal_candidates=candidates,
    )

    assert classification.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert candidates == []
    assert profile.signals == []
    assert profile.claims == []


def test_non_durable_candidates_do_not_support_profile_claims() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    non_durable = candidates[0].model_copy(update={"durable": False})

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=classifications,
        signal_candidates=[non_durable],
    )

    assert profile.signals == []
    assert profile.claims == []


def test_prohibited_signals_are_rejected_even_if_constructed_unsafely() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    prohibited = candidates[0].model_copy(update={"claim_level": ClaimLevel.PROHIBITED})

    with pytest.raises(CompilerError, match="prohibited signal cannot compile"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=artifacts,
            classifications=classifications,
            signal_candidates=[prohibited],
        )


def test_bounded_interpretations_are_excluded_by_default() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    bounded = candidates[0].model_copy(update={"claim_level": ClaimLevel.BOUNDED_INTERPRETATION})

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=classifications,
        signal_candidates=[bounded],
    )

    assert profile.signals == []
    assert profile.claims == []


def test_bounded_interpretations_compile_only_with_review_gated_policy() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    bounded = candidates[0].model_copy(update={"claim_level": ClaimLevel.BOUNDED_INTERPRETATION})

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=classifications,
        signal_candidates=[bounded],
        allow_bounded_interpretations=True,
    )

    assert len(profile.claims) == 1
    assert profile.claims[0].level == ClaimLevel.BOUNDED_INTERPRETATION
    assert ClaimValidationMethod.REVIEW_BASED in profile.claims[0].validation.methods


def test_profile_support_preserves_public_safe_versioned_metadata() -> None:
    _, _, _, profile = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    support = profile.signals[0].support
    assert support.signal_ids
    assert support.rule_ids
    assert support.classification_model_versions == ["sprint04-rule-v1"]
    assert support.signal_model_versions == ["sprint05-rule-v1"]
    assert support.evidence_refs[0].artifact_ref.artifact_id
    assert support.evidence_refs[0].artifact_ref.source_id.startswith("source-")
    assert support.evidence_refs[0].classification_id
    assert support.raw_content_available is False


def test_mixed_classifier_versions_are_recorded_in_support_and_manifest() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json"
    )
    assert len(classifications) >= 2
    changed_confidence = classifications[1].confidence.model_copy(
        update={"model_version": "sprint04-rule-v2"}
    )
    changed_classification = classifications[1].model_copy(
        update={"confidence": changed_confidence}
    )

    profile = ProfileCompiler().compile_profile(
        subject_id="synthetic-subject",
        artifacts=artifacts,
        classifications=[classifications[0], changed_classification, *classifications[2:]],
        signal_candidates=candidates,
    )

    manifest_versions = profile.build_manifest.classifier_version.split(",")
    assert sorted(manifest_versions) == ["sprint04-rule-v1", "sprint04-rule-v2"]
    support_versions = {
        version
        for signal in profile.signals
        for version in signal.support.classification_model_versions
    }
    assert support_versions == {"sprint04-rule-v1", "sprint04-rule-v2"}


def test_public_safe_compiled_profile_excludes_raw_text_and_paths() -> None:
    _, _, _, profile = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    serialized = profile.model_dump_json()
    assert "Start here" not in serialized
    assert "signal-transcript.json" not in serialized
    assert "/tests/fixtures/" not in serialized


def test_compilation_is_deterministic() -> None:
    first = compile_fixture(FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json")[3]
    second = compile_fixture(FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json")[3]

    assert first.model_dump(mode="json") == second.model_dump(mode="json")


def test_incompatible_signal_model_versions_are_rejected() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript-5-5.json"
    )
    assert len(candidates) >= 2
    changed_evidence = candidates[1].evidence.model_copy(
        update={"signal_model_version": "other-v1"}
    )
    mixed = candidates[1].model_copy(update={"evidence": changed_evidence})

    with pytest.raises(CompilerError, match="incompatible signal model versions"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=artifacts,
            classifications=classifications,
            signal_candidates=[candidates[0], mixed],
        )


def test_path_like_source_ids_are_rejected() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    path_like = candidates[0].model_copy(update={"source_id": "/private/source.txt"})

    with pytest.raises(ValueError, match="source_id cannot expose filesystem paths"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=artifacts,
            classifications=classifications,
            signal_candidates=[path_like],
        )


def test_missing_classification_or_artifact_is_rejected() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    with pytest.raises(CompilerError, match="signal has no classification result"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=artifacts,
            classifications=[],
            signal_candidates=[candidates[0]],
        )

    with pytest.raises(CompilerError, match="signal has no artifact"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=[],
            classifications=classifications,
            signal_candidates=[candidates[0]],
        )


def test_classification_id_mismatch_is_rejected() -> None:
    artifacts, classifications, candidates, _ = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )
    changed_classification = classifications[0].classification.model_copy(
        update={"classification_id": "classification-mismatch"}
    )
    mismatched_result = classifications[0].model_copy(
        update={"classification": changed_classification}
    )

    with pytest.raises(CompilerError, match="signal classification mismatch"):
        ProfileCompiler().compile_profile(
            subject_id="synthetic-subject",
            artifacts=artifacts,
            classifications=[mismatched_result, *classifications[1:]],
            signal_candidates=[candidates[0]],
        )


def test_compiler_uses_no_provider_or_llm_manifest_dependencies() -> None:
    _, _, _, profile = compile_fixture(
        FIXTURES / "local_transcript_json" / "signal-transcript.json"
    )

    assert profile.build_manifest.model_provider is None
    assert profile.build_manifest.model_name is None
    assert profile.build_manifest.model_version is None
    assert profile.build_manifest.profile_affecting_model_invocations == []


def test_compile_cli_smoke() -> None:
    result = RUNNER.invoke(
        app,
        [
            "compile",
            "--source-type",
            "local_transcript_json",
            "--path",
            str(FIXTURES / "local_transcript_json" / "signal-transcript.json"),
        ],
    )

    assert result.exit_code == 0
    assert "profile_id=profile-synthetic-subject-" in result.output
    assert "compiler_version=sprint06-rule-v1" in result.output
