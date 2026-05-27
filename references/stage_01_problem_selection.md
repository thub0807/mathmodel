# Legacy Reference: Selection and Framing Heuristics

This file is no longer an active workflow stage in `v1.2-alpha`.

The active workflow assumes a single working problem in `workspace/problem/problem.md`. Use this file only for optional framing help when the problem statement itself contains multiple possible interpretations, approaches, or decomposition strategies.

## What Still Matters

- Compare candidate framings before committing to one decomposition.
- Evaluate whether a candidate framing is data-supported, computationally realistic, and coherent with the final paper goal.
- Surface risks early instead of letting them appear during implementation.

## Reuse in v1.2

This material can inform:
- `workspace/output/question_index.md`
- `q*/solution_plan.md`
- `q*/candidates.md`

## Practical Comparison Questions

- Which framing best matches the real task stated in `problem.md`.
- Which framing uses the available attachments most naturally.
- Which framing leads to a model family that can be validated credibly.
- Which framing avoids overcomplicating a question that only needs a baseline-quality answer.
- Which framing is easiest to explain in the final paper without inventing unsupported claims.

## What Was Removed

- multi-problem or multi-topic selection flow
- topic-letter scoring and lock-in
- competition-specific `topic_specs.json` dependence
- `decision_log`-based candidate ranking
