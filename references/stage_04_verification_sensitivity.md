# Stage 4: Verification and Sensitivity

## Purpose

Verify each `q*` result and test whether important conclusions are stable under reasonable perturbations.

## Required Inputs

```text
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
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

1. Run sanity checks.
   - Check result magnitude, sign, unit, monotonicity, and obvious feasibility.
   - Compare a small toy case or manual calculation when possible.
   - Confirm `result.json` fields match the expected outputs from `model.md`.
2. Check constraints and dimensions.
   - Verify hard constraints, capacity, budget, conservation, domains, and boundary requirements.
   - Confirm units and symbol meanings match `notation.md`.
   - Record any violation in `validation.md`.
3. Check boundary conditions.
   - Test zero, minimum, maximum, empty, extreme, or known-simple cases when meaningful.
   - Explain why a boundary case is not applicable if it cannot be tested.
4. Compare against a baseline.
   - Use the baseline from `candidates.md` when available.
   - Acceptable alternatives include ablation, cross-method comparison, historical reference, or defensible manual calculation.
   - Record whether the main model improves, matches, or underperforms the baseline.
5. Identify key parameters.
   - Use `model.md`, `assumptions.md`, and domain reasoning to choose parameters that could change conclusions.
   - Prioritize parameters tied to cost, capacity, demand, weight, threshold, error rate, or policy scenario.
6. Run parameter perturbation.
   - Vary each key parameter over plausible low, nominal, and high settings.
   - Record perturbation range, source or rationale, output change, and conclusion impact.
7. Run multi-variable joint perturbation.
   - Test combined optimistic, pessimistic, and mixed scenarios.
   - For models with many parameters, choose the 2-4 most influential parameters and justify the selection.
8. Locate instability boundaries.
   - Identify thresholds where feasibility, ranking, classification, or main conclusion changes.
   - Report stable range, conditionally stable range, and failure range.
9. Decide validation status.
   - `PASS`: checks support the result and no high issue remains.
   - `PARTIAL`: result is usable with explicit limitations.
   - `FAIL`: result cannot support paper claims.
10. Update `validation.md` and `sensitivity.md`.
   - `validation.md` records sanity checks, baseline comparison, constraints, boundary cases, failures, and final validation judgment.
   - `sensitivity.md` records key parameters, single-parameter perturbation, joint perturbation, instability boundary, and paper impact.
11. Run local critic and cross-artifact backtrack.
   - Use `references/feedback_layer1_critic.md` for local completeness.
   - Use `references/feedback_layer2_backtrack.md` if validation or sensitivity contradicts earlier Plan, Build, assumptions, or notation.

## Output Contract

`workspace/output/q*/validation.md` must include:

```text
sanity check
baseline or comparison method
constraint satisfaction
boundary conditions
consistency with assumptions and notation
failure cases
PASS/PARTIAL/FAIL judgment
affected claims
```

`workspace/output/q*/sensitivity.md` must include:

```text
key parameters
perturbation ranges
single-parameter results
joint perturbation scenarios
instability boundary
stable or unstable conclusions
paper impact
```

Risks that affect final paper use must be phrased so they can be carried into:

```text
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## Quality Gate

Before Stage 5:

- `validation.md` must state `PASS`, `PARTIAL`, or `FAIL`;
- baseline or comparison must exist, or its absence must be justified;
- constraints and boundary cases must be checked or marked not applicable;
- sensitivity must test important parameters, not decorative parameters;
- joint perturbation must be attempted or its infeasibility explained;
- any `PARTIAL` or `FAIL` risk must be carried forward for final reporting.

## Exit Conditions

- `validation.md` gives a final `PASS`, `PARTIAL`, or `FAIL` validation judgment with evidence.
- `sensitivity.md` states whether the main conclusion is stable, conditionally stable, or unstable.
- Any mismatch between `result.json.status` and validation status is explained.

## Failure Handling

- If validation fails, update or qualify downstream status before Stage 5.
- If sensitivity undermines a result, mark the affected conclusion as limited or unusable.
- If validation contradicts `result.json.status`, record the mismatch and treat the stricter judgment as paper-facing.
- If sensitivity reveals an instability boundary, downstream summaries must state the stable range before using the result.
- If risks need final reporting, write them in wording suitable for later `quality_report.md`.

## Manual Mode Behavior

Pause if verification overturns the selected Plan or makes a previously pass result unusable.

## AP Mode Behavior

Continue only with explicit limitation notes in `validation.md` and `sensitivity.md`.
