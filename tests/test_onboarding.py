from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from imprint import __version__
from imprint.cli import app
from imprint.connectors import build_default_connector_registry, load_connector_config

ROOT = Path(__file__).parents[1]
RUNNER = CliRunner()


def test_package_import_exposes_version() -> None:
    assert __version__ == "0.1.0"


def test_cli_help_exposes_public_onboarding_commands() -> None:
    result = RUNNER.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "connectors-dry-run" in result.output
    assert "example" in result.output
    assert "export-profile" in result.output


def test_public_example_config_validates_without_credentials() -> None:
    config = load_connector_config(ROOT / "imprint.config.example.yaml")
    discoveries = build_default_connector_registry().discover_config(config)

    enabled = [discovery for discovery in discoveries if discovery.enabled]
    assert [discovery.connector_name for discovery in enabled] == [
        "synthetic_markdown",
        "synthetic_chat",
        "synthetic_transcript",
    ]
    assert all(discovery.artifact_count > 0 for discovery in enabled)


def test_example_command_writes_public_safe_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "synthetic-demo"
    result = RUNNER.invoke(app, ["example", "--output-dir", str(output_dir)])

    assert result.exit_code == 0
    assert "example=synthetic_transcript" in result.output
    assert "outputs=profile.imprint.json,profile.md,what-imprint-learned.md" in result.output

    expected = {
        "profile.imprint.json",
        "profile.md",
        "what-imprint-learned.md",
        "mosvera.expression.json",
        "human-cli.consumer.json",
    }
    assert {path.name for path in output_dir.iterdir()} == expected

    profile_payload = json.loads((output_dir / "profile.imprint.json").read_text(encoding="utf-8"))
    assert profile_payload["export_type"] == "canonical_json"
    assert profile_payload["profile"]["subject_id"] == "example_subject"

    combined = "\n".join(path.read_text(encoding="utf-8") for path in output_dir.iterdir())
    assert "The Queue Underneath" not in combined
    assert "example_article.md" not in combined
    assert "synthetic-demo.json" not in combined
    assert "/examples/synthetic_corpus/" not in combined
    assert "IMPRINT_PRIVATE_SOURCE_TOKEN" not in combined
