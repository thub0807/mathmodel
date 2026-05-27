# Feedback Layer 1: Local Critic

Layer 1 is the first-pass self-check for a single artifact or a tightly related artifact packet.

Use it for:
- `solution_plan.md`
- `validation.md`
- `q_i_summary.md`
- `paper.md` or section drafts

## Goal

Catch the most important local problems early and suggest targeted fixes without forcing a full rewrite.

## Recommended Process

1. Read the target artifact.
2. Score it against the relevant rubric section in `rubrics.md`.
3. List a short set of concrete issues.
4. Apply targeted edits only where needed.
5. Recheck once or twice if the artifact changed materially.

## Output Shape

Keep the review compact:

```json
{
  "artifact": "solution_plan.md",
  "scores": {
    "problem_fit": 8,
    "candidate_quality": 7,
    "assumption_quality": 6,
    "notation_quality": 7,
    "build_readiness": 8
  },
  "issues": [
    {
      "severity": "medium",
      "where": "assumptions.md",
      "fix": "Make A2 explicit and explain why it is acceptable for q1."
    }
  ],
  "verdict": "pass_with_edits"
}
```

## Good Uses in v1.2

- plan check before Manual review handoff
- validation quality check before evidence lock
- summary check before final integration
- local paper-section cleanup before final review

## Avoid

- turning this layer into a workflow state machine
- scoring for competition-topic selection
- requiring legacy state files to run the check
