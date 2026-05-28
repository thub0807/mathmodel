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
references/rubrics.md
references/feedback_layer1_critic.md
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

1. Treat `q*_summary.md` as a draft paper subsection, not a loose file summary.
2. State the subquestion goal and why the selected model is needed.
3. Write the model motivation.
   - Connect the task type, data condition, constraints, and chosen model family.
   - Mention rejected routes only when it helps justify the selected route.
4. Write the formula and algorithm narrative.
   - Include core variables, objective or metric, constraints, and solve steps.
   - Use notation from `notation.md` and assumptions from `assumptions.md`.
5. Write the result narrative.
   - Use only hard results that appear in `result.json`, `validation.md`, or `sensitivity.md`.
   - Include units, status, and source fields when a number is important.
6. Write validation and sensitivity narrative.
   - Explain sanity checks, baseline comparison, important perturbations, and stable or unstable conclusions.
7. Write limitations and improvement direction.
   - Preserve all `partial` and `fail` limitations.
   - Do not soften a validation failure into a confident result.
8. Attach figure and table references.
   - Use only visuals marked include in paper.
   - State what each visual contributes to the answer.
9. Run a local quality critic from `references/feedback_layer1_critic.md`.
   - Fix unsupported hard numbers, missing limitations, or unclear formula narrative before Stage 7.

## Output Contract

`q*_summary.md` must include:

```text
question goal
model motivation
core assumptions and notation
core formulas
algorithm or solve process
main results with source fields
validation conclusion
sensitivity conclusion
figures and tables for paper use
paper-ready subsection draft
limitations and improvements
status: pass / partial / fail
```

Hard numbers must be copied only from:

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

## Quality Gate

Before Stage 7:

- the summary can be adapted directly into a paper subsection;
- every hard number has a source file and field;
- validation and sensitivity conclusions are visible;
- limitations are near the affected claim;
- figure and table references support specific claims;
- no new result is invented in prose.

## Exit Conditions

- `q*_summary.md` contains goal, route, formulas, solve process, main result, validation, sensitivity, figure/table index, draft paper text, limitations, and improvements.
- Any `partial` or `fail` result is visibly labeled.

## Failure Handling

- If verification is missing, mark the summary as `partial` or `fail` and limit paper use.
- If summary conflicts with validation, pause and reconcile before Stage 7.
- If a paper-ready paragraph needs a number that is not traceable, remove the number or return to Stage 3/4.

## Manual Mode Behavior

Usually continue. Pause if the summary changes or softens a conclusion the user has already reviewed.

## AP Mode Behavior

Continue with explicit limitation notes.
