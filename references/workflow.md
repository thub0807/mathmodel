# Workflow

This is the active `v1.2-alpha` workflow for `mathmodel-md-copilot`. It is Markdown-first, agent-first, and single-workspace. The agent reads the problem materials directly, decomposes the work semantically, and advances question by question.

## Stage -1 Project Contract

Create `workspace/output/project_contract.md` before formal modeling.

Record:
- `implementation_language`, default `python`
- `mode`: `AP` or `Manual`
- `parallel_capability`: `available`, `unavailable`, or `unknown`
- source policy
- output policy

## Stage 0 Workspace Reading and Problem Audit

Read:
- `workspace/problem/problem.md`
- `workspace/problem/images/`
- `workspace/problem/attachments/`
- `workspace/problem/reference.pdf`

Write:
- `workspace/output/problem_audit.md`
- `workspace/output/material_index.md`

## Stage 1 Question Decomposition

The agent decomposes the problem from the problem materials and builds one workspace per question.

Write:
- `workspace/output/question_index.md`
- `workspace/output/q1/`
- `workspace/output/q2/`
- later question workspaces as needed

## Stage 2 Per-Question Plan

For each question workspace, write:
- `solution_plan.md`
- `analysis.md`
- `candidates.md`
- `model.md`
- `assumptions.md`
- `notation.md`
- `data_recon.md`

## Stage 2.5 Mode Gate

Manual:
- stop after the question plan files are written
- return review file paths only
- resume build after user review and confirmation

AP:
- continue automatically
- write `review_note.md`
- write `warnings.md`

## Stage 3 Per-Question Build

For each question workspace, write:
- `code/`
- `results/result.json`
- `results/run.log`

## Stage 4 Verification

For each question workspace, write:
- `code/verify_qi.py`
- `validation.md`
- `sensitivity.md`

## Stage 5 Figures and Tables

For each question workspace, write:
- `figures/`
- `tables/`

## Stage 6 Per-Question Summary

For each question workspace, write:
- `q_i_summary.md`

## Stage 7 Final Integration and Evidence Lock

Write:
- `workspace/output/final_results.md`
- `workspace/output/final_figures_index.md`
- `workspace/output/final_tables_index.md`
- `workspace/output/traceability.md`
- `workspace/output/locked_numbers.md`

## Stage 8 Paper Generation

Write:
- `workspace/output/paper.md`
- `workspace/output/paper.tex`
- `workspace/output/paper.pdf`
- `workspace/output/source/`

## Stage 9 Final Review

Write:
- `workspace/output/review_report.md`
- `workspace/output/anonymity_report.md`
- `workspace/output/quality_report.md`

## Loading Notes

- Load supporting references progressively by stage.
- Use `competitions/` assets as optional support for planning, writing, and review.
- Treat legacy state files and legacy scoring helpers as background assets only, not as part of the active workflow.
