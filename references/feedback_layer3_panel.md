# Feedback Layer 3: Multi-Perspective Panel

Layer 3 is a final-review method for environments that can support several independent review passes.

Use it for:
- final paper review
- anti-pattern review
- readiness review before calling the document complete

## Core Idea

Have several perspectives review the paper independently, then merge the findings.

## Recommended Perspectives

- mathematical rigor
- implementation and reproducibility
- writing and presentation
- evidence discipline
- overall reviewer impression

## Output Shape

Each perspective can return a compact result:

```json
{
  "panelist": "evidence_discipline",
  "scores": {
    "traceability": 8,
    "locked_number_use": 9,
    "claim_honesty": 7
  },
  "must_fix": [
    "Two numbers in the conclusion are not clearly tied back to locked evidence."
  ]
}
```

## Aggregation Goal

- identify the weakest perspective
- collect repeated issues across reviewers
- prioritize fixes that affect paper credibility most

## Good Uses in v1.2

- final paper anti-pattern pass
- quality report support
- deciding what to fix before the last PDF pass

## Avoid

- tying this layer to any single harness
- requiring parallel agents when they are unavailable
- using it as an early-stage workflow gate
