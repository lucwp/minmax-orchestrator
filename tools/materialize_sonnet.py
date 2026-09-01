#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "minmax-orchestrator-luna"
DST = ROOT / "minmax-orchestrator-sonnet"
VARIANT = ROOT / "variants" / "sonnet"
IDENTITY = json.loads((VARIANT / "identity.json").read_text(encoding="utf-8"))


def replace_required(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"FAIL: expected source text missing in {path}: {old!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not (SRC / "SKILL.md").is_file():
        raise SystemExit("FAIL: stable Luna distribution is missing")

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    luna_slug = IDENTITY["stable_base_skill_name"]
    sonnet_slug = IDENTITY["skill_name"]
    luna_name = IDENTITY["stable_base_display_name"]
    sonnet_name = IDENTITY["display_name"]

    replace_required(DST / "SKILL.md", [
        (f"name: {luna_slug}", f"name: {sonnet_slug}"),
        ('description: "Luna-specific workspace-level manager/orchestrator', 'description: "Claude Sonnet-specific workspace-level manager/orchestrator'),
        (f"# {luna_name}", f"# {sonnet_name}"),
        ('- Model selection/escalation -> `references/model-routing.md`.', '- Anthropic model selection, effort calibration, advisor use, or escalation -> `references/model-routing.md`.'),
    ])
    replace_required(DST / "agents" / "openai.yaml", [
        (f"display_name: {luna_name}", f"display_name: {sonnet_name}"),
    ])
    replace_required(DST / "references" / "loop-mode.md", [
        (f"{luna_name} remains the root control plane", f"{sonnet_name} remains the root control plane"),
    ])
    replace_required(DST / "references" / "workspace-integration.md", [
        (luna_slug, sonnet_slug),
        (luna_name, sonnet_name),
    ])

    skill = DST / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    old = '''## Model routing summary

Use capability per node, not project prestige. Load `references/model-routing.md` for details.

Default principles:
- current/root or economical model for trivial/mechanical work;
- normal substantive model for bounded workers;
- stronger reasoning only for genuinely hard, narrow planning/reasoning nodes;
- capability/coordination escalation only after context/scope/tool/validation failures are repaired;
- strongest critic only for narrow high-consequence judgment.

Do not claim model-specific routing occurred when runtime controls do not expose it.
'''
    new = '''## Model routing summary

Use a **Sonnet-first, effort-first, model-switch-last** policy. Keep Claude Sonnet as the default substantive/root model and use supported `effort` levels inside Sonnet as the primary capability ladder. Load `references/model-routing.md` for the current stable routing policy.

Default Anthropic policy:
- **Claude Sonnet 5** stays root/workhorse for substantive execution, planning, tool use, coding, research, synthesis, and most agentic loops; choose the lowest supported Sonnet effort likely to complete the node reliably;
- **Claude Haiku 4.5** is a specialized economical offload for mechanical, high-volume, low-latency, or cheaply verified bounded work, not the first reasoning rung;
- **Claude Opus 5** is a narrow advisor/escalation for load-bearing reasoning or judgment when Sonnet plus appropriate effort is insufficient or the expected failure reduction justifies the premium;
- **Claude Fable 5** is a last-resort frontier path for exceptional nodes where Opus is insufficient and the expected lift justifies the added cost;
- **Claude Mythos 5** is never a required dependency or normal routing tier because general access is restricted.

Before switching models, repair context/scope/tool/verification problems and raise supported Sonnet effort when reasoning depth is the likely bottleneck. If Anthropic's Advisor tool is exposed, prefer a narrow Opus/Fable consultation over replacing the Sonnet executor when that is cheaper and sufficient.

Do not claim model routing, effort control, Advisor use, or model switching occurred when the runtime does not expose those controls.
'''
    if old not in text:
        raise SystemExit("FAIL: generic model-routing summary missing")
    skill.write_text(text.replace(old, new), encoding="utf-8")

    shutil.copy2(VARIANT / "model-routing.md", DST / "references" / "model-routing.md")
    shutil.copy2(VARIANT / "test_anthropic_model_routing.py", DST / "tests" / "test_anthropic_model_routing.py")

    reliability_path = DST / "reliability.json"
    reliability = json.loads(reliability_path.read_text(encoding="utf-8"))
    reliability.setdefault("controls", {})["anthropic_model_routing"] = {
        "status": "implemented",
        "evidence": ["references/model-routing.md", "tests/test_anthropic_model_routing.py", "SKILL.md"],
    }
    tests = reliability.setdefault("tests", [])
    if "tests/test_anthropic_model_routing.py" not in tests:
        tests.append("tests/test_anthropic_model_routing.py")
    reliability_path.write_text(json.dumps(reliability, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for cache in list(DST.rglob("__pycache__")) + list(DST.rglob(".pytest_cache")):
        if cache.is_dir():
            shutil.rmtree(cache)

    skill_text = skill.read_text(encoding="utf-8")
    if f"name: {sonnet_slug}" not in skill_text or f"# {sonnet_name}" not in skill_text:
        raise SystemExit("FAIL: Sonnet identity was not materialized")

    print("PASS: materialized Sonnet from stable Luna baseline plus Anthropic deltas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
