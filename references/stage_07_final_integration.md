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
workspace/output/q*/model.md
references/feedback_layer2_backtrack.md
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

1. Harmonize symbols, units, and model names.
   - Merge duplicate symbols or rename conflicts before paper generation.
   - Keep model names concise and consistent across `q*_summary.md`, `final_results.md`, and paper text.
2. Integrate cross-question dependencies.
   - Record which result, parameter, or assumption from one `q*` feeds another `q*`.
   - Confirm downstream questions do not use obsolete or failed upstream results.
3. Resolve result conflicts.
   - Compare summaries, validation, sensitivity, and result status.
   - If two results disagree, prefer the validated source or mark both with limitation.
   - Use `references/feedback_layer2_backtrack.md` when conflicts affect earlier assumptions, notation, or claims.
4. Merge usable per-question conclusions into `final_results.md`.
   - Mark each result as abstract-eligible or body-only.
   - Do not mark a `fail` result as abstract-eligible.
   - Mark `partial` results with limitation text.
5. Merge figure and table indexes into final indexes.
   - Preserve supported claim, source file, source field, validation status, and intended paper section.
6. Build `traceability.md`.
   - Map each paper claim to source question, source file, source field, validation status, abstract eligibility, and limitation note.
   - For hard numeric claims, prefer direct mapping to `workspace/output/q*/results/result.json` fields.
7. Propagate limitations.
   - Any `partial` or `fail` status from `result.json`, `validation.md`, or `sensitivity.md` must appear in `final_results.md` and `traceability.md`.

## Output Contract

`final_results.md` must include:

```text
final result id
source q*
claim
hard numbers and units
status
abstract eligibility
limitation note
source files
```

`traceability.md` must include:

```text
paper claim
source question
source file
source field
validation status
allowed in abstract
limitation note
```

`final_figures_index.md` and `final_tables_index.md` must preserve claim binding and citation location.

## Quality Gate

Before Stage 8:

- symbols, units, and model names are consistent across questions;
- cross-question dependencies are recorded;
- result conflicts are resolved or visibly limited;
- final results mark abstract eligibility;
- every paper-facing hard claim has a traceability row;
- `partial` and `fail` restrictions are carried forward.

## Exit Conditions

- `traceability.md` can trace every hard number, figure claim, table claim, assumption, and symbol used in final results.
- `final_results.md` does not present `fail` artifacts as conclusions.
- Abstract-eligible claims are explicitly marked.

## Failure Handling

- Remove or mark untraceable claims before Stage 8.
- Record symbol, unit, or cross-question conflicts for Stage 9 review.
- If a conflict invalidates a result, return to the affected `q*` artifact or mark the result unusable for paper conclusions.

## Manual Mode Behavior

Recommended pause before Stage 8. List final file paths for user review.

## AP Mode Behavior

Continue to Stage 8 only with traceability limitations preserved.
