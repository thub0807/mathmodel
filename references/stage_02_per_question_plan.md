# Stage 2: Per-Question Plan

## Purpose

Create a reviewable Plan file set for each `q*` before any build, solve, or verification work.

## Required Inputs

```text
workspace/output/question_index.md
workspace/output/problem_audit.md
workspace/output/material_index.md
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
```

## Required Outputs

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode or if needed
```

## Templates

```text
templates/workspace/q/analysis.md
templates/workspace/q/candidates.md
templates/workspace/q/model.md
templates/workspace/q/assumptions.md
templates/workspace/q/notation.md
templates/workspace/q/data_recon.md
templates/workspace/q/warnings.md
templates/workspace/q/review_note.md
```

## Entry Conditions

- Stage 1 has produced `question_index.md`.
- The current `q*` has defined inputs, outputs, dependencies, and materials.

## Procedure

1. Read `references/model_catalog.md` to map the current `q*` task type to plausible model families.
2. Read `references/rubrics.md` and the Plan section of `references/feedback_layer1_critic.md` to define quality expectations.
3. Write `analysis.md` with target, inputs, outputs, dependencies, attachments, evaluation criteria, and paper-facing answer form.
4. Generate at least three candidate models or explain why fewer than three are defensible.
   - Include a baseline candidate whenever possible.
   - Include a main model candidate.
   - Include a robust or alternative candidate when data and time allow.
5. Write `candidates.md` with a comparison matrix:

```text
candidate
model family
fit to q*
data requirements
interpretability
competition-paper expressiveness
implementation risk
validation route
reason kept or rejected
```

6. Select the final model route.
   - State why the selected model fits the task, data, constraints, and expected paper explanation.
   - State why rejected candidates are weaker.
   - If no candidate is strong, write `warnings.md` and pause in Manual mode.
7. Create model naming variants.
   - Give the selected model a concise paper-facing name.
   - Avoid inflated novelty; the name should describe the actual mechanism.
   - Record alternate names in `model.md` or `candidates.md` when useful.
8. Write `model.md` with selected model, variables, formulas, constraints, objective or evaluation metric, algorithm, expected `result.json` fields, and verification plan.
9. Plan a toy demo or minimal feasibility check.
   - Define the smallest input that can exercise the model.
   - Define the expected qualitative output.
   - Define what failure would block Stage 3.
10. Write `assumptions.md` with source-backed assumptions, reason, impact, and how each assumption could fail.
11. Write `notation.md` with symbols, units, domains, and source files.
12. Write `data_recon.md` with data sources, preprocessing plan, missing data, abnormal values, and trace plan.
13. Perform a red-team risk attack.
   - Ask how the selected route could fail mathematically, computationally, or in paper review.
   - Record responses in `review_note.md` or `warnings.md`.
14. Write `warnings.md` when a material gap, strong assumption, model fragility, or unresolved risk exists.

## Output Contract

The Plan file set for each `q*` must include enough detail for Stage 3 to build without inventing a new route:

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode or risky route
```

`candidates.md` must contain either at least three candidates or an explicit shortage reason.

`model.md` must name the selected model, expected result fields, and minimal feasibility check.

## Quality Gate

Before Stage 3:

- candidate comparison must be specific, not generic;
- selected model must match the data and the expected answer form;
- formulas and variables must be clear enough to implement;
- assumptions must be visible and tied to source material or domain reasoning;
- data plan must explain preprocessing and missing data handling;
- high risks must appear in `warnings.md` or `review_note.md`;
- Manual mode must pause after the Plan and list file paths only.

## Exit Conditions

- The Plan file set exists for each planned `q*`.
- Model choice, data plan, assumptions, notation, and risks are clear enough for Build.
- Manual mode has paused after each `q*` Plan and shown file paths only.

## Failure Handling

- If a modeling route cannot be selected, write the competing options and pause for user confirmation.
- If data or materials are insufficient, write `warnings.md` and do not hide the limitation.
- If fewer than three candidates are possible, record the reason in `candidates.md` and strengthen the baseline or toy demo plan.
- If red-team review finds a blocking issue, do not enter Stage 3 until the route is revised or accepted with a visible limitation.

## Manual Mode Behavior

After each `q*` Plan, pause before Stage 3 and list only the generated Plan file paths for review.

## AP Mode Behavior

Continue without waiting, but write `review_note.md` explaining why the selected route is acceptable.
