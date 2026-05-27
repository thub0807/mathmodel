# Legacy Reference: Problem Analysis

This file now serves as a reference for `per_question_plan.md`, not as an active stage contract.

## Knowledge To Keep

- Restate each question in your own words before modeling.
- Build a question card that clarifies inputs, outputs, constraints, dependencies, and intended objective.
- Separate decision variables, state variables, parameters, and random quantities early.
- Sketch a dependency graph across questions so downstream work reuses upstream results intentionally.
- Scan attachments for schema, missingness, outliers, and field-to-symbol mapping before claiming a model is ready.

## Useful Artifacts

- `analysis.md`
- `data_recon.md`
- `workspace/output/question_index.md`

## Recommended Analysis Moves

- Read `problem.md` multiple times with different purposes: task, constraints, and data.
- Write one compact card per question.
- Build a preliminary variable list before formal notation.
- Map attachment columns to model symbols.
- Note which later questions depend on earlier outputs.

## What Was Removed

- stage frontmatter and execution contract
- old JSON-state writes
- PDF-first assumptions
- fixed subquestion numbering workflow as a control mechanism
