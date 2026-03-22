import json
from pathlib import Path

from src.swarmguard.shadow_export_pack import build_export_pack
from src.swarmguard.shadow_manifest import write_manifest
from src.swarmguard.shadow_models import ShadowDecision, ShadowRunManifest, ShadowSignal


def _manifest(run_id: str) -> ShadowRunManifest:
    manifest = ShadowRunManifest(run_id=run_id, profile="frontier", experiment="demo")
    manifest.add_signal(
        ShadowSignal(
            run_id=run_id,
            cycle=1,
            integrity=0.9,
            stress=0.2,
            resonance=0.7,
            sleep_debt=0.04,
            canonical_promotions=1,
            exploratory_promotions=2,
            mode="FLOW",
        )
    )
    manifest.add_decision(
        ShadowDecision(
            run_id=run_id,
            cycle=1,
            action="promote_canonical",
            reason="ready",
            confidence=0.8,
        )
    )
    return manifest


def test_build_export_pack_creates_index_and_summary(tmp_path: Path) -> None:
    manifest_dir = tmp_path / "manifests"
    output_root = tmp_path / "packs"
    manifest_dir.mkdir(parents=True)

    write_manifest(_manifest("run-a"), output_dir=manifest_dir)
    write_manifest(_manifest("run-b"), output_dir=manifest_dir)

    result = build_export_pack(manifest_dir=manifest_dir, output_root=output_root, pack_name="pack-a")

    assert result["manifest_count"] == 2
    assert result["invalid_count"] == 0

    index_file = Path(str(result["index_file"]))
    executive_file = Path(str(result["executive_file"]))
    assert index_file.exists()
    assert executive_file.exists()

    payload = json.loads(index_file.read_text(encoding="utf-8"))
    assert payload["manifest_count"] == 2
    assert payload["summary"]["total_manifests"] == 2
    assert payload["validation_errors"] == {}
