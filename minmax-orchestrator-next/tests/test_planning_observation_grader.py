import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];pspec=importlib.util.spec_from_file_location('p',ROOT/'tests'/'test_plan_spec.py');p=importlib.util.module_from_spec(pspec);pspec.loader.exec_module(p);gspec=importlib.util.spec_from_file_location('g',ROOT/'scripts'/'grade_planning_observations.py');g=importlib.util.module_from_spec(gspec);gspec.loader.exec_module(g)
def test_planning_grader_accepts_matching_observation_and_rejects_missing_full_suite():
 cases=json.loads((ROOT/'evals'/'planning'/'cases.json').read_text(encoding='utf-8'))['cases'];case=next(c for c in cases if c['id']=='partial_observability');plan=p.base_plan();assert g.grade_case(case,plan)==[];results=g.grade(cases,{'partial_observability':plan},allow_partial=False);assert any(errors and 'missing runtime planning observation' in errors[0] for _,errors in results)
