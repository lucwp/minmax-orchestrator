# MinMax Orchestrator

![Validate orchestrators](https://github.com/lucwp/minmax-orchestrator/actions/workflows/validate.yml/badge.svg)

MinMax Orchestrator is a control plane for agentic work.

It does not try to make an agent "think harder" by default. It decides how a task should be planned, when work should be delegated, what evidence counts as progress, when a plan should change, and when the agent should stop.

The project is maintained as a family of standalone Skills. `NEXT` is the architectural upstream. Model-specific versions inherit that architecture and can diverge only where the model itself justifies a different orchestration strategy.

## Why this exists

Agentic systems tend to fail in predictable ways: they over-plan simple work, delegate without a real benefit, keep iterating after progress has stopped, confuse activity with evidence, or let a worker quietly redefine the task.

MinMax Orchestrator turns those choices into an explicit operating system for the workflow.

A substantive task can follow a path like this:

```text
user intent
    ↓
task model
    ↓
feasibility & affordance check
    ↓
planning regime
    ↓
execution topology
    ↓
plan
    ↓
execute
    ↓
verify
    ↓
adapt, replan or stop
```

The exact path is not fixed. A deterministic task should stay simple. A partially observable task may need local replanning. A formal planning problem may be better handed to a solver. The orchestrator chooses the minimum structure that still gives the task a credible path to completion.

## What it controls

When the runtime exposes the required capabilities, the orchestrator can govern:

- task decomposition and dependency ordering;
- planning regime selection;
- delegation and worker boundaries;
- planner, worker and verifier contracts;
- tool-use assumptions and feasibility checks;
- local repair versus global replanning;
- iteration budgets and no-progress exits;
- approval boundaries for Loop Mode;
- terminal verification and final synthesis.

The Skill is not the runtime. It cannot create parallel workers, persistent state, model routing, cancellation, or tool permissions where the host does not provide them. It defines how to use those capabilities when they exist.

## Planning regimes

The current planning engine separates the way a plan evolves from the way work is distributed.

It supports five primary regimes:

| Regime | Best fit |
| --- | --- |
| `fixed_sequential` | Known ordered steps with stable state and deterministic completion |
| `hierarchical_adaptive` | Stable high-level plan with local decisions that depend on new evidence |
| `reactive_stepwise` | Partial observability or environments where every action changes what can happen next |
| `deliberative_search` | Real branching, backtracking and candidate comparison |
| `solver_assisted` | Problems that can be formalized and checked by an external solver or verifier |

Planning regime and execution topology are separate decisions. A hierarchical plan, for example, may still run as a single adaptive loop or use bounded workers if there is a concrete reason to delegate.

## Loop Mode

Loop Mode is opt-in.

Writing a useful loop is harder than telling an agent to "keep iterating until it is good". A loop needs a clear objective, a bounded scope, evidence that can distinguish progress from activity, sensible retry and cost limits, explicit decision boundaries, and a reliable way to know when to repair, replan or stop. Getting those pieces right is one of the hardest parts of agentic work, and many users should not have to design that control logic by hand every time.

MinMax Orchestrator handles that work. From the user's intent, it architects the loop, writes the contract, chooses the planning regime and execution topology, defines what counts as progress and PASS, sets budgets and exit conditions, establishes verification and approval boundaries, and manages the loop as execution unfolds.

When a user explicitly asks the orchestrator to execute a task iteratively, it first produces a human-readable contract that freezes the outcome, boundaries, budget, verification strategy and exit conditions. Execution starts only after approval.

A loop is expected to make measurable progress. More reasoning by itself does not count.

```text
observe
  ↓
identify a verified gap
  ↓
choose the smallest useful action
  ↓
act
  ↓
verify
  ↓
update state
  ↓
continue only if another actionable gap remains
```

Repeated failure with the same strategy is treated as no progress. Terminal success should come from deterministic tests, authoritative state, receipts or an independent verifier whenever those are available.

## Distributions

### MinMax Orchestrator NEXT

`minmax-orchestrator-next/` is the main architectural upstream.

New planning rules, verification mechanisms, Loop Mode changes, safety controls and research-backed orchestration ideas land here first. NEXT is where the architecture evolves.

### MinMax Orchestrator Luna

`minmax-orchestrator-luna/` is the first model-specific distribution.

It is a standalone Skill. It does not require NEXT, Agent Memory, a persistent profile, or repository-level support files at runtime.

At the moment, Luna is behaviorally aligned with NEXT. Its initial differences are identity and model-specific naming. Future Luna-specific behavior must be justified by observed Luna behavior or evaluation evidence and recorded in `shared/luna-deltas.md`.

This lets the project optimize for a model without turning every model version into an unrelated fork.

## Repository model

```text
minmax-orchestrator/
├── minmax-orchestrator-next/      # architectural upstream
├── minmax-orchestrator-luna/      # standalone Luna distribution
├── variants/
│   └── luna/                      # Luna-specific source metadata/deltas
├── shared/
│   ├── model-variant-policy.md
│   └── luna-deltas.md
├── tools/
│   ├── materialize_luna.py
│   └── validate_all.py
└── .github/workflows/
    ├── validate.yml
    └── sync-luna.yml
```

`variants/` and `shared/` are repository-maintenance surfaces. Packaged orchestrators do not depend on them.

## Keeping Luna in sync

Luna is materialized from NEXT plus its declared model-specific deltas:

```bash
python tools/materialize_luna.py
python tools/validate_all.py
```

The GitHub sync workflow runs the same process when NEXT or the Luna variant source changes. It validates both distributions before committing the regenerated Luna snapshot.

This makes drift visible. A difference between Luna and NEXT should exist because it was declared, not because somebody forgot to copy a file six months ago.

## Validation

Run the complete repository check with:

```bash
python tools/validate_all.py
```

Each distribution runs its own pytest suite. Validation fails if a distribution is missing, zero tests are collected, or any test fails.

The current suites cover the planning contract, Loop Mode, approval binding, checkpoint behavior, interaction rules, side-effect boundaries, plan validation and adversarial cases. Runtime-specific stochastic benchmarks remain a separate layer of evidence and should not be confused with deterministic structural tests.

## Design principles

A few rules carry most of the architecture:

1. Keep simple work simple.
2. Choose a planning regime before adding orchestration complexity.
3. Delegate only when delegation has a concrete benefit.
4. Treat objective, constraints and approvals as root-owned state.
5. Prefer deterministic or authoritative verification over another round of model judgment.
6. Repair the smallest failed component before rebuilding the whole plan.
7. Stop when there is no verified, actionable gap left to close.
8. Never claim a capability the runtime did not actually provide.

## Status

NEXT and Luna are structurally hardened and covered by deterministic/adversarial test suites. The project deliberately does not label that evidence as proof of universal runtime reliability. Model-specific stochastic evaluation is the next layer required before stronger production claims are justified.

## Author

Lucas W. Portella
