# Legacy Reference: Model Selection

This file now supports `per_question_plan.md` and `per_question_build.md`.

## Knowledge To Keep

- Generate at least three candidates per question: baseline, main, and alternative.
- Make the candidates structurally different when possible rather than offering three near-duplicates.
- Record why the selected model fits the question, not just why it sounds sophisticated.
- Prefer model names that describe the actual method or improvement rather than generic textbook labels.
- Run a small toy demo or feasibility probe before committing to an implementation-heavy model.

## Reuse in v1.2

Use this material to strengthen:
- `candidates.md`
- `model.md`
- `solution_plan.md`

## Recommended Selection Heuristics

- Fit to the real task and evidence.
- solver or implementation feasibility.
- expected validation path.
- interpretability in the paper.
- fallback options if the main method underperforms.

## What Was Removed

- championship-only branching as workflow control
- `decision_log` storage requirements
- harness-specific question prompts
- stage-based gating rules
