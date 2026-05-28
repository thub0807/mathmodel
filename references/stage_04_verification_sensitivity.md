# Stage 4: Verification and Sensitivity

## Purpose

Verify each `q*` result and test whether important conclusions are stable under reasonable perturbations.

## Required Inputs

```text
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
```

## Required Outputs

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

## Templates

```text
templates/workspace/q/validation.md
templates/workspace/q/sensitivity.md
```

## Entry Conditions

- Stage 3 has produced `result.json`.
- `result.json.status` is present and is `pass`, `partial`, or `fail`.

## Procedure

1. Check constraints, dimensions, boundary cases, feasibility, and consistency with assumptions.
2. Compare against a baseline, ablation, cross-method result, or defensible manual calculation.
3. Define sensitive parameters, perturbation ranges, and expected direction of change.
4. Record how validation and sensitivity affect paper claims.

## Exit Conditions

- `validation.md` gives a final `PASS`, `PARTIAL`, or `FAIL` validation judgment with evidence.
- `sensitivity.md` states whether the main conclusion is stable, conditionally stable, or unstable.
- Any mismatch between `result.json.status` and validation status is explained.

## Failure Handling

- If validation fails, update or qualify downstream status before Stage 5.
- If sensitivity undermines a result, mark the affected conclusion as limited or unusable.

## Manual Checkpoint Behavior

Pause if verification overturns the selected Plan or makes a previously pass result unusable.

## AP Mode Behavior

Continue only with explicit limitation notes in `validation.md` and `sensitivity.md`.
