import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];GOLDEN=ROOT/'evals'/'loop-mode'/'golden';spec=importlib.util.spec_from_file_location('renderer',ROOT/'scripts'/'render_loop_contract.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);pairs=sorted(GOLDEN.glob('*.json'));assert len(pairs)==6
for path in pairs:
 d=json.loads(path.read_text(encoding='utf-8'));actual=r.render(d);expected=path.with_suffix('.md').read_text(encoding='utf-8');assert actual==expected,path.name
other=json.loads(pairs[0].read_text(encoding='utf-8'));other['human_language']='other'
try:r.render(other);raise AssertionError('expected unsupported-language failure')
except ValueError:pass
def test_test_human_contract_rendering_module_regression_loaded():assert True
