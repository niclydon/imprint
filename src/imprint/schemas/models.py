from __future__ import annotations

from datetime import datetime
from enum import StrEnum
import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, model_validator


class ImprintSchemaModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class ArtifactStorageMode(StrEnum):
    METADATA_ONLY = "metadata_only"
    LOCAL_ARTIFACT_STORE = "local_artifact_store"
    EXTERNAL_REFERENCE = "external_reference"


class AuditLimitation(StrEnum):
    RAW_CONTENT_UNAVAILABLE = "raw_content_unavailable"
    REGENERATION_REQUIRES_REHARVEST = "regeneration_requires_reharvest"
    AGGREGATE_EVIDENCE_ONLY = "aggregate_evidence_only"
    HASH_ONLY_REFERENCE = "hash_only_reference"


class ArtifactType(StrEnum):
    CHAT_MESSAGE = "chat_message"
    EMAIL_SENT = "email_sent"
    LONGFORM_ARTICLE = "longform_article"
    TECHNICAL_NOTE = "technical_note"
    TRANSCRIPT_SEGMENT = "transcript_segment"
    DOCUMENT = "document"
    UNKNOWN = "unknown"


class ArtifactClassificationLabel(StrEnum):
    INCLUDED = "included"
    EXCLUDED = "excluded"
    QUARANTINED = "quarantined"


class AuthorshipOrigin(StrEnum):
    UNKNOWN_SPEAKER = "unknown_speaker"
    QUOTED_OR_FORWARDED = "quoted_or_forwarded"
    TEMPLATE_OR_NOTIFICATION = "template_or_notification"
    MISSING_METADATA = "missing_metadata"
    SUSPECTED_AI_ASSISTED = "suspected_ai_assisted"
    PARSER_UNCERTAIN = "parser_uncertain"
    MIXED_AUTHORSHIP = "mixed_authorship"
    ASSISTANT_OUTPUT = "assistant_output"
    HUMAN_ORIGIN = "human_origin"
    HUMAN_DIRECTED_AI_ASSISTED = "human_directed_ai_assisted"


class SourcePolicyAction(StrEnum):
    INCLUDE = "include"
    EXCLUDE = "exclude"
    QUARANTINE = "quarantine"
    DOWNWEIGHT = "downweight"


class SignalFamily(StrEnum):
    LEXICAL = "lexical"
    TONE = "tone"
    HUMOR = "humor"
    REASONING = "reasoning"
    STRUCTURE = "structure"
    NARRATIVE = "narrative"
    ANTI_PATTERN = "anti_pattern"


class ArtifactSignalFamily(StrEnum):
    STRUCTURE = "structure"
    LEXICAL = "lexical"
    RHETORICAL_PATTERN = "rhetorical_pattern"
    FORMATTING = "formatting"
    TONE_MARKER = "tone_marker"
    REASONING = "reasoning"
    NARRATIVE = "narrative"
    ANTI_PATTERN = "anti_pattern"


class ExtractorFamily(StrEnum):
    RULE_BASELINE = "rule_baseline"
    SEMANTIC_LLM = "semantic_llm"
    HYBRID_REVIEW = "hybrid_review"


class ClaimLevel(StrEnum):
    OBSERVATION = "observation"
    BOUNDED_INTERPRETATION = "bounded_interpretation"
    PROHIBITED = "prohibited"
    QUARANTINED = "quarantined"


class ClaimValidationMethod(StrEnum):
    RULE_BASED = "rule_based"
    TAXONOMY_BASED = "taxonomy_based"
    REVIEW_BASED = "review_based"


class ClaimValidationStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    QUARANTINED = "quarantined"


class ExportMode(StrEnum):
    CANONICAL = "canonical"
    PUBLIC_SAFE = "public_safe"
    PRIVATE_LOCAL = "private_local"
    FULL_LOCAL = "full_local"


class ModelRole(StrEnum):
    CLASSIFIER_LLM = "classifier_llm"
    SIGNAL_EXTRACTOR_LLM = "signal_extractor_llm"
    CLAIM_VALIDATOR_LLM = "claim_validator_llm"
    EVIDENCE_INTERPRETER_LLM = "evidence_interpreter_llm"
    CONFIDENCE_ASSESSOR_LLM = "confidence_assessor_llm"
    DRIFT_COMPARATOR_LLM = "drift_comparator_llm"
    PROFILE_SUMMARIZER_LLM = "profile_summarizer_llm"
    FIRST_RUN_ARTIFACT_LLM = "first_run_artifact_llm"
    REPORT_WRITER_LLM = "report_writer_llm"
    EMBEDDING_MODEL = "embedding_model"
    RERANKER_MODEL = "reranker_model"


class ProviderKind(StrEnum):
    OPENAI_COMPATIBLE = "openai_compatible"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    LM_STUDIO = "lm_studio"
    LOCAL_HTTP = "local_http"
    FORGE = "forge"
    CUSTOM = "custom"


class BaseUrlKind(StrEnum):
    DEFAULT_PROVIDER_ENDPOINT = "default_provider_endpoint"
    LOCALHOST = "localhost"
    USER_CONFIGURED_REMOTE = "user_configured_remote"
    USER_CONFIGURED_LOCAL = "user_configured_local"
    UNSPECIFIED = "unspecified"


class ModelCapability(StrEnum):
    STRUCTURED_OUTPUT = "structured_output"
    JSON_SCHEMA_OUTPUT = "json_schema_output"
    LOW_TEMPERATURE_OPERATION = "low_temperature_operation"
    LONG_CONTEXT = "long_context"
    STABLE_EMBEDDING_DIMENSION = "stable_embedding_dimension"
    DETERMINISTIC_SEED_SUPPORT = "deterministic_seed_support"
    ARTIFACT_ID_CITATION_SUPPORT = "artifact_id_citation_support"
    LOCAL_ONLY_SUPPORT = "local_only_support"
    NO_RETENTION_POLICY = "no_retention_policy"
    NO_TRAINING_POLICY = "no_training_policy"
    BATCH_INFERENCE = "batch_inference"
    STREAMING_OUTPUT = "streaming_output"


class ModelExecutionEnvironment(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"
    UNKNOWN = "unknown"


class ProviderPolicyStatus(StrEnum):
    NO_RETENTION = "no_retention"
    NO_TRAINING = "no_training"
    RETENTION_LIMITED = "retention_limited"
    TRAINING_OPT_OUT = "training_opt_out"
    UNKNOWN = "unknown"


class ComparabilityLabel(StrEnum):
    COMPARABLE = "comparable"
    PARTIALLY_COMPARABLE = "partially_comparable"
    NOT_COMPARABLE = "not_comparable"


class ComparabilityReason(StrEnum):
    SAME_SCHEMA_FAMILY = "same_schema_family"
    SAME_EXTRACTOR_FAMILY_MAJOR = "same_extractor_family_major"
    SAME_SOURCE_POLICY = "same_source_policy"
    COMPATIBLE_CORPUS = "compatible_corpus"
    MINOR_EXTRACTOR_CHANGE = "minor_extractor_change"
    PROMPT_VERSION_CHANGE = "prompt_version_change"
    MODEL_VERSION_CHANGE = "model_version_change"
    MIXED_CLASSIFIER_VERSIONS = "mixed_classifier_versions"
    SOURCE_MIX_CHANGE = "source_mix_change"
    DIFFERENT_EXTRACTOR_FAMILY = "different_extractor_family"
    DIFFERENT_MODEL_FAMILY = "different_model_family"
    INCOMPATIBLE_SCHEMA = "incompatible_schema"
    DIFFERENT_CORPUS = "different_corpus"
    EXPLICIT_MIGRATION = "explicit_migration"


class DriftKind(StrEnum):
    EXPRESSION_DRIFT = "expression_drift"
    COMPILER_DRIFT = "compiler_drift"
    CORPUS_DRIFT = "corpus_drift"
    SCHEMA_DRIFT = "schema_drift"


class DivergenceDirection(StrEnum):
    CONTEXT_HIGHER = "context_higher"
    CONTEXT_LOWER = "context_lower"
    CONTEXT_DIFFERENT = "context_different"
    CONTEXT_MORE_DIRECT = "context_is_more_direct"
    CONTEXT_MORE_FORMAL = "context_is_more_formal"


class CollisionLabel(StrEnum):
    CONTEXT_SPECIFIC = "context_specific"
    BASELINE_WEAK = "baseline_weak"
    CONTEXT_WEAK = "context_weak"
    POLICY_CONFLICT = "policy_conflict"
    NOT_COMPARABLE = "not_comparable"


class ArtifactReference(ImprintSchemaModel):
    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    artifact_type: ArtifactType
    source_type: str = Field(min_length=1)
    content_hash: str | None = None
    timestamp: datetime | None = None
    time_bucket: str | None = None
    raw_content_available: bool = False


class ArtifactStoragePolicy(ImprintSchemaModel):
    mode: ArtifactStorageMode = ArtifactStorageMode.METADATA_ONLY
    raw_content_available: bool = False
    audit_limitations: list[AuditLimitation] = Field(
        default_factory=lambda: [
            AuditLimitation.RAW_CONTENT_UNAVAILABLE,
            AuditLimitation.REGENERATION_REQUIRES_REHARVEST,
            AuditLimitation.AGGREGATE_EVIDENCE_ONLY,
        ]
    )
    retention_reason: str = "profile_compilation_audit_and_regeneration"

    @model_validator(mode="after")
    def metadata_only_discloses_limits(self) -> ArtifactStoragePolicy:
        if self.mode == ArtifactStorageMode.METADATA_ONLY:
            if self.raw_content_available:
                raise ValueError("metadata_only storage cannot declare raw_content_available=true")
            required = {
                AuditLimitation.RAW_CONTENT_UNAVAILABLE,
                AuditLimitation.REGENERATION_REQUIRES_REHARVEST,
            }
            if not required.issubset(set(self.audit_limitations)):
                raise ValueError("metadata_only storage must disclose raw-content and regeneration limits")
        return self


class ArtifactClassification(ImprintSchemaModel):
    classification_id: str = Field(min_length=1)
    label: ArtifactClassificationLabel
    authorship_origin: AuthorshipOrigin
    authorship_confidence: float = Field(ge=0, le=1)
    ai_detector_score: float | None = Field(default=None, ge=0, le=1)
    ai_detector_is_ground_truth: Literal[False] = False
    reason_categories: list[AuthorshipOrigin] = Field(default_factory=list)

    @model_validator(mode="after")
    def detector_is_weak_metadata_only(self) -> ArtifactClassification:
        if self.ai_detector_score is not None and self.authorship_origin == AuthorshipOrigin.HUMAN_ORIGIN:
            if self.authorship_confidence < 0.5:
                raise ValueError("AI detector output alone cannot establish human authorship")
        return self


class Artifact(ImprintSchemaModel):
    artifact_id: str = Field(min_length=1)
    reference: ArtifactReference
    storage_policy: ArtifactStoragePolicy = Field(default_factory=ArtifactStoragePolicy)
    classification: ArtifactClassification
    source_hints: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def source_hints_are_export_safe(self) -> Artifact:
        forbidden_hint_keys = {"raw_text", "content", "text", "source_path", "local_path", "filepath"}
        path_pattern = re.compile(r"^(?:/|[A-Za-z]:[\\/])")
        for key, value in self.source_hints.items():
            lowered = key.lower()
            if lowered in forbidden_hint_keys or "path" in lowered:
                raise ValueError("source_hints cannot include raw text or filesystem paths")
            if isinstance(value, str) and path_pattern.match(value):
                raise ValueError("source_hints cannot include filesystem paths")
        return self


class ClassificationEvidence(ImprintSchemaModel):
    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    source_hints_considered: dict[str, Any] = Field(default_factory=dict)
    rule_ids: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    evidence_summary: str = Field(min_length=1)
    quote_or_forward_likelihood: float = Field(ge=0, le=1)
    template_or_notification_likelihood: float = Field(ge=0, le=1)
    assistant_output_likelihood: float = Field(ge=0, le=1)
    contamination_risk: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def evidence_uses_opaque_source_id(self) -> ClassificationEvidence:
        if self.source_id.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", self.source_id):
            raise ValueError("classification evidence cannot expose filesystem paths")
        return self


class ClassificationConfidence(ImprintSchemaModel):
    model_version: str = Field(min_length=1)
    attribution: float = Field(ge=0, le=1)
    authorship_origin: float = Field(ge=0, le=1)
    evidence_strength: float = Field(ge=0, le=1)
    source_reliability: float = Field(ge=0, le=1)
    policy_fit: float = Field(ge=0, le=1)
    contamination_penalty: float = Field(ge=0, le=1)
    display: float = Field(ge=0, le=1)


class ArtifactClassificationResult(ImprintSchemaModel):
    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    artifact_type: ArtifactType
    classification: ArtifactClassification
    evidence: ClassificationEvidence
    confidence: ClassificationConfidence

    @model_validator(mode="after")
    def result_ids_remain_consistent(self) -> ArtifactClassificationResult:
        if self.artifact_id != self.evidence.artifact_id:
            raise ValueError("classification result and evidence artifact_id must match")
        if self.source_id != self.evidence.source_id:
            raise ValueError("classification result and evidence source_id must match")
        return self


class SignalEvidencePolicy(StrEnum):
    NO_RAW_TEXT = "no_raw_text"


class ArtifactSignalEvidence(ImprintSchemaModel):
    signal_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    classification_id: str = Field(min_length=1)
    classification_label: ArtifactClassificationLabel
    classification_model_version: str = Field(min_length=1)
    signal_model_version: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    observed_feature: str = Field(min_length=1)
    evidence_policy: SignalEvidencePolicy = SignalEvidencePolicy.NO_RAW_TEXT
    limitations: list[str] = Field(default_factory=list)
    no_raw_text: Literal[True] = True

    @model_validator(mode="after")
    def evidence_remains_public_safe(self) -> ArtifactSignalEvidence:
        if self.source_id.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", self.source_id):
            raise ValueError("artifact signal evidence cannot expose filesystem paths")
        return self


class ArtifactSignalCandidate(ImprintSchemaModel):
    signal_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    family: ArtifactSignalFamily
    name: str = Field(min_length=1)
    observed_feature: str = Field(min_length=1)
    claim_level: ClaimLevel
    confidence: Confidence
    evidence: ArtifactSignalEvidence
    durable: bool

    @model_validator(mode="after")
    def signal_candidate_is_bounded(self) -> ArtifactSignalCandidate:
        prohibited_terms = (
            "introvert",
            "analytical",
            "anxious",
            "depressed",
            "bipolar",
            "adhd",
            "prefers written communication",
        )
        haystack = f"{self.name} {self.observed_feature}".lower()
        if any(term in haystack for term in prohibited_terms):
            raise ValueError("artifact signal candidates cannot contain personality or diagnostic claims")
        if self.claim_level == ClaimLevel.PROHIBITED:
            raise ValueError("artifact signal candidates must not emit prohibited claims")
        if self.durable and self.claim_level == ClaimLevel.QUARANTINED:
            raise ValueError("quarantined signal candidates cannot be durable")
        return self


class SourcePolicy(ImprintSchemaModel):
    policy_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    max_context_profiles: int = Field(default=5, ge=0)
    allow_context_budget_override: bool = False
    default_unknown_authorship_action: SourcePolicyAction = SourcePolicyAction.DOWNWEIGHT
    authorship_actions: dict[AuthorshipOrigin, SourcePolicyAction] = Field(default_factory=dict)


class Confidence(ImprintSchemaModel):
    attribution: float = Field(ge=0, le=1)
    authorship_origin: float = Field(ge=0, le=1)
    extraction: float = Field(ge=0, le=1)
    evidence_strength: float = Field(ge=0, le=1)
    source_diversity: float = Field(ge=0, le=1)
    policy_fit: float = Field(ge=0, le=1)
    model_agreement: float | None = Field(default=None, ge=0, le=1)
    display: float = Field(ge=0, le=1)


class EvidenceReference(ImprintSchemaModel):
    evidence_id: str = Field(min_length=1)
    artifact_ref: ArtifactReference
    classification_id: str = Field(min_length=1)
    extraction_run_id: str = Field(min_length=1)
    inclusion_status: ArtifactClassificationLabel
    authorship_origin: AuthorshipOrigin
    support_count: NonNegativeInt = 1


class SignalSupport(ImprintSchemaModel):
    evidence_refs: list[EvidenceReference] = Field(default_factory=list)
    signal_ids: list[str] = Field(default_factory=list)
    classification_model_versions: list[str] = Field(default_factory=list)
    signal_model_versions: list[str] = Field(default_factory=list)
    rule_ids: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    artifact_count: NonNegativeInt
    included_count: NonNegativeInt
    excluded_count: NonNegativeInt = 0
    quarantined_count: NonNegativeInt = 0
    source_types: list[str] = Field(default_factory=list)
    time_window: str | None = None
    source_diversity: float = Field(ge=0, le=1)
    raw_content_available: bool = False
    audit_limitations: list[AuditLimitation] = Field(default_factory=list)

    @model_validator(mode="after")
    def counts_are_consistent(self) -> SignalSupport:
        if self.included_count + self.excluded_count + self.quarantined_count > self.artifact_count:
            raise ValueError("support counts cannot exceed artifact_count")
        if self.artifact_count == 0 and not self.evidence_refs:
            raise ValueError("signal support requires evidence references or aggregate artifact support")
        return self


class ClaimValidation(ImprintSchemaModel):
    status: ClaimValidationStatus
    methods: list[ClaimValidationMethod]
    rule_ids: list[str] = Field(default_factory=list)
    reviewer: str | None = None
    rationale: str = Field(min_length=1)


class Claim(ImprintSchemaModel):
    claim_id: str = Field(min_length=1)
    level: ClaimLevel
    text: str = Field(min_length=1)
    confidence: Confidence
    support: SignalSupport
    validation: ClaimValidation

    @model_validator(mode="after")
    def level_matches_validation(self) -> Claim:
        if self.level == ClaimLevel.PROHIBITED and self.validation.status != ClaimValidationStatus.FAILED:
            raise ValueError("prohibited claims must have failed validation")
        if self.level == ClaimLevel.QUARANTINED and self.validation.status != ClaimValidationStatus.QUARANTINED:
            raise ValueError("quarantined claims must have quarantined validation")
        if self.level in {ClaimLevel.OBSERVATION, ClaimLevel.BOUNDED_INTERPRETATION}:
            if self.validation.status != ClaimValidationStatus.PASSED:
                raise ValueError("allowed claims must pass validation")
        return self


class Signal(ImprintSchemaModel):
    signal_id: str = Field(min_length=1)
    family: SignalFamily
    name: str = Field(min_length=1)
    claim: Claim
    support: SignalSupport


class DecodingPolicy(ImprintSchemaModel):
    temperature: float | None = Field(default=None, ge=0)
    seed: int | None = None
    deterministic: bool | None = None
    policy_name: str | None = None


class ProfileAffectingModelInvocation(ImprintSchemaModel):
    invocation_id: str = Field(min_length=1)
    model_role: ModelRole
    scope: Literal["profile_affecting"] = "profile_affecting"
    provider_kind: ProviderKind
    provider_name: str = Field(min_length=1)
    base_url_kind: BaseUrlKind = BaseUrlKind.UNSPECIFIED
    model_name: str = Field(min_length=1)
    model_version: str | None = None
    extractor_family: ExtractorFamily | None = None
    extractor_major_version: int | None = Field(default=None, ge=0)
    extractor_minor_version: int | None = Field(default=None, ge=0)
    prompt_version: str | None = None
    schema_version: str = Field(min_length=1)
    decoding_policy: DecodingPolicy = Field(default_factory=DecodingPolicy)
    capabilities: list[ModelCapability] = Field(default_factory=list)
    execution_environment: ModelExecutionEnvironment
    retention_policy: ProviderPolicyStatus = ProviderPolicyStatus.UNKNOWN
    training_policy: ProviderPolicyStatus = ProviderPolicyStatus.UNKNOWN
    sends_artifact_text: bool
    local_alternative_available: bool | None = None

    @model_validator(mode="after")
    def profile_roles_are_durable_roles(self) -> ProfileAffectingModelInvocation:
        experience_only_roles = {
            ModelRole.PROFILE_SUMMARIZER_LLM,
            ModelRole.FIRST_RUN_ARTIFACT_LLM,
            ModelRole.REPORT_WRITER_LLM,
        }
        if self.model_role in experience_only_roles:
            raise ValueError("experience-only model roles do not belong in build manifest invocations")
        return self


class BuildManifest(ImprintSchemaModel):
    schema_version: str = Field(min_length=1)
    schema_family: str = "imprint_profile"
    compiler_version: str = Field(min_length=1)
    classifier_version: str = Field(min_length=1)
    extractor_family: ExtractorFamily
    extractor_major_version: int = Field(ge=0)
    extractor_minor_version: int = Field(ge=0)
    extractor_prompt_version: str = Field(min_length=1)
    extractor_code_version: str = Field(min_length=1)
    model_provider: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    source_policy_version: str = Field(min_length=1)
    authorship_policy_version: str = Field(min_length=1)
    export_schema_version: str = Field(min_length=1)
    artifact_store_mode: ArtifactStorageMode = ArtifactStorageMode.METADATA_ONLY
    config_hash: str = Field(min_length=1)
    profile_affecting_model_invocations: list[ProfileAffectingModelInvocation] = Field(
        default_factory=list
    )


class ComparabilityResult(ImprintSchemaModel):
    label: ComparabilityLabel
    reasons: list[ComparabilityReason]
    explanation: str = Field(min_length=1)

    @classmethod
    def from_manifests(
        cls, baseline: BuildManifest, candidate: BuildManifest, *, compatible_corpus: bool
    ) -> ComparabilityResult:
        if (
            baseline.schema_family != candidate.schema_family
            or baseline.schema_version.split(".")[0] != candidate.schema_version.split(".")[0]
        ):
            return cls(
                label=ComparabilityLabel.NOT_COMPARABLE,
                reasons=[ComparabilityReason.INCOMPATIBLE_SCHEMA],
                explanation="Schema family or major schema version differs.",
            )
        if baseline.extractor_family != candidate.extractor_family:
            return cls(
                label=ComparabilityLabel.NOT_COMPARABLE,
                reasons=[ComparabilityReason.DIFFERENT_EXTRACTOR_FAMILY],
                explanation="Extractor families differ.",
            )
        if baseline.model_provider != candidate.model_provider or baseline.model_name != candidate.model_name:
            return cls(
                label=ComparabilityLabel.NOT_COMPARABLE,
                reasons=[ComparabilityReason.DIFFERENT_MODEL_FAMILY],
                explanation="Semantic extraction model family differs without explicit migration.",
            )
        if baseline.extractor_major_version != candidate.extractor_major_version:
            return cls(
                label=ComparabilityLabel.NOT_COMPARABLE,
                reasons=[ComparabilityReason.DIFFERENT_EXTRACTOR_FAMILY],
                explanation="Extractor major versions differ.",
            )
        if not compatible_corpus:
            return cls(
                label=ComparabilityLabel.NOT_COMPARABLE,
                reasons=[ComparabilityReason.DIFFERENT_CORPUS],
                explanation="Corpus windows or artifact sets are materially different.",
            )
        baseline_invocations = {
            invocation.model_role: invocation
            for invocation in baseline.profile_affecting_model_invocations
        }
        candidate_invocations = {
            invocation.model_role: invocation
            for invocation in candidate.profile_affecting_model_invocations
        }
        if baseline_invocations.keys() != candidate_invocations.keys():
            return cls(
                label=ComparabilityLabel.PARTIALLY_COMPARABLE,
                reasons=[ComparabilityReason.MODEL_VERSION_CHANGE],
                explanation="Profile-affecting model role coverage changed.",
            )
        model_invocation_changed = False
        for role, baseline_invocation in baseline_invocations.items():
            candidate_invocation = candidate_invocations[role]
            if (
                baseline_invocation.provider_kind != candidate_invocation.provider_kind
                or baseline_invocation.provider_name != candidate_invocation.provider_name
                or baseline_invocation.model_name != candidate_invocation.model_name
            ):
                return cls(
                    label=ComparabilityLabel.NOT_COMPARABLE,
                    reasons=[ComparabilityReason.DIFFERENT_MODEL_FAMILY],
                    explanation="Profile-affecting provider or model family changed.",
                )
            if (
                baseline_invocation.model_version != candidate_invocation.model_version
                or baseline_invocation.prompt_version != candidate_invocation.prompt_version
                or baseline_invocation.decoding_policy != candidate_invocation.decoding_policy
                or set(baseline_invocation.capabilities) != set(candidate_invocation.capabilities)
            ):
                model_invocation_changed = True
        partial_reasons: list[ComparabilityReason] = []
        if baseline.extractor_minor_version != candidate.extractor_minor_version:
            partial_reasons.append(ComparabilityReason.MINOR_EXTRACTOR_CHANGE)
        if baseline.classifier_version != candidate.classifier_version:
            partial_reasons.append(ComparabilityReason.MODEL_VERSION_CHANGE)
        if _has_mixed_versions(baseline.classifier_version) or _has_mixed_versions(
            candidate.classifier_version
        ):
            partial_reasons.append(ComparabilityReason.MIXED_CLASSIFIER_VERSIONS)
        if baseline.extractor_prompt_version != candidate.extractor_prompt_version:
            partial_reasons.append(ComparabilityReason.PROMPT_VERSION_CHANGE)
        if baseline.model_version != candidate.model_version:
            partial_reasons.append(ComparabilityReason.MODEL_VERSION_CHANGE)
        if model_invocation_changed:
            partial_reasons.append(ComparabilityReason.MODEL_VERSION_CHANGE)
        if baseline.source_policy_version != candidate.source_policy_version:
            partial_reasons.append(ComparabilityReason.SOURCE_MIX_CHANGE)
        partial_reasons = list(dict.fromkeys(partial_reasons))
        if partial_reasons:
            return cls(
                label=ComparabilityLabel.PARTIALLY_COMPARABLE,
                reasons=partial_reasons,
                explanation="Builds are schema-compatible with structured caveats.",
            )
        return cls(
            label=ComparabilityLabel.COMPARABLE,
            reasons=[
                ComparabilityReason.SAME_SCHEMA_FAMILY,
                ComparabilityReason.SAME_EXTRACTOR_FAMILY_MAJOR,
                ComparabilityReason.SAME_SOURCE_POLICY,
                ComparabilityReason.COMPATIBLE_CORPUS,
            ],
            explanation="Structured manifest fields support expression-drift comparison.",
        )


def _has_mixed_versions(value: str) -> bool:
    return len({item.strip() for item in value.split(",") if item.strip()}) > 1


class DivergenceValue(ImprintSchemaModel):
    summary: str = Field(min_length=1)
    confidence: Confidence


class DerivedProfileDivergence(ImprintSchemaModel):
    signal_family: SignalFamily
    pattern: str = Field(min_length=1)
    baseline_value: DivergenceValue
    context_value: DivergenceValue
    direction: DivergenceDirection
    claim_level: ClaimLevel
    support: SignalSupport
    collision_label: CollisionLabel

    @model_validator(mode="after")
    def divergence_claims_must_be_safe(self) -> DerivedProfileDivergence:
        if self.claim_level == ClaimLevel.PROHIBITED:
            raise ValueError("profile divergences cannot compile prohibited claims")
        return self


class ContextProfile(ImprintSchemaModel):
    profile_id: str = Field(min_length=1)
    baseline_profile_id: str = Field(min_length=1)
    context_label: str = Field(min_length=1)
    source_filters: dict[str, Any] = Field(default_factory=dict)
    artifact_type_filters: list[ArtifactType] = Field(default_factory=list)
    source_policy_overrides: dict[str, Any] = Field(default_factory=dict)
    authorship_policy_overrides: dict[str, Any] = Field(default_factory=dict)
    included_count: NonNegativeInt
    quarantined_count: NonNegativeInt = 0
    excluded_count: NonNegativeInt = 0
    compilation_strategy: Literal["filtered_evidence_recompile"] = "filtered_evidence_recompile"
    divergences: list[DerivedProfileDivergence] = Field(default_factory=list)


class ExtractorManifest(ImprintSchemaModel):
    extractor_family: ExtractorFamily
    extractor_major_version: int = Field(ge=0)
    extractor_minor_version: int = Field(ge=0)
    extractor_prompt_version: str = Field(min_length=1)
    extractor_code_version: str = Field(min_length=1)
    signal_families: list[SignalFamily]
    model_provider: str | None = None
    model_name: str | None = None
    model_version: str | None = None


class ExpressionProfile(ImprintSchemaModel):
    profile_id: str = Field(min_length=1)
    subject_id: str = Field(min_length=1)
    build_manifest: BuildManifest
    artifact_storage: ArtifactStoragePolicy = Field(default_factory=ArtifactStoragePolicy)
    source_policy: SourcePolicy
    signals: list[Signal] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    context_profiles: list[ContextProfile] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_context_budget_and_claim_safety(self) -> ExpressionProfile:
        if len(self.context_profiles) > self.source_policy.max_context_profiles:
            if not self.source_policy.allow_context_budget_override:
                raise ValueError("context profile count exceeds source policy budget")
        prohibited = [claim.claim_id for claim in self.claims if claim.level == ClaimLevel.PROHIBITED]
        prohibited.extend(
            signal.claim.claim_id for signal in self.signals if signal.claim.level == ClaimLevel.PROHIBITED
        )
        if prohibited:
            raise ValueError(f"compiled expression profile contains prohibited claims: {prohibited}")
        return self


FORBIDDEN_EXPORT_FIELDS = {
    "prompt",
    "system_prompt",
    "instruction",
    "temperature",
    "decoding",
    "model_hint",
    "top_p",
    "frequency_penalty",
    "presence_penalty",
}


class ProfileExport(ImprintSchemaModel):
    export_id: str = Field(min_length=1)
    mode: ExportMode
    schema_version: str = Field(min_length=1)
    profile: ExpressionProfile
    target_consumer: str | None = None
    projection_metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def public_exports_fail_closed(self) -> ProfileExport:
        if self.mode in {ExportMode.CANONICAL, ExportMode.PUBLIC_SAFE}:
            prohibited = [claim.claim_id for claim in self.profile.claims if claim.level == ClaimLevel.PROHIBITED]
            prohibited.extend(
                signal.claim.claim_id
                for signal in self.profile.signals
                if signal.claim.level == ClaimLevel.PROHIBITED
            )
            if prohibited:
                raise ValueError("canonical and public-safe exports fail when prohibited claims survive")
        forbidden = set(self.projection_metadata).intersection(FORBIDDEN_EXPORT_FIELDS)
        if forbidden:
            raise ValueError(f"core exports cannot include generation-control fields: {sorted(forbidden)}")
        return self


class DriftReport(ImprintSchemaModel):
    report_id: str = Field(min_length=1)
    baseline_profile_id: str = Field(min_length=1)
    candidate_profile_id: str = Field(min_length=1)
    comparability: ComparabilityResult
    drift_kinds: list[DriftKind]
    changed_signal_ids: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def expression_drift_requires_comparability(self) -> DriftReport:
        if DriftKind.EXPRESSION_DRIFT in self.drift_kinds:
            if self.comparability.label == ComparabilityLabel.NOT_COMPARABLE:
                raise ValueError("expression drift cannot be reported for not_comparable profiles")
        return self
