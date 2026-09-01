#!/usr/bin/env python3
import argparse
import json
import math
import re
from pathlib import Path
SCHEMA_VERSION="1.0";REGIMES={"fixed_sequential","hierarchical_adaptive","reactive_stepwise","deliberative_search","solver_assisted"};OBSERVABILITY={"full","partial","dynamic"};FEASIBILITY={"solvable","conditional","needs_discovery","blocked","unsatisfiable"};EFFECTS={"read_only","reversible_write","external_write","irreversible_high_consequence"};EXECUTABLE_FEASIBILITY={"solvable","conditional","needs_discovery"}
def present(value):
    if value is None:return False
    if isinstance(value,str):return bool(value.strip())
    if isinstance(value,(list,dict)):return bool(value)
    return True
def positive_int(value):return isinstance(value,int) and not isinstance(value,bool) and value>0
def _cycle(nodes,deps):
    visiting=set();visited=set()
    def visit(node):
        if node in visiting:return True
        if node in visited:return False
        visiting.add(node)
        for dep in deps.get(node,[]):
            if dep in nodes and visit(dep):return True
        visiting.remove(node);visited.add(node);return False
    return any(visit(node) for node in nodes)
def validate(data):
    errors=[]
    if data.get("schema_version")!=SCHEMA_VERSION:errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not isinstance(data.get("plan_id"),str) or len(data.get("plan_id","").strip())<8:errors.append("plan_id must be a stable identifier of at least 8 characters")
    for key in ("objective","terminal_state","completion_condition"):
        if not present(data.get(key)):errors.append(f"{key} is required")
    constraints=data.get("constraints")
    if not isinstance(constraints,dict):errors.append("constraints must be an object")
    else:
        for key in ("hard","soft","resources"):
            if not isinstance(constraints.get(key),list):errors.append(f"constraints.{key} must be an array")
        if isinstance(constraints.get("hard"),list) and not constraints.get("hard"):errors.append("constraints.hard must contain at least one substantive hard constraint")
    state=data.get("state");observability=None
    if not isinstance(state,dict):errors.append("state must be an object")
    else:
        for key in ("known","unknown"):
            if not isinstance(state.get(key),list):errors.append(f"state.{key} must be an array")
        observability=state.get("observability")
        if observability not in OBSERVABILITY:errors.append(f"state.observability must be one of {sorted(OBSERVABILITY)}")
    feasibility=data.get("feasibility");feasibility_status=None;unresolved=[]
    if not isinstance(feasibility,dict):errors.append("feasibility must be an object")
    else:
        feasibility_status=feasibility.get("status")
        if feasibility_status not in FEASIBILITY:errors.append(f"feasibility.status must be one of {sorted(FEASIBILITY)}")
        if not isinstance(feasibility.get("evidence"),list) or not feasibility.get("evidence"):errors.append("feasibility.evidence must be a non-empty array")
        unresolved=feasibility.get("unresolved_conditions")
        if not isinstance(unresolved,list):errors.append("feasibility.unresolved_conditions must be an array");unresolved=[]
        if feasibility_status in {"conditional","needs_discovery","blocked"} and not unresolved:errors.append(f"feasibility.status={feasibility_status} requires unresolved_conditions")
        if feasibility_status=="unsatisfiable" and not unresolved:errors.append("unsatisfiable feasibility requires the contradictory/blocking conditions to be named")
    regime=data.get("planning_regime");primary=None
    if not isinstance(regime,dict):errors.append("planning_regime must be an object")
    else:
        primary=regime.get("primary")
        if primary not in REGIMES:errors.append(f"planning_regime.primary must be one of {sorted(REGIMES)}")
        if not present(regime.get("rationale")):errors.append("planning_regime.rationale is required")
        if primary=="solver_assisted" and not present(regime.get("solver_or_verifier")):errors.append("solver_assisted requires planning_regime.solver_or_verifier")
        if primary=="deliberative_search" and not positive_int(regime.get("search_branch_budget")):errors.append("deliberative_search requires a positive finite planning_regime.search_branch_budget")
    tools=data.get("tool_affordances");required=set();available=set()
    if not isinstance(tools,dict):errors.append("tool_affordances must be an object")
    else:
        for key in ("required","available","assumptions"):
            if not isinstance(tools.get(key),list):errors.append(f"tool_affordances.{key} must be an array")
        if isinstance(tools.get("required"),list):required=set(map(str,tools.get("required",[])))
        if isinstance(tools.get("available"),list):available=set(map(str,tools.get("available",[])))
        missing=sorted(required-available)
        if missing and feasibility_status=="solvable":errors.append("solvable plan requires every required tool capability to be available: "+", ".join(missing))
        if missing and feasibility_status in {"conditional","blocked"}:
            unresolved_text=" ".join(map(str,unresolved)).lower()
            for capability in missing:
                if capability.lower() not in unresolved_text:errors.append(f"missing capability {capability!r} must be explicit in feasibility.unresolved_conditions")
        if primary=="solver_assisted" and isinstance(regime,dict):
            solver=str(regime.get("solver_or_verifier",""))
            if solver and solver not in available:errors.append("declared solver_or_verifier must appear in tool_affordances.available")
    adaptation=data.get("adaptation")
    if not isinstance(adaptation,dict):errors.append("adaptation must be an object");local_triggers=[]
    else:
        local_triggers=adaptation.get("local_adaptation_triggers");global_triggers=adaptation.get("global_replan_triggers")
        if not isinstance(local_triggers,list):errors.append("adaptation.local_adaptation_triggers must be an array");local_triggers=[]
        if not isinstance(global_triggers,list) or not global_triggers:errors.append("adaptation.global_replan_triggers must be a non-empty array")
        if observability in {"partial","dynamic"} and not local_triggers:errors.append(f"{observability} observability requires local_adaptation_triggers")
    work_units=data.get("work_units");nodes=set();deps={}
    if not isinstance(work_units,list):errors.append("work_units must be an array");work_units=[]
    if feasibility_status in {"blocked","unsatisfiable"} and work_units:errors.append(f"feasibility.status={feasibility_status} cannot contain executable work_units")
    if feasibility_status in EXECUTABLE_FEASIBILITY and not work_units:errors.append(f"feasibility.status={feasibility_status} requires at least one work_unit")
    for index,unit in enumerate(work_units):
        prefix=f"work_units[{index}]"
        if not isinstance(unit,dict):errors.append(f"{prefix} must be an object");continue
        uid=unit.get("id")
        if not isinstance(uid,str) or not uid.strip():errors.append(f"{prefix}.id is required");continue
        if uid in nodes:errors.append(f"duplicate work unit id {uid!r}")
        nodes.add(uid)
        for key in ("outcome","completion_evidence"):
            if not present(unit.get(key)):errors.append(f"{prefix}.{key} is required")
        if not isinstance(unit.get("preconditions"),list):errors.append(f"{prefix}.preconditions must be an array")
        unit_deps=unit.get("depends_on")
        if not isinstance(unit_deps,list):errors.append(f"{prefix}.depends_on must be an array");unit_deps=[]
        deps[uid]=list(map(str,unit_deps))
        if unit.get("effect") not in EFFECTS:errors.append(f"{prefix}.effect must be one of {sorted(EFFECTS)}")
    for uid,unit_deps in deps.items():
        for dep in unit_deps:
            if dep not in nodes:errors.append(f"work unit {uid!r} depends on unknown unit {dep!r}")
            if dep==uid:errors.append(f"work unit {uid!r} cannot depend on itself")
    if nodes and _cycle(nodes,deps):errors.append("work unit dependency graph must be acyclic")
    if feasibility_status=="needs_discovery" and work_units:
        first=work_units[0] if isinstance(work_units[0],dict) else {};text=" ".join(str(first.get(k,"")) for k in ("outcome","completion_evidence"));unresolved_text=" ".join(map(str,unresolved));terms=[t.lower() for t in re.findall(r"[A-Za-z0-9_\-]{4,}",unresolved_text)]
        if terms and not any(t in text.lower() for t in terms):errors.append("needs_discovery requires the first work_unit to address an unresolved condition")
    verification=data.get("verification")
    if not isinstance(verification,dict):errors.append("verification must be an object")
    else:
        for key in ("action","terminal"):
            if not present(verification.get(key)):errors.append(f"verification.{key} is required")
    return errors
def main(argv=None):
    parser=argparse.ArgumentParser(description="Validate a MinMax PlanSpec");parser.add_argument("plan",type=Path);args=parser.parse_args(argv)
    try:data=json.loads(args.plan.read_text(encoding="utf-8"))
    except Exception as exc:print(f"FAIL: invalid JSON: {exc}");return 1
    errors=validate(data)
    for error in errors:print(f"FAIL: {error}")
    print(f"RESULT: {'FAIL' if errors else 'PASS'} ({len(errors)} errors)");return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
