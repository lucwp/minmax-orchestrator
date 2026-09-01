# Luna variant source

This directory defines the model-specific source inputs used to materialize `minmax-orchestrator-luna/` from `minmax-orchestrator-next/`.

The generated distribution is standalone. Runtime code must never depend on this directory.

Current Luna delta: identity/naming only. There is no behavioral divergence from NEXT at initialization.

Future model-specific changes must be documented in `shared/luna-deltas.md` and represented as narrowly scoped transformations or patches here, with Luna-specific eval coverage where practical.
