# Feedback Layer 4: Calibration Check

Layer 4 is an optional meta-check for important reviews when you want to see whether a strong score is real or merely prompt-shaped.

Use it sparingly for:
- high-confidence `solution_plan.md` reviews
- unusually clean `validation.md` reviews
- polished `q_i_summary.md` reviews
- final paper passes that feel suspiciously easy

## Goal

Recheck a strong artifact from a different angle and see whether the conclusion still holds.

## Calibration Moves

- swap from rubric-style scoring to scenario-style judgment
- ask for failure reasons instead of success reasons
- ask for the strongest objection first
- compare whether the same artifact still looks strong under a different framing

## Example Questions

- What is the strongest reason this plan could fail during build?
- Which validation claim is least convincing and why?
- Which summary sentence overstates the evidence?
- What would make a skeptical reviewer hesitate?

## Output Shape

```json
{
  "artifact": "validation.md",
  "original_verdict": "strong_pass",
  "calibration_verdict": "still_strong",
  "largest_gap": "Cross-method comparison is thinner than the first review implied."
}
```

## Good Uses in v1.2

- final AP-mode quality checks
- high-stakes paper polishing
- sanity-checking overconfident internal reviews

## Avoid

- running it by default on every artifact
- treating it as a legacy iterative score reset system
