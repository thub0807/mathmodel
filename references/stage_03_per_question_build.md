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
templates/workspace/q/results/run.log
```

## Entry Conditions

- Stage 2 Plan exists for the current `q*`.
- Manual mode has received user confirmation, or AP mode has written `review_note.md`.
- Required data paths and preprocessing decisions are recorded in `data_recon.md`.

## Procedure

1. Place all solve, verification-prep, figure-prep, and data-processing code under `workspace/output/q*/code/`.
2. Run the implementation in the locked implementation language.
3. Write `workspace/output/q*/results/run.log` with command, inputs, outputs, environment notes, warnings, and failures.
4. Write `workspace/output/q*/results/result.json` according to the schema.

## Exit Conditions

- `result.json` exists and validates conceptually against `templates/workspace/q/results/result.schema.json`.
- `result.json.status` is exactly one of `pass`, `partial`, or `fail`.
- `run.log` explains how results were produced or why they failed.

## Failure Handling

- If execution fails, write `run.log`, set `result.json.status` to `fail` or `partial`, and preserve useful diagnostics.
- Do not promote hard numbers to paper-facing artifacts unless they appear in `result.json` with trace fields.

## Manual Checkpoint Behavior

Usually continue to Stage 4. If status is `partial` or `fail`, summarize the limitation and affected files.

## AP Mode Behavior

Continue to Stage 4, carrying all warnings into validation and traceability.
