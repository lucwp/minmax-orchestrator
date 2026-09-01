# Sonnet Variant

This directory defines the model-specific source metadata for the stable **MinMax Orchestrator Sonnet** distribution.

The materialized `minmax-orchestrator-sonnet/` Skill is standalone at runtime. It must not depend on NEXT, Luna, this directory, shared repository files, persistent memory, or a profile switch.

## Stable base

Sonnet is derived from the current stable model-specific baseline rather than tracking NEXT directly. NEXT remains the experimental laboratory; stable model releases only adopt changes after compatibility review and validation.

## Anthropic-specific routing

The Sonnet distribution uses a **Sonnet-first, effort-first, model-switch-last** policy.

The primary capability ladder stays inside Claude Sonnet through supported effort levels. Model switching is reserved for cases where another model has clearly better expected utility:

- Claude Sonnet 5: default root/workhorse across supported effort levels
- Claude Haiku 4.5: specialized economical offload for mechanical, high-volume, cheaply verified work
- Claude Opus 5: narrow premium advisor/escalation when Sonnet plus appropriate effort is insufficient or failure cost justifies it
- Claude Fable 5: exceptional last-resort frontier escalation
- Claude Mythos 5: restricted-access only; never a required dependency

Model-specific instructions also account for Anthropic `effort`, adaptive thinking, optional Advisor use, and Claude-specific over-verification/tool-use tendencies.
