# Planning Regimes

## Purpose

Select how a plan should evolve as information arrives. This is separate from execution topology: **planning regime controls plan evolution; topology controls responsibility and coordination**.

Use the minimum sufficient regime. Do not add search, replanning, formal solvers, or multiple planning passes merely because a task is important.

## Regimes

### `fixed_sequential`

Use when the relevant state is known, the action order is stable, future steps do not depend materially on unseen observations, and completion can be checked deterministically or authoritatively.

Control flow:

`PLAN -> EXECUTE ORDERED STEP -> VERIFY -> NEXT STEP -> TERMINAL VERIFY`

Avoid this regime when the validity of a later action depends on state that will only exist after an earlier action.

### `hierarchical_adaptive`

Use for long or complex work where a stable high-level outcome/dependency structure can be planned now but local implementation details depend on evidence discovered during execution.

Control flow:

`MACROPLAN -> EXECUTE SMALLEST VALID CHUNK -> OBSERVE -> MICROPLAN -> VERIFY -> CONTINUE/LOCAL REPAIR/REPLAN`

This is the default substantive planning regime when the task is partially predictable. Freeze the macroplan's objective, terminal state, hard constraints, approval boundaries, and stable dependencies. Derive microplans only from currently observed state.

### `reactive_stepwise`

Use when the environment is partially observable or dynamic and each action reveals or changes state needed to choose the next action.

Control flow:

`OBSERVE -> CHOOSE NEXT ACTION -> ACT -> VERIFY -> UPDATE STATE -> OBSERVE AGAIN`

Do not let retrieved or tool-produced content rewrite root objective, policy, hard constraints, approval boundaries, or terminal criteria.

### `deliberative_search`

Use when materially different candidate paths exist, early choices have meaningful downstream effects, backtracking has value, and candidates can be scored against a sufficiently reliable criterion.

Control flow:

`GENERATE CANDIDATES -> SCORE/VERIFY -> EXPAND -> PRUNE -> SELECT`

Requirements:
- finite branch/search budget;
- explicit candidate scoring/evidence;
- stop when search cost exceeds expected improvement;
- never use search as the default merely to "think more".

### `solver_assisted`

Use when important state, constraints, preconditions, effects, schedules, or optimization objectives can be represented for a sound external solver, planner, compiler, test system, or authoritative verifier.

Control flow:

`LLM FORMALIZES -> EXTERNAL SYSTEM SOLVES/VERIFIES -> LLM INTERPRETS/EXECUTES BOUNDED RESULT`

Prefer this over unsupported free-form LLM planning when a sound primitive exists. The declared solver/verifier must actually be available before execution.

## Planning Regime Gate

Classify the task before choosing execution topology.

1. If hard constraints are unsatisfiable or required capabilities are unavailable, stop or recover before planning execution.
2. If the path is known and ordered with full observability, prefer `fixed_sequential`.
3. If the macro structure is stable but local actions depend on future evidence, prefer `hierarchical_adaptive`.
4. If the next action is primarily determined by newly observed state, prefer `reactive_stepwise`.
5. If reliable branching/backtracking is the load-bearing mechanism, use `deliberative_search`.
6. If a sound external planning/verification primitive can carry the load-bearing reasoning, use `solver_assisted`.

When two regimes remain plausible, use the simpler regime unless the more complex one has a concrete expected gain.

## Macroplan vs microplan

The **macroplan** contains approval-relevant and relatively stable outcomes, hard dependencies, hard constraints, tool/capability assumptions, and terminal evidence.

A **microplan** is the smallest next executable chunk derived from currently observed state.

Never encode a future micro-action as a frozen macroplan step when its validity depends on an observation that does not yet exist.

## Replanning levels

Use the smallest necessary adaptation:

- `microplan_update`: local next-action change; frozen boundaries unchanged;
- `local_repair`: a verified local failure has a changed strategy inside frozen boundaries;
- `macroplan_repair`: a non-approval-relevant dependency/assumption changes but objective/scope/verifier/risk envelope remain intact;
- `material_replan`: a frozen approval boundary changes; stop and obtain fresh approval when Loop Mode applies.

Do not regenerate a healthy macroplan merely to produce more reasoning text.
