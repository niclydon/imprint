from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from imprint.adapters import ArtifactEnvelope
from imprint.adapters import LocalJsonlAdapter, LocalMarkdownAdapter, LocalTextAdapter, LocalTranscriptJsonAdapter
from imprint.adapters.normalization import envelope_to_artifact
from imprint.classification import RuleBasedArtifactClassifier
from imprint.cli import app
from imprint.connectors import ConsentAction, ConsentClass, evaluate_consent_boundary
from imprint.schemas import ArtifactStoragePolicy
from imprint.schemas import ArtifactClassificationLabel, ArtifactType, AuthorshipOrigin


FIXTURES = Path(__file__).parent / "fixtures"
RUNNER = CliRunner()


def test_classifier_reassesses_jsonl_hints_as_advisory() -> None:
    artifacts = LocalJsonlAdapter().ingest(FIXTURES / "local_jsonl" / "synthetic-records.jsonl")

    results = RuleBasedArtifactClassifier().classify_artifacts(artifacts)

    first = results[0]
    second = results[1]
    assert first.classification.authorship_origin == AuthorshipOrigin.MISSING_METADATA
    assert first.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert second.artifact_type == ArtifactType.DOCUMENT
    assert second.classification.authorship_origin == AuthorshipOrigin.HUMAN_DIRECTED_AI_ASSISTED
    assert second.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert second.classification.authorship_confidence < 0.7
    assert second.confidence.model_version == "sprint04-rule-v1"
    assert second.confidence.display < 0.65
    assert second.evidence.source_hints_considered["artifact_type_hint"] == "technical_note"
    assert second.evidence.source_hints_considered["ingest_classification_label"] == "included"


def test_classifier_quarantines_unknown_speaker_transcript_segment() -> None:
    artifacts = LocalTranscriptJsonAdapter().ingest(
        FIXTURES / "local_transcript_json" / "synthetic-transcript.json"
    )

    results = RuleBasedArtifactClassifier().classify_artifacts(artifacts)

    assert results[0].classification.label == ArtifactClassificationLabel.INCLUDED
    assert results[0].classification.authorship_origin == AuthorshipOrigin.HUMAN_ORIGIN
    assert results[0].confidence.display >= 0.65
    assert results[1].classification.label == ArtifactClassificationLabel.QUARANTINED
    assert results[1].classification.authorship_origin == AuthorshipOrigin.UNKNOWN_SPEAKER
    assert results[1].classification.authorship_confidence < 0.5
    assert results[1].confidence.display < results[0].confidence.display


def test_classifier_excludes_assistant_output_artifacts() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "assistant-output.txt")[0]

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.authorship_origin == AuthorshipOrigin.ASSISTANT_OUTPUT
    assert result.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert result.evidence.assistant_output_likelihood >= 0.85
    assert result.confidence.display < 0.8


def test_classifier_quarantines_forwarded_and_excludes_template_notifications() -> None:
    forwarded = LocalTextAdapter().ingest(FIXTURES / "local_text" / "forwarded-thread.txt")[0]
    template = LocalMarkdownAdapter().ingest(FIXTURES / "local_markdown" / "template-notification.md")[0]

    forwarded_result = RuleBasedArtifactClassifier().classify_artifact(forwarded)
    template_result = RuleBasedArtifactClassifier().classify_artifact(template)

    assert forwarded_result.classification.authorship_origin == AuthorshipOrigin.QUOTED_OR_FORWARDED
    assert forwarded_result.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert forwarded_result.evidence.quote_or_forward_likelihood >= 0.85

    assert template_result.classification.authorship_origin == AuthorshipOrigin.TEMPLATE_OR_NOTIFICATION
    assert template_result.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert template_result.evidence.template_or_notification_likelihood >= 0.85
    assert template_result.confidence.contamination_penalty >= 0.85


def test_classification_output_is_opaque_and_explainable() -> None:
    artifact = LocalMarkdownAdapter().ingest(FIXTURES / "local_markdown" / "synthetic-brief.md")[0]

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.source_id.startswith("source-")
    assert "synthetic-brief.md" not in result.source_id
    assert result.evidence.rule_ids
    assert result.evidence.evidence_summary
    assert "line_count" in result.evidence.source_hints_considered
    assert result.confidence.model_version == "sprint04-rule-v1"


def test_classifier_policy_tree_matches_exclude_vs_quarantine_rules() -> None:
    assistant = LocalTextAdapter().ingest(FIXTURES / "local_text" / "assistant-output.txt")[0]
    forwarded = LocalTextAdapter().ingest(FIXTURES / "local_text" / "forwarded-thread.txt")[0]

    classifier = RuleBasedArtifactClassifier()
    assistant_result = classifier.classify_artifact(assistant)
    forwarded_result = classifier.classify_artifact(forwarded)

    assert assistant_result.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert forwarded_result.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert "exclude_non_subject_authorship" in assistant_result.evidence.rule_ids
    assert "quarantine_uncertain_authorship" in forwarded_result.evidence.rule_ids


def test_consent_boundary_excludes_received_mail_before_durable_support() -> None:
    artifact = envelope_to_artifact(
        ArtifactEnvelope(
            source_type="gmail",
            source_id="synthetic-received-mail",
            content="A third party wrote this received message.",
            metadata={"source_family": "gmail", "source_role": "received"},
        ),
        storage_policy=ArtifactStoragePolicy(),
    )

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert result.evidence.source_hints_considered["consent_class"] == ConsentClass.THIRD_PARTY_AUTHORED
    assert result.evidence.source_hints_considered["consent_action"] == ConsentAction.EXCLUDE
    assert "consent_boundary_excludes_non_subject_content" in result.evidence.rule_ids


def test_consent_boundary_quarantines_group_chat_participant_messages() -> None:
    artifact = envelope_to_artifact(
        ArtifactEnvelope(
            source_type="imessage",
            source_id="synthetic-group-chat",
            content="A group chat participant wrote this message.",
            metadata={"source_family": "imessage", "group_chat": True},
        ),
        storage_policy=ArtifactStoragePolicy(),
    )

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert result.evidence.source_hints_considered["consent_class"] == ConsentClass.MIXED
    assert result.evidence.source_hints_considered["consent_action"] == ConsentAction.QUARANTINE
    assert "consent_boundary_quarantines_unproven_subject_authorship" in result.evidence.rule_ids


def test_consent_boundary_excludes_third_party_transcript_speaker() -> None:
    artifact = envelope_to_artifact(
        ArtifactEnvelope(
            source_type="local_transcript_json",
            source_id="synthetic-third-party-speaker",
            content="A non-subject speaker said this transcript segment.",
            metadata={"source_family": "transcript", "speaker_present": True, "speaker_role": "other"},
        ),
        storage_policy=ArtifactStoragePolicy(),
    )

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.label == ArtifactClassificationLabel.EXCLUDED
    assert result.evidence.source_hints_considered["consent_class"] == ConsentClass.THIRD_PARTY_AUTHORED
    assert result.evidence.source_hints_considered["consent_action"] == ConsentAction.EXCLUDE


def test_consent_boundary_allows_subject_authored_source_hints() -> None:
    decision = evaluate_consent_boundary(
        "gmail",
        {"source_family": "gmail", "source_role": "sent"},
    )

    assert decision.allows_durable_support is True
    assert decision.consent_class == ConsentClass.OWNER_AUTHORED


def test_private_source_alias_without_consent_hints_quarantines() -> None:
    decision = evaluate_consent_boundary("sent_mail", {})

    assert decision.allows_durable_support is False
    assert decision.consent_class == ConsentClass.UNKNOWN
    assert decision.action == ConsentAction.QUARANTINE


def test_transcript_segment_without_speaker_role_quarantines() -> None:
    artifact = envelope_to_artifact(
        ArtifactEnvelope(
            source_type="local_transcript_json",
            source_id="synthetic-speaker-without-role",
            content="A speaker is named, but the subject role is not explicit.",
            metadata={"speaker_present": True},
        ),
        storage_policy=ArtifactStoragePolicy(),
    )

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.label == ArtifactClassificationLabel.QUARANTINED
    assert result.evidence.source_hints_considered["consent_class"] == ConsentClass.UNKNOWN


def test_classifier_runs_without_provider_configuration() -> None:
    artifact = LocalTextAdapter().ingest(FIXTURES / "local_text" / "synthetic-note.txt")[0]

    result = RuleBasedArtifactClassifier().classify_artifact(artifact)

    assert result.classification.classification_id.startswith("classified-")
    assert result.evidence.rule_ids


def test_classifier_handles_small_batch_without_cross_artifact_state() -> None:
    artifacts = [LocalTextAdapter().ingest(FIXTURES / "local_text" / "synthetic-note.txt")[0] for _ in range(250)]
    for index, artifact in enumerate(artifacts):
        artifact.artifact_id = f"{artifact.artifact_id}-{index}"  # type: ignore[misc]

    results = RuleBasedArtifactClassifier().classify_artifacts(artifacts)

    assert len(results) == 250
    assert all(result.confidence.model_version == "sprint04-rule-v1" for result in results)


def test_cli_classify_reports_classification_summary() -> None:
    result = RUNNER.invoke(
        app,
        [
            "classify",
            "--source-type",
            "local_transcript_json",
            "--path",
            str(FIXTURES / "local_transcript_json" / "synthetic-transcript.json"),
        ],
    )

    assert result.exit_code == 0
    assert "source_type=local_transcript_json" in result.stdout
    assert "classified=2" in result.stdout
    assert "included=1" in result.stdout
    assert "quarantined=1" in result.stdout
