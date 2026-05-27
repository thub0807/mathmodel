# Verification Protocol

Stage 4 verifies the build outputs for each question workspace.

## Required Outputs

- `code/verify_qi.py`
- `validation.md`
- `sensitivity.md`

## `validation.md`

Include these sections:
- constraint checks
- boundary checks
- numerical stability
- baseline comparison
- ablation or cross-method check
- failure cases
- final `PASS` or `FAIL`

Use concise evidence tables when useful. Record what was tested, what passed, what failed, and what that means for later writing.

## `sensitivity.md`

Include:
- sensitive parameters
- perturbation ranges
- result changes
- stability interpretation
- paper impact

The goal is to show whether the reported conclusion is stable enough to keep as locked evidence.

## Optional Exact Check

- For optimization-heavy questions, use a small-instance exact check when feasible.
- Record how the reduced instance was constructed and what it confirms or fails to confirm.

## Default Posture

- Verification is a normal per-question step, not an optional supervisor workflow.
- Do not require heartbeat, supervisor, or orchestration layers as part of the default protocol.
