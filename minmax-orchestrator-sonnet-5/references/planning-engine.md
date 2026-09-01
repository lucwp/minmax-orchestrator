# Planning Engine

## Purpose

Use for Route C, unusually complex Route B work, or Loop Mode plans with material dependencies. Separate task modeling, feasibility, planning-regime selection, execution topology, and execution. A plan is an operational hypothesis, not a script that must survive contrary evidence.

## Lifecycle

For substantive planning use:

`TASK MODEL -> FEASIBILITY & AFFORDANCE GATE -> PLANNING REGIME GATE -> TOPOLOGY GATE -> PLAN AT RIGHT ALTITUDE -> COMPILE MATERIAL DEPENDENCIES -> PREFLIGHT -> EXECUTE -> VERIFY -> UPDATE OBSERVED STATE -> ADAPT/REPLAN AT SMALLEST NECESSARY LEVEL -> TERMINAL VERIFY`

Do not impose this machinery on Route A or bounded Route B work whose path and completion test are obvious.

## 1. Task Model

Capture only the state needed to plan correctly:

- objective;
- terminal state/deliverable;
- hard constraints, soft preferences, and resource constraints;
- known authoritative state;
- unknown state and evidence gaps;
- observability: `full`, `partial`, or `dynamic`;
- required tool/capability affordances;
- approval and side-effect boundaries;
- user-owned directional decisions after authoritative retrieval;
- completion evidence.

Do not guess missing facts. Mark them unknown.

## 2. Feasibility & Affordance Gate

Before decomposition ask:

- Can the terminal state actually be reached?
- Are hard constraints mutually satisfiable?
- Is required information available or recoverable?
- Do available tools expose every load-bearing capability?
- Is any proposed tool extraneous to completion?
- Does an action depend on state that has not yet been observed?

Classify:

- `solvable`: current evidence supports execution;
- `conditional`: execution is viable if named unresolved conditions are satisfied;
- `needs_discovery`: obtain missing evidence before committing to dependent actions;
- `blocked`: a required capability/state is unavailable;
- `unsatisfiable`: hard requirements cannot jointly be met.

`blocked` and `unsatisfiable` must not compile executable work units. `needs_discovery` starts with the smallest evidence-acquisition work unit that can resolve the blocker.

## 3. Planning Regime Gate

Load `planning-regimes.md` and choose one primary planning regime before execution topology:

- `fixed_sequential`;
- `hierarchical_adaptive`;
- `reactive_stepwise`;
- `deliberative_search`;
- `solver_assisted`.

Planning regime and topology are orthogonal: the first determines how the plan evolves as information arrives; the second determines how execution responsibility is organized.

Use `hierarchical_adaptive` as the default for substantive partially predictable work. Do not use search, repeated planning, or a solver merely because a task is difficult.

## 4. Plan at the Right Altitude

Plan deliverables and material dependencies upfront. Defer implementation details whose correctness depends on evidence that will only exist during execution; represent those details as microplans derived from observed state.

Freeze upfront:

- objective and terminal state;
- hard constraints;
- authoritative constraints and stable dependencies;
- success criteria;
- hard budgets when applicable;
- tool/skill risk class;
- side-effect envelope;
- human boundaries.

### Macroplan

Plan stable outcomes, hard dependencies, capability assumptions, constraints, and terminal evidence.

### Microplan

Derive only the smallest next executable chunk from currently observed state.

Never freeze a future micro-action whose validity depends on an observation that does not yet exist.

## 5. PlanSpec

For Route C, unusually complex Route B work, and Loop Mode plans with material dependencies, compile `references/planning-spec-schema.md` and validate with `scripts/validate_plan_spec.py` when practical.

PlanSpec structure is evidence of an explicit plan; it is not proof that real-world claims inside the plan are true. Root semantic preflight remains authoritative for claims such as whether a tool is truly available or a dependency is materially necessary.

## 6. Minimal Work Units

For Loop Mode and other human-visible complex plans, every material unit must remain explainable as: `action -> purpose -> output -> what the output enables next`.

Create the smallest units that have a distinct outcome, dependency, tool/context boundary, ownership boundary, or verification value. Merge nodes that differ only in wording or implementation detail.

Represent material dependencies explicitly and keep the graph acyclic.

Parallelize only ready nodes whose ownership does not overlap and whose parallelism/context-isolation benefit exceeds coordination and integration cost.

## 7. Delegation Gate

Compare:

`expected benefit`

against:

`context transfer + worker run + integration + verification`

Delegate only for concrete parallelism, context isolation, specialist capability, dynamic decomposition, scout/rework prevention, or independent risk reduction. "More thinking" is not a benefit type.

## 8. Verification and observed-state update

After each material action/chunk:

1. verify the immediate intended effect;
2. update known/unknown state from authoritative or protected evidence;
3. check hard constraints and preconditions;
4. determine whether the current microplan remains valid;
5. adapt at the smallest sufficient level.

Do not use same-model self-critique as sole evidence that an otherwise passing state is wrong. Prefer deterministic tests, authoritative reads, receipts, tool-grounded feedback, or genuinely independent review.

## 9. Adaptation hierarchy

Prefer, in order:

1. `microplan_update`: choose a different next action from new state;
2. `local_repair`: fix one verified local failure with a changed strategy;
3. `macroplan_repair`: revise a non-approval-relevant dependency/assumption;
4. `material_replan`: a frozen objective, scope, verifier, hard budget, risk class, side-effect envelope, or human boundary must change.

Do not pre-ask implementation choices the agent owns. Use `user-interaction-protocol.md` for genuine user-owned directional decisions.

## 10. Replan triggers

Global replanning is justified only by observable triggers such as:

- invalidated macro assumption;
- impossible dependency;
- changed hard constraint;
- tool/capability assumption proven false;
- terminal completion test impossible under current plan;
- repeated verified failure requiring a different macro strategy;
- material ownership/risk/approval boundary change.

Do not regenerate a healthy macroplan merely to think more.

## Internal Work-Unit Contracts

For evaluator-optimizer work or large complex chunks, a bounded internal completion contract may be created:

1. state expected chunk outcome;
2. define completion evidence;
3. verify the evidence represents the actual outcome rather than a proxy loophole;
4. execute the chunk;
5. verify the result.

Do not add work-unit contracts to small tasks.

## Planning output

```text
Objective:
Terminal state / deliverable:
Hard constraints:
Known / unknown state:
Observability:
Feasibility status / evidence:
Required / available affordances:
Planning regime / rationale:
Topology / rationale:
Macroplan or work units:
Critical dependencies:
Local adaptation triggers:
Global replan triggers:
Completion evidence:
Unresolved user decisions / owner:
Approval boundaries:
```
