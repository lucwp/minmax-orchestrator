# Planning Eval Suite

This suite measures planning competence separately from Loop Mode contract safety/usability.

Evidence layers must remain separate:

1. **Specification validation:** `scripts/validate_planning_evals.py` checks that cases are substantive and cover the required failure surfaces. It does not prove model behavior.
2. **Observation grading:** `scripts/grade_planning_observations.py` grades captured PlanSpecs from real runtime trials. It does not invoke a model.
3. **External benchmarks:** `benchmark-manifest.json` names candidate benchmark families. A benchmark is evidence only after it is actually executed with recorded model/tool/budget settings.

Full-suite runtime PASS requires observations for every case unless `--allow-partial` is explicitly used for diagnostics. Use at least 3 trials for ambiguous/stochastic cases when the host can isolate repeated executions.
