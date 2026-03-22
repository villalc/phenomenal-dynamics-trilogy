from pathlib import Path

from src.swarmguard.shadow_signing import sign_pack


def test_sign_pack_creates_hash_file(tmp_path: Path) -> None:
    pack_dir = tmp_path / "pack"
    manifests = pack_dir / "manifests"
    manifests.mkdir(parents=True)

    (pack_dir / "pack_index.json").write_text("{}", encoding="utf-8")
    (pack_dir / "executive_summary.md").write_text("# demo\n", encoding="utf-8")
    (manifests / "m1.json").write_text("{\"a\":1}", encoding="utf-8")

    output = sign_pack(pack_dir)

    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "sha256" in content
    assert "pack_index.json" in content
    assert "manifests/m1.json" in content.replace("\\\\", "/")
