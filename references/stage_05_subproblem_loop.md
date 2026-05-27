# Legacy Reference: Per-Question Execution Loop

This file now acts as background guidance for:
- `per_question_build.md`
- `verification_protocol.md`
- `figures_tables_protocol.md`

## Knowledge To Keep

- Treat each question as a small pipeline: model completion, implementation, verification, sensitivity, interpretation, and summary.
- Make reuse across questions explicit when one question depends on the outputs of another.
- Save runnable code and machine-readable results, not just prose conclusions.
- Add at least one interpretation step so results are not left as raw numbers.

## A Useful Per-Question Rhythm

1. Complete the question-specific model.
2. Implement the solve path in the locked language.
3. Record outputs in `results/result.json` and `results/run.log`.
4. Verify with boundary checks, baseline comparison, and targeted validation.
5. Run sensitivity where the result is parameter-dependent.
6. Produce figures, tables, and `q_i_summary.md`.

## Reuse in v1.2

Use this material to improve:
- `code/`
- `results/result.json`
- `validation.md`
- `sensitivity.md`
- `q_i_summary.md`

## What Was Removed

- recursive stage contract semantics
- per-Qi verdict machinery as active workflow control
- `decision_log` writes, weights, and review queues
- script-driven gating as a required step
