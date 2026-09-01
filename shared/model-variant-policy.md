# Model Variant Policy

## Principle

MinMax Orchestrator NEXT is the architectural upstream. A model-specific distribution is a standalone release optimized for one model family, not an independent fork of the orchestration architecture.

## Allowed divergence

A model variant may diverge from NEXT only when all are true:

1. the delta addresses a model-specific behavior, capability, failure mode, cost profile, context behavior, planning tendency, tool-use behavior or verification characteristic;
2. the delta is documented in the variant delta ledger;
3. the change has a model-specific acceptance test or evaluation where practical;
4. shared safety, approval, planning-contract and verification invariants are not silently weakened;
5. the variant remains installable and executable as a standalone Skill.

## Promotion flow

```text
NEXT change
  -> shared structural/regression validation
  -> candidate stable architecture
  -> model-specific compatibility review
  -> model-specific evals
  -> variant adoption or documented rejection
```

A NEXT change is not automatically correct for every model variant.

## Synchronization

Synchronization is semantic, not blind copying. `variants/<model>/` is the source of model-specific deltas. The materialized `minmax-orchestrator-<model>/` directory is a release artifact: regenerate it from NEXT plus declared deltas, then rerun shared and model-specific tests.

## Runtime independence

No distribution may require `../shared`, `../variants`, another orchestrator folder, Agent Memory, or a persistent profile switch to function. Repository-level tooling may use shared metadata, but packaged Skills must remain self-contained.

## README synchronization

Every repository change requires a README accuracy review. Any change that affects user-visible behavior, supported models, release identity, compatibility, usage, capabilities, limitations, or status must update the root `README.md` in the same change. The README remains client-facing and must not contain private environment or maintainer-only operational context.
