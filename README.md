# MinMax Orchestrator

Evidence-informed orchestration system maintained as a family of standalone model distributions.

## Distributions

| Distribution | Role | Status |
| --- | --- | --- |
| `minmax-orchestrator-next/` | Primary upstream for architecture, planning, Loop Mode, safety, verification, interaction and new research-backed mechanisms. | Active upstream |
| `minmax-orchestrator-luna/` | Luna-specific standalone distribution materialized from NEXT plus declared Luna deltas. | Active model variant |

## Source model

`minmax-orchestrator-next/` is the architectural upstream. Model-specific source metadata lives under `variants/<model>/`; materialized distributions live at `minmax-orchestrator-<model>/` and must be installable without NEXT, `variants/`, `shared/`, Agent Memory, or a persistent profile switch.

Luna is currently behaviorally identical to NEXT. Its initial differences are distribution identity and naming only. Future Luna-specific changes require an explicit delta, evidence/eval coverage, and preservation of shared safety and verification invariants.

## Synchronization

Luna is regenerated deterministically:

```bash
python tools/materialize_luna.py
python tools/validate_all.py
```

The GitHub sync workflow performs the same operation when NEXT or the Luna variant source changes and commits the materialized Luna distribution only after both suites pass.

## Validation

```bash
python tools/validate_all.py
```

This executes each distribution's pytest suite independently and fails if either distribution is missing, no tests are collected, or any test fails.
