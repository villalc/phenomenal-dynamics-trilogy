from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Any

from .shadow_manifest import read_manifest
from .shadow_validate import validate_manifest_payload


PACK_SCHEMA_VERSION = "1.0"


def _as_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return default


def collect_manifest_files(manifest_dir: Path) -> list[Path]:
    return sorted(path for path in manifest_dir.glob("*_shadow_manifest.json") if path.is_file())


def _aggregate(manifest_payloads: list[dict[str, object]]) -> dict[str, object]:
    total = len(manifest_payloads)
    profiles: dict[str, int] = {}
    experiments: dict[str, int] = {}
    integrity_values: list[float] = []
    sleep_debt_values: list[float] = []

    for payload in manifest_payloads:
        profile = str(payload.get("profile", "unknown"))
        experiment = str(payload.get("experiment", "unknown"))
        profiles[profile] = profiles.get(profile, 0) + 1
        experiments[experiment] = experiments.get(experiment, 0) + 1

        summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
        integrity_values.append(_as_float(summary.get("integrity_mean"), 0.0))
        sleep_debt_values.append(_as_float(summary.get("sleep_debt_mean"), 0.0))

    integrity_mean = sum(integrity_values) / total if total else 0.0
    sleep_debt_mean = sum(sleep_debt_values) / total if total else 0.0

    top_profiles = sorted(profiles.items(), key=lambda item: item[1], reverse=True)
    top_experiments = sorted(experiments.items(), key=lambda item: item[1], reverse=True)

    return {
        "total_manifests": total,
        "integrity_mean": round(integrity_mean, 4),
        "sleep_debt_mean": round(sleep_debt_mean, 4),
        "profiles": profiles,
        "experiments": experiments,
        "top_profiles": top_profiles[:10],
        "top_experiments": top_experiments[:10],
    }


def _build_executive_markdown(summary: dict[str, object], validation_errors: dict[str, list[str]]) -> str:
    lines: list[str] = []
    lines.append("# Shadow Export Pack")
    lines.append("")
    lines.append(f"- schema_version: {PACK_SCHEMA_VERSION}")
    lines.append(f"- total_manifests: {int(summary.get('total_manifests', 0))}")
    lines.append(f"- integrity_mean: {float(summary.get('integrity_mean', 0.0)):.4f}")
    lines.append(f"- sleep_debt_mean: {float(summary.get('sleep_debt_mean', 0.0)):.4f}")
    lines.append("")

    lines.append("## Top Profiles")
    for profile, count in summary.get("top_profiles", []):
        lines.append(f"- {profile}: {count}")
    if not summary.get("top_profiles"):
        lines.append("- none")
    lines.append("")

    lines.append("## Top Experiments")
    for experiment, count in summary.get("top_experiments", []):
        lines.append(f"- {experiment}: {count}")
    if not summary.get("top_experiments"):
        lines.append("- none")
    lines.append("")

    lines.append("## Validation")
    if validation_errors:
        lines.append(f"- invalid_manifests: {len(validation_errors)}")
        for file_name, errors in sorted(validation_errors.items()):
            lines.append(f"- {file_name}: {', '.join(errors)}")
    else:
        lines.append("- all_manifests_valid")

    return "\n".join(lines) + "\n"


def build_export_pack(
    *,
    manifest_dir: Path,
    output_root: Path,
    pack_name: str = "shadow_pack",
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    pack_dir = output_root / pack_name
    manifests_dir = pack_dir / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    manifest_files = collect_manifest_files(manifest_dir)
    payloads: list[dict[str, object]] = []
    validation_errors: dict[str, list[str]] = {}
    copied_files: list[str] = []

    for manifest_file in manifest_files:
        destination = manifests_dir / manifest_file.name
        shutil.copy2(manifest_file, destination)
        copied_files.append(str(destination))

        payload = read_manifest(manifest_file).to_dict()
        payloads.append(payload)
        errors = validate_manifest_payload(payload)
        if errors:
            validation_errors[manifest_file.name] = errors

    summary = _aggregate(payloads)

    index_payload: dict[str, Any] = {
        "schema_version": PACK_SCHEMA_VERSION,
        "pack_name": pack_name,
        "source_manifest_dir": str(manifest_dir),
        "manifest_count": len(payloads),
        "summary": summary,
        "validation_errors": validation_errors,
        "files": copied_files,
    }

    index_file = pack_dir / "pack_index.json"
    index_file.write_text(json.dumps(index_payload, indent=2, ensure_ascii=True), encoding="utf-8")

    executive = _build_executive_markdown(summary, validation_errors)
    executive_file = pack_dir / "executive_summary.md"
    executive_file.write_text(executive, encoding="utf-8")

    return {
        "pack_dir": str(pack_dir),
        "index_file": str(index_file),
        "executive_file": str(executive_file),
        "manifest_count": len(payloads),
        "invalid_count": len(validation_errors),
    }
