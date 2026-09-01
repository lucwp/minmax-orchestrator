#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "minmax-orchestrator-next"
DST = ROOT / "minmax-orchestrator-luna"
IDENTITY = json.loads((ROOT / "variants" / "luna" / "identity.json").read_text(encoding="utf-8"))


def replace_required(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"FAIL: expected Luna materialization source text missing in {path}: {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not (SRC / "SKILL.md").is_file():
        raise SystemExit("FAIL: NEXT distribution is missing")
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    next_slug = IDENTITY["upstream_skill_name"]
    luna_slug = IDENTITY["skill_name"]
    next_name = IDENTITY["upstream_display_name"]
    luna_name = IDENTITY["display_name"]

    replace_required(DST / "SKILL.md", [
        (f"name: {next_slug}", f"name: {luna_slug}"),
        ('description: "Next-generation workspace-level manager/orchestrator', 'description: "Luna-specific workspace-level manager/orchestrator'),
        (f"# {next_name}", f"# {luna_name}"),
    ])
    replace_required(DST / "agents" / "openai.yaml", [
        (f"display_name: {next_name}", f"display_name: {luna_name}"),
    ])
    replace_required(DST / "references" / "loop-mode.md", [
        (f"{next_name} remains the root control plane", f"{luna_name} remains the root control plane"),
    ])
    replace_required(DST / "references" / "workspace-integration.md", [
        (next_slug, luna_slug),
        (next_name, luna_name),
    ])

    skill_text = (DST / "SKILL.md").read_text(encoding="utf-8")
    if f"name: {luna_slug}" not in skill_text or f"# {luna_name}" not in skill_text:
        raise SystemExit("FAIL: Luna identity was not materialized")
    print("PASS: materialized Luna from NEXT plus declared identity delta")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
