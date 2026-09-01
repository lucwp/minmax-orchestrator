# Verification Evidence Policy

## Purpose

Match the verification method to the kind of truth being claimed. Verification is strongest when the evidence source is structurally capable of disproving the claim, not merely when another model agrees with it.

Core rule:

`claim type -> strongest reasonably available matching evidence`

Do not use model knowledge, executor self-report, or same-model semantic judgment as a substitute for direct external evidence when the claim is about the external world and such evidence is reasonably available.

## Truth domains and preferred evidence

| Truth domain | Preferred evidence |
| --- | --- |
| deterministic artifact/result | deterministic test, assertion, schema, compiler, render check |
| authoritative system state | authoritative state read from the owning system |
| external mutation/action | transaction receipt plus authoritative read-back when useful |
| external-world factual claim | authoritative external source; otherwise tool-grounded external evidence |
| qualitative/semantic criterion | independent reviewer when failure cost justifies it; otherwise bounded semantic rubric |

Use the evidence closest to the source of truth. Web research is not automatically stronger than a deterministic test or an authoritative system read.

## External-world claims

A claim is `external_world` when its truth depends on facts outside the current artifact/runtime state, such as current product capabilities, laws, prices, scientific findings, company facts, benchmarks, public events, or claims about what external evidence says.

When an external-world claim is load-bearing:

1. identify the exact claim that must be verified;
2. determine whether a current authoritative external source or grounded tool is reasonably available;
3. acquire that evidence before terminal PASS;
4. prefer primary/authoritative sources when practical, then strong independent sources appropriate to the domain;
5. record provenance and any material limitation;
6. if matching external evidence is not reasonably available, do not silently substitute model memory or self-critique; narrow the claim, mark it `UNCERTAIN`, or state the evidence limitation.

Do not browse merely because browsing exists. If the criterion is local and directly testable, use the local/direct verifier instead.

## Evidence hierarchy

When applicable, prefer:

1. deterministic test/assertion;
2. authoritative state read;
3. transaction/tool receipt bound to the intended action;
4. authoritative external evidence;
5. other tool-grounded external evidence;
6. independent verifier/reviewer;
7. bounded semantic judgment with explicit rubric;
8. same-model semantic feedback, auxiliary only.

This is a default priority, not a license to use a mismatched higher-ranked source. A deterministic unit test cannot establish a current legal requirement; an external article cannot prove that a local write actually occurred.

## Same-model feedback

Same-model feedback may:

- identify candidate errors;
- propose a repair hypothesis;
- point to evidence that should be collected.

It must not:

- be the sole terminal evidence for a load-bearing claim when better evidence exists;
- convert an externally unverified claim into PASS;
- independently elevate confidence after the same model generated the claim;
- justify repeated repair cycles without a grounded, actionable delta.

## Structured evidence plans

For load-bearing verification with several claims, or when an external-world claim is terminal, a structured Evidence Plan can make the policy machine-checkable. Use `scripts/validate_evidence_plan.py` when practical.

Minimal shape:

```json
{
  "schema_version": "1.0",
  "claims": [
    {
      "id": "claim-1",
      "truth_domain": "external_world",
      "terminal": true,
      "status": "PASS",
      "matching_evidence_reasonably_available": true,
      "evidence": [
        {"type": "authoritative_external", "source": "named primary source"}
      ],
      "limitations": []
    }
  ]
}
```

The validator is a policy guard, not a fact checker. It checks that the declared evidence class is appropriate and that external claims do not pass on self-report alone. The underlying source still has to be inspected and judged for relevance, authority, freshness, and scope.

## Source rationale

This policy is consistent with evidence from the LLM self-correction literature: reliable external feedback is materially more dependable than unsupported intrinsic self-correction for general tasks, and tool-grounded critique can improve correction quality. The policy does not claim that every external source is correct or that external verification is always required; it requires evidence-source matching.
