# Stage 5: Figures and Tables

## Purpose

Create figure and table indexes that make every visual artifact traceable to data, code, and conclusions.

## Required Inputs

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/code/
competitions/cumcm/distilled_formats.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
```

## Required Outputs

```text
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
```

## Templates

```text
templates/workspace/q/figures/figure_index.md
templates/workspace/q/figures/figure_check.md
templates/workspace/q/tables/table_index.md
templates/workspace/q/tables/table.md
```

## Entry Conditions

- Stage 4 has produced validation and sensitivity outputs, or a limitation is recorded.
- Any data figure or table can be tied back to `result.json`, code, or source material.

## Procedure

1. Decide the paper role of each visual before listing it.
   - A figure or table should support a claim, explain a method, diagnose reliability, or summarize a result.
   - Do not keep visuals that are merely decorative or disconnected from the paper argument.
2. Classify each figure.
   - `data figure`: plotted from result fields, processed data, or source attachments.
   - `diagnostic figure`: validates fit, residuals, convergence, feasibility, sensitivity, or baseline comparison.
   - `conceptual figure`: explains model structure, workflow, dependency, or mechanism; it must be labeled conceptual.
3. List every generated or intended figure in `figure_index.md`.
4. List every generated or intended table in `table_index.md`.
5. Bind every figure and table to a paper claim.
   - Record the supported claim, source file, source field, validation status, intended paper section, and citation location.
   - For data figures and result tables, source fields should point to `result.json`, `validation.md`, `sensitivity.md`, or source data.
6. Apply CUMCM caption and format discipline.
   - Use `competitions/cumcm/distilled_formats.md` for figure titles, table titles, numbering style, notes, and formula/table references.
   - Use concise captions that state what the reader should notice.
7. Check visual quality against `competitions/cumcm/winning_patterns.md`.
   - Prefer visuals that reveal model structure, result comparison, sensitivity, or answer logic.
   - Avoid thin visuals that only repeat a number already written in text.
8. Check visual anti-patterns against `competitions/cumcm/anti_patterns.md`.
   - Flag missing titles, missing units, untraceable data, default-looking charts, unsupported conclusions, and mismatched numbering.
9. Exclude or downgrade visuals that cannot be traced to a source.

## Output Contract

`figure_index.md` and `table_index.md` must record:

```text
visual id
type: data / diagnostic / conceptual
title or caption
supported claim
source file
source field
generation code or manual source
validation status
intended paper section
body citation location
limitations or notes
include in paper: yes / no
```

Each table file created from `templates/workspace/q/tables/table.md` must include source, column meaning, units, and supported conclusion.

## Quality Gate

Before Stage 6:

- every included visual has a claim and source;
- every data figure/table traces to a result, validation, sensitivity, source material, or code output;
- every diagnostic visual states what reliability question it answers;
- every conceptual figure is marked conceptual and does not pretend to be data;
- captions and notes are suitable for a CUMCM-style paper;
- visuals that trigger anti-patterns are fixed or excluded.

## Exit Conditions

- Each figure and table has a source path, data source, intended paper use, and validation status.
- Unavailable or rejected visuals are documented rather than silently omitted.

## Failure Handling

- If a figure or table source is unclear, do not allow it into the final paper.
- If a missing visual affects the explanation, write the limitation into `warnings.md` or final review.
- If a visual supports a claim that later becomes `partial` or `fail`, update the index and carry the limitation forward.

## Manual Mode Behavior

Usually continue. Pause only if figure/table choices change a scientific conclusion.

## AP Mode Behavior

Continue with source-backed visuals and carry all visual limitations forward.
