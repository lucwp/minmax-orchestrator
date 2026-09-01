# PlanSpec Schema

## Purpose

Use a machine-checkable PlanSpec for Route C, unusually complex Route B work, and Loop Mode plans with material dependencies. The PlanSpec validates structure and declared semantics; the root remains responsible for task-truth judgments that cannot be proven deterministically.

## Schema 1.0

```json
{
  "schema_version": "1.0",
  "plan_id": "plan-stable-id",
  "objective": "...",
  "terminal_state": "...",
  "constraints": {"hard": ["..."], "soft": [], "resources": []},
  "state": {"known": ["..."], "unknown": ["..."], "observability": "full"},
  "feasibility": {"status": "solvable", "evidence": ["..."], "unresolved_conditions": []},
  "planning_regime": {"primary": "hierarchical_adaptive", "rationale": "...", "solver_or_verifier": null, "search_branch_budget": null},
  "tool_affordances": {"required": ["filesystem_write"], "available": ["filesystem_write"], "assumptions": []},
  "work_units": [{"id": "A", "outcome": "...", "preconditions": [], "depends_on": [], "completion_evidence": "...", "effect": "read_only"}],
  "adaptation": {"local_adaptation_triggers": ["..."], "global_replan_triggers": ["..."]},
  "verification": {"action": "...", "terminal": "..."},
  "completion_condition": "..."
}
```

## Enumerations

Planning regimes: `fixed_sequential`, `hierarchical_adaptive`, `reactive_stepwise`, `deliberative_search`, `solver_assisted`.

Observability: `full`, `partial`, `dynamic`.

Feasibility: `solvable`, `conditional`, `needs_discovery`, `blocked`, `unsatisfiable`.

Effects: `read_only`, `reversible_write`, `external_write`, `irreversible_high_consequence`.

## Hard semantic gates

- A plan cannot be executable when feasibility is `blocked` or `unsatisfiable`.
- `needs_discovery` requires the first executable work unit to obtain evidence/information that addresses an unresolved condition.
- `partial` or `dynamic` observability requires a non-empty local adaptation policy.
- `solver_assisted` requires a declared available solver/verifier.
- `deliberative_search` requires a finite positive branch budget.
- Every dependency must reference a declared work unit and the dependency graph must be acyclic.
- Every executable work unit requires completion evidence.
- Every capability listed in `required` must be present in `available` unless feasibility is `blocked`/`conditional` and the missing capability is explicitly named as unresolved.
- Hard constraints and terminal completion evidence cannot be empty for substantive plans.
