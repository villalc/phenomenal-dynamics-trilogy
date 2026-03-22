from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .shadow_bridge import ShadowDecisionBridge, phenomenal_to_shadow_metrics
from .shadow_manifest import write_manifest
from .shadow_models import ShadowDecision, ShadowRunManifest, ShadowSignal
from .shadow_window import DecisionWindowState


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _as_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return default


def _as_int(value: object, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return default


def _as_dict(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return value
    return {}


def _as_list(value: object) -> list[object]:
    if isinstance(value, list):
        return value
    return []


def _pick_float(summary: dict[str, object], keys: list[str], default: float = 0.0) -> float:
    for key in keys:
        if key in summary:
            return _as_float(summary.get(key), default)
    return default


def _pick_int(summary: dict[str, object], keys: list[str], default: int = 0) -> int:
    for key in keys:
        if key in summary:
            return _as_int(summary.get(key), default)
    return default


def _mode_from_summary(*, stress: float, resonance: float, canonical: int, sleep_debt: float) -> str:
    if canonical > 0 and stress <= 0.45:
        return "CANONICAL_READY"
    if sleep_debt >= 0.25 or stress >= 0.70:
        return "STRESSED"
    if resonance >= 0.75 and stress <= 0.40:
        return "FLOW"
    return "STABLE"


def _extract_run_contexts(payload: dict[str, object], artifact_stem: str) -> list[dict[str, object]]:
    contexts: list[dict[str, object]] = []

    runs = _as_list(payload.get("runs"))
    for idx, item in enumerate(runs, start=1):
        run = _as_dict(item)
        contexts.append(
            {
                "schema": "runs",
                "artifact": artifact_stem,
                "index": idx,
                "profile": str(run.get("seed_name", "shadow")),
                "summary": _as_dict(run.get("summary")),
                "run": run,
            }
        )

    variants = _as_list(payload.get("variants"))
    for variant in variants:
        variant_map = _as_dict(variant)
        variant_name = str(variant_map.get("variant", "variant"))
        nested_runs = _as_list(variant_map.get("runs"))
        for idx, item in enumerate(nested_runs, start=1):
            run = _as_dict(item)
            contexts.append(
                {
                    "schema": "variants",
                    "artifact": artifact_stem,
                    "index": idx,
                    "profile": variant_name,
                    "summary": _as_dict(run.get("summary")),
                    "run": run,
                }
            )

    profiles = _as_list(payload.get("profiles"))
    for profile in profiles:
        profile_map = _as_dict(profile)
        profile_name = str(profile_map.get("profile", "profile"))
        nested_runs = _as_list(profile_map.get("runs"))
        for idx, item in enumerate(nested_runs, start=1):
            run = _as_dict(item)
            contexts.append(
                {
                    "schema": "profiles",
                    "artifact": artifact_stem,
                    "index": idx,
                    "profile": profile_name,
                    "summary": _as_dict(run.get("summary")),
                    "run": run,
                }
            )

    return contexts


def _build_manifest_from_context(
    context: dict[str, object],
    source_file: Path,
    *,
    window_state: DecisionWindowState | None = None,
) -> ShadowRunManifest:
    summary = _as_dict(context.get("summary"))
    run = _as_dict(context.get("run"))

    reward = _pick_float(summary, ["reward_score", "continuity_score", "attractor_strength", "final_coherence"], 0.5)
    risk = _pick_float(summary, ["risk_score", "attack_energy_mean"], 0.0)
    integrity = _pick_float(summary, ["final_integrity"], 1.0)
    sleep_debt = _pick_float(summary, ["sleep_debt_final", "final_sleep_debt", "final_debt"], 0.0)
    canonical = _pick_int(summary, ["canonical_stable_seeds", "canonical_seed_count", "canonical_promotions"], 0)
    exploratory = _pick_int(summary, ["exploratory_stable_seeds", "exploratory_seed_count", "exploratory_promotions"], 0)

    stress = _clamp(risk if risk > 0 else (sleep_debt * 2.0) + max(0.0, 1.0 - integrity))
    resonance = _clamp(reward)
    mode = _mode_from_summary(stress=stress, resonance=resonance, canonical=canonical, sleep_debt=sleep_debt)

    profile = str(context.get("profile", "shadow"))
    artifact = str(context.get("artifact", source_file.stem))
    index = _as_int(context.get("index"), 1)
    run_id = f"{artifact}:{profile}:run-{index}"

    manifest = ShadowRunManifest(
        run_id=run_id,
        profile=profile,
        experiment=artifact,
        metadata={
            "source_artifact": str(source_file),
            "schema": str(context.get("schema", "unknown")),
            "run_index": str(run.get("run_index", index)),
        },
    )

    cycle = _as_int(run.get("cycles"), index)
    signal = ShadowSignal(
        run_id=run_id,
        cycle=cycle,
        integrity=round(_clamp(integrity), 4),
        stress=round(stress, 4),
        resonance=round(resonance, 4),
        sleep_debt=round(_clamp(sleep_debt), 4),
        canonical_promotions=canonical,
        exploratory_promotions=exploratory,
        mode=mode,
        note=f"ingested:{artifact}",
    )
    manifest.add_signal(signal)

    continuity = _pick_float(summary, ["continuity_score"], 0.0)
    trauma_memory = _clamp(1.0 - continuity) if continuity > 0 else 0.0
    metrics = phenomenal_to_shadow_metrics(
        integrity=signal.integrity,
        stress=signal.stress,
        resonance=signal.resonance,
        trauma_memory=trauma_memory,
        flourishing=0.2 if canonical > 0 else 0.0,
    )

    bridge = ShadowDecisionBridge(source="frontier-ingest", policy_name="conservative", window_state=window_state)
    action, reason, confidence = bridge.recommend_action_for_cycle(run_id=run_id, cycle=cycle, metrics=metrics)
    manifest.add_decision(
        ShadowDecision(
            run_id=run_id,
            cycle=cycle,
            action=action,
            reason=reason,
            confidence=confidence,
        )
    )

    return manifest


def ingest_frontier_artifact(file_path: Path, output_dir: Path | None = None) -> list[Path]:
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    contexts = _extract_run_contexts(_as_dict(payload), file_path.stem)
    window_state = DecisionWindowState()

    written: list[Path] = []
    for context in contexts:
        manifest = _build_manifest_from_context(context, file_path, window_state=window_state)
        target = write_manifest(manifest, output_dir=output_dir)
        written.append(target)
    return written


def ingest_frontier_directory(artifact_dir: Path, output_dir: Path | None = None, pattern: str = "Frontier*.json") -> list[Path]:
    outputs: list[Path] = []
    for artifact in sorted(artifact_dir.glob(pattern)):
        if artifact.is_file():
            outputs.extend(ingest_frontier_artifact(artifact, output_dir=output_dir))
    return outputs
