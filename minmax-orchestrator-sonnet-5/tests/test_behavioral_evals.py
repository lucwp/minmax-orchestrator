import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SCRIPT=ROOT/'scripts'/'validate_behavioral_evals.py';spec=importlib.util.spec_from_file_location('behavioral_validator',SCRIPT);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);data=json.loads((ROOT/'evals'/'loop-mode'/'cases.json').read_text(encoding='utf-8'));errors=v.validate(data);assert not errors,errors;ids={c['id'] for c in data['cases']};assert len(ids)>=14;assert {'redteam_complexity_prestige','redteam_verifier_gaming','redteam_no_progress_reasoning','human_contract_ptbr_clarity','human_contract_english_humanized'}<=ids
def test_test_behavioral_evals_module_regression_loaded():assert True
