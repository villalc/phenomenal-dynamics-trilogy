from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sign_pack(pack_dir: Path, *, output_file: str = "pack_signatures.json") -> Path:
    manifests_dir = pack_dir / "manifests"
    files = []

    if manifests_dir.exists():
        for item in sorted(manifests_dir.glob("*.json")):
            files.append(item)

    for item in [pack_dir / "pack_index.json", pack_dir / "executive_summary.md"]:
        if item.exists():
            files.append(item)

    payload: dict[str, Any] = {
        "pack_dir": str(pack_dir),
        "algorithm": "sha256",
        "files": [],
    }

    for file_path in files:
        payload["files"].append(
            {
                "file": str(file_path.relative_to(pack_dir)),
                "sha256": _sha256_file(file_path),
            }
        )

    destination = pack_dir / output_file
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    return destination
