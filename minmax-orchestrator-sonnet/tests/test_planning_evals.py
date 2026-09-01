import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('v',ROOT/'scripts'/'validate_planning_evals.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def test_planning_eval_suite_is_complete():d=json.loads((ROOT/'evals'/'planning'/'cases.json').read_text(encoding='utf-8'));assert v.validate(d)==[];assert len(d['cases'])>=20
