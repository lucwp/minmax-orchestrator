#!/usr/bin/env python3
import argparse,json
from pathlib import Path
REQUIRED_CASES={"deterministic_ordered_task","hidden_dependency","partial_observability","dynamic_environment","missing_required_information","extraneous_tool","broken_required_tool","unsatisfiable_constraints","formalizable_planning","branching_search","long_horizon_constraints","local_global_constraint_conflict","premature_irreversible_action","observation_invalidates_macro_assumption","self_critique_false_positive","repeated_no_progress_repair","hidden_user_decision","unnecessary_global_replan","local_repair_sufficient","untrusted_observation_objective_mutation"};VALID_REGIMES={"fixed_sequential","hierarchical_adaptive","reactive_stepwise","deliberative_search","solver_assisted"};VALID_FEASIBILITY={"solvable","conditional","needs_discovery","blocked","unsatisfiable"}
def validate(data):
 e=[]
 if data.get("schema_version")!="1.0":e.append("schema_version must be 1.0")
 s=data.get("scoring")
 if not isinstance(s,dict):e.append("scoring must be an object")
 else:
  dims=["feasibility_detection","planning_regime_fit","dependency_correctness","tool_affordance_correctness","constraint_preservation","adaptation_replan_correctness","verification_quality","efficiency"]
  if any(not isinstance(s.get(k),int) or s.get(k)<=0 for k in dims):e.append("all planning scoring dimensions must be positive integers")
  if sum(s.get(k,0) for k in dims)!=100:e.append("planning scoring dimensions must sum to 100")
  if s.get("pass_score")!=95:e.append("pass_score must be 95")
  if s.get("hard_gates_override_score") is not True:e.append("hard_gates_override_score must be true")
 cases=data.get("cases")
 if not isinstance(cases,list):return e+["cases must be an array"]
 ids=[]
 for i,c in enumerate(cases):
  if not isinstance(c,dict):e.append(f"cases[{i}] must be an object");continue
  cid=c.get("id");ids.append(cid)
  if not isinstance(cid,str) or len(cid)<4:e.append(f"cases[{i}].id is invalid")
  if not isinstance(c.get("prompt_class"),str) or len(c.get("prompt_class","").strip())<12:e.append(f"{cid}: prompt_class is too weak")
  regs=c.get("acceptable_regimes");feas=c.get("expected_feasibility")
  if not isinstance(regs,list) or not regs or set(regs)-VALID_REGIMES:e.append(f"{cid}: acceptable_regimes invalid")
  if not isinstance(feas,list) or not feas or set(feas)-VALID_FEASIBILITY:e.append(f"{cid}: expected_feasibility invalid")
  for key in ("required_properties","forbidden_properties"):
   value=c.get(key)
   if not isinstance(value,list) or not value or any(not isinstance(x,str) or len(x.strip())<4 for x in value):e.append(f"{cid}: {key} must contain substantive entries")
 if len(ids)!=len(set(ids)):e.append("case ids must be unique")
 missing=sorted(REQUIRED_CASES-set(ids))
 if missing:e.append("missing required planning cases: "+", ".join(missing))
 return e
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("cases",type=Path);a=p.parse_args(argv)
 try:d=json.loads(a.cases.read_text(encoding="utf-8"))
 except Exception as x:print(f"FAIL: invalid JSON: {x}");return 1
 e=validate(d)
 for x in e:print("FAIL: "+x)
 print(f"RESULT: {'FAIL' if e else 'PASS'} ({len(e)} errors)");return 1 if e else 0
if __name__=="__main__":raise SystemExit(main())
