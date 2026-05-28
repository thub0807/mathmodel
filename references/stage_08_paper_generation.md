# Stage 8: Paper Generation

## Purpose

Generate the final paper from validated and traceable artifacts only.

## Required Inputs

```text
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

## Required Outputs

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

## Templates

```text
templates/workspace/final/paper.md
templates/workspace/final/paper.tex
templates/workspace/final/source/README.md
templates/latex/cumcm/
```

## Entry Conditions

- Stage 7 outputs exist.
- `traceability.md` marks the claims allowed for paper and abstract use.
- No untraceable hard number is required for the intended paper conclusion.

## Procedure

1. Draft `paper.md` from `q*_summary.md`, `final_results.md`, and traceable figure/table indexes.
2. Use only claims whose source files and validation status are recorded in `traceability.md`.
3. Convert or prepare `paper.tex` using the available LaTeX template and safe placeholders for missing formal fields.
4. Generate `paper.pdf` when the environment supports it.
5. Store copied paper assets under `workspace/output/final/source/`.

## Exit Conditions

- `paper.md` and `paper.tex` do not introduce unsupported claims.
- Any generated `paper.pdf` corresponds to the current `paper.tex`.
- PDF generation failure is recorded for final review instead of hidden.

## Failure Handling

- If a claim is not traceable, remove it or rewrite it as a clearly limited statement.
- If PDF generation fails, record the command, error, and affected output in Stage 9 reports.

## Manual Checkpoint Behavior

After generation, list `paper.md`, `paper.tex`, `paper.pdf` if present, and any failure record paths.

## AP Mode Behavior

Continue to Stage 9 with all generation warnings preserved.
