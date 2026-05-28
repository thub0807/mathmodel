# Active Workflow Index

`mathmodel-copilot` 是固定工作区、单题、Markdown-first、CUMCM-only 的数学建模 workflow。

## Fixed Paths

| Role | Path |
|---|---|
| 主题面 | `workspace/problem/problem.md` |
| 审计支持材料 | `workspace/problem/reference.pdf` |
| 图片 | `workspace/problem/images/` |
| 附件 | `workspace/problem/attachments/` |
| 全部输出 | `workspace/output/` |

`problem.md` 是主工作文本。`reference.pdf` 仅作 audit-only 支持材料。

## Layer Roles

| Layer | Role | Paths |
|---|---|---|
| Workflow control layer | 控制阶段顺序、固定路径、Manual/AP 模式、产物生命周期 | `SKILL.md`; `references/workspace_protocol.md`; `references/workflow.md`; `references/modes_ap_manual.md`; `references/stage_00_workspace_audit.md` ... `references/stage_09_final_review.md` |
| Modeling and quality layer | 提供建模方法、rubric、反馈层、traceability 和 quality gate | `references/model_catalog.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md`; `references/feedback_layer3_panel.md`; `references/feedback_layer4_calibration.md`; `references/result_traceability.md`; `references/quality_gate.md` |
| CUMCM competition and output layer | 提供 CUMCM 写作质量材料、正式 LaTeX 资产、workspace artifact contract | `competitions/cumcm/`; `templates/latex/cumcm/cumcmthesis/`; `templates/workspace/` |

`templates/workspace/` 是 artifact contract。
`competitions/cumcm/` 是 CUMCM writing-quality layer。
`templates/latex/cumcm/` 是 final rendering asset。
`legacy/` 是开发迁移档案，不是 active runtime source。

## Execution Rule

运行某个 stage 前，读取该 stage reference 和下表列出的 knowledge layer、templates/assets。进入下一 stage 前，必须按 `templates/workspace/` 契约写入 required outputs，并把 `partial` / `fail` 限制传递到后续产物。

## Stage Reference Knowledge Layer Templates Assets Outputs

| Stage | Reference | Knowledge layer | Templates/assets | Outputs |
|---|---|---|---|---|
| Stage 0 Workspace Audit | `references/stage_00_workspace_audit.md` | `references/workspace_protocol.md` | `templates/workspace/root/problem_audit.md`; `templates/workspace/root/material_index.md` | `workspace/output/problem_audit.md`; `workspace/output/material_index.md` |
| Stage 1 Question Decomposition | `references/stage_01_question_decomposition.md` | `references/workspace_protocol.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md` | `templates/workspace/root/question_index.md` | `workspace/output/question_index.md`; `workspace/output/q*/` |
| Stage 2 Per-Question Plan | `references/stage_02_per_question_plan.md` | `references/model_catalog.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md` | `templates/workspace/q/analysis.md`; `templates/workspace/q/solution_plan.md`; `templates/workspace/q/candidates.md`; `templates/workspace/q/model.md`; `templates/workspace/q/assumptions.md`; `templates/workspace/q/notation.md`; `templates/workspace/q/data_recon.md`; `templates/workspace/q/warnings.md`; `templates/workspace/q/review_note.md` | `workspace/output/q*/analysis.md`; `workspace/output/q*/solution_plan.md`; `workspace/output/q*/candidates.md`; `workspace/output/q*/model.md`; `workspace/output/q*/assumptions.md`; `workspace/output/q*/notation.md`; `workspace/output/q*/data_recon.md`; optional `warnings.md`; AP/risk `review_note.md` |
| Stage 3 Per-Question Build | `references/stage_03_per_question_build.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/model_catalog.md` | `templates/workspace/q/code/README.md`; `templates/workspace/q/results/result.schema.json`; `templates/workspace/q/results/result.example.json`; `templates/workspace/q/results/run_log.md`; `templates/shared/code_starter/*.py` | `workspace/output/q*/code/`; `workspace/output/q*/results/result.json`; `workspace/output/q*/results/run.log` |
| Stage 4 Verification and Sensitivity | `references/stage_04_verification_sensitivity.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md`; `references/result_traceability.md` | `templates/workspace/q/validation.md`; `templates/workspace/q/sensitivity.md` | `workspace/output/q*/validation.md`; `workspace/output/q*/sensitivity.md`; updated `review_note.md` or `warnings.md` if needed |
| Stage 5 Figures and Tables | `references/stage_05_figures_tables.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `competitions/cumcm/distilled_formats.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/anti_patterns.md` | `templates/workspace/q/figures/figure_index.md`; `templates/workspace/q/figures/figure_check.md`; `templates/workspace/q/tables/table_index.md`; `templates/workspace/q/tables/table.md` | `workspace/output/q*/figures/figure_index.md`; `workspace/output/q*/tables/table_index.md` |
| Stage 6 Per-Question Summary | `references/stage_06_per_question_summary.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/result_traceability.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/phrase_bank.md` | `templates/workspace/q/q_summary.md` | `workspace/output/q*/q*_summary.md`; updated `review_note.md` if needed |
| Stage 7 Final Integration | `references/stage_07_final_integration.md` | `references/result_traceability.md`; `references/quality_gate.md`; `references/feedback_layer2_backtrack.md`; `references/rubrics.md` | `templates/workspace/final/final_results.md`; `templates/workspace/final/final_figures_index.md`; `templates/workspace/final/final_tables_index.md`; `templates/workspace/final/traceability.md` | `workspace/output/final/final_results.md`; `workspace/output/final/final_figures_index.md`; `workspace/output/final/final_tables_index.md`; `workspace/output/final/traceability.md` |
| Stage 8 Paper Generation | `references/stage_08_paper_generation.md` | `references/result_traceability.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md`; `competitions/cumcm/*` | `templates/workspace/final/paper.md`; `templates/workspace/final/paper.tex` fallback scaffold; `templates/workspace/final/source/README.md`; `templates/latex/cumcm/cumcmthesis/` | `workspace/output/final/paper.md`; `workspace/output/final/paper.tex`; `workspace/output/final/paper.pdf` if generated; `workspace/output/final/source/` |
| Stage 9 Final Review | `references/stage_09_final_review.md` | `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md`; `references/feedback_layer3_panel.md`; `references/feedback_layer4_calibration.md`; `references/result_traceability.md`; `references/quality_gate.md`; `competitions/cumcm/anti_patterns.md`; `competitions/cumcm/winning_patterns.md`; `competitions/cumcm/abstract_template.md`; `competitions/cumcm/distilled_formats.md`; `competitions/cumcm/empirical.json`; `competitions/cumcm/empirical_notes.md` | `templates/workspace/final/review_report.md`; `templates/workspace/final/anonymity_report.md`; `templates/workspace/final/quality_report.md` | `workspace/output/final/review_report.md`; `workspace/output/final/anonymity_report.md`; `workspace/output/final/quality_report.md` |

## Supporting Contracts

| Contract | File |
|---|---|
| Workspace and template contract | `references/workspace_protocol.md` |
| Manual and AP modes | `references/modes_ap_manual.md` |
| Result traceability | `references/result_traceability.md` |
| Quality gate | `references/quality_gate.md` |

## CUMCM-only Rule

Stage 8 和 Stage 9 只引用：

```text
competitions/cumcm/
templates/latex/cumcm/
```

其他历史竞赛材料位于 `legacy/`，不属于 active workflow。
