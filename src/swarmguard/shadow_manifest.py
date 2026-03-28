"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .shadow_models import ShadowDecision, ShadowRunManifest, ShadowSignal


def _safe_file_name(value: str) -> str:
    # Replace '..' with '__' to prevent path traversal
    cleaned = value.replace("..", "__")
    # Restrict to alphanumeric, underscore, and hyphen
    cleaned = re.sub(r"[^a-zA-Z0-9_\-]", "_", cleaned)
    return cleaned


def exports_root(base_dir: Path | None = None) -> Path:
    root = base_dir or Path(__file__).resolve().parents[2] / "data" / "shadow_exports"
    root.mkdir(parents=True, exist_ok=True)
    return root


def write_manifest(manifest: ShadowRunManifest, output_dir: Path | None = None, file_name: str | None = None) -> Path:
    destination_dir = exports_root(output_dir)
    target_name = file_name or f"{_safe_file_name(manifest.run_id)}_shadow_manifest.json"
    destination = destination_dir / target_name
    destination.write_text(json.dumps(manifest.to_dict(), indent=2, ensure_ascii=True), encoding="utf-8")
    return destination


def _signal_from_dict(payload: dict[str, Any]) -> ShadowSignal:
    return ShadowSignal(
        run_id=str(payload.get("run_id", "")),
        cycle=int(payload.get("cycle", 0)),
        integrity=float(payload.get("integrity", 0.0)),
        stress=float(payload.get("stress", 0.0)),
        resonance=float(payload.get("resonance", 0.0)),
        sleep_debt=float(payload.get("sleep_debt", 0.0)),
        canonical_promotions=int(payload.get("canonical_promotions", 0)),
        exploratory_promotions=int(payload.get("exploratory_promotions", 0)),
        mode=str(payload.get("mode", "")),
        note=str(payload.get("note", "")),
        timestamp=str(payload.get("timestamp", "")),
    )


def _decision_from_dict(payload: dict[str, Any]) -> ShadowDecision:
    return ShadowDecision(
        run_id=str(payload.get("run_id", "")),
        cycle=int(payload.get("cycle", 0)),
        action=str(payload.get("action", "")),
        reason=str(payload.get("reason", "")),
        confidence=float(payload.get("confidence", 0.0)),
        timestamp=str(payload.get("timestamp", "")),
    )


def read_manifest(file_path: Path) -> ShadowRunManifest:
    payload = json.loads(file_path.read_text(encoding="utf-8"))

    manifest = ShadowRunManifest(
        run_id=str(payload.get("run_id", "")),
        profile=str(payload.get("profile", "")),
        experiment=str(payload.get("experiment", "")),
        created_at=str(payload.get("created_at", "")),
        metadata={str(key): str(value) for key, value in dict(payload.get("metadata", {})).items()},
    )

    for row in payload.get("signals", []):
        if isinstance(row, dict):
            manifest.add_signal(_signal_from_dict(row))

    for row in payload.get("decisions", []):
        if isinstance(row, dict):
            manifest.add_decision(_decision_from_dict(row))

    return manifest
