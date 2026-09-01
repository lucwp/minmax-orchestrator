# Anthropic Model Routing for Sonnet 5

## Purpose

Keep Claude Sonnet 5 as the default workhorse and spend additional model capability only on nodes where the expected increase in verified task success exceeds the extra token, latency, and coordination cost.

This distribution is calibrated against Anthropic's generally available model lineup as of 2026-09-01. Pricing changes over time; treat the numeric prices below as a dated fallback snapshot, not a live pricing source. When current authoritative pricing is available and routing cost materially matters, prefer the current source.

## Stable capability ladder

| Role | Model | API model | Price snapshot (input/output per MTok) | Default use |
| --- | --- | --- | ---: | --- |
| economical worker | Claude Haiku 4.5 | `claude-haiku-4-5` | $1 / $5 | mechanical, high-volume, low-latency, cheaply verified bounded work |
| default root/workhorse | Claude Sonnet 5 | `claude-sonnet-5` | $3 / $15 | normal substantive work, coding, research, tool use, planning, most agentic loops |
| premium escalation/advisor | Claude Opus 5 | `claude-opus-5` | $5 / $25 | genuinely hard narrow reasoning, root cause, ambiguous integration, high failure cost |
| frontier escalation | Claude Fable 5 | `claude-fable-5` | $10 / $50 | exceptional long-horizon/frontier work where Opus is insufficient and the gain is worth ~2x Opus token price |

Claude Mythos 5 is not part of the normal ladder. It is restricted-access and must never be required for this Skill to function. Use it only when the runtime explicitly exposes authorized access and the user/domain context independently justifies it.

## Routing policy

### Stay on Sonnet 5 by default

Sonnet 5 is the default because it provides the strongest general efficiency/capability balance for agentic work in the current Anthropic lineup. Keep the root on Sonnet unless there is a concrete reason to move a node.

Use Sonnet for:
- substantive planning and synthesis;
- ordinary software engineering and debugging;
- research and tool-driven knowledge work;
- multi-step agentic execution;
- most Loop Mode cycles;
- integration across worker outputs.

### Route down to Haiku 4.5

Use Haiku when all load-bearing uncertainty is low or externally/deterministically bounded and the work benefits from lower cost or latency. Good examples include:
- extraction and normalization;
- source collection with explicit query/coverage instructions;
- deterministic transformations;
- routine formatting;
- straightforward code edits guarded by strong tests;
- independent fan-out where each worker has a narrow contract.

Do not send ambiguous strategic decisions, weakly specified research synthesis, or hard planning nodes to Haiku merely to save tokens. If the Haiku worker would need nearly all root context or repeated repairs, keep the work on Sonnet.

### Escalate to Opus 5 narrowly

Use Opus only when the failure class points to capability rather than missing context, bad scope, wrong tools, or weak verification. Strong candidates include:
- a narrow planning problem with material downstream consequences;
- difficult root-cause analysis after ordinary debugging failed;
- ambiguous integration across several constraints/domains;
- high-consequence qualitative judgment with no deterministic verifier;
- a verifier/advisor role where stronger judgment materially reduces expected failure cost.

Prefer escalating one load-bearing node over moving the whole workflow to Opus.

### Escalate to Fable 5 exceptionally

Fable is the frontier tier, not the default premium tier. Use it only when at least one is true:
- Opus 5 failed after context/scope/tool issues were repaired;
- the node is unusually long-horizon or complex and frontier capability is plausibly decisive;
- the cost of an incorrect judgment is high enough that the expected quality lift justifies the price;
- an independent frontier review materially reduces residual risk.

Fable has stricter safeguards and may fall back on some requests. Do not build a workflow whose correctness depends on Fable being available for every domain.

## Effort before escalation

Sonnet 5 and Opus 5 use adaptive thinking by default and expose `effort` as the main cost/performance control. Fable 5 always uses adaptive thinking and also responds to effort. Haiku 4.5 does not support the same effort control.

Use effort as an intra-model throttle:
1. keep routine work at low/medium effort when the runtime exposes it and verification is cheap;
2. use normal/high effort for substantive Sonnet work;
3. raise effort on the current model before switching models when the problem is reasoning depth and the expected token cost remains lower than escalation;
4. do not use xhigh/max or frontier models by default;
5. if a deterministic solver/test/verifier can carry the hard reasoning, prefer `solver_assisted` over simply raising effort.

Never use legacy `budget_tokens` instructions for Sonnet 5, Opus 5, or Fable 5. Do not add temperature/top-p tuning as an orchestration mechanism for current Sonnet/Opus/Fable models.

## Advisor tool

If the runtime exposes Anthropic's Advisor tool, treat it as a narrow capability-escalation primitive. It fits this Orchestrator well because the executor can remain economical while a stronger model advises on one difficult decision.

Preferred patterns:
- Haiku executor -> Sonnet/Opus advisor for a bounded hard decision;
- Sonnet executor -> Opus advisor for difficult planning/judgment;
- Sonnet or Opus executor -> Fable advisor only when frontier lift plausibly matters.

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

Before moving up the ladder:
1. repair missing context;
2. tighten the objective/scope;
3. correct tool selection or tool failures;
4. strengthen verification;
5. adjust supported effort if the issue is reasoning depth;
6. use a narrow advisor if available and sufficient;
7. escalate only the failed/load-bearing node.

`same failure + same model + same strategy = no progress`

## Runtime honesty

If the harness does not expose explicit model selection, effort control, Advisor, or model identity, follow the semantic routing policy but do not claim those controls were used. Never infer that a worker ran on Haiku, Opus, or Fable unless the runtime provides evidence of that routing.
