from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from swarmguard.shadow_signing import sign_pack


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SHA-256 signatures for a Shadow export pack")
    parser.add_argument("--pack-dir", required=True, help="Path to pack directory containing pack_index.json")
    parser.add_argument("--output-file", default="pack_signatures.json", help="Output signature file name")
    args = parser.parse_args()

    pack_dir = Path(args.pack_dir)
    if not pack_dir.exists():
        print(f"Pack directory not found: {pack_dir}")
        return 1

    destination = sign_pack(pack_dir, output_file=args.output_file)
    print(json.dumps({"signature_file": str(destination)}, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
