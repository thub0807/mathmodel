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

## Layer Roles

| Layer | Role | Paths |
|---|---|---|
| Workflow control | Stage order, fixed paths, mode behavior, output lifecycle | `SKILL.md`; `references/workspace_protocol.md`; `references/workflow.md`; `references/modes_ap_manual.md`; `references/stage_00...stage_09...` |
| Modeling and quality | Model selection, rubrics, feedback, traceability, quality gates | `references/model_catalog.md`; `references/rubrics.md`; `references/feedback_layer*.md`; `references/result_traceability.md`; `references/quality_gate.md` |
| Competition and output | CUMCM writing-quality knowledge, formal rendering assets, artifact contracts | `competitions/cumcm/`; `templates/latex/cumcm/cumcmthesis/`; `templates/workspace/` |

`templates/workspace/` is the artifact contract library.

`competitions/` is competition writing-quality knowledge.

`templates/latex/` is final rendering asset storage.

## Stage Knowledge Template Output Map

| Stage | Reference | Knowledge Layer | Template/Asset | Required outputs |
|---|---|---|---|---|
| Stage 0 Workspace Audit | `references/stage_00_workspace_audit.md` | `references/workspace_protocol.md` | `templates/workspace/root/problem_audit.md`; `templates/workspace/root/material_index.md` | `workspace/output/problem_audit.md`; `workspace/output/material_index.md` |
| Stage 1 Question Decomposition | `references/stage_01_question_decomposition.md` | `references/workspace_protocol.md`; `references/rubrics.md` as needed | `templates/workspace/root/question_index.md` | `workspace/output/question_index.md`; `workspace/output/q*/` |
| Stage 2 Per-Question Plan | `references/stage_02_per_question_plan.md` | `references/model_catalog.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md` | `templates/workspace/q/analysis.md`; `templates/workspace/q/candidates.md`; `templates/workspace/q/model.md`; `templates/workspace/q/assumptions.md`; `templates/workspace/q/notation.md`; `templates/workspace/q/data_recon.md`; `templates/workspace/q/warnings.md`; `templates/workspace/q/review_note.md` | `workspace/output/q*/analysis.md`; `candidates.md`; `model.md`; `assumptions.md`; `notation.md`; `data_recon.md`; optional `warnings.md`; AP or risk `review_note.md` |
| Stage 3 Per-Question Build | `references/stage_03_per_question_build.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md` | `templates/workspace/q/code/README.md`; `templates/workspace/q/results/result.schema.json`; `templates/workspace/q/results/result.example.json`; `templates/workspace/q/results/run_log.md` | `workspace/output/q*/code/`; `workspace/output/q*/results/result.json`; `workspace/output/q*/results/run.log` |
| Stage 4 Verification and Sensitivity | `references/stage_04_verification_sensitivity.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md` | `templates/workspace/q/validation.md`; `templates/workspace/q/sensitivity.md` | `workspace/output/q*/validation.md`; `workspace/output/q*/sensitivity.md` |
| Stage 5 Figures and Tables | `references/stage_05_figures_tables.md` | `competitions/cumcm/distilled_formats.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/anti_patterns.md`; `references/rubrics.md` | `templates/workspace/q/figures/figure_index.md`; `templates/workspace/q/figures/figure_check.md`; `templates/workspace/q/tables/table_index.md`; `templates/workspace/q/tables/table.md` | `workspace/output/q*/figures/figure_index.md`; `workspace/output/q*/tables/table_index.md` |
| Stage 6 Per-Question Summary | `references/stage_06_per_question_summary.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/phrase_bank.md` as needed | `templates/workspace/q/q_summary.md` | `workspace/output/q*/q*_summary.md` |
| Stage 7 Final Integration | `references/stage_07_final_integration.md` | `references/result_traceability.md`; `references/quality_gate.md`; `references/feedback_layer2_backtrack.md` | `templates/workspace/final/final_results.md`; `templates/workspace/final/final_figures_index.md`; `templates/workspace/final/final_tables_index.md`; `templates/workspace/final/traceability.md` | `workspace/output/final/final_results.md`; `final_figures_index.md`; `final_tables_index.md`; `traceability.md` |
| Stage 8 Paper Generation | `references/stage_08_paper_generation.md` | `competitions/cumcm/paper_skeleton.md`; `competitions/cumcm/abstract_template.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/phrase_bank.md`; `competitions/cumcm/anti_patterns.md`; `competitions/cumcm/distilled_structures.md`; `competitions/cumcm/distilled_formats.md`; `references/result_traceability.md` | `templates/workspace/final/paper.md`; `templates/workspace/final/paper.tex` fallback scaffold; `templates/workspace/final/source/README.md`; `templates/latex/cumcm/cumcmthesis/` | `workspace/output/final/paper.md`; `paper.tex`; `paper.pdf`; `source/` |
| Stage 9 Final Review | `references/stage_09_final_review.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md`; `references/feedback_layer3_panel.md`; `references/feedback_layer4_calibration.md`; `references/result_traceability.md`; `references/quality_gate.md`; `competitions/cumcm/anti_patterns.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/abstract_template.md`; `competitions/cumcm/distilled_formats.md`; `competitions/cumcm/empirical.json`; `competitions/cumcm/empirical_notes.md` | `templates/workspace/final/review_report.md`; `templates/workspace/final/anonymity_report.md`; `templates/workspace/final/quality_report.md` | `workspace/output/final/review_report.md`; `anonymity_report.md`; `quality_report.md` |

## Supporting Contracts

| Contract | File |
|---|---|
| Workspace and template contract | `references/workspace_protocol.md` |
| Manual and AP modes | `references/modes_ap_manual.md` |
| Result traceability | `references/result_traceability.md` |
| Quality gate | `references/quality_gate.md` |

## Next Stage Rule

A stage may enter the next stage only when its required outputs exist, required fields are filled with source-backed content, and any `partial` or `fail` condition has a written limitation note.
