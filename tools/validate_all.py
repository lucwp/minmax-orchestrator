#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTIONS = [
    ROOT / "minmax-orchestrator-next",
    ROOT / "minmax-orchestrator-luna",
    ROOT / "minmax-orchestrator-sonnet",
]


def run_distribution(path: Path) -> bool:
    print(f"\n==> validating {path.name}")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=path,
        text=True,
    )
    if proc.returncode == 5:
        print(f"FAIL: {path.name} collected zero tests", file=sys.stderr)
        return False
    if proc.returncode != 0:
        print(f"FAIL: {path.name} pytest exit={proc.returncode}", file=sys.stderr)
        return False
    return True


def main() -> int:
    missing = [str(p) for p in DISTRIBUTIONS if not (p / "SKILL.md").is_file()]
    if missing:
        print("FAIL: missing distribution entrypoints: " + ", ".join(missing), file=sys.stderr)
        return 1
    ok = all(run_distribution(path) for path in DISTRIBUTIONS)
    print("\nRESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
