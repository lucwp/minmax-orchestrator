import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];text=(ROOT/'SKILL.md').read_text(encoding='utf-8');loop=(ROOT/'references'/'loop-mode.md').read_text(encoding='utf-8');assert 'Loop Mode is opt-in only'.lower() in text.lower();assert 'Loop approval is mandatory'.lower() in text.lower();assert 'TASK MODEL -> FEASIBILITY & AFFORDANCE GATE -> PLANNING REGIME GATE -> TOPOLOGY GATE'.lower() in loop.lower();assert 'New contracts **must use schema `1.5`**'.lower() in loop.lower();SCRIPT=ROOT/'scripts'/'validate_loop_contract.py';spec=importlib.util.spec_from_file_location('v',SCRIPT);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def test_test_loop_mode_contract_module_regression_loaded():assert True
