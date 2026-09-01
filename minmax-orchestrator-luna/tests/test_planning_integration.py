import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_planning_architecture_is_integrated_without_over_orchestration():
 skill=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower();planning=(ROOT/'references'/'planning-engine.md').read_text(encoding='utf-8').lower();regimes=(ROOT/'references'/'planning-regimes.md').read_text(encoding='utf-8').lower();loop=(ROOT/'references'/'loop-mode.md').read_text(encoding='utf-8').lower();top=(ROOT/'references'/'loop-topology.md').read_text(encoding='utf-8').lower();assert 'planning regime and execution topology are orthogonal' in skill;assert 'feasibility & affordance gate' in planning;assert 'fixed_sequential' in regimes and 'solver_assisted' in regimes;assert 'planning regime comes first' in top;assert 'schema `1.5`' in loop;assert 'iteration utility gate' in loop;assert 'same failure + same strategy = no progress' in loop;assert 'route a' in skill and 'do not impose this machinery on route a' in planning
def test_reliability_claim_is_not_stronger_than_runtime_evidence():
 d=json.loads((ROOT/'reliability.json').read_text(encoding='utf-8'));assert d['level']=='structurally-hardened-runtime-validation-required';assert d['controls']['runtime_stochastic_planning_validation']['status']=='required_not_executed'
