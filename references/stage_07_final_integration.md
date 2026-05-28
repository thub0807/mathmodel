# Stage 7: Final Integration

## Purpose

Integrate all `q*` summaries into final results, final visual indexes, and a traceability chain for paper generation.

## Required Inputs

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
```

## Required Outputs

```text
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

## Templates

```text
templates/workspace/final/final_results.md
templates/workspace/final/final_figures_index.md
templates/workspace/final/final_tables_index.md
templates/workspace/final/traceability.md
```

## Entry Conditions

- At least one `q*` has a completed `q*_summary.md`.
- Each included result has a declared `pass`, `partial`, or `fail` status.

## Procedure

1. Merge usable per-question conclusions into `final_results.md`.
2. Merge figure and table indexes into final indexes.
3. Build `traceability.md` for paper claims, source question, source file, source field, validation status, abstract eligibility, and limitation note.
4. Exclude or clearly limit `fail` and `partial` artifacts.

## Exit Conditions

- `traceability.md` can trace every hard number, figure claim, table claim, assumption, and symbol used in final results.
- `final_results.md` does not present `fail` artifacts as conclusions.
- Abstract-eligible claims are explicitly marked.

## Failure Handling

- Remove or mark untraceable claims before Stage 8.
- Record symbol, unit, or cross-question conflicts for Stage 9 review.

## Manual Checkpoint Behavior

Recommended pause before Stage 8. List final file paths for user review.

## AP Mode Behavior

Continue to Stage 8 only with traceability limitations preserved.
