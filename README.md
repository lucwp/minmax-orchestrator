# MinMax Orchestrator

![Validate orchestrators](https://github.com/lucwp/minmax-orchestrator/actions/workflows/validate.yml/badge.svg)

MinMax Orchestrator is a control plane for agentic work.

It helps an AI agent decide how a task should be planned, when work should be delegated, what evidence counts as progress, when a plan needs to change, and when the work is actually done.

Instead of adding more agents or more reasoning by default, it tries to use the smallest amount of orchestration that can reliably complete the job.

## Why use an orchestrator?

Agentic workflows are easy to make complicated and surprisingly hard to make reliable.

An agent can over-plan a simple task, split work that should stay together, keep iterating after progress has stopped, trust its own output too easily, or continue down a plan that stopped making sense several steps ago.

MinMax Orchestrator manages those decisions explicitly.

A substantive task can follow a path like this:

```text
user intent
    ↓
understand the task
    ↓
check constraints and available capabilities
    ↓
choose how to plan
    ↓
choose how to execute
    ↓
act
    ↓
verify
    ↓
adapt, replan or stop
```

The path changes with the task. Straightforward work stays straightforward. Tasks that depend on new observations can adapt as evidence arrives. Problems with reliable external solvers or verifiers can use them instead of relying on free-form model reasoning.

## What it can manage

When the runtime provides the necessary capabilities, MinMax Orchestrator can manage:

- task decomposition and dependency ordering;
- planning depth and planning strategy;
- delegation and worker boundaries;
- planner, worker and verifier roles;
- tool and capability checks before execution;
- parallel work when it provides a real benefit;
- local repairs and larger replans;
- retry, iteration and no-progress limits;
- user approval boundaries;
- verification and evidence gathering;
- final synthesis of the work.

The orchestrator does not invent capabilities the host environment does not have. If a runtime cannot create parallel workers, switch models, persist state or use a particular tool, the Skill cannot make those capabilities appear. It controls how available capabilities are used.

## Planning that fits the task

Different tasks need different kinds of planning. MinMax Orchestrator selects among several planning regimes instead of applying one workflow to everything.

| Planning regime | Useful when |
| --- | --- |
| `fixed_sequential` | The steps are known, ordered and easy to verify |
| `hierarchical_adaptive` | The high-level plan is stable, but local decisions depend on evidence gathered during execution |
| `reactive_stepwise` | Each action reveals or changes information needed for the next action |
| `deliberative_search` | Several meaningful paths need to be compared, expanded or abandoned |
| `solver_assisted` | A solver, compiler, test system or other external verifier can handle the load-bearing reasoning more reliably |

The goal is not to choose the most sophisticated regime. It is to choose the simplest one that still fits the problem.

## Loop Mode

Loop Mode is for work that genuinely benefits from iteration.

Writing a good loop is harder than telling an agent to "keep iterating until it is good." A useful loop needs a clear objective, bounded scope, evidence that separates progress from activity, sensible retry and cost limits, decision boundaries, and a reliable rule for when to repair, replan or stop.

Many people know what result they want but do not want to manually architect that control flow, write a detailed loop contract, choose the right agent topology, define verification gates, or manage every iteration themselves.

MinMax Orchestrator handles that layer. From the user's intent, it can:

- architect the loop;
- write a human-readable execution contract;
- choose the planning regime and execution topology;
- define what counts as progress and what counts as PASS;
- set retry, iteration and no-progress limits;
- define evidence and verification requirements;
- establish which decisions the agent can make and which return to the user;
- manage repairs, replans and stopping conditions as the work evolves.

When Loop Mode is requested, the orchestrator first presents the proposed contract. Execution begins only after the user approves it.

A typical loop behaves like this:

```text
observe current state
        ↓
find a verified gap
        ↓
choose the smallest useful action
        ↓
execute
        ↓
verify the result
        ↓
update the known state
        ↓
continue only if another actionable gap remains
```

A loop is expected to make measurable progress. More reasoning, more messages or more iterations do not count by themselves. Repeating the same failed strategy is treated as no progress.

## Verification is part of the work

The orchestrator does not treat the agent's confidence as proof that a task succeeded.

It tries to match the evidence to the kind of claim being verified:

```text
code or deterministic output  → tests, schemas, compilers or assertions
system state                  → authoritative read-back
external action               → receipt and authoritative state when available
claim about the outside world → authoritative or tool-grounded external evidence
qualitative judgment          → independent review or an explicit rubric
```

If a load-bearing claim depends on facts outside the current environment, the orchestrator should obtain appropriate external evidence when that evidence is reasonably available. The model's memory, the executor's own report or another round of self-critique should not substitute for a source that can actually verify the claim.

If suitable evidence cannot be obtained, the result should be narrowed or reported with the remaining uncertainty instead of being promoted to PASS without support.

## Which version should I use?

MinMax Orchestrator separates experimentation from stable model-specific releases.

### MinMax Orchestrator NEXT

NEXT is the laboratory version.

It is where new orchestration ideas are designed, combined, stress-tested and refined before they are considered stable enough for a model-specific release. New planning mechanisms, verification rules, Loop Mode behavior and other architectural experiments can appear here first and may change as those experiments are evaluated.

Use NEXT when you want to explore the newest MinMax Orchestrator work and are comfortable with an experimental release channel.

Do not assume that every NEXT experiment has already been promoted to a stable distribution.

### Model-specific releases

Versions named after models are the stable release channel.

Each model-specific Orchestrator is a self-contained distribution intended for normal use with that model. It should not depend on NEXT, another Orchestrator, repository support files, persistent memory, a profile switch, or any other MinMax runtime component to function.

Changes move from NEXT into a model-specific release only after they are considered suitable for that model. This allows the stable distributions to keep the parts of the architecture that have earned their place without inheriting every experiment from the laboratory branch.

### MinMax Orchestrator Luna

Luna is a stable model-specific release.

Use it when running the Luna model and you want the stable, standalone MinMax Orchestrator distribution. Installing or invoking Orchestrator Luna is enough to select that version; it does not require NEXT to be installed alongside it.

As model-specific behavior is validated, Luna can diverge from NEXT where a different orchestration choice produces a better result for Luna.

### MinMax Orchestrator Sonnet

Sonnet is the stable Anthropic release.

Use it with the Claude Sonnet family when you want a standalone Orchestrator calibrated for Anthropic's efficiency-to-capability trade-offs. Its primary routing strategy is **Sonnet-first and effort-first**: substantive work normally stays on Sonnet, and the Orchestrator raises or lowers supported Sonnet effort before changing models when reasoning depth is the bottleneck.

Haiku is used as a specialized economical offload for mechanical or cheaply verified work rather than as the first reasoning tier. Opus is reserved for narrow advisor/escalation roles when Sonnet with appropriate effort is insufficient or the cost of failure justifies the premium. Frontier models remain exceptional last-resort paths.

The release name is intentionally **Sonnet**, not tied to a specific model version. The routing policy can track the current stable Claude Sonnet generation without changing the Skill's public identity every time Anthropic updates the model family.

Like every model-specific release, Orchestrator Sonnet is self-contained at runtime and does not require NEXT, Luna, persistent memory, a profile switch, or repository support files.

```text
                    MinMax Orchestrator NEXT
                    experimental laboratory
                              ↓
                 validated model-specific promotion
                         ↙             ↘
       MinMax Orchestrator Luna     MinMax Orchestrator Sonnet
       stable standalone release    stable standalone release
```

Future model-specific distributions follow the same separation: experimentation happens in NEXT; stable, dependency-free releases are named for the model family they are designed to orchestrate.

## What the orchestrator will not do

MinMax Orchestrator is deliberately conservative about adding complexity.

It should not:

- create multiple workers just because a task is important;
- use a loop when direct execution is sufficient;
- keep retrying without evidence of useful progress;
- let a worker redefine the user's objective;
- claim tools, models, parallelism or verification that did not actually run;
- treat self-critique as strong evidence when a better verifier exists;
- make a material user-owned decision without returning that decision to the user;
- continue past explicit approval or safety boundaries.

## Core principles

1. Keep simple work simple.
2. Choose the planning method before adding execution complexity.
3. Delegate only when delegation has a concrete benefit.
4. Preserve the user's objective, constraints and decision rights.
5. Match evidence to the truth being claimed.
6. Prefer direct verification over another round of model judgment.
7. Repair the smallest failed part before rebuilding the whole plan.
8. Stop when there is no verified, actionable gap left to close.
9. Never claim a capability the runtime did not provide.

## Status

MinMax Orchestrator includes deterministic and adversarial validation for its orchestration rules. That does not mean every model, runtime and tool combination is guaranteed to behave identically. Real-world reliability still depends on the capabilities exposed by the host environment and the behavior of the model running the Skill.

## Author

Lucas W. Portella
