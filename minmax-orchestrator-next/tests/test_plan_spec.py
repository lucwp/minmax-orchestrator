import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('v',ROOT/'scripts'/'validate_plan_spec.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def base_plan():return {'schema_version':'1.0','plan_id':'plan-test-0001','objective':'implement change','terminal_state':'all checks pass','constraints':{'hard':['do not widen write envelope'],'soft':[],'resources':[]},'state':{'known':['target exists'],'unknown':['local failure'],'observability':'partial'},'feasibility':{'status':'solvable','evidence':['tools available'],'unresolved_conditions':[]},'planning_regime':{'primary':'hierarchical_adaptive','rationale':'local repairs depend on evidence','solver_or_verifier':None,'search_branch_budget':None},'tool_affordances':{'required':['filesystem_write','pytest'],'available':['filesystem_write','pytest'],'assumptions':[]},'work_units':[{'id':'A','outcome':'implement bounded change','preconditions':[],'depends_on':[],'completion_evidence':'targeted check passes','effect':'reversible_write'},{'id':'B','outcome':'verify candidate','preconditions':[],'depends_on':['A'],'completion_evidence':'full suite passes','effect':'read_only'}],'adaptation':{'local_adaptation_triggers':['local failure'],'global_replan_triggers':['hard constraint changes']},'verification':{'action':'targeted test','terminal':'full suite'},'completion_condition':'all tests pass'}
def test_valid_plan_spec_passes():assert v.validate(base_plan())==[]
def test_unknown_dependency_rejected():d=base_plan();d['work_units'][1]['depends_on']=['Z'];assert any('unknown unit' in x for x in v.validate(d))
def test_dependency_cycle_rejected():d=base_plan();d['work_units'][0]['depends_on']=['B'];assert any('acyclic' in x for x in v.validate(d))
def test_missing_terminal_state_rejected():d=base_plan();d['terminal_state']='';assert v.validate(d)
def test_missing_completion_evidence_rejected():d=base_plan();d['work_units'][0]['completion_evidence']='';assert v.validate(d)
def test_invalid_regime_rejected():d=base_plan();d['planning_regime']['primary']='magic';assert v.validate(d)
def test_partial_observability_requires_adaptation():d=base_plan();d['adaptation']['local_adaptation_triggers']=[];assert v.validate(d)
def test_solver_assisted_requires_available_solver():d=base_plan();d['planning_regime'].update(primary='solver_assisted',solver_or_verifier='solver');assert v.validate(d)
def test_deliberative_search_requires_branch_budget():d=base_plan();d['planning_regime']['primary']='deliberative_search';assert v.validate(d)
def test_solvable_plan_cannot_require_unavailable_capability():d=base_plan();d['tool_affordances']['required'].append('missing');assert v.validate(d)
def test_unsatisfiable_plan_cannot_have_work_units():d=base_plan();d['feasibility'].update(status='unsatisfiable',unresolved_conditions=['contradiction']);assert v.validate(d)
