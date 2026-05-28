# Stage 2: Per-Question Plan

## Purpose

Create a reviewable Plan file set for each `q*` before any build, solve, or verification work.

## Required Inputs

```text
workspace/output/question_index.md
workspace/output/problem_audit.md
workspace/output/material_index.md
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

1. Write `analysis.md` with target, inputs, outputs, dependencies, attachments, and evaluation criteria.
2. Write `candidates.md` with compared candidate routes and rejection reasons.
3. Write `model.md` with selected model, formulas, constraints, objective, algorithm, and expected result form.
4. Write `assumptions.md` with source-backed assumptions and impact.
5. Write `notation.md` with symbols, units, domains, and source files.
6. Write `data_recon.md` with data sources, preprocessing plan, missing data, and trace plan.
7. Write `warnings.md` when a material gap, strong assumption, or unresolved risk exists.

## Exit Conditions

- The Plan file set exists for each planned `q*`.
- Model choice, data plan, assumptions, notation, and risks are clear enough for Build.
- Manual mode has paused after each `q*` Plan and shown file paths only.

## Failure Handling

- If a modeling route cannot be selected, write the competing options and pause for user confirmation.
- If data or materials are insufficient, write `warnings.md` and do not hide the limitation.

## Manual Checkpoint Behavior

After each `q*` Plan, pause before Stage 3 and list only the generated Plan file paths for review.

## AP Mode Behavior

Continue without waiting, but write `review_note.md` explaining why the selected route is acceptable.
