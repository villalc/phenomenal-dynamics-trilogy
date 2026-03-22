from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from swarmguard.frontier_ingest import ingest_frontier_directory


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Frontier artifacts into Shadow manifests")
    parser.add_argument("--artifact-dir", default=str(PROJECT_ROOT.parent / "artifacts"), help="Directory containing Frontier JSON artifacts")
    parser.add_argument("--output-dir", default=str(PROJECT_ROOT / "data" / "shadow_exports" / "frontier_ingest"), help="Directory to write generated manifests")
    parser.add_argument("--pattern", default="Frontier*.json", help="Glob pattern for artifacts")
    args = parser.parse_args()

    artifact_dir = Path(args.artifact_dir)
    output_dir = Path(args.output_dir)

    if not artifact_dir.exists():
        print(f"Artifact directory not found: {artifact_dir}")
        return 1

    written = ingest_frontier_directory(artifact_dir=artifact_dir, output_dir=output_dir, pattern=args.pattern)
    payload = {
        "artifact_dir": str(artifact_dir),
        "output_dir": str(output_dir),
        "generated_manifests": len(written),
        "files": [str(path) for path in written],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
