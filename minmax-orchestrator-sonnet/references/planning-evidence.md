# Planning Evidence Map

## Use

Use this reference only when changing planning policy, designing planning evals, or explaining why a regime exists. Treat evidence as conditional rather than proof of a universal best reasoning sequence.

## Evidence hierarchy

Prefer, in order: peer-reviewed comparative studies; reproducible benchmarks; laboratory technical reports; preprints/whitepapers; expert opinion. Record scope and limitations before generalizing.

## Load-bearing evidence

- **Plan-and-Solve Prompting (ACL 2023):** explicit planning can improve multistep reasoning relative to unstructured zero-shot reasoning in evaluated tasks.
- **ReAct (ICLR 2023):** interleaving reasoning/actions is useful when actions reveal information needed for subsequent decisions.
- **Tree of Thoughts (NeurIPS 2023):** deliberative branching/search can help tasks where candidate states are meaningfully evaluable; it is not a default-cost-free strategy.
- **PlanBench (NeurIPS 2023):** LLMs remain unreliable as autonomous formal planners; external planning/verification primitives should be preferred when sound and available.
- **CRITIC (ICLR 2024) and self-correction literature:** external/tool-grounded feedback is more reliable than unconstrained intrinsic self-critique as a general correction signal.
- **Plan-and-Act (ICML 2025):** separating high-level planning from low-level execution can improve long-horizon agent behavior.
- **DeepPlanning / hierarchical web-agent analyses (2026):** long-horizon constraint handling, information gathering, low-level execution, and replanning are distinct failure surfaces.
- **Agent Planning Benchmark (2026 preprint):** explicitly tests holistic/stepwise planning, irrelevant/broken tools, and unsolvable tasks; useful but newer evidence should be weighted below established peer-reviewed results.

## Policy implication

Do not encode one universal reasoning procedure. Select a planning regime from task observability, feasibility, affordances, constraint structure, and verifier availability; benchmark the resulting policy against baseline behavior.
