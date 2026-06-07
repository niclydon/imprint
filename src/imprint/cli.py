from __future__ import annotations

from pathlib import Path
import json

import typer

from imprint.adapters import build_default_registry
from imprint.adapters.protocol import AdapterError
from imprint.classification import RuleBasedArtifactClassifier
from imprint.compiler import CompilerError, ProfileCompiler
from imprint.exports import (
    ExportSafetyError,
    canonical_profile_json,
    first_run_summary,
    markdown_profile_export,
    mosvera_expression_overlay,
)
from imprint.signals import RuleBasedSignalExtractor
from imprint.schemas import ArtifactStorageMode, ArtifactStoragePolicy, ExpressionProfile

app = typer.Typer(help="Imprint identity and expression profile compiler.")


def _compile_local_profile(
    source_type: str,
    path: Path,
    subject_id: str,
    storage_mode: ArtifactStorageMode,
) -> tuple[ExpressionProfile, int, int]:
    registry = build_default_registry()
    storage_policy = ArtifactStoragePolicy(mode=storage_mode)
    try:
        artifact_registry = registry.ingest(
            source_type,
            path,
            storage_policy=storage_policy,
        )
    except AdapterError as exc:
        raise typer.BadParameter(str(exc)) from exc

    artifacts = artifact_registry.values()
    classifier = RuleBasedArtifactClassifier()
    classifications = classifier.classify_artifacts(artifacts)
    extractor = RuleBasedSignalExtractor()
    signals = extractor.extract_batch(artifacts, classifications)
    try:
        profile = ProfileCompiler().compile_profile(
            subject_id=subject_id,
            artifacts=artifacts,
            classifications=classifications,
            signal_candidates=signals,
        )
    except CompilerError as exc:
        raise typer.BadParameter(str(exc)) from exc
    return profile, len(artifacts), len(signals)


@app.command()
def version() -> None:
    """Print the Imprint version."""
    from imprint import __version__

    typer.echo(__version__)


@app.command()
def ingest(
    source_type: str = typer.Option(..., help="Registered local adapter source type."),
    path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True),
    storage_mode: ArtifactStorageMode = typer.Option(
        ArtifactStorageMode.METADATA_ONLY,
        help="Artifact storage mode for normalized artifacts.",
    ),
) -> None:
    """Normalize local artifacts and print a compact ingestion summary."""
    registry = build_default_registry()
    storage_policy = ArtifactStoragePolicy(mode=storage_mode)
    try:
        artifact_registry = registry.ingest(
            source_type,
            path,
            storage_policy=storage_policy,
        )
    except AdapterError as exc:
        raise typer.BadParameter(str(exc)) from exc

    summary = artifact_registry.summary()
    typer.echo(f"source_type={source_type}")
    typer.echo(f"artifacts={summary['total']}")
    typer.echo(f"included={summary['included']}")
    typer.echo(f"excluded={summary['excluded']}")
    typer.echo(f"quarantined={summary['quarantined']}")


@app.command()
def classify(
    source_type: str = typer.Option(..., help="Registered local adapter source type."),
    path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True),
    storage_mode: ArtifactStorageMode = typer.Option(
        ArtifactStorageMode.METADATA_ONLY,
        help="Artifact storage mode for normalized artifacts.",
    ),
) -> None:
    """Classify normalized local artifacts and print compact decision counts."""
    registry = build_default_registry()
    storage_policy = ArtifactStoragePolicy(mode=storage_mode)
    try:
        artifact_registry = registry.ingest(
            source_type,
            path,
            storage_policy=storage_policy,
        )
    except AdapterError as exc:
        raise typer.BadParameter(str(exc)) from exc

    classifier = RuleBasedArtifactClassifier()
    results = classifier.classify_artifacts(artifact_registry.values())
    counts = {"included": 0, "excluded": 0, "quarantined": 0}
    for result in results:
        counts[result.classification.label] += 1

    typer.echo(f"source_type={source_type}")
    typer.echo(f"classified={len(results)}")
    typer.echo(f"included={counts['included']}")
    typer.echo(f"excluded={counts['excluded']}")
    typer.echo(f"quarantined={counts['quarantined']}")


@app.command(name="extract-signals")
def extract_signals(
    source_type: str = typer.Option(..., help="Registered local adapter source type."),
    path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True),
    storage_mode: ArtifactStorageMode = typer.Option(
        ArtifactStorageMode.METADATA_ONLY,
        help="Artifact storage mode for normalized artifacts.",
    ),
) -> None:
    """Extract deterministic artifact-level signals from classified local artifacts."""
    registry = build_default_registry()
    storage_policy = ArtifactStoragePolicy(mode=storage_mode)
    try:
        artifact_registry = registry.ingest(
            source_type,
            path,
            storage_policy=storage_policy,
        )
    except AdapterError as exc:
        raise typer.BadParameter(str(exc)) from exc

    artifacts = artifact_registry.values()
    classifier = RuleBasedArtifactClassifier()
    classifications = classifier.classify_artifacts(artifacts)
    extractor = RuleBasedSignalExtractor()
    signals = extractor.extract_batch(artifacts, classifications)
    durable = sum(1 for signal in signals if signal.durable)
    quarantined = sum(1 for signal in signals if signal.claim_level == "quarantined")

    typer.echo(f"source_type={source_type}")
    typer.echo(f"artifacts={len(artifacts)}")
    typer.echo(f"signals={len(signals)}")
    typer.echo(f"durable={durable}")
    typer.echo(f"quarantined={quarantined}")


@app.command(name="compile")
def compile_profile(
    source_type: str = typer.Option(..., help="Registered local adapter source type."),
    path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True),
    subject_id: str = typer.Option("synthetic-subject", help="Opaque profile subject ID."),
    storage_mode: ArtifactStorageMode = typer.Option(
        ArtifactStorageMode.METADATA_ONLY,
        help="Artifact storage mode for normalized artifacts.",
    ),
) -> None:
    """Compile deterministic profile patterns from local artifact signals."""
    profile, artifact_count, signal_count = _compile_local_profile(
        source_type,
        path,
        subject_id,
        storage_mode,
    )

    typer.echo(f"profile_id={profile.profile_id}")
    typer.echo(f"subject_id={profile.subject_id}")
    typer.echo(f"artifacts={artifact_count}")
    typer.echo(f"candidate_signals={signal_count}")
    typer.echo(f"profile_signals={len(profile.signals)}")
    typer.echo(f"context_profiles={len(profile.context_profiles)}")
    typer.echo(f"compiler_version={profile.build_manifest.compiler_version}")


@app.command(name="export-profile")
def export_profile(
    source_type: str = typer.Option(..., help="Registered local adapter source type."),
    path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True, readable=True),
    subject_id: str = typer.Option("synthetic-subject", help="Opaque profile subject ID."),
    export_format: str = typer.Option(
        "json",
        "--format",
        help="Export format: json, markdown, first-run, or mosvera.",
    ),
    storage_mode: ArtifactStorageMode = typer.Option(
        ArtifactStorageMode.METADATA_ONLY,
        help="Artifact storage mode for normalized artifacts.",
    ),
) -> None:
    """Export a compiled local profile in a public-safe Sprint 07 format."""
    profile, _, _ = _compile_local_profile(source_type, path, subject_id, storage_mode)
    try:
        if export_format == "json":
            typer.echo(canonical_profile_json(profile), nl=False)
        elif export_format == "markdown":
            typer.echo(markdown_profile_export(profile), nl=False)
        elif export_format == "first-run":
            typer.echo(first_run_summary(profile), nl=False)
        elif export_format == "mosvera":
            typer.echo(json.dumps(mosvera_expression_overlay(profile), indent=2, sort_keys=True))
        else:
            raise typer.BadParameter("format must be one of: json, markdown, first-run, mosvera")
    except ExportSafetyError as exc:
        raise typer.BadParameter(str(exc)) from exc


if __name__ == "__main__":
    app()
