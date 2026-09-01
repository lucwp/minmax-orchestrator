# Loop Mode

## Purpose

Use Loop Mode only when the user explicitly asks to execute the current task with a loop or equivalent bounded iterative autonomous/semi-autonomous behavior.

This mode incorporates the load-bearing principles of Max Milian's `loop-engineering` project: machine-checkable completion, independent verification, explicit exits, finite budgets, context economy, durable state when required, and human gates for consequential actions. If that external skill is unavailable, use this reference as the compatibility protocol and do not claim it was invoked.

- Source: https://github.com/maxmilian/loop-engineering
- Author: Max Milian (`maxmilian`)
- License: MIT

MinMax Orchestrator Luna remains the root control plane for task modeling, feasibility, planning regime, topology, approvals, user-visible communication, directional decision gates, domain-skill authority, side effects, recovery, and final synthesis. During Loop Mode execution, always apply `user-interaction-protocol.md`.

## Hard lifecycle

Loop Mode has two stages:

`DESIGN STAGE -> USER APPROVAL -> EXECUTION STAGE`

The design stage may perform read-only inspection/retrieval needed to design a correct loop. It must not perform the substantive task, mutate target state, create the requested final deliverable, or start iterative execution.

### Design stage

Always run:

`TASK MODEL -> FEASIBILITY & AFFORDANCE GATE -> PLANNING REGIME GATE -> TOPOLOGY GATE -> PLAN AT RIGHT ALTITUDE -> COMPILE INTERNAL CONTRACT -> PREFLIGHT -> RENDER HUMAN CONTRACT -> USER APPROVAL -> STOP`

### Execution stage

Only after explicit approval of the presented contract:

`CHECKPOINT IF REQUIRED -> OBSERVE -> IDENTIFY VERIFIED GAP -> SELECT SMALLEST USEFUL ACTION -> EXECUTE -> ACTION VERIFY -> UPDATE STATE -> OBTAIN GROUNDED FEEDBACK -> ITERATION UTILITY GATE -> CYCLE VERIFY -> RECORD PROGRESS -> CHECKPOINT IF REQUIRED -> TRANSITION -> TERMINAL VERIFY -> SYNTHESIZE`

The original instruction to "use a loop" is **not** approval of the loop contract. Silence is not approval. Prior generic authorization is not approval of a newly compiled plan.

## 1. TASK MODEL

Capture:

- objective;
- terminal deliverable/state;
- authoritative inputs and evidence gaps;
- hard constraints, soft preferences, resource constraints, scope and exclusions;
- known and unknown state;
- observability: `full`, `partial`, or `dynamic`;
- required tool/capability affordances;
- hard dependencies;
- completion condition/evidence;
- approval and side-effect boundaries;
- unresolved user-owned directional decisions after authoritative retrieval.

Do not use vague objectives such as "keep improving until perfect". Do not guess unknown state.

## 2. FEASIBILITY & AFFORDANCE GATE

Before planning execution, classify feasibility using `planning-engine.md`:

- `solvable`;
- `conditional`;
- `needs_discovery`;
- `blocked`;
- `unsatisfiable`.

Check hard-constraint satisfiability, information sufficiency, required tool/capability availability, and whether proposed tools are actually relevant. `blocked` and `unsatisfiable` must not compile executable work units. `needs_discovery` starts with evidence acquisition.

## 3. PLANNING REGIME GATE

Always load `planning-regimes.md` and choose exactly one primary planning regime:

- `fixed_sequential`;
- `hierarchical_adaptive`;
- `reactive_stepwise`;
- `deliberative_search`;
- `solver_assisted`.

Planning regime defines how the plan evolves as information arrives. It is separate from topology. Prefer the minimum sufficient regime. `hierarchical_adaptive` is the default for substantive partially predictable work; search and solver-assisted planning require concrete task conditions.

## 4. TOPOLOGY GATE

Always load `loop-topology.md` and choose exactly one primary topology class:

- `deterministic_prompt_chain`;
- `router`;
- `single_adaptive_loop`;
- `parallel_sectioning`;
- `parallel_independent_review`;
- `orchestrator_workers`;
- `evaluator_optimizer`.

Use the minimum sufficient complexity. Loop Mode does not imply multi-agent execution. Task complexity alone does not justify orchestrator-workers. Evaluator-optimizer requires a gradable artifact and useful critique/repair economics.

## 5. PLAN AT THE RIGHT ALTITUDE

Use `planning-engine.md` when material dependencies exist. For complex Route B, Route C, and Loop Mode plans with material dependencies, compile a PlanSpec from `planning-spec-schema.md` and validate it with `scripts/validate_plan_spec.py` when practical.

Freeze approval-relevant outcomes and boundaries, but do not over-specify implementation details that depend on future observations. Separate stable macroplan from evidence-dependent microplans.

## 6. COMPILE INTERNAL CONTRACT

New contracts **must use schema `1.5`**. Schemas `1.0`–`1.4` are legacy and may be validated only through an explicit resume/migration path. Never emit an older schema for a new loop and never downgrade a contract to avoid current hard gates.

Minimum `1.5` shape:

```text
schema_version
mode
contract_id
contract_digest
loop_name
human_language
objective
terminal_deliverable
completion_condition

planning:
  regime
  observability
  feasibility_basis
  hard_constraints
  tool_affordance_assumptions
  local_adaptation_policy
  solver_or_verifier
  search_branch_budget

execution_plan:
  - name
    action
    purpose
    output
    next
    effect
    requires_human_approval

topology
topology_rationale
complexity_gate

authoritative_inputs
cycle_observation
cycle_action

progress:
  evidence_definition
  allowed_evidence_types
  fingerprint
  max_no_progress_cycles

feedback_policy:
  cycle_feedback_source
  same_model_feedback_role:
    auxiliary_only
  actionable_delta_required

iteration_policy:
  changed_strategy_after_failure
  max_same_failure_repeats

verification:
  method
  evidence
  layers:
    action
    cycle
    terminal
  independent_terminal_verifier
  terminal_actor
  evidence_source
  evidence_ledger:
    mode
    hard_criteria_require_pass
  proxy_hardening

success_exit
failure_exit
budget_exit
budgets
no_progress_rule
local_repair_triggers
material_replan_triggers
human_escalation_boundary
side_effect_class
state
approved_boundaries
domain_skills
tools
final_synthesis_requirement
approval
```

### Contract identity and approval binding

Before rendering the Human Contract:

1. assign a stable `contract_id`;
2. compute `contract_digest` from the canonical immutable contract payload using `scripts/validate_loop_contract.py --stamp-digest`;
3. present the Human Contract generated from that payload;
4. when the user approves, the root approval boundary captures that digest outside executor-editable state;
5. set `approval.status=approved`, preserve the user approval reference, and bind `approval.approved_contract_digest` to that captured digest;
6. before execution or resume, validate with `--approved-digest <captured_digest>`;
7. approved autonomous `external_write` also requires a root-captured explicit preauthorization reference validated with `--external-write-preauthorization-ref`.

A matching string inside the contract is not sufficient evidence of approval. If the external approved digest no longer matches, approval is invalidated and execution stops.

## 7. SEMANTIC HARD GATES

### Planning

- planning regime and topology must both be explicit;
- partial/dynamic observability requires a local adaptation policy;
- `solver_assisted` requires a declared available solver/verifier;
- `deliberative_search` requires a finite branch/search budget;
- feasibility/tool-affordance assumptions must be stated rather than silently guessed.

### Execution steps

Every execution step declares side-effect `effect` and `requires_human_approval`. An `irreversible_high_consequence` step always requires a human approval boundary before acting. The reference validator rejects obvious external mutations hidden inside `read_only`.

### Machine-checkable completion

Prefer tests, schemas, expected files, render QA, authoritative state, receipts, or named-source coverage. When deterministic verification is impossible, use a bounded semantic rubric with explicit pass/fail criteria.

### Progress

`activity != progress`.

Progress requires material new evidence/state: verified artifact/state change, completed action, resolved dependency, removed blocker, or measurable verifier movement. **Reasoning text alone is not progress.** Use a compact progress fingerprint when practical.

### Feedback provenance

Prefer cycle feedback in this order when applicable:

1. deterministic test;
2. authoritative state;
3. transaction receipt;
4. external/tool-grounded evidence;
5. independent reviewer;
6. same-model semantic feedback.

Same-model semantic feedback is auxiliary only. It may propose hypotheses or candidate repairs, but it cannot be sole terminal evidence, independently elevate confidence, or justify repeated repair without an actionable grounded delta.

### Iteration Utility Gate

Before another cycle require all of:

1. a criterion is still failing or unresolved;
2. evidence supports that gap;
3. a materially useful action can attack it;
4. the next cycle contains new information, a changed strategy, or a newly enabled action;
5. expected improvement justifies the remaining budget/cost.

`same failure + same strategy = no progress`.

### Proxy hardening

For every contract ask: `How could the executor make this verifier pass without satisfying the actual objective?`

Protect tests, thresholds, coverage, receipts, authoritative state, and other load-bearing verifier elements whenever possible. A prose reminder is not sufficient.

### Evidence ledger

For long-horizon work, aggregate terminal evidence incrementally by criterion rather than asking a holistic model judge to reread a long trajectory. Hard terminal criteria must individually reach PASS from permitted evidence sources.

## 8. STATE POLICY

Load `loop-state.md` and select `ephemeral` or `checkpointed`.

Use checkpointed state for long-running work, HITL interruption, expensive completed work, writes, parallel work, context-reset risk, or external receipts/read-back. Runtime checkpoint state is separate from the immutable contract and must validate with `scripts/validate_loop_checkpoint.py` against both the contract and the external approved digest.

Do not use conversation history as the only durable memory.

Local microplanning and replanning do not reset consumed budgets unless a newly approved contract explicitly changes them.

## 9. LAYERED VERIFICATION

Define three semantics:

### Action Verification

Confirms the just-executed action produced its intended immediate effect.

### Cycle Verification

Confirms material progress occurred, hard constraints/invariants remain intact, another cycle has actionable utility, and feedback provenance is acceptable.

### Terminal Verification

Independently confirms the terminal deliverable satisfies the global completion condition. Executor self-report and same-model self-critique are not terminal authority when better evidence exists.

## 10. PREFLIGHT

Before asking for approval verify:

### Contract

- loop name, objective, deliverable, scope, success/failure/budget exits;
- finite budgets;
- material dependencies and frozen boundaries;
- schema `1.5` validity.

### Planning

- Task Model is sufficient;
- feasibility/affordance status is evidence-backed;
- planning regime is appropriate to observability/constraint structure;
- PlanSpec validates when required;
- macroplan contains no speculative future micro-actions;
- solver/search requirements are actually available/bounded.

### Human clarity

- descriptive task-specific name;
- explicit user-facing language;
- each material step exposes action, purpose, output, and handoff/next logic;
- generic labels do not carry the plan;
- Portuguese rendering follows the embedded MinMax PT-BR Output principles and English rendering follows the embedded Humanizer principles; these language gates cannot alter scope, certainty, or approval boundaries.

### Topology

- topology class is explicit;
- a simpler topology was considered;
- parallelism/delegation has concrete benefit;
- evaluator-optimizer has stable criteria;
- root performs a bounded semantic task-truth check for claims deterministic validators cannot prove.

### Verification and iteration

- action/cycle/terminal semantics exist;
- terminal evidence is sufficiently independent;
- proxy-hardening is adequate;
- feedback provenance is explicit;
- same-model feedback cannot become terminal authority;
- changed-strategy and no-progress limits are consistent with hard budgets;
- evidence ledger is incremental for long-horizon work.

### State, interaction, safety

- state mode/resume strategy is appropriate;
- only high-signal context is carried forward;
- root owns user-visible communication;
- recoverable facts are retrieved before asking;
- user-owned forks use `decision_pause`;
- side-effect class is explicit;
- state-changing work follows `production-safety.md` and action manifests;
- child workers cannot recursively invoke the Orchestrator or Loop Mode;
- blast-radius/human boundaries are bounded.

If a load-bearing preflight item fails, repair once where possible. Otherwise present the blocker instead of asking approval for a knowingly invalid contract.

## 11. RENDER HUMAN CONTRACT

Load `loop-contract-rendering.md` and render from the validated Internal Contract. The Human Contract must preserve a clear mental model and all approval-relevant boundaries without dumping internal schema.

Its first line must be the largest Markdown header (`H1`): `# Contrato de Loop - <o que é>` for pt-BR or `# Loop Contract - <what it is>` for English.

Show planning regime/adaptation only when it materially changes how the user should understand execution. Then stop. **Do not execute the substantive task or any loop cycle in the same turn** as the contract presentation.

## 12. APPROVAL HANDLING

Approval must unambiguously refer to the presented contract. Capture the approved digest at the root boundary and freeze objective, terminal deliverable, material scope, hard constraints/dependencies, success criteria, hard budgets, tool/skill risk class, side-effect envelope, and human boundaries.

If the user edits the contract before approval, revise and re-present it.

## 13. EXECUTE CYCLE

Each cycle must be small enough to verify:

1. reconstruct minimum current state;
2. observe the verified completion gap;
3. select the smallest useful approved action from the current microplan;
4. execute it;
5. run action verification;
6. update observed state;
7. obtain the best available grounded feedback and record provenance;
8. run the Iteration Utility Gate;
9. run cycle verification;
10. record progress evidence/fingerprint and evidence-ledger updates;
11. emit/aggregate user-visible progress where runtime permits;
12. checkpoint when required;
13. choose exactly one transition.

Allowed transitions:

- `success`;
- `continue`;
- `microplan_update`;
- `local_repair`;
- `decision_pause`;
- `material_replan`;
- `fail_escalate`;
- `budget_exit`.

Use Route A/B/C internally as appropriate. Loop Mode does not force delegation.

## 14. TRANSITIONS

### success

Terminal verifier establishes completion -> exit.

### continue

Measurable progress exists, the Iteration Utility Gate passes, and the next approved action remains valid -> next cycle.

### microplan_update

New observed state changes only the next local action while frozen macro boundaries remain valid -> update microplan and continue without global replan.

### local_repair

A verifier fails but repair stays inside frozen boundaries -> make one changed-strategy repair by default, then re-verify. Repeating the same failure with the same strategy is prohibited progress.

### decision_pause

A genuine user-owned directional choice is required but current approved boundaries do not yet need to change -> root asks the user and pauses. **Preserve the approved contract/digest**. If checkpointing is required, represent the interruption with existing checkpoint `status=blocked` and a concise decision blocker. Resume directly when the answer stays inside frozen boundaries; otherwise transition to `material_replan`.

### material_replan

A frozen approval boundary must change -> pause immediately.

### fail_escalate

Unrecoverable blocker, ambiguous unsafe write, missing primitive, or human boundary -> stop with best verified partial state.

### budget_exit

Any hard budget trips -> stop with best verified partial state.

## 15. MATERIAL REPLAN = NEW APPROVAL

A **fresh approval is mandatory** when a replan changes any of:

- objective or terminal deliverable;
- material scope/dependency topology;
- hard constraints or success/terminal verification criteria;
- hard iteration/time/cost/search budget;
- tool/skill class in a way that changes capability or risk;
- side-effect/write envelope;
- human approval boundary.

Use:

`PAUSE -> REPLAN -> PREFLIGHT -> RENDER REVISION -> STOP -> WAIT FOR APPROVAL`

A `decision_pause`, `microplan_update`, or local repair that stays inside frozen boundaries does not require new approval.

## 16. SIDE EFFECTS

**Loop Mode never expands the autonomous write envelope.**

For state-changing work, follow `production-safety.md`, validate an action manifest when required, and read authoritative state before retrying any ambiguous write.

Autonomous `external_write` requires explicit preauthorization. `irreversible_high_consequence` always stops at a human approval boundary.

Loop approval is not blanket approval for separately gated domain actions.

## 17. FINAL SYNTHESIS

When the loop exits, root returns one integrated result containing:

- what completed;
- terminal verification evidence/evidence ledger;
- any remaining gap or budget/approval exit;
- the final artifact/action/result;
- runtime-evidence limitations that prevent stronger reliability claims.

Do not dump cycle transcripts, internal checkpoints, or chain-of-thought unless explicitly requested and otherwise permitted.
