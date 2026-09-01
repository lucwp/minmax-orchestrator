import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evidence_plan.py"
spec = importlib.util.spec_from_file_location("validate_evidence_plan", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def plan(claim):
    return {"schema_version": "1.0", "claims": [claim]}


def evidence(kind, source="source"):
    item = {"type": kind}
    if kind != "same_model_feedback":
        item["source"] = source
    return item


def base_claim(domain, status="PASS", available=True, ev=None, terminal=True, limitations=None):
    return {
        "id": "c1",
        "truth_domain": domain,
        "terminal": terminal,
        "status": status,
        "matching_evidence_reasonably_available": available,
        "evidence": ev or [],
        "limitations": limitations or [],
    }


def test_external_world_claim_with_authoritative_external_evidence_passes():
    c = base_claim("external_world", ev=[evidence("authoritative_external", "primary source")])
    assert mod.validate(plan(c)) == []


def test_external_world_claim_cannot_pass_on_same_model_feedback():
    c = base_claim("external_world", ev=[evidence("same_model_feedback")])
    errors = mod.validate(plan(c))
    assert any("external-world PASS requires" in e for e in errors)
    assert any("terminal PASS cannot rely only" in e for e in errors)


def test_unavailable_external_evidence_requires_uncertainty_and_limitation():
    c = base_claim(
        "external_world",
        status="UNCERTAIN",
        available=False,
        ev=[evidence("same_model_feedback")],
        limitations=["No authoritative external source or grounded tool is available in this runtime."],
    )
    assert mod.validate(plan(c)) == []


def test_unavailable_external_evidence_cannot_be_silently_upgraded_to_pass():
    c = base_claim(
        "external_world",
        status="PASS",
        available=False,
        ev=[evidence("independent_reviewer", "reviewer")],
        limitations=["External evidence unavailable."],
    )
    errors = mod.validate(plan(c))
    assert any("external-world PASS requires" in e for e in errors)


def test_deterministic_claim_prefers_direct_test_over_external_research():
    good = base_claim("deterministic_result", ev=[evidence("deterministic_test", "pytest")])
    assert mod.validate(plan(good)) == []
    bad = base_claim("deterministic_result", ev=[evidence("authoritative_external", "article")])
    errors = mod.validate(plan(bad))
    assert any("matching evidence is required for deterministic_result" in e for e in errors)


def test_normal_and_loop_verification_paths_share_external_evidence_policy():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
    loop = (ROOT / "references" / "loop-mode.md").read_text(encoding="utf-8").lower()
    contracts = (ROOT / "references" / "assignment-contracts.md").read_text(encoding="utf-8").lower()
    policy = (ROOT / "references" / "verification-evidence.md").read_text(encoding="utf-8").lower()
    assert "match evidence to the truth being claimed" in skill
    assert "authoritative external evidence" in skill
    assert "external-world claim" in loop and "terminal pass" in loop
    assert "external-world claims" in contracts and "uncertain" in contracts
    assert "claim type -> strongest reasonably available matching evidence" in policy


def test_same_model_feedback_is_auxiliary_across_policy_surfaces():
    for path in [
        ROOT / "SKILL.md",
        ROOT / "references" / "verification-evidence.md",
        ROOT / "references" / "loop-mode.md",
        ROOT / "references" / "assignment-contracts.md",
    ]:
        text = path.read_text(encoding="utf-8").lower()
        assert "same-model" in text
    assert "auxiliary" in (ROOT / "references" / "verification-evidence.md").read_text(encoding="utf-8").lower()


def test_reliability_records_claim_evidence_control():
    reliability = json.loads((ROOT / "reliability.json").read_text(encoding="utf-8"))
    control = reliability["controls"]["claim_evidence_matching"]
    assert control["status"] == "implemented"
    assert "scripts/validate_evidence_plan.py" in control["evidence"]
