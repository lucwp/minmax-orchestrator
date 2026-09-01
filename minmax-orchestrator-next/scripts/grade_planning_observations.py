#!/usr/bin/env python3
"""Grade captured PlanSpecs against planning case envelopes. Does not invoke a model."""
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; spec=importlib.util.spec_from_file_location("plan_validator",ROOT/"scripts"/"validate_plan_spec.py"); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
def grade_case(case,plan):
    errors=["invalid PlanSpec: "+x for x in v.validate(plan)]; regime=(plan.get("planning_regime") or {}).get("primary")
    if regime not in case.get("acceptable_regimes",[]): errors.append(f"planning regime {regime!r} not acceptable")
    feasibility=(plan.get("feasibility") or {}).get("status")
    if feasibility not in case.get("expected_feasibility",[]): errors.append(f"feasibility {feasibility!r} not acceptable")
    return errors
def grade(cases,observations,allow_partial=False):
    results=[]; declared={c["id"] for c in cases}
    for unknown in sorted(set(observations)-declared): results.append((unknown,["observation has no declared planning case"]))
    for case in cases:
        cid=case["id"]
        if cid not in observations:
            if not allow_partial: results.append((cid,["missing runtime planning observation"]))
            continue
        results.append((cid,grade_case(case,observations[cid])))
    return results
def main(argv=None):
    p=argparse.ArgumentParser(description="Grade captured PlanSpecs against planning eval cases"); p.add_argument("cases",type=Path); p.add_argument("observations",type=Path); p.add_argument("--allow-partial",action="store_true"); args=p.parse_args(argv); cases=json.loads(args.cases.read_text(encoding="utf-8"))["cases"]; observations=json.loads(args.observations.read_text(encoding="utf-8")); results=grade(cases,observations,args.allow_partial); failed=0
    for cid,errors in results:
        if errors: failed+=1; print(f"FAIL {cid}: "+"; ".join(errors))
        else: print(f"PASS {cid}")
    print(f"RESULT: {'FAIL' if failed else 'PASS'} ({len(results)-failed}/{len(results)} case checks passed; {len(observations)}/{len(cases)} observations supplied)"); return 1 if failed else 0
if __name__=="__main__": raise SystemExit(main())
