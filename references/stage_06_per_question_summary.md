# Stage 6: Per-Question Summary

## Purpose

Convert each `q*` artifact set into a paper-ready summary grounded in results, validation, sensitivity, and figures/tables.

## Required Inputs

```text
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
```

## Required Outputs

```text
workspace/output/q*/q*_summary.md
```

## Templates

```text
templates/workspace/q/q_summary.md
```

## Entry Conditions

- Current `q*` has Build and Verification artifacts.
- Figure and table indexes exist or explicitly state that no visual artifact is used.

## Procedure

1. Summarize the problem goal and modeling route.
2. Extract core formulas, solve steps, main results, and limitations.
3. Include validation and sensitivity conclusions.
4. Link all figures, tables, assumptions, and symbols to their source files.
5. Draft paper-ready paragraphs without adding new hard numbers.

## Exit Conditions

- `q*_summary.md` contains goal, route, formulas, solve process, main result, validation, sensitivity, figure/table index, draft paper text, limitations, and improvements.
- Any `partial` or `fail` result is visibly labeled.

## Failure Handling

- If verification is missing, mark the summary as `partial` or `fail` and limit paper use.
- If summary conflicts with validation, pause and reconcile before Stage 7.

## Manual Checkpoint Behavior

Usually continue. Pause if the summary changes or softens a conclusion the user has already reviewed.

## AP Mode Behavior

Continue with explicit limitation notes.
