# Sonnet Variant

This directory defines the model-specific source metadata for the stable **MinMax Orchestrator Sonnet** distribution.

The materialized `minmax-orchestrator-sonnet/` Skill is standalone at runtime. It must not depend on NEXT, Luna, this directory, shared repository files, persistent memory, or a profile switch.

## Stable base

Sonnet is derived from the current stable model-specific baseline rather than tracking NEXT directly. NEXT remains the experimental laboratory; stable model releases only adopt changes after compatibility review and validation.

## Anthropic-specific routing

The Sonnet distribution uses the current Anthropic capability ladder:

- Claude Haiku 4.5: economical bounded workers
- Claude Sonnet 5: default root/workhorse
- Claude Opus 5: narrow premium escalation/advisor
- Claude Fable 5: exceptional frontier escalation
- Claude Mythos 5: restricted-access only; never a required dependency

Model-specific instructions also account for Anthropic `effort`, adaptive thinking, optional Advisor use, and Claude-specific over-verification/tool-use tendencies.
