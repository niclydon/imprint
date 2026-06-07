from __future__ import annotations

import re

from imprint.classification.engine import clamp
from imprint.schemas import (
    Artifact,
    ArtifactClassificationLabel,
    ArtifactClassificationResult,
    ArtifactSignalCandidate,
    ArtifactSignalEvidence,
    ArtifactSignalFamily,
    ClaimLevel,
    Confidence,
    SignalEvidencePolicy,
)

SIGNAL_CONFIDENCE_MODEL_VERSION = "sprint05-rule-v1"


def signal_id_for(artifact_id: str, family: ArtifactSignalFamily, rule_id: str) -> str:
    return f"signal-{artifact_id}-{family.value}-{rule_id}"


def validate_source_id(source_id: str) -> None:
    """Validate that source_id is opaque and does not expose filesystem paths.

    Raises ValueError if source_id contains filesystem path characters, traversal patterns,
    or common file extensions that would indicate a path leak.

    Args:
        source_id: The source identifier to validate.

    Raises:
        ValueError: If source_id contains filesystem path patterns or extensions.
    """
    if not source_id or not isinstance(source_id, str):
        raise ValueError("source_id must be a non-empty string")
    if source_id.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", source_id):
        raise ValueError("source_id cannot expose filesystem paths")
    if ".." in source_id or source_id.endswith((".txt", ".json", ".yaml", ".yml", ".csv", ".db")):
        raise ValueError("source_id cannot contain path traversal or file extensions")


class RuleBasedSignalExtractor:
    """Deterministic artifact-level signal extractor."""

    def extract_from_result(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
    ) -> list[ArtifactSignalCandidate]:
        if classification_result.classification.label == ArtifactClassificationLabel.EXCLUDED:
            return []

        candidates: list[ArtifactSignalCandidate] = []
        hints = artifact.source_hints
        candidates.extend(self._structure_signals(artifact, classification_result, hints))
        candidates.extend(self._lexical_signals(artifact, classification_result, hints))
        candidates.extend(self._rhetorical_signals(artifact, classification_result, hints))
        candidates.extend(self._formatting_signals(artifact, classification_result, hints))
        candidates.extend(self._tone_signals(artifact, classification_result, hints))
        candidates.extend(self._reasoning_signals(artifact, classification_result, hints))
        candidates.extend(self._narrative_signals(artifact, classification_result, hints))
        candidates.extend(self._anti_pattern_signals(artifact, classification_result, hints))
        return candidates

    def extract_batch(
        self,
        artifacts: list[Artifact],
        classifications: list[ArtifactClassificationResult],
    ) -> list[ArtifactSignalCandidate]:
        classification_by_artifact = {result.artifact_id: result for result in classifications}
        candidates: list[ArtifactSignalCandidate] = []
        for artifact in artifacts:
            result = classification_by_artifact[artifact.artifact_id]
            candidates.extend(self.extract_from_result(artifact, result))
        return candidates

    def _structure_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if hints.get("short_paragraph_count", 0) and hints.get("paragraph_count", 0):
            if int(hints["short_paragraph_count"]) == int(hints["paragraph_count"]):
                candidates.append(
                    self._candidate(
                        artifact,
                        classification_result,
                        family=ArtifactSignalFamily.STRUCTURE,
                        rule_id="structure_short_paragraphs",
                        name="short_paragraphs",
                        observed_feature="All observed paragraphs are short.",
                        rule_reliability=0.82,
                        evidence_strength=0.72,
                    )
                )
        if hints.get("has_direct_opening"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.STRUCTURE,
                    rule_id="structure_direct_opening",
                    name="direct_opening_sentence",
                    observed_feature="The artifact opens with a short direct sentence.",
                    rule_reliability=0.78,
                    evidence_strength=0.65,
                )
            )
        return candidates

    def _lexical_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if int(hints.get("contraction_count", 0)) > 0:
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.LEXICAL,
                    rule_id="lexical_contractions",
                    name="contraction_usage",
                    observed_feature="The artifact includes contractions.",
                    rule_reliability=0.75,
                    evidence_strength=0.62,
                )
            )
        return candidates

    def _rhetorical_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if hints.get("uses_contrast_framing"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.RHETORICAL_PATTERN,
                    rule_id="rhetorical_contrast_framing",
                    name="contrast_framing",
                    observed_feature="The artifact uses a not-X-but-Y contrast structure.",
                    rule_reliability=0.84,
                    evidence_strength=0.76,
                )
            )
        return candidates

    def _formatting_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if hints.get("uses_bullets"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.FORMATTING,
                    rule_id="formatting_bullet_usage",
                    name="bullet_usage",
                    observed_feature="The artifact uses bullet formatting.",
                    rule_reliability=0.88,
                    evidence_strength=0.8,
                )
            )
        if hints.get("uses_headings"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.FORMATTING,
                    rule_id="formatting_heading_usage",
                    name="heading_usage",
                    observed_feature="The artifact uses heading formatting.",
                    rule_reliability=0.9,
                    evidence_strength=0.8,
                )
            )
        return candidates

    def _tone_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if int(hints.get("question_count", 0)) > 0:
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.TONE_MARKER,
                    rule_id="tone_question_marker",
                    name="question_marker",
                    observed_feature="The artifact uses explicit question markers.",
                    rule_reliability=0.72,
                    evidence_strength=0.6,
                )
            )
        if int(hints.get("exclamation_count", 0)) > 0:
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.TONE_MARKER,
                    rule_id="tone_exclamation_marker",
                    name="exclamation_marker",
                    observed_feature="The artifact uses exclamation markers.",
                    rule_reliability=0.7,
                    evidence_strength=0.58,
                )
            )
        return candidates

    def _reasoning_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if hints.get("uses_causal_explanation"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.REASONING,
                    rule_id="reasoning_causal_explanation",
                    name="causal_explanation_marker",
                    observed_feature="The artifact uses explicit causal explanation markers.",
                    rule_reliability=0.8,
                    evidence_strength=0.72,
                )
            )
        if hints.get("uses_tradeoff_framing"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.REASONING,
                    rule_id="reasoning_tradeoff_framing",
                    name="tradeoff_framing_marker",
                    observed_feature="The artifact uses explicit tradeoff or exchange framing.",
                    rule_reliability=0.84,
                    evidence_strength=0.76,
                )
            )
        if hints.get("uses_hedging") or hints.get("uses_caveat_markers"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.REASONING,
                    rule_id="reasoning_caveat_handling",
                    name="caveat_or_uncertainty_marker",
                    observed_feature="The artifact includes caveat or uncertainty markers.",
                    rule_reliability=0.74,
                    evidence_strength=0.64,
                )
            )
        return candidates

    def _narrative_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if int(hints.get("sequence_marker_count", 0)) >= 2:
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.NARRATIVE,
                    rule_id="narrative_ordered_sequence",
                    name="ordered_sequence_marker",
                    observed_feature="The artifact uses explicit ordered sequence markers.",
                    rule_reliability=0.8,
                    evidence_strength=0.7,
                )
            )
        if hints.get("uses_before_after_transition"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.NARRATIVE,
                    rule_id="narrative_before_after_transition",
                    name="before_after_transition",
                    observed_feature="The artifact uses an explicit before-and-after transition.",
                    rule_reliability=0.82,
                    evidence_strength=0.74,
                )
            )
        if hints.get("uses_example_marker"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.NARRATIVE,
                    rule_id="narrative_example_grounding",
                    name="example_grounding_marker",
                    observed_feature="The artifact grounds a point with an explicit example marker.",
                    rule_reliability=0.78,
                    evidence_strength=0.68,
                )
            )
        return candidates

    def _anti_pattern_signals(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        hints: dict[str, object],
    ) -> list[ArtifactSignalCandidate]:
        candidates: list[ArtifactSignalCandidate] = []
        if hints.get("has_question_burst"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.ANTI_PATTERN,
                    rule_id="anti_pattern_question_burst",
                    name="question_burst_requires_recurrence",
                    observed_feature="The artifact stacks multiple questions; downstream consumers should not promote that into a stable uncertainty claim without recurrence.",
                    rule_reliability=0.77,
                    evidence_strength=0.66,
                )
            )
        if hints.get("has_exclamation_burst"):
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.ANTI_PATTERN,
                    rule_id="anti_pattern_punctuation_emphasis",
                    name="punctuation_emphasis_not_emotional_ground_truth",
                    observed_feature="The artifact uses clustered punctuation emphasis; downstream consumers should not treat that as emotional ground truth.",
                    rule_reliability=0.79,
                    evidence_strength=0.67,
                )
            )
        if (hints.get("uses_bullets") or hints.get("uses_headings")) and int(hints.get("sentence_count", 0)) <= 2:
            candidates.append(
                self._candidate(
                    artifact,
                    classification_result,
                    family=ArtifactSignalFamily.ANTI_PATTERN,
                    rule_id="anti_pattern_formatting_without_explanatory_prose",
                    name="formatting_not_reasoning_evidence",
                    observed_feature="The artifact relies on formatting cues with limited explanatory prose; formatting alone should not be promoted into a reasoning claim.",
                    rule_reliability=0.83,
                    evidence_strength=0.73,
                )
            )
        return candidates

    def _candidate(
        self,
        artifact: Artifact,
        classification_result: ArtifactClassificationResult,
        *,
        family: ArtifactSignalFamily,
        rule_id: str,
        name: str,
        observed_feature: str,
        rule_reliability: float,
        evidence_strength: float,
    ) -> ArtifactSignalCandidate:
        durable = classification_result.classification.label == ArtifactClassificationLabel.INCLUDED
        claim_level = ClaimLevel.OBSERVATION if durable else ClaimLevel.QUARANTINED
        signal_id = signal_id_for(artifact.artifact_id, family, rule_id)
        source_id = artifact.reference.source_id
        validate_source_id(source_id)
        confidence = self._signal_confidence(
            classification_result,
            rule_reliability=rule_reliability,
            evidence_strength=evidence_strength,
            durable=durable,
        )
        evidence = ArtifactSignalEvidence(
            signal_id=signal_id,
            artifact_id=artifact.artifact_id,
            source_id=source_id,
            source_type=artifact.reference.source_type,
            classification_id=classification_result.classification.classification_id,
            classification_label=classification_result.classification.label,
            classification_model_version=classification_result.confidence.model_version,
            signal_model_version=SIGNAL_CONFIDENCE_MODEL_VERSION,
            rule_id=rule_id,
            observed_feature=observed_feature,
            evidence_policy=SignalEvidencePolicy.NO_RAW_TEXT,
            limitations=[] if durable else ["non-included artifacts cannot produce durable support"],
        )
        return ArtifactSignalCandidate(
            signal_id=signal_id,
            artifact_id=artifact.artifact_id,
            source_id=artifact.reference.source_id,
            source_type=artifact.reference.source_type,
            family=family,
            name=name,
            observed_feature=observed_feature,
            claim_level=claim_level,
            confidence=confidence,
            evidence=evidence,
            durable=durable,
        )

    def _signal_confidence(
        self,
        classification_result: ArtifactClassificationResult,
        *,
        rule_reliability: float,
        evidence_strength: float,
        durable: bool,
    ) -> Confidence:
        """Compute signal confidence from classification and rule-level evidence.

        Formula (weighted average):
        - 25% attribution: how well the artifact is assigned to the subject.
        - 20% authorship_origin: confidence that the subject authored the artifact.
        - 25% extraction: rule reliability, bounded [0.2, 0.95] to avoid extreme overconfidence.
        - 20% evidence_strength: how reliable the specific observed feature is as a signal.
        - 10% policy_fit: 1.0 for durable (included) signals, 0.6 for quarantined signals.

        The final display score is clamped to [0.05, 0.95] and multiplied by the
        classification confidence to preserve the dependency chain.

        Args:
            classification_result: The artifact's classification output.
            rule_reliability: How reliable this extraction rule is (0.0-1.0).
            evidence_strength: How reliable the observed feature is (0.0-1.0).
            durable: Whether the artifact is eligible for durable support (included vs. quarantined).

        Returns:
            A Confidence object with all components decomposed for auditing.
        """
        attribution = classification_result.confidence.attribution
        authorship_origin = classification_result.confidence.authorship_origin
        extraction = clamp(rule_reliability, low=0.2, high=0.95)
        source_diversity = 1.0
        policy_fit = 1.0 if durable else 0.6
        display = clamp(
            (
                0.25 * attribution
                + 0.2 * authorship_origin
                + 0.25 * extraction
                + 0.2 * evidence_strength
                + 0.1 * policy_fit
            )
            * classification_result.confidence.display,
            low=0.05,
            high=0.95,
        )
        return Confidence(
            attribution=round(attribution, 3),
            authorship_origin=round(authorship_origin, 3),
            extraction=round(extraction, 3),
            evidence_strength=round(evidence_strength, 3),
            source_diversity=round(source_diversity, 3),
            policy_fit=round(policy_fit, 3),
            display=round(display, 3),
        )
