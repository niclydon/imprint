from __future__ import annotations

import base64
import json
from pathlib import Path

from typer.testing import CliRunner

from imprint.cli import app
from imprint.quality import compare_export_files, validate_export_file

RUNNER = CliRunner()
JWT_CREDENTIAL = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJzdWJqZWN0IiwiaWF0IjoxNzAwMDAwMDAwfQ."
    "c2lnbmF0dXJl"
)
OPENAI_STYLE_CREDENTIAL = "s" "k-" + "ABCDEFGHIJKLMNOPQRSTUVWX"


def _example_export(tmp_path: Path) -> Path:
    result = RUNNER.invoke(app, ["example", "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    return tmp_path / "profile.imprint.json"


def test_validate_export_passes_canonical_example(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)

    report = validate_export_file(export_path)

    assert report["status"] == "PASS"
    assert report["release_gate"]["status"] == "PASS"
    assert {check["name"] for check in report["checks"]} >= {
        "schema",
        "export_version",
        "compatibility",
        "source_ids",
        "privacy",
    }


def test_validate_export_fails_raw_text_and_path_leak(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["raw_text"] = "raw text from /private/corpus/source.txt"
    bad_path = tmp_path / "bad-export.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert report["release_gate"]["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]
    assert "privacy" in report["release_gate"]["reason_codes"]


def test_validate_export_fails_jwt_credential(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["limitations"].append(JWT_CREDENTIAL)
    bad_path = tmp_path / "bad-jwt.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]


def test_validate_export_fails_base64_encoded_credential(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["limitations"].append(
        base64.b64encode(f"api_key={OPENAI_STYLE_CREDENTIAL}".encode()).decode()
    )
    bad_path = tmp_path / "bad-base64.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]


def test_validate_export_fails_root_level_private_metadata(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["_metadata"] = {"note": "looks harmless"}
    bad_path = tmp_path / "bad-root-metadata.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]


def test_validate_export_fails_nested_underscore_metadata_escape(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["profile"]["_debug"] = {"prompt": "hidden generation control"}
    bad_path = tmp_path / "bad-nested-metadata.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]


def test_validate_export_fails_invalid_source_id(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["expression_patterns"][0]["support"]["source_ids"] = ["/private/source.txt"]
    bad_path = tmp_path / "bad-source-id.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "privacy" in report["release_gate"]["blocking_failures"]


def test_validate_export_fails_missing_compatibility(tmp_path: Path) -> None:
    export_path = _example_export(tmp_path)
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    del payload["compatibility"]
    bad_path = tmp_path / "missing-compatibility.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_export_file(bad_path)

    assert report["status"] == "FAIL"
    assert "schema" in report["release_gate"]["blocking_failures"]


def test_validate_export_accepts_consumer_contract_with_warnings(tmp_path: Path) -> None:
    result = RUNNER.invoke(app, ["example", "--output-dir", str(tmp_path)])
    assert result.exit_code == 0
    contract_path = tmp_path / "human-cli.consumer.json"

    report = validate_export_file(contract_path)

    assert report["status"] == "PASS"
    assert any(check["name"] == "consumer_contract" for check in report["checks"])


def test_diff_reports_comparable_for_identical_exports(tmp_path: Path) -> None:
    baseline = _example_export(tmp_path / "a")
    candidate = _example_export(tmp_path / "b")

    report = compare_export_files(baseline, candidate)

    assert report["comparability"]["state"] == "COMPARABLE"
    assert report["drift"]["kinds"] == []
    assert report["drift"]["implementation_drift_reported_as_expression"] is False


def test_diff_detects_version_drift_without_expression_overclaim(tmp_path: Path) -> None:
    baseline = _example_export(tmp_path / "a")
    candidate = _example_export(tmp_path / "b")
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    payload["profile"]["build_manifest"]["extractor_minor_version"] = 2
    payload["profile"]["build_manifest"]["extractor_code_version"] = "sprint12-mutated"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    report = compare_export_files(baseline, candidate)

    assert report["comparability"]["state"] == "PARTIALLY_COMPARABLE"
    assert "compiler_drift" in report["drift"]["kinds"]
    assert report["drift"]["implementation_drift_reported_as_expression"] is False
    assert report["release_gate"]["status"] == "WARN"
    assert "partially_comparable" in report["release_gate"]["reason_codes"]


def test_diff_flags_mixed_classifier_versions_as_review_required(tmp_path: Path) -> None:
    baseline = _example_export(tmp_path / "a")
    candidate = _example_export(tmp_path / "b")
    for path in (baseline, candidate):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["profile"]["build_manifest"]["classifier_version"] = "classifier-v1,classifier-v2"
        payload["compatibility"]["classifier_versions"] = ["classifier-v1", "classifier-v2"]
        path.write_text(json.dumps(payload), encoding="utf-8")

    report = compare_export_files(baseline, candidate)

    assert report["comparability"]["state"] == "PARTIALLY_COMPARABLE"
    assert "mixed_classifier_versions" in report["comparability"]["reasons"]
    assert report["comparability"]["version_metadata"]["mixed_classifier_versions"] is True
    assert report["release_gate"]["status"] == "WARN"
    assert "mixed_classifier_versions" in report["release_gate"]["reason_codes"]


def test_diff_marks_corpus_change_not_comparable(tmp_path: Path) -> None:
    baseline = _example_export(tmp_path / "a")
    candidate = _example_export(tmp_path / "b")
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    payload["profile"]["build_manifest"]["config_hash"] = "different-corpus"
    candidate.write_text(json.dumps(payload), encoding="utf-8")

    report = compare_export_files(baseline, candidate)

    assert report["comparability"]["state"] == "NOT_COMPARABLE"
    assert "corpus_drift" in report["drift"]["kinds"]
    assert report["drift"]["expression_drift_reported"] is False


def test_quality_cli_commands_smoke(tmp_path: Path) -> None:
    baseline = _example_export(tmp_path / "a")
    candidate = _example_export(tmp_path / "b")

    validate_result = RUNNER.invoke(app, ["validate-export", str(baseline)])
    diff_result = RUNNER.invoke(app, ["diff", str(baseline), str(candidate)])

    assert validate_result.exit_code == 0
    assert '"status": "PASS"' in validate_result.output
    assert diff_result.exit_code == 0
    assert '"state": "COMPARABLE"' in diff_result.output
