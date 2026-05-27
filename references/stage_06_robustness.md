# Legacy Reference: Robustness and Sensitivity

This file now supports `verification_protocol.md`.

## Knowledge To Keep

- Choose parameters that genuinely matter to the reported conclusion.
- Prefer realistic perturbation ranges over arbitrary ones.
- Multivariate sensitivity is usually more informative than a single-parameter-only story.
- Record both stable regions and failure regions.
- For optimization-heavy tasks, a small-instance exact check can be valuable when feasible.

## Reuse in v1.2

Apply this guidance in:
- `validation.md`
- `sensitivity.md`
- `locked_numbers.md`

## Useful Checks

- constraint preservation under perturbation
- stability of rankings or decisions
- stability of headline metrics
- existence of threshold effects or failure modes
- practical interpretation for the final paper

## What Was Removed

- old stage frontmatter
- mode-specific branching as control logic
- old JSON-state backtracking protocol
