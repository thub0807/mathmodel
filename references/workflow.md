# Active Workflow Index

`mathmodel-copilot` is a fixed-workspace, single-problem, Markdown-first modeling workflow.

## Fixed Paths

| Role | Path |
|---|---|
| Primary problem statement | `workspace/problem/problem.md` |
| Supporting audit material | `workspace/problem/reference.pdf` |
| Images | `workspace/problem/images/` |
| Attachments | `workspace/problem/attachments/` |
| All outputs | `workspace/output/` |

## Execution Rule

Before running a stage, read its stage reference. Before entering the next stage, write the required outputs and fill them according to the listed `templates/workspace/` contracts. A missing, partial, or failed artifact must be recorded in the current stage output and carried into final review.

## Stage Reference Template Output Map

| Stage | Reference | Templates | Required outputs |
|---|---|---|---|
| Stage 0 Workspace Audit | `references/stage_00_workspace_audit.md` | `templates/workspace/root/problem_audit.md`; `templates/workspace/root/material_index.md` | `workspace/output/problem_audit.md`; `workspace/output/material_index.md` |
| Stage 1 Question Decomposition | `references/stage_01_question_decomposition.md` | `templates/workspace/root/question_index.md` | `workspace/output/question_index.md`; `workspace/output/q*/` |
| Stage 2 Per-Question Plan | `references/stage_02_per_question_plan.md` | `templates/workspace/q/analysis.md`; `templates/workspace/q/candidates.md`; `templates/workspace/q/model.md`; `templates/workspace/q/assumptions.md`; `templates/workspace/q/notation.md`; `templates/workspace/q/data_recon.md`; `templates/workspace/q/warnings.md`; `templates/workspace/q/review_note.md` | `workspace/output/q*/analysis.md`; `candidates.md`; `model.md`; `assumptions.md`; `notation.md`; `data_recon.md`; optional `warnings.md`; AP or risk `review_note.md` |
| Stage 3 Per-Question Build | `references/stage_03_per_question_build.md` | `templates/workspace/q/code/README.md`; `templates/workspace/q/results/result.schema.json`; `templates/workspace/q/results/result.example.json`; `templates/workspace/q/results/run.log` | `workspace/output/q*/code/`; `workspace/output/q*/results/result.json`; `workspace/output/q*/results/run.log` |
| Stage 4 Verification and Sensitivity | `references/stage_04_verification_sensitivity.md` | `templates/workspace/q/validation.md`; `templates/workspace/q/sensitivity.md` | `workspace/output/q*/validation.md`; `workspace/output/q*/sensitivity.md` |
| Stage 5 Figures and Tables | `references/stage_05_figures_tables.md` | `templates/workspace/q/figures/figure_index.md`; `templates/workspace/q/figures/figure_check.md`; `templates/workspace/q/tables/table_index.md`; `templates/workspace/q/tables/table.md` | `workspace/output/q*/figures/figure_index.md`; `workspace/output/q*/tables/table_index.md` |
| Stage 6 Per-Question Summary | `references/stage_06_per_question_summary.md` | `templates/workspace/q/q_summary.md` | `workspace/output/q*/q*_summary.md` |
| Stage 7 Final Integration | `references/stage_07_final_integration.md` | `templates/workspace/final/final_results.md`; `templates/workspace/final/final_figures_index.md`; `templates/workspace/final/final_tables_index.md`; `templates/workspace/final/traceability.md` | `workspace/output/final/final_results.md`; `final_figures_index.md`; `final_tables_index.md`; `traceability.md` |
| Stage 8 Paper Generation | `references/stage_08_paper_generation.md` | `templates/workspace/final/paper.md`; `templates/workspace/final/paper.tex`; `templates/workspace/final/source/README.md`; `templates/latex/cumcm/` | `workspace/output/final/paper.md`; `paper.tex`; `paper.pdf`; `source/` |
| Stage 9 Final Review | `references/stage_09_final_review.md` | `templates/workspace/final/review_report.md`; `templates/workspace/final/anonymity_report.md`; `templates/workspace/final/quality_report.md` | `workspace/output/final/review_report.md`; `anonymity_report.md`; `quality_report.md` |

## Supporting Contracts

| Contract | File |
|---|---|
| Workspace and template contract | `references/workspace_protocol.md` |
| Manual and AP modes | `references/modes_ap_manual.md` |
| Result traceability | `references/result_traceability.md` |
| Quality gate | `references/quality_gate.md` |

## Next Stage Rule

A stage may enter the next stage only when its required outputs exist, required fields are filled with source-backed content, and any `partial` or `fail` condition has a written limitation note.
