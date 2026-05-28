# Stage 5: Figures and Tables

## Purpose

Create figure and table indexes that make every visual artifact traceable to data, code, and conclusions.

## Required Inputs

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/code/
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

1. List every generated or intended figure in `figure_index.md`.
2. List every generated or intended table in `table_index.md`.
3. For data figures, record data source, code source, result field, and validation status.
4. Mark conceptual diagrams as `conceptual` and state what they illustrate.
5. Exclude visuals that cannot be traced to a source.

## Exit Conditions

- Each figure and table has a source path, data source, intended paper use, and validation status.
- Unavailable or rejected visuals are documented rather than silently omitted.

## Failure Handling

- If a figure or table source is unclear, do not allow it into the final paper.
- If a missing visual affects the explanation, write the limitation into `warnings.md` or final review.

## Manual Checkpoint Behavior

Usually continue. Pause only if figure/table choices change a scientific conclusion.

## AP Mode Behavior

Continue with source-backed visuals and carry all visual limitations forward.
