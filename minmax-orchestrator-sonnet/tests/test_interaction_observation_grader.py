import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('g',ROOT/'scripts'/'grade_interaction_observations.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);data=json.loads((ROOT/'evals'/'interaction'/'cases.json').read_text(encoding='utf-8'));perfect={c['id']:{'observed_checks':list(c['required_checks'])} for c in data['cases']};r=g.grade(data,perfect);assert g.score(r)==100 and all(not e for _,e in r)
def test_test_interaction_observation_grader_module_regression_loaded():assert True
