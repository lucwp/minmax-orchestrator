# Anthropic Model Routing for Sonnet

## Purpose

Optimize for `verified task success / expected total cost` using a **Sonnet-first, effort-first, model-switch-last** policy.

Claude Sonnet is the default substantive/root model. Treat supported `effort` levels inside Sonnet as the primary capability ladder. Change models only when a specialized offload or a narrow capability escalation has better expected utility than staying on Sonnet.

This distribution is calibrated against Anthropic's generally available model lineup as of 2026-09-01. Pricing changes over time; treat numeric prices below as a dated fallback snapshot, not a live pricing source. When current authoritative pricing is available and routing cost materially matters, prefer the current source.

## Economic roles

| Role | Model | API model | Price snapshot (input/output per MTok) | Default use |
| --- | --- | --- | ---: | --- |
| specialized economical offload | Claude Haiku 4.5 | `claude-haiku-4-5` | $1 / $5 | mechanical, high-volume, low-latency, cheaply verified bounded work |
| default root/workhorse | Claude Sonnet 5 | `claude-sonnet-5` | $2 / $10 | normal substantive work, coding, research, tool use, planning, synthesis, most agentic loops |
| narrow premium advisor/escalation | Claude Opus 5 | `claude-opus-5` | $5 / $25 | difficult load-bearing reasoning or judgment when Sonnet plus appropriate effort is insufficient or failure cost justifies the premium |
| exceptional frontier escalation | Claude Fable 5 | `claude-fable-5` | $10 / $50 | rare frontier/long-horizon nodes where Opus is insufficient and the expected lift justifies the additional cost |

Claude Mythos 5 is not part of the normal routing policy. It is restricted-access and must never be required for this Skill to function. Use it only when the runtime explicitly exposes authorized access and the user/domain context independently justifies it.

These roles are **not** a difficulty staircase. Haiku is not the first reasoning rung, and Opus/Fable are not automatic next steps because a task feels important.

## Sonnet effort is the primary ladder

Keep substantive work on Sonnet whenever the expected gain from additional Sonnet reasoning is sufficient relative to the expected cost of switching models.

When the runtime exposes supported effort controls, use them conceptually as:

```text
Sonnet low effort
        ↓
Sonnet medium effort
        ↓
Sonnet high effort
        ↓
Sonnet max effort
```

Choose the **lowest Sonnet effort that is likely to complete the node reliably**.

Typical policy:
1. low/medium effort for bounded substantive work with strong observability or cheap verification;
2. normal/high effort for planning, synthesis, coding, research, ambiguous tool use, and most Loop Mode reasoning;
3. high/max effort for genuinely difficult load-bearing reasoning when more internal reasoning is likely to resolve the gap;
4. before changing models, repair missing context, bad scope, wrong tools, and weak verification;
5. prefer a solver, compiler, test system, authoritative source, or deterministic verifier over buying more model capability when it can carry the load-bearing reasoning more reliably.

Do not escalate effort merely because a project is prestigious or large. Effort is justified by uncertainty, reasoning depth, failure cost, observability, and expected rework.

## Haiku is a specialized offload path

Use Haiku when all load-bearing uncertainty is low or externally/deterministically bounded and lower cost or latency has clear value.

Good candidates include:
- extraction and normalization;
- classification with explicit labels and checks;
- source collection with explicit query/coverage instructions;
- deterministic transformations;
- routine formatting;
- straightforward code edits guarded by strong tests;
- independent fan-out where each worker has a narrow contract and cheap verification.

**Haiku is a specialized offload path, not the first reasoning rung.** Do not move a cognitively meaningful node from Sonnet to Haiku merely to save tokens. If Haiku needs nearly all root context, repeated repairs, or substantive synthesis, keep the work on Sonnet.

## Opus is a narrow advisor/escalation

Prefer keeping Sonnet as executor and escalating only the difficult decision or failed/load-bearing node.

Use Opus when the failure class points to capability rather than missing context, bad scope, wrong tools, or weak verification. Strong candidates include:
- a narrow planning problem with material downstream consequences after Sonnet effort was calibrated appropriately;
- difficult root-cause analysis after ordinary debugging and stronger Sonnet effort failed;
- ambiguous integration across several constraints/domains;
- high-consequence qualitative judgment with no deterministic verifier;
- a verifier/advisor role where stronger judgment materially reduces expected failure cost.

If Anthropic's Advisor tool is available, **prefer an Opus advisor before replacing Sonnet as the executor** when one bounded consultation can resolve the hard node more cheaply.

Move a node to Opus execution only when the expected increase in verified success exceeds the incremental token, latency, context-transfer, integration, and verification cost.

## Fable is a last-resort frontier path

Fable is not the default premium tier. Use it only when at least one is true:
- Opus was insufficient after context/scope/tool issues were repaired;
- the node is unusually long-horizon or frontier-level and additional capability is plausibly decisive;
- the cost of an incorrect judgment is high enough that the expected quality lift justifies the price;
- an independent frontier review materially reduces residual risk that cannot be reduced more cheaply.

Prefer a narrow Fable consultation or isolated load-bearing node over moving the whole workflow. Do not build a workflow whose correctness depends on Fable being available for ordinary work.

## Effort and thinking controls

Sonnet 5 and Opus 5 use adaptive thinking by default and expose `effort` as the main cost/performance control. Fable 5 always uses adaptive thinking and also responds to effort. Haiku 4.5 does not support the same effort control.

Rules:
- use supported effort as the first capability throttle on Sonnet;
- do not automatically switch to Opus because Sonnet low/medium effort struggled;
- increase Sonnet effort when reasoning depth is the likely bottleneck and expected total cost remains favorable;
- do not use max effort by default when lower effort plus strong verification is sufficient;
- if a deterministic solver/test/verifier can carry the hard reasoning, prefer `solver_assisted` over simply raising effort or changing models.

Never use legacy `budget_tokens` instructions for Sonnet 5, Opus 5, or Fable 5. Do not add temperature/top-p tuning as an orchestration mechanism for current Sonnet/Opus/Fable models.

## Advisor tool

If the runtime exposes Anthropic's Advisor tool, treat it as the preferred narrow model-escalation primitive before replacing a capable Sonnet executor.

Preferred patterns:
- Sonnet executor -> Opus advisor for difficult planning/judgment;
- Sonnet executor -> Fable advisor only when frontier lift plausibly matters;
- Haiku executor -> Sonnet/Opus advisor only for a bounded hard decision inside an otherwise mechanical workload.

Rules:
- the advisor must be at least as capable as the executor;
- do not call an advisor merely because the task is important;
- gather enough task/tool context before consulting unless a workload-specific eval proves an early consultation helps;
- do not force repeated advisor calls after the actionable uncertainty is resolved;
- advisor output is guidance, not authoritative terminal evidence; verify externally/deterministically when a better verifier exists.

## Claude-specific prompting discipline

Current Claude models are proactive. Avoid legacy scaffolding that repeatedly says to be exhaustive, use every tool, re-check everything, or keep thinking. Such prompts can increase latency and tool overuse without improving verified outcomes.

- Keep instructions clear, direct, and bounded.
- Use explicit sequential steps only when order/completeness matters.
- Preserve the Orchestrator's user-visible progress protocol, but do not request hidden chain-of-thought.
- On Opus 5, do not add blanket self-check prompts: the model already tends to verify its own work, and extra self-verification can cause over-verification. The Orchestrator's independent verification requirements still apply.
- Sonnet 5 and Haiku 4.5 have context awareness; even so, pass the smallest sufficient task packet and checkpoint durable state when the harness may compact/reset context.

## Escalation sequence

For a substantive node, use this order:
1. keep or return the node to Sonnet unless it is clearly mechanical and cheaply verified;
2. repair missing context;
3. tighten objective and scope;
4. correct tool selection or tool failures;
5. strengthen verification;
6. raise supported Sonnet effort if reasoning depth is the bottleneck;
7. use a narrow Opus advisor if available and sufficient;
8. move only the failed/load-bearing node to Opus when the expected utility is positive;
9. use Fable only as an exceptional frontier escalation.

`same failure + same model + same strategy = no progress`

## Runtime honesty

If the harness does not expose explicit model selection, effort control, Advisor, or model identity, follow the semantic routing policy but do not claim those controls were used. Never infer that a worker ran on Haiku, Opus, or Fable unless the runtime provides evidence of that routing.
