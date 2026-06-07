from __future__ import annotations

from imprint.schemas import (
    Artifact,
    ArtifactClassification,
    ArtifactClassificationLabel,
    ClassificationConfidence,
    ArtifactClassificationResult,
    ArtifactType,
    AuthorshipOrigin,
    ClassificationEvidence,
)

CLASSIFICATION_CONFIDENCE_MODEL_VERSION = "sprint04-rule-v1"
OVERSIZED_ARTIFACT_BYTES = 10 * 1024 * 1024


def classification_id_for(artifact: Artifact, label: ArtifactClassificationLabel, origin: AuthorshipOrigin) -> str:
    return f"classified-{artifact.artifact_id}-{label.value}-{origin.value}"


def clamp(value: float, *, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


class RuleBasedArtifactClassifier:
    """Deterministic artifact-only classifier.

    This classifier consumes normalized artifacts plus safe source hints. It never reads raw
    artifact text or trusts adapter outputs as final classification truth.
    """

    def classify_artifact(self, artifact: Artifact) -> ArtifactClassificationResult:
        hints = self._source_hints_considered(artifact)
        rule_ids: list[str] = []
        limitations: list[str] = []

        artifact_type = self._classify_artifact_type(artifact, hints, rule_ids)
        quote_likelihood = self._quote_or_forward_likelihood(hints, rule_ids)
        template_likelihood = self._template_or_notification_likelihood(hints, rule_ids)
        assistant_likelihood = self._assistant_output_likelihood(hints, rule_ids)
        contamination_risk = self._contamination_risk(
            artifact,
            hints,
            quote_likelihood,
            template_likelihood,
            assistant_likelihood,
            rule_ids,
        )
        authorship_origin, authorship_confidence = self._classify_authorship(
            artifact,
            hints,
            quote_likelihood,
            template_likelihood,
            assistant_likelihood,
            rule_ids,
            limitations,
        )
        label = self._classify_label(
            authorship_origin,
            authorship_confidence,
            contamination_risk,
            rule_ids,
        )
        confidence = self._classification_confidence(
            artifact,
            authorship_confidence,
            contamination_risk,
            label,
            hints,
        )

        classification = ArtifactClassification(
            classification_id=classification_id_for(artifact, label, authorship_origin),
            label=label,
            authorship_origin=authorship_origin,
            authorship_confidence=authorship_confidence,
            reason_categories=self._reason_categories(authorship_origin, hints),
        )
        evidence = ClassificationEvidence(
            artifact_id=artifact.artifact_id,
            source_id=artifact.reference.source_id,
            source_type=artifact.reference.source_type,
            source_hints_considered=hints,
            rule_ids=rule_ids,
            limitations=limitations,
            evidence_summary=self._evidence_summary(
                artifact,
                authorship_origin,
                label,
                quote_likelihood,
                template_likelihood,
                assistant_likelihood,
                contamination_risk,
            ),
            quote_or_forward_likelihood=quote_likelihood,
            template_or_notification_likelihood=template_likelihood,
            assistant_output_likelihood=assistant_likelihood,
            contamination_risk=contamination_risk,
        )
        return ArtifactClassificationResult(
            artifact_id=artifact.artifact_id,
            source_id=artifact.reference.source_id,
            source_type=artifact.reference.source_type,
            artifact_type=artifact_type,
            classification=classification,
            evidence=evidence,
            confidence=confidence,
        )

    def classify_artifacts(self, artifacts: list[Artifact]) -> list[ArtifactClassificationResult]:
        return [self.classify_artifact(artifact) for artifact in artifacts]

    def _source_hints_considered(self, artifact: Artifact) -> dict[str, object]:
        return {
            **artifact.source_hints,
            "ingest_authorship_origin": artifact.classification.authorship_origin,
            "ingest_authorship_confidence": artifact.classification.authorship_confidence,
            "ingest_classification_label": artifact.classification.label,
            "ingest_artifact_type": artifact.reference.artifact_type,
        }

    def _classify_artifact_type(
        self,
        artifact: Artifact,
        hints: dict[str, object],
        rule_ids: list[str],
    ) -> ArtifactType:
        if artifact.reference.source_type == "local_transcript_json":
            rule_ids.append("artifact_type_transcript_source_shape")
            return ArtifactType.TRANSCRIPT_SEGMENT
        if hints.get("artifact_type_hint") and hints.get("artifact_type_hint") != artifact.reference.artifact_type:
            rule_ids.append("artifact_type_hint_not_promoted_without_corroboration")
        rule_ids.append("artifact_type_preserve_normalized_shape")
        return ArtifactType(artifact.reference.artifact_type)

    def _quote_or_forward_likelihood(self, hints: dict[str, object], rule_ids: list[str]) -> float:
        score = 0.0
        if hints.get("oversized_artifact"):
            rule_ids.append("oversized_artifact_detected")
            score = max(score, 0.6)
        if hints.get("contains_forward_marker"):
            rule_ids.append("forward_marker_detected")
            score = max(score, 0.95)
        if hints.get("contains_quote_marker") or hints.get("contains_reply_header"):
            rule_ids.append("quote_or_reply_marker_detected")
            score = max(score, 0.8)
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.QUOTED_OR_FORWARDED.value:
            rule_ids.append("adapter_quote_hint_considered")
            score = max(score, 0.7)
        return score

    def _template_or_notification_likelihood(self, hints: dict[str, object], rule_ids: list[str]) -> float:
        score = 0.0
        if hints.get("contains_notification_marker"):
            rule_ids.append("notification_marker_detected")
            score = max(score, 0.95)
        if hints.get("contains_template_marker"):
            rule_ids.append("template_marker_detected")
            score = max(score, 0.8)
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.TEMPLATE_OR_NOTIFICATION.value:
            rule_ids.append("adapter_template_hint_considered")
            score = max(score, 0.75)
        return score

    def _assistant_output_likelihood(self, hints: dict[str, object], rule_ids: list[str]) -> float:
        score = 0.0
        if hints.get("contains_assistant_marker"):
            rule_ids.append("assistant_marker_detected")
            score = max(score, 0.9)
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.ASSISTANT_OUTPUT.value:
            rule_ids.append("adapter_assistant_hint_considered")
            score = max(score, 0.75)
        return score

    def _contamination_risk(
        self,
        artifact: Artifact,
        hints: dict[str, object],
        quote_likelihood: float,
        template_likelihood: float,
        assistant_likelihood: float,
        rule_ids: list[str],
    ) -> float:
        contamination = max(quote_likelihood, template_likelihood, assistant_likelihood)
        if hints.get("speaker_present") is False:
            rule_ids.append("speaker_missing_in_transcript")
            contamination = max(contamination, 0.7)
        if hints.get("oversized_artifact"):
            contamination = max(contamination, 0.65)
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.MIXED_AUTHORSHIP.value:
            rule_ids.append("mixed_authorship_hint_considered")
            contamination = max(contamination, 0.85)
        if artifact.classification.authorship_origin == AuthorshipOrigin.MISSING_METADATA:
            contamination = max(contamination, 0.55)
        return contamination

    def _classify_authorship(
        self,
        artifact: Artifact,
        hints: dict[str, object],
        quote_likelihood: float,
        template_likelihood: float,
        assistant_likelihood: float,
        rule_ids: list[str],
        limitations: list[str],
    ) -> tuple[AuthorshipOrigin, float]:
        if template_likelihood >= 0.85:
            return AuthorshipOrigin.TEMPLATE_OR_NOTIFICATION, 0.95
        if assistant_likelihood >= 0.85:
            return AuthorshipOrigin.ASSISTANT_OUTPUT, 0.9
        if quote_likelihood >= 0.85:
            return AuthorshipOrigin.QUOTED_OR_FORWARDED, 0.85
        if hints.get("oversized_artifact"):
            rule_ids.append("oversized_artifact_requires_review")
            limitations.append("oversized artifact quarantined for manual review")
            return AuthorshipOrigin.PARSER_UNCERTAIN, 0.3
        if artifact.reference.source_type == "local_transcript_json":
            if hints.get("speaker_present") is False:
                limitations.append("speaker metadata missing; transcript segment quarantined")
                return AuthorshipOrigin.UNKNOWN_SPEAKER, 0.35
            rule_ids.append("speaker_metadata_supports_human_origin")
            return AuthorshipOrigin.HUMAN_ORIGIN, 0.72
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.HUMAN_DIRECTED_AI_ASSISTED.value:
            rule_ids.append("adapter_ai_assistance_hint_reassessed")
            limitations.append("adapter AI-assistance hint treated as advisory")
            return AuthorshipOrigin.HUMAN_DIRECTED_AI_ASSISTED, 0.55
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.SUSPECTED_AI_ASSISTED.value:
            rule_ids.append("adapter_suspected_ai_hint_reassessed")
            limitations.append("suspected AI assistance remains unverified without stronger evidence")
            return AuthorshipOrigin.SUSPECTED_AI_ASSISTED, 0.45
        if hints.get("authorship_origin_hint") == AuthorshipOrigin.HUMAN_ORIGIN.value:
            rule_ids.append("adapter_human_origin_hint_not_trusted_as_ground_truth")
            limitations.append("human-origin hint lacked corroborating evidence")
            return AuthorshipOrigin.MISSING_METADATA, 0.4
        if hints.get("ingest_authorship_origin") == AuthorshipOrigin.HUMAN_ORIGIN.value:
            limitations.append("ingestion authorship label treated as provisional")
        return AuthorshipOrigin.MISSING_METADATA, 0.4

    def _classify_label(
        self,
        authorship_origin: AuthorshipOrigin,
        authorship_confidence: float,
        contamination_risk: float,
        rule_ids: list[str],
    ) -> ArtifactClassificationLabel:
        if authorship_origin in {
            AuthorshipOrigin.ASSISTANT_OUTPUT,
            AuthorshipOrigin.TEMPLATE_OR_NOTIFICATION,
        }:
            rule_ids.append("exclude_non_subject_authorship")
            return ArtifactClassificationLabel.EXCLUDED
        if authorship_origin in {
            AuthorshipOrigin.QUOTED_OR_FORWARDED,
            AuthorshipOrigin.UNKNOWN_SPEAKER,
            AuthorshipOrigin.MISSING_METADATA,
            AuthorshipOrigin.PARSER_UNCERTAIN,
            AuthorshipOrigin.MIXED_AUTHORSHIP,
            AuthorshipOrigin.SUSPECTED_AI_ASSISTED,
            AuthorshipOrigin.HUMAN_DIRECTED_AI_ASSISTED,
        }:
            rule_ids.append("quarantine_uncertain_authorship")
            return ArtifactClassificationLabel.QUARANTINED
        if contamination_risk >= 0.5 or authorship_confidence < 0.65:
            rule_ids.append("quarantine_due_to_risk_or_low_confidence")
            return ArtifactClassificationLabel.QUARANTINED
        rule_ids.append("include_confident_human_origin")
        return ArtifactClassificationLabel.INCLUDED

    def _classification_confidence(
        self,
        artifact: Artifact,
        authorship_confidence: float,
        contamination_risk: float,
        label: ArtifactClassificationLabel,
        hints: dict[str, object],
    ) -> ClassificationConfidence:
        attribution = 0.95 if artifact.reference.source_id.startswith("source-") else 0.5
        evidence_strength = self._evidence_strength(artifact, hints, contamination_risk)
        source_reliability = self._source_reliability(artifact, hints)
        policy_fit = 1.0 if label in {
            ArtifactClassificationLabel.EXCLUDED,
            ArtifactClassificationLabel.QUARANTINED,
            ArtifactClassificationLabel.INCLUDED,
        } else 0.5
        contamination_penalty = contamination_risk
        display = clamp(
            (
                0.15 * attribution
                + 0.35 * authorship_confidence
                + 0.2 * evidence_strength
                + 0.15 * source_reliability
                + 0.15 * policy_fit
            )
            - (0.2 * contamination_penalty),
            low=0.05,
            high=0.95,
        )
        return ClassificationConfidence(
            model_version=CLASSIFICATION_CONFIDENCE_MODEL_VERSION,
            attribution=round(attribution, 3),
            authorship_origin=round(authorship_confidence, 3),
            evidence_strength=round(evidence_strength, 3),
            source_reliability=round(source_reliability, 3),
            policy_fit=round(policy_fit, 3),
            contamination_penalty=round(contamination_penalty, 3),
            display=round(display, 3),
        )

    def _evidence_strength(
        self,
        artifact: Artifact,
        hints: dict[str, object],
        contamination_risk: float,
    ) -> float:
        if hints.get("oversized_artifact"):
            return 0.35
        if artifact.reference.source_type == "local_transcript_json" and hints.get("speaker_present") is True:
            return 0.8
        if any(
            hints.get(key)
            for key in (
                "contains_forward_marker",
                "contains_notification_marker",
                "contains_assistant_marker",
            )
        ):
            return 0.85
        if contamination_risk >= 0.5:
            return 0.45
        return 0.55

    def _source_reliability(self, artifact: Artifact, hints: dict[str, object]) -> float:
        if hints.get("oversized_artifact"):
            return 0.4
        if artifact.reference.source_type == "local_transcript_json":
            return 0.8 if hints.get("speaker_present") is True else 0.45
        if artifact.reference.source_type == "local_jsonl":
            return 0.55
        if artifact.reference.source_type in {"local_text", "local_markdown"}:
            return 0.6
        return 0.5

    def _reason_categories(
        self,
        authorship_origin: AuthorshipOrigin,
        hints: dict[str, object],
    ) -> list[AuthorshipOrigin]:
        categories = [authorship_origin]
        for key in ("authorship_origin_hint", "ingest_authorship_origin"):
            value = hints.get(key)
            if isinstance(value, str):
                try:
                    category = AuthorshipOrigin(value)
                except ValueError:
                    continue
                if category not in categories:
                    categories.append(category)
        return categories

    def _evidence_summary(
        self,
        artifact: Artifact,
        authorship_origin: AuthorshipOrigin,
        label: ArtifactClassificationLabel,
        quote_likelihood: float,
        template_likelihood: float,
        assistant_likelihood: float,
        contamination_risk: float,
    ) -> str:
        return (
            f"Artifact {artifact.artifact_id} from {artifact.reference.source_type} classified as "
            f"{label.value} with authorship {authorship_origin.value}; quote={quote_likelihood:.2f}, "
            f"template={template_likelihood:.2f}, assistant={assistant_likelihood:.2f}, "
            f"contamination={contamination_risk:.2f}."
        )
