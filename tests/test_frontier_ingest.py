import json
from pathlib import Path

from src.swarmguard.frontier_ingest import ingest_frontier_artifact
from src.swarmguard.shadow_manifest import read_manifest


def _write_json(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    return path


def test_ingest_runs_schema(tmp_path: Path) -> None:
    artifact = _write_json(
        tmp_path / "Frontier_runs_report.json",
        {
            "runs": [
                {
                    "run_index": 1,
                    "cycles": 2500,
                    "seed_name": "seed-1",
                    "summary": {
                        "reward_score": 0.7,
                        "risk_score": 0.2,
                        "final_integrity": 0.95,
                        "sleep_debt_final": 0.04,
                        "canonical_stable_seeds": 1,
                        "exploratory_stable_seeds": 2,
                    },
                }
            ]
        },
    )

    outputs = ingest_frontier_artifact(artifact, output_dir=tmp_path)

    assert len(outputs) == 1
    manifest = read_manifest(outputs[0])
    assert manifest.profile == "seed-1"
    assert manifest.experiment == "Frontier_runs_report"
    assert len(manifest.signals) == 1
    assert len(manifest.decisions) == 1


def test_ingest_variants_schema(tmp_path: Path) -> None:
    artifact = _write_json(
        tmp_path / "Frontier_variants_report.json",
        {
            "variants": [
                {
                    "variant": "v2.9shadow",
                    "runs": [
                        {
                            "run_index": 1,
                            "summary": {
                                "reward_score": 0.5,
                                "risk_score": 0.3,
                                "final_integrity": 0.9,
                                "sleep_debt_final": 0.06,
                            },
                        }
                    ],
                }
            ]
        },
    )

    outputs = ingest_frontier_artifact(artifact, output_dir=tmp_path)

    assert len(outputs) == 1
    manifest = read_manifest(outputs[0])
    assert manifest.profile == "v2.9shadow"
    assert manifest.metadata["schema"] == "variants"


def test_ingest_profiles_schema(tmp_path: Path) -> None:
    artifact = _write_json(
        tmp_path / "Frontier_profiles_report.json",
        {
            "profiles": [
                {
                    "profile": "intentional-collapse",
                    "runs": [
                        {
                            "run_index": 1,
                            "summary": {
                                "continuity_score": 0.52,
                                "final_integrity": 0.61,
                                "final_sleep_debt": 0.29,
                            },
                        }
                    ],
                }
            ]
        },
    )

    outputs = ingest_frontier_artifact(artifact, output_dir=tmp_path)

    assert len(outputs) == 1
    manifest = read_manifest(outputs[0])
    assert manifest.profile == "intentional-collapse"
    assert manifest.metadata["schema"] == "profiles"
    assert manifest.signals[0].mode in {"STABLE", "STRESSED", "FLOW", "CANONICAL_READY"}
