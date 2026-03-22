from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from swarmguard.shadow_export_pack import build_export_pack


def main() -> int:
    parser = argparse.ArgumentParser(description="Build portable Shadow export pack")
    parser.add_argument(
        "--manifest-dir",
        default=str(PROJECT_ROOT / "data" / "shadow_exports" / "frontier_ingest"),
        help="Directory containing shadow manifest json files",
    )
    parser.add_argument(
        "--output-root",
        default=str(PROJECT_ROOT / "data" / "shadow_exports" / "packs"),
        help="Directory where the pack folder will be created",
    )
    parser.add_argument("--pack-name", default="shadow_pack_latest", help="Name of generated pack folder")
    args = parser.parse_args()

    manifest_dir = Path(args.manifest_dir)
    output_root = Path(args.output_root)

    if not manifest_dir.exists():
        print(f"Manifest directory not found: {manifest_dir}")
        return 1

    result = build_export_pack(manifest_dir=manifest_dir, output_root=output_root, pack_name=args.pack_name)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
