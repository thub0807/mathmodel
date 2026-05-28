# Stage 3: Per-Question Build

## Purpose

Implement the confirmed Plan for each `q*`, run the solve or computation, and create the result gate.

## Required Inputs

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
references/rubrics.md
references/feedback_layer1_critic.md
```

## Required Outputs

```text
workspace/output/q*/code/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

## Templates

```text
templates/workspace/q/code/README.md
templates/workspace/q/results/result.schema.json
templates/workspace/q/results/result.example.json
templates/workspace/q/results/run_log.md
```

## Entry Conditions

- Stage 2 Plan exists for the current `q*`.
- Manual mode has received user confirmation, or AP mode has written `review_note.md`.
- Required data paths and preprocessing decisions are recorded in `data_recon.md`.

## Procedure

1. Complete the model before coding.
   - Translate the selected model into implementable formulas, constraints, objective or metric, and algorithm steps.
   - Confirm every symbol used in code appears in `notation.md`.
   - Confirm every assumption needed by the implementation appears in `assumptions.md`.
2. Implement data preprocessing.
   - Read only indexed materials and paths described in `data_recon.md`.
   - Record cleaning, filtering, unit conversion, missing value handling, and abnormal value handling.
   - Preserve intermediate outputs when they are needed for audit or later figures.
3. Place all solve, verification-prep, figure-prep, and data-processing code under `workspace/output/q*/code/`.
4. Run the implementation in the locked implementation language.
5. Generate results.
   - Produce the expected fields described in `model.md`.
   - Include objective values, predictions, rankings, classifications, fitted parameters, scenario outcomes, or other task-specific outputs.
   - Include enough metadata to support traceability and rerun.
6. Handle exceptions explicitly.
   - Solver infeasibility, missing data, convergence failure, unstable estimates, empty outputs, or timeout must be recorded.
   - Do not silently replace a failed result with a guessed value.
7. Write `workspace/output/q*/results/run.log`.
   - Include command, implementation language, environment notes, input files, output files, random seed if relevant, warnings, errors, and runtime notes.
8. Write `workspace/output/q*/results/result.json` according to `templates/workspace/q/results/result.schema.json`.
   - `status` must be exactly `pass`, `partial`, or `fail`.
   - Include warnings and limitations when status is not fully reliable.
   - Align field names with the expected fields stated in `model.md`.
9. Add a physical, business, or practical meaning note.
   - Record this in `result.json` fields when the schema allows, or in `run.log` as interpretation notes for Stage 4 and Stage 6.
   - The note should explain what the number means, not only repeat it.
10. Run a local quality critic from `references/feedback_layer1_critic.md`.
   - If it finds high issues, update `run.log`, `result.json`, or `warnings.md` before Stage 4.

## Output Contract

`workspace/output/q*/code/` must contain implementation files or a README explaining why no executable code was possible.

`workspace/output/q*/results/run.log` must record:

```text
command
inputs
outputs
implementation language
environment notes
preprocessing notes
warnings
errors
runtime or solver notes
interpretation notes
```

`workspace/output/q*/results/result.json` must align conceptually with:

```text
templates/workspace/q/results/result.schema.json
```

Hard numbers intended for paper use must appear in `result.json` before they can enter summaries, traceability, or final paper text.

## Quality Gate

Before Stage 4:

- code path exists and is auditable;
- preprocessing follows `data_recon.md`;
- formulas in code match `model.md`;
- units match `notation.md`;
- assumptions needed by code are recorded;
- `run.log` explains success or failure;
- `result.json.status` is present and justified;
- unverified results are not written as final conclusions.

## Exit Conditions

- `result.json` exists and validates conceptually against `templates/workspace/q/results/result.schema.json`.
- `result.json.status` is exactly one of `pass`, `partial`, or `fail`.
- `run.log` explains how results were produced or why they failed.

## Failure Handling

- If execution fails, write `run.log`, set `result.json.status` to `fail` or `partial`, and preserve useful diagnostics.
- Do not promote hard numbers to paper-facing artifacts unless they appear in `result.json` with trace fields.
- If data preprocessing changes the modeling route, return to Stage 2 for the affected `q*` or write a limitation in `review_note.md`.
- If the toy demo or minimal feasibility check fails, mark the route as blocked unless a revised route is recorded.

## Manual Mode Behavior

Usually continue to Stage 4. If status is `partial` or `fail`, summarize the limitation and affected files.

## AP Mode Behavior

Continue to Stage 4, carrying all warnings into validation and traceability.
