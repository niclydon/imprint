from __future__ import annotations

import pytest
from pydantic import ValidationError

from imprint.schemas import (
    ArtifactClassificationLabel,
    ArtifactReference,
    ArtifactStoragePolicy,
    AuthorshipOrigin,
    BuildManifest,
    Claim,
    ClaimLevel,
    ClaimValidation,
    ClaimValidationMethod,
    ClaimValidationStatus,
    ComparabilityLabel,
    ComparabilityResult,
    Confidence,
    ContextProfile,
    DecodingPolicy,
    EvidenceReference,
    ExportMode,
    ExpressionProfile,
    ModelCapability,
    ModelExecutionEnvironment,
    ModelRole,
    ProfileAffectingModelInvocation,
    ProfileExport,
    ProviderKind,
    ProviderPolicyStatus,
    SignalSupport,
    SourcePolicy,
)


def confidence() -> Confidence:
    return Confidence(
        attribution=0.9,
        authorship_origin=0.85,
        extraction=0.8,
        evidence_strength=0.75,
        source_diversity=0.7,
        policy_fit=0.95,
        display=0.82,
    )


def artifact_ref(artifact_id: str = "artifact-1") -> ArtifactReference:
    return ArtifactReference(
        artifact_id=artifact_id,
        source_id="source-1",
        artifact_type="technical_note",
        source_type="notes",
        content_hash="sha256:synthetic",
        raw_content_available=False,
    )


def support() -> SignalSupport:
    return SignalSupport(
        evidence_refs=[
            EvidenceReference(
                evidence_id="evidence-1",
                artifact_ref=artifact_ref(),
                classification_id="classification-1",
                extraction_run_id="run-1",
                inclusion_status=ArtifactClassificationLabel.INCLUDED,
                authorship_origin=AuthorshipOrigin.HUMAN_ORIGIN,
            )
        ],
        artifact_count=1,
        included_count=1,
        source_types=["notes"],
        source_diversity=1.0,
        raw_content_available=False,
    )


def validation(status: ClaimValidationStatus = ClaimValidationStatus.PASSED) -> ClaimValidation:
    return ClaimValidation(
        status=status,
        methods=[ClaimValidationMethod.RULE_BASED, ClaimValidationMethod.TAXONOMY_BASED],
        rule_ids=["no-diagnosis", "no-intent"],
        rationale="Synthetic claim satisfies observation boundary.",
    )


def claim(level: ClaimLevel = ClaimLevel.OBSERVATION) -> Claim:
    status = ClaimValidationStatus.PASSED
    if level == ClaimLevel.PROHIBITED:
        status = ClaimValidationStatus.FAILED
    if level == ClaimLevel.QUARANTINED:
        status = ClaimValidationStatus.QUARANTINED
    return Claim(
        claim_id=f"claim-{level}",
        level=level,
        text="Often cites concrete evidence before summarizing.",
        confidence=confidence(),
        support=support(),
        validation=validation(status),
    )


def manifest(**overrides: object) -> BuildManifest:
    fields = {
        "schema_version": "0.1",
        "compiler_version": "0.1.0",
        "classifier_version": "0.1.0",
        "extractor_family": "rule_baseline",
        "extractor_major_version": 0,
        "extractor_minor_version": 1,
        "extractor_prompt_version": "none",
        "extractor_code_version": "0.1.0",
        "model_provider": None,
        "model_name": None,
        "model_version": None,
        "source_policy_version": "0.1",
        "authorship_policy_version": "0.1",
        "export_schema_version": "0.1",
        "config_hash": "synthetic-config",
    }
    fields.update(overrides)
    return BuildManifest(**fields)


def model_invocation(**overrides: object) -> ProfileAffectingModelInvocation:
    fields = {
        "invocation_id": "model-run-1",
        "model_role": ModelRole.SIGNAL_EXTRACTOR_LLM,
        "provider_kind": ProviderKind.CUSTOM,
        "provider_name": "synthetic-provider",
        "model_name": "synthetic-model",
        "model_version": "2026-06-07",
        "extractor_family": "semantic_llm",
        "extractor_major_version": 0,
        "extractor_minor_version": 1,
        "prompt_version": "signal-v1",
        "schema_version": "0.1",
        "decoding_policy": DecodingPolicy(temperature=0.0, seed=123, deterministic=True),
        "capabilities": [
            ModelCapability.STRUCTURED_OUTPUT,
            ModelCapability.JSON_SCHEMA_OUTPUT,
            ModelCapability.ARTIFACT_ID_CITATION_SUPPORT,
        ],
        "execution_environment": ModelExecutionEnvironment.REMOTE,
        "retention_policy": ProviderPolicyStatus.UNKNOWN,
        "training_policy": ProviderPolicyStatus.UNKNOWN,
        "sends_artifact_text": True,
        "local_alternative_available": True,
    }
    fields.update(overrides)
    return ProfileAffectingModelInvocation(**fields)


def profile(**overrides: object) -> ExpressionProfile:
    fields = {
        "profile_id": "profile-1",
        "subject_id": "synthetic-subject",
        "build_manifest": manifest(),
        "artifact_storage": ArtifactStoragePolicy(),
        "source_policy": SourcePolicy(policy_id="source-policy", version="0.1"),
        "claims": [claim()],
        "signals": [],
        "context_profiles": [],
    }
    fields.update(overrides)
    return ExpressionProfile(**fields)


def test_metadata_only_storage_discloses_audit_limitations() -> None:
    storage = ArtifactStoragePolicy()

    assert storage.mode == "metadata_only"
    assert storage.raw_content_available is False
    assert "raw_content_unavailable" in storage.audit_limitations
    assert "regeneration_requires_reharvest" in storage.audit_limitations


def test_unknown_authorship_is_not_a_single_unknown_bucket() -> None:
    origins = {origin.value for origin in AuthorshipOrigin}

    assert "unknown" not in origins
    assert {
        "unknown_speaker",
        "quoted_or_forwarded",
        "missing_metadata",
        "suspected_ai_assisted",
        "parser_uncertain",
        "mixed_authorship",
        "assistant_output",
        "human_origin",
        "human_directed_ai_assisted",
    }.issubset(origins)


def test_prohibited_claim_must_fail_validation() -> None:
    with pytest.raises(ValidationError, match="prohibited claims must have failed validation"):
        Claim(
            claim_id="bad-claim",
            level=ClaimLevel.PROHIBITED,
            text="Synthetic subject is anxious.",
            confidence=confidence(),
            support=support(),
            validation=validation(ClaimValidationStatus.PASSED),
        )


def test_compiled_profile_rejects_prohibited_claims() -> None:
    with pytest.raises(ValidationError, match="compiled expression profile contains prohibited claims"):
        profile(claims=[claim(ClaimLevel.PROHIBITED)])


def test_context_profile_budget_requires_explicit_override() -> None:
    contexts = [
        ContextProfile(
            profile_id=f"context-{index}",
            baseline_profile_id="profile-1",
            context_label=f"context-{index}",
            included_count=1,
        )
        for index in range(6)
    ]

    with pytest.raises(ValidationError, match="context profile count exceeds source policy budget"):
        profile(context_profiles=contexts)

    override_policy = SourcePolicy(
        policy_id="source-policy",
        version="0.1",
        max_context_profiles=5,
        allow_context_budget_override=True,
    )
    assert profile(context_profiles=contexts, source_policy=override_policy).context_profiles == contexts


def test_comparability_is_computed_from_structured_manifest_fields() -> None:
    comparable = ComparabilityResult.from_manifests(manifest(), manifest(), compatible_corpus=True)
    assert comparable.label == ComparabilityLabel.COMPARABLE

    partial = ComparabilityResult.from_manifests(
        manifest(), manifest(extractor_minor_version=2), compatible_corpus=True
    )
    assert partial.label == ComparabilityLabel.PARTIALLY_COMPARABLE

    not_comparable = ComparabilityResult.from_manifests(
        manifest(), manifest(extractor_family="semantic_llm"), compatible_corpus=True
    )
    assert not_comparable.label == ComparabilityLabel.NOT_COMPARABLE


def test_public_safe_export_forbids_generation_controls() -> None:
    with pytest.raises(ValidationError, match="generation-control fields"):
        ProfileExport(
            export_id="export-1",
            mode=ExportMode.PUBLIC_SAFE,
            schema_version="0.1",
            profile=profile(),
            projection_metadata={"temperature": 0.2},
        )


def test_serialization_and_json_schema_generation() -> None:
    export = ProfileExport(
        export_id="export-1",
        mode=ExportMode.PUBLIC_SAFE,
        schema_version="0.1",
        profile=profile(),
        projection_metadata={"projection": "synthetic-public-safe"},
    )

    data = export.model_dump(mode="json")
    assert data["profile"]["artifact_storage"]["mode"] == "metadata_only"
    assert ProfileExport.model_json_schema()["title"] == "ProfileExport"


def test_build_manifest_records_profile_affecting_model_invocations() -> None:
    build = manifest(profile_affecting_model_invocations=[model_invocation()])

    data = build.model_dump(mode="json")
    invocation = data["profile_affecting_model_invocations"][0]
    assert invocation["model_role"] == "signal_extractor_llm"
    assert invocation["provider_kind"] == "custom"
    assert invocation["execution_environment"] == "remote"
    assert invocation["decoding_policy"]["temperature"] == 0.0
    assert "json_schema_output" in invocation["capabilities"]


def test_experience_only_roles_do_not_enter_build_manifest_invocations() -> None:
    with pytest.raises(ValidationError, match="experience-only model roles"):
        model_invocation(model_role=ModelRole.FIRST_RUN_ARTIFACT_LLM)


def test_comparability_tracks_profile_affecting_model_invocation_changes() -> None:
    baseline = manifest(profile_affecting_model_invocations=[model_invocation()])
    candidate = manifest(
        profile_affecting_model_invocations=[model_invocation(model_name="different-model")]
    )

    result = ComparabilityResult.from_manifests(baseline, candidate, compatible_corpus=True)

    assert result.label == ComparabilityLabel.NOT_COMPARABLE
