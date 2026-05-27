# Paper Generation Protocol

Stage 8 assembles the final paper from audited and locked project outputs.

## Required Outputs

- `workspace/output/final/paper.md`
- `workspace/output/final/paper.tex`
- `workspace/output/final/paper.pdf`
- `workspace/output/final/source/`

## Required Inputs

Build the paper from:
- per-question summaries
- `workspace/output/final/final_results.md`
- `workspace/output/final/locked_numbers.md`

Do not introduce new quantitative results during paper drafting.

## Asset Reuse

Reuse the valuable existing assets progressively:
- `templates/latex/`
- competition-specific abstract templates
- phrase banks
- paper skeletons
- anti-pattern references

## Current Alpha Scope

- In `v1.2-alpha`, keep the paper-generation interface stable even if some template adaptation remains lightweight.
- It is acceptable for this stage to rely on existing LaTeX assets with TODO-level integration notes, as long as the workflow contract is clear.

## Source Directory

`workspace/output/final/source/` should hold the assembled markdown, LaTeX fragments, bibliographic helpers, or other paper-source materials needed to regenerate the final document.
