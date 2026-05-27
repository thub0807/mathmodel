# Figures and Tables Protocol

Stage 5 organizes visual and tabular outputs for each question workspace.

## Required Outputs

- `figures/`
- `tables/`

## Default Structure

- Use a light default structure.
- Store only the files needed to support the question summary, final integration, and paper.
- Complex projects may use per-figure subdirectories, but that is optional rather than default.

## Figure Rules

- Data figures must state or imply their source in the surrounding markdown or in the index later.
- Conceptual figures should be labeled `conceptual`.
- Conceptual figures must not be used as numerical evidence.

## Table Rules

- Tables should align with `result.json`, `validation.md`, or `sensitivity.md`.
- If a table contains hard numbers, those numbers must remain traceable into evidence lock.

## Practical Goal

- Keep figures and tables easy to cite later from `q_i_summary.md`, final integration files, and the paper.
