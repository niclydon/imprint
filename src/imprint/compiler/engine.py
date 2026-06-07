from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from statistics import fmean

from imprint.classification.engine import CLASSIFICATION_CONFIDENCE_MODEL_VERSION, clamp
from imprint.schemas import (
    Artifact,
    ArtifactClassificationLabel,
    ArtifactClassificationResult,
    ArtifactSignalCandidate,
    ArtifactSignalFamily,
    ArtifactStorageMode,
    ArtifactStoragePolicy,
    AuditLimitation,
    BuildManifest,
    Claim,
    ClaimLevel,
    ClaimValidation,
    ClaimValidationMethod,
    ClaimValidationStatus,
    Confidence,
    ContextProfile,
    EvidenceReference,
    ExpressionProfile,
    ExtractorFamily,
    Signal,
    SignalFamily,
    SignalSupport,
    SourcePolicy,
)
from imprint.signals.engine import SIGNAL_CONFIDENCE_MODEL_VERSION, validate_source_id

COMPILER_VERSION = "sprint06-rule-v1"
COMPILER_CONFIDENCE_MODEL_VERSION = "sprint06-confidence-v1"
SCHEMA_VERSION = "0.1"
SOURCE_POLICY_VERSION = "sprint06-source-policy-v1"
AUTHORSHIP_POLICY_VERSION = "sprint06-authorship-policy-v1"
EXPORT_SCHEMA_VERSION = "0.1"


class CompilerError(ValueError):
    pass


@dataclass(frozen=True)
class _PatternKey:
    family: SignalFamily
    name: str
    observed_feature: str
    rule_id: str


class ProfileCompiler:
    """Compile durable artifact-level observations into evidence-backed profiles."""

    def compile_profile(
        self,
        *,
        subject_id: str,
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
        signal_candidates: list[ArtifactSignalCandidate],
        source_policy: SourcePolicy | None = None,
        allow_bounded_interpretations: bool = False,
    ) -> ExpressionProfile:
        artifact_by_id = {artifact.artifact_id: artifact for artifact in artifacts}
        classification_by_id = {result.artifact_id: result for result in classifications}
        eligible = self._eligible_candidates(
            signal_candidates,
            classification_by_id,
            allow_bounded_interpretations=allow_bounded_interpretations,
        )
        self._reject_incompatible_signal_model_versions(eligible)

        grouped: dict[_PatternKey, list[ArtifactSignalCandidate]] = defaultdict(list)
        for candidate in eligible:
            if candidate.artifact_id not in artifact_by_id:
                raise CompilerError(f"signal has no artifact: {candidate.signal_id}")
            grouped[self._pattern_key(candidate)].append(candidate)

        signals = [
            self._compile_signal(key, candidates, artifact_by_id, classification_by_id)
            for key, candidates in sorted(
                grouped.items(),
                key=lambda item: (
                    item[0].family.value,
                    item[0].name,
                    item[0].observed_feature,
                    item[0].rule_id,
                ),
            )
        ]
        claims = [signal.claim for signal in signals]
        policy = source_policy or SourcePolicy(
            policy_id="sprint06-default-source-policy",
            version=SOURCE_POLICY_VERSION,
        )
        profile_id = self._profile_id(
            subject_id,
            signals,
            artifacts,
            classifications,
            signal_candidates,
        )
        return ExpressionProfile(
            profile_id=profile_id,
            subject_id=subject_id,
            build_manifest=self._build_manifest(artifacts, classifications, signal_candidates),
            artifact_storage=self._artifact_storage_policy(artifacts),
            source_policy=policy,
            signals=signals,
            claims=claims,
            context_profiles=self._context_profiles(profile_id, classifications),
        )

    def _eligible_candidates(
        self,
        candidates: list[ArtifactSignalCandidate],
        classification_by_id: dict[str, ArtifactClassificationResult],
        *,
        allow_bounded_interpretations: bool,
    ) -> list[ArtifactSignalCandidate]:
        eligible: list[ArtifactSignalCandidate] = []
        for candidate in candidates:
            validate_source_id(candidate.source_id)
            classification = classification_by_id.get(candidate.artifact_id)
            if classification is None:
                raise CompilerError(f"signal has no classification result: {candidate.signal_id}")
            if classification.source_id != candidate.source_id:
                raise CompilerError(f"signal source mismatch: {candidate.signal_id}")
            if (
                classification.classification.classification_id
                != candidate.evidence.classification_id
            ):
                raise CompilerError(f"signal classification mismatch: {candidate.signal_id}")
            if candidate.claim_level == ClaimLevel.PROHIBITED:
                raise CompilerError(f"prohibited signal cannot compile: {candidate.signal_id}")
            if not candidate.durable:
                continue
            if candidate.evidence.classification_label != ArtifactClassificationLabel.INCLUDED:
                continue
            if classification.classification.label != ArtifactClassificationLabel.INCLUDED:
                continue
            if candidate.claim_level == ClaimLevel.BOUNDED_INTERPRETATION:
                if allow_bounded_interpretations:
                    eligible.append(candidate)
                continue
            if candidate.claim_level == ClaimLevel.QUARANTINED:
                continue
            if candidate.claim_level != ClaimLevel.OBSERVATION:
                continue
            eligible.append(candidate)
        return eligible

    def _reject_incompatible_signal_model_versions(
        self, candidates: list[ArtifactSignalCandidate]
    ) -> None:
        versions = sorted({candidate.evidence.signal_model_version for candidate in candidates})
        if len(versions) > 1:
            raise CompilerError(
                "cannot merge incompatible signal model versions: " + ", ".join(versions)
            )

    def _pattern_key(self, candidate: ArtifactSignalCandidate) -> _PatternKey:
        return _PatternKey(
            family=self._profile_family(candidate.family),
            name=candidate.name,
            observed_feature=candidate.observed_feature,
            rule_id=candidate.evidence.rule_id,
        )

    def _compile_signal(
        self,
        key: _PatternKey,
        candidates: list[ArtifactSignalCandidate],
        artifact_by_id: dict[str, Artifact],
        classification_by_id: dict[str, ArtifactClassificationResult],
    ) -> Signal:
        ordered = sorted(candidates, key=lambda candidate: candidate.signal_id)
        support = self._support(ordered, artifact_by_id, classification_by_id)
        confidence = self._confidence(ordered, support)
        signal_id = self._compiled_signal_id(key)
        claim_level = self._claim_level(ordered)
        validation_methods = [
            ClaimValidationMethod.RULE_BASED,
            ClaimValidationMethod.TAXONOMY_BASED,
        ]
        if claim_level == ClaimLevel.BOUNDED_INTERPRETATION:
            validation_methods.append(ClaimValidationMethod.REVIEW_BASED)
        claim = Claim(
            claim_id=f"claim-{signal_id}",
            level=claim_level,
            text=self._claim_text(key, support.included_count),
            confidence=confidence,
            support=support,
            validation=ClaimValidation(
                status=ClaimValidationStatus.PASSED,
                methods=validation_methods,
                rule_ids=sorted({candidate.evidence.rule_id for candidate in ordered}),
                rationale=(
                    "Compiled only from durable validated signals on included artifacts; "
                    f"confidence model {COMPILER_CONFIDENCE_MODEL_VERSION}."
                ),
            ),
        )
        return Signal(
            signal_id=signal_id,
            family=key.family,
            name=key.name,
            claim=claim,
            support=support,
        )

    def _support(
        self,
        candidates: list[ArtifactSignalCandidate],
        artifact_by_id: dict[str, Artifact],
        classification_by_id: dict[str, ArtifactClassificationResult],
    ) -> SignalSupport:
        evidence_refs: list[EvidenceReference] = []
        source_types = sorted({candidate.source_type for candidate in candidates})
        artifact_ids = sorted({candidate.artifact_id for candidate in candidates})
        for candidate in candidates:
            artifact = artifact_by_id[candidate.artifact_id]
            classification = classification_by_id[candidate.artifact_id]
            evidence_refs.append(
                EvidenceReference(
                    evidence_id=f"evidence-{candidate.signal_id}",
                    artifact_ref=artifact.reference,
                    classification_id=candidate.evidence.classification_id,
                    extraction_run_id=candidate.signal_id,
                    inclusion_status=classification.classification.label,
                    authorship_origin=classification.classification.authorship_origin,
                )
            )
        return SignalSupport(
            evidence_refs=evidence_refs,
            signal_ids=[candidate.signal_id for candidate in candidates],
            classification_model_versions=sorted(
                {
                    classification_by_id[candidate.artifact_id].confidence.model_version
                    for candidate in candidates
                }
            ),
            signal_model_versions=sorted(
                {candidate.evidence.signal_model_version for candidate in candidates}
            ),
            rule_ids=sorted({candidate.evidence.rule_id for candidate in candidates}),
            limitations=[
                "profile confidence summarizes support strength, not truth about a person",
                "public-safe support excludes raw artifact text",
            ],
            artifact_count=len(artifact_ids),
            included_count=len(artifact_ids),
            excluded_count=0,
            quarantined_count=0,
            source_types=source_types,
            source_diversity=self._source_diversity(source_types, artifact_ids),
            raw_content_available=False,
            audit_limitations=[
                AuditLimitation.RAW_CONTENT_UNAVAILABLE,
                AuditLimitation.AGGREGATE_EVIDENCE_ONLY,
                AuditLimitation.HASH_ONLY_REFERENCE,
            ],
        )

    def _confidence(
        self, candidates: list[ArtifactSignalCandidate], support: SignalSupport
    ) -> Confidence:
        attribution = fmean(candidate.confidence.attribution for candidate in candidates)
        authorship_origin = fmean(
            candidate.confidence.authorship_origin for candidate in candidates
        )
        extraction = fmean(candidate.confidence.extraction for candidate in candidates)
        evidence_strength = fmean(
            candidate.confidence.evidence_strength for candidate in candidates
        )
        policy_fit = fmean(candidate.confidence.policy_fit for candidate in candidates)
        support_factor = min(1.0, 0.55 + 0.15 * support.included_count)
        display = clamp(
            (
                0.2 * attribution
                + 0.2 * authorship_origin
                + 0.2 * extraction
                + 0.2 * evidence_strength
                + 0.1 * support.source_diversity
                + 0.1 * policy_fit
            )
            * support_factor,
            low=0.05,
            high=0.95,
        )
        return Confidence(
            attribution=round(attribution, 3),
            authorship_origin=round(authorship_origin, 3),
            extraction=round(extraction, 3),
            evidence_strength=round(evidence_strength, 3),
            source_diversity=round(support.source_diversity, 3),
            policy_fit=round(policy_fit, 3),
            display=round(display, 3),
        )

    def _build_manifest(
        self,
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
        signal_candidates: list[ArtifactSignalCandidate],
    ) -> BuildManifest:
        classifier_versions = sorted(
            {result.confidence.model_version for result in classifications}
        )
        signal_versions = sorted(
            {candidate.evidence.signal_model_version for candidate in signal_candidates}
        ) or [SIGNAL_CONFIDENCE_MODEL_VERSION]
        return BuildManifest(
            schema_version=SCHEMA_VERSION,
            compiler_version=COMPILER_VERSION,
            classifier_version=(
                ",".join(classifier_versions) or CLASSIFICATION_CONFIDENCE_MODEL_VERSION
            ),
            extractor_family=ExtractorFamily.RULE_BASELINE,
            extractor_major_version=0,
            extractor_minor_version=1,
            extractor_prompt_version="none",
            extractor_code_version=",".join(signal_versions),
            model_provider=None,
            model_name=None,
            model_version=None,
            source_policy_version=SOURCE_POLICY_VERSION,
            authorship_policy_version=AUTHORSHIP_POLICY_VERSION,
            export_schema_version=EXPORT_SCHEMA_VERSION,
            artifact_store_mode=self._artifact_store_mode(artifacts),
            config_hash=self._config_hash(artifacts, classifications, signal_candidates),
        )

    def _artifact_storage_policy(self, artifacts: list[Artifact]) -> ArtifactStoragePolicy:
        if not artifacts:
            return ArtifactStoragePolicy()
        modes = {artifact.storage_policy.mode for artifact in artifacts}
        if len(modes) == 1:
            return artifacts[0].storage_policy
        return ArtifactStoragePolicy(mode=ArtifactStorageMode.METADATA_ONLY)

    def _artifact_store_mode(self, artifacts: list[Artifact]) -> ArtifactStorageMode:
        if not artifacts:
            return ArtifactStorageMode.METADATA_ONLY
        modes = {artifact.storage_policy.mode for artifact in artifacts}
        if len(modes) == 1:
            return ArtifactStorageMode(next(iter(modes)))
        return ArtifactStorageMode.METADATA_ONLY

    def _context_profiles(
        self,
        profile_id: str,
        classifications: list[ArtifactClassificationResult],
    ) -> list[ContextProfile]:
        counts_by_source_type: dict[str, dict[str, int]] = defaultdict(
            lambda: {"included": 0, "excluded": 0, "quarantined": 0}
        )
        for result in classifications:
            counts_by_source_type[result.source_type][result.classification.label] += 1
        contexts: list[ContextProfile] = []
        for source_type, counts in sorted(counts_by_source_type.items()):
            if counts["included"] == 0:
                continue
            contexts.append(
                ContextProfile(
                    profile_id=f"{profile_id}-context-{self._slug(source_type)}",
                    baseline_profile_id=profile_id,
                    context_label=f"source_type:{source_type}",
                    source_filters={"source_type": source_type},
                    included_count=counts["included"],
                    quarantined_count=counts["quarantined"],
                    excluded_count=counts["excluded"],
                )
            )
        return contexts

    def _profile_family(self, family: ArtifactSignalFamily) -> SignalFamily:
        return {
            ArtifactSignalFamily.STRUCTURE: SignalFamily.STRUCTURE,
            ArtifactSignalFamily.LEXICAL: SignalFamily.LEXICAL,
            ArtifactSignalFamily.RHETORICAL_PATTERN: SignalFamily.REASONING,
            ArtifactSignalFamily.FORMATTING: SignalFamily.STRUCTURE,
            ArtifactSignalFamily.TONE_MARKER: SignalFamily.TONE,
            ArtifactSignalFamily.REASONING: SignalFamily.REASONING,
            ArtifactSignalFamily.NARRATIVE: SignalFamily.NARRATIVE,
            ArtifactSignalFamily.ANTI_PATTERN: SignalFamily.ANTI_PATTERN,
        }[family]

    def _claim_level(self, candidates: list[ArtifactSignalCandidate]) -> ClaimLevel:
        if any(
            candidate.claim_level == ClaimLevel.BOUNDED_INTERPRETATION
            for candidate in candidates
        ):
            return ClaimLevel.BOUNDED_INTERPRETATION
        return ClaimLevel.OBSERVATION

    def _claim_text(self, key: _PatternKey, included_count: int) -> str:
        count_label = "artifact" if included_count == 1 else "artifacts"
        observed = key.observed_feature.rstrip(".")
        return (
            "Across included artifacts, "
            f"{observed[0].lower()}{observed[1:]} appears in "
            f"{included_count} {count_label}."
        )

    def _compiled_signal_id(self, key: _PatternKey) -> str:
        slug = self._slug(key.name)
        digest = self._short_hash(key.observed_feature + key.rule_id)
        return f"profile-signal-{key.family.value}-{slug}-{digest}"

    def _profile_id(
        self,
        subject_id: str,
        signals: list[Signal],
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
        signal_candidates: list[ArtifactSignalCandidate],
    ) -> str:
        material = self._config_material(artifacts, classifications, signal_candidates)
        material += "".join(signal.signal_id for signal in signals)
        return f"profile-{self._slug(subject_id)}-{self._short_hash(material)}"

    def _config_hash(
        self,
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
        signal_candidates: list[ArtifactSignalCandidate],
    ) -> str:
        material = self._config_material(artifacts, classifications, signal_candidates)
        return f"sha256:{self._short_hash(material, length=24)}"

    def _config_material(
        self,
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
        signal_candidates: list[ArtifactSignalCandidate],
    ) -> str:
        parts = [
            COMPILER_VERSION,
            *sorted(artifact.artifact_id for artifact in artifacts),
            *sorted(result.classification.classification_id for result in classifications),
            *sorted(candidate.signal_id for candidate in signal_candidates),
            *sorted(candidate.evidence.signal_model_version for candidate in signal_candidates),
        ]
        return "|".join(parts)

    def _source_diversity(self, source_types: list[str], artifact_ids: list[str]) -> float:
        if not artifact_ids:
            return 0.0
        return min(1.0, len(source_types) / max(1, len(artifact_ids)))

    def _slug(self, value: str) -> str:
        return "".join(
            character if character.isalnum() else "-" for character in value.lower()
        ).strip("-")

    def _short_hash(self, value: str, *, length: int = 12) -> str:
        return sha256(value.encode("utf-8")).hexdigest()[:length]
