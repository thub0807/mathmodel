# Final Integration and Evidence Lock

Stage 7 consolidates per-question outputs into project-level evidence before paper generation.

## Required Outputs

- `workspace/output/final_results.md`
- `workspace/output/final_figures_index.md`
- `workspace/output/final_tables_index.md`
- `workspace/output/traceability.md`
- `workspace/output/locked_numbers.md`

## File Roles

### `final_results.md`

Summarize the project-level conclusions assembled from the question summaries.

### `final_figures_index.md`

Index the figures that may appear in the paper, their source question, and their role.

### `final_tables_index.md`

Index the tables that may appear in the paper, their source question, and their role.

### `traceability.md`

Track how each major claim or result maps back to question outputs and evidence files.

### `locked_numbers.md`

Record the hard numbers that are allowed to enter the paper.

## Evidence Rule

- The paper stage may use hard numbers only from `locked_numbers.md`.
- If a number is not locked, it should not appear as a final quantitative claim in the paper.

## Optional Extension

- Do not require `locked_claims.json` by default.
- Complex projects may add it later if tighter claim tracking becomes necessary.
