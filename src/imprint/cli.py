from __future__ import annotations

from pathlib import Path

import typer

from imprint.adapters import build_default_registry
from imprint.adapters.protocol import AdapterError
from imprint.classification import RuleBasedArtifactClassifier
from imprint.schemas import ArtifactStorageMode, ArtifactStoragePolicy

app = typer.Typer(help="Imprint identity and expression profile compiler.")


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
