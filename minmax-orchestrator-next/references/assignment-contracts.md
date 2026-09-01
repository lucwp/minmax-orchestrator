# Assignment Contracts

## Root Manager

Root owns user intent, Task Model, feasibility/affordance classification, planning-regime selection, execution topology, global constraints, approvals, user-visible communication, conflict resolution, claim-to-evidence matching, authoritative-state/external verification, and final synthesis. Root is the only public voice during managed execution; follow `user-interaction-protocol.md`.

## Planner

Planner receives the smallest sufficient context and returns:

- objective and terminal state;
- hard/soft/resource constraints;
- known and unknown relevant state;
- observability class;
- feasibility status and evidence;
- information gaps;
- required/available tool affordances and assumptions;
- recommended planning regime and rationale;
- macroplan or minimum work units;
- material dependencies/preconditions;
- local adaptation triggers;
- global replan triggers;
- completion evidence, including external-world evidence requirements when a load-bearing claim depends on facts outside the runtime;
- ownership/tool recommendations.

Planner stops after one initial planning pass plus at most one pre-execution repair. It does not execute the task, spawn another planner, continuously self-critique, or treat same-model criticism as proof that its own plan is invalid.

In Loop Mode, planner output is design-stage material only and cannot authorize execution.

## Worker

Worker receives one bounded outcome, exact ownership surface, prerequisites, relevant known state, explicitly unknown state that must not be guessed, allowed tools/skills, expected immediate effect, completion evidence, runtime budget, and return schema.

Worker may adapt locally but may not redesign the global planning regime/topology, weaken hard constraints, recursively invoke the Orchestrator/Loop Mode, or independently address the user. If a genuine user-owned directional fork appears, return it to root as `decision_request`.

Return:
- `status: PASS | BLOCKED | PARTIAL`;
- outcome;
- evidence/change;
- completion-test result;
- feedback provenance when a repair/judgment occurred;
- concise blocker/residual risk;
- optional `decision_request`: decision needed, viable options/ambiguity, relevant evidence/trade-off, and whether the answer appears to remain inside current approved boundaries.

## Verifier

Before choosing a verifier, classify the criterion's truth domain and load `verification-evidence.md` for non-trivial cases. Use a model verifier only when direct deterministic, authoritative-state, transaction, or external/tool-grounded evidence is insufficient and failure cost justifies another call.

For load-bearing external-world claims, acquire authoritative or tool-grounded external evidence when reasonably available before returning terminal PASS. If it is unavailable, narrow the claim or return `UNCERTAIN` with the evidence limitation; do not substitute model memory, executor self-report, or same-model agreement.

Return:
- `PASS | FAIL | UNCERTAIN`;
- criterion evaluated;
- discriminating evidence;
- truth domain plus evidence/feedback provenance;
- evidence strength or limitation;
- whether the result is local, cycle/chunk, or terminal;
- exact failing criterion.

A verifier does not repair unless separately assigned. Same-model semantic feedback is auxiliary evidence, not terminal authority.
