# Feedback Layer 2: Cross-Artifact Consistency

Layer 2 checks whether later artifacts still agree with earlier commitments and evidence.

Use it after:
- per-question verification
- final integration
- paper assembly

## Goal

Find contradictions, hidden assumption drift, notation drift, or evidence drift before they spread into the final paper.

## What To Compare

- plan versus build
- build versus validation
- question summary versus underlying evidence
- final integration versus question summaries
- paper claims versus `locked_numbers.md`

## Typical Concerns

- a later artifact uses a symbol differently
- an unstated assumption appears during implementation
- a paper claim is stronger than the validated result
- a hard number appears without a traceable source
- a final summary contradicts a per-question result

## Output Shape

```json
{
  "scope": "final integration",
  "checks": [
    {
      "severity": "warning",
      "from": "q2_summary.md",
      "to": "final_results.md",
      "concern": "The final text generalizes beyond the validated scenario range.",
      "fix": "Limit the claim to the tested parameter range and update locked wording."
    }
  ],
  "verdict": "patch_needed"
}
```

## Good Uses in v1.2

- before locking final numbers
- before paper generation
- before final review closes

## Avoid

- full workflow rollback by default
- treating this as a replacement for local validation
- depending on a legacy JSON state controller
