from src.swarmguard.shadow_manifest import read_manifest, write_manifest
from src.swarmguard.shadow_models import ShadowDecision, ShadowRunManifest, ShadowSignal


def test_manifest_roundtrip(tmp_path) -> None:
    manifest = ShadowRunManifest(
        run_id="run-shadow-01",
        profile="frontier",
        experiment="v4_shadow_alignment",
        metadata={"source": "local-copy"},
    )
    manifest.add_signal(
        ShadowSignal(
            run_id="run-shadow-01",
            cycle=1,
            integrity=0.87,
            stress=0.25,
            resonance=0.66,
            sleep_debt=0.08,
            canonical_promotions=1,
            exploratory_promotions=2,
            mode="FLOW",
        )
    )
    manifest.add_decision(
        ShadowDecision(
            run_id="run-shadow-01",
            cycle=1,
            action="promote_canonical",
            reason="readiness high and risk controlled",
            confidence=0.83,
        )
    )

    output = write_manifest(manifest, output_dir=tmp_path, file_name="manifest.json")
    loaded = read_manifest(output)

    assert loaded.run_id == "run-shadow-01"
    assert loaded.profile == "frontier"
    assert len(loaded.signals) == 1
    assert len(loaded.decisions) == 1
    assert loaded.summary()["signals"] == 1
