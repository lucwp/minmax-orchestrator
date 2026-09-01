import copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('v',ROOT/'scripts'/'validate_interaction_evals.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);data=json.loads((ROOT/'evals'/'interaction'/'cases.json').read_text(encoding='utf-8'));assert not v.validate(data);assert data['scoring']['pass_score']==100;mut=copy.deepcopy(data);mut['cases'][0]['required_checks']=[];assert v.validate(mut)
def test_test_interaction_evals_module_regression_loaded():assert True
