# Active Workflow Index

`mathmodel-copilot` 是固定工作区、单题、Markdown-first、CUMCM-only 的数学建模 workflow。v1.2 的运行顺序是 question-major：先完成一个问题的完整闭环，再进入下一个问题。

## Fixed Paths

| Role | Path |
|---|---|
| 主题面 | `workspace/problem/problem.md` |
| 审计支持材料 | `workspace/problem/reference.pdf` |
| 图片 | `workspace/problem/images/` |
| 附件 | `workspace/problem/attachments/` |
| 全部输出 | `workspace/output/` |

`problem.md` 是主工作文本。`reference.pdf` 仅作 audit-only 支持材料。

## Question-Major Execution Rule

先执行一次全局阶段：

```text
Stage 0 Workspace Audit
Stage 1 Question Decomposition
```

然后按 `question_index.md` 的编号顺序，对每个 `q*` 执行完整闭环：

```text
Stage 2 Plan -> Review Gate -> Stage 3 Build -> Stage 4 Verification/Sensitivity -> Stage 5 Figures/Tables -> Stage 6 Summary -> Review Gate
```

当前 `q*` 未完成 Stage 6 前，不得开始下一个 `q*` 的 Stage 2。后续问题必须读取上游问题的已完成产物，并显式说明上游 `partial` / `fail` 对本问的降级影响。

全部问题闭环完成后，再执行：

```text
Stage 7 Final Integration
Stage 8 Paper Generation
Stage 9 Final Review
```

## Parallelism Rule

默认串行。只有满足以下条件时才可并行：

- 运行环境支持 sub-agent 或等价并行能力；
- 任务无上游结果依赖；
- 并行任务不会写同一个文件；
- 并行结果最终由主 Agent 串行整合。

链式问题的主 Plan、Build、Verification、Summary 必须串行。可并行的典型任务仅包括局部 critic、图表自检、最终 panel review 等独立审查。

## Stage Reference Matrix

| Stage | Reference | Active outputs |
|---|---|---|
| Stage 0 Workspace Audit | `references/stage_00_workspace_audit.md` | `workspace/output/problem_audit.md`; `workspace/output/material_index.md` |
| Stage 1 Question Decomposition | `references/stage_01_question_decomposition.md` | `workspace/output/question_index.md`; `workspace/output/q*/` |
| Stage 2 Per-Question Plan | `references/stage_02_per_question_plan.md` | `workspace/output/q*/review_packet.md`; `warnings.md`; `review_note.md` |
| Review Gate before Build | `references/modes_ap_manual.md` | Manual: stop and return paths only; AP: write auto-review note |
| Stage 3 Per-Question Build | `references/stage_03_per_question_build.md` | `workspace/output/q*/code/`; `workspace/output/q*/results/result.json`; `workspace/output/q*/results/run.log` |
| Stage 4 Verification and Sensitivity | `references/stage_04_verification_sensitivity.md` | `workspace/output/q*/validation.md`; `workspace/output/q*/sensitivity.md`; updated `warnings.md` / `review_note.md` |
| Stage 5 Figures and Tables | `references/stage_05_figures_tables.md` | `workspace/output/q*/figures/figure_index.md`; `workspace/output/q*/tables/table_index.md` |
| Stage 6 Per-Question Summary | `references/stage_06_per_question_summary.md` | `workspace/output/q*/q*_summary.md`; updated `review_note.md` |
| Stage 7 Final Integration | `references/stage_07_final_integration.md` | `workspace/output/final/final_results.md`; `final_figures_index.md`; `final_tables_index.md`; `traceability.md` |
| Stage 8 Paper Generation | `references/stage_08_paper_generation.md` | `workspace/output/final/paper.md`; `paper.tex`; `paper.pdf` if generated; `source/`; `latex_compile.log`; `render_report.json` |
| Stage 9 Final Review | `references/stage_09_final_review.md` | `workspace/output/final/review_report.md`; `anonymity_report.md`; `quality_report.md` |

`review_packet.md` is the single Plan review entry for each `q*`. Legacy split Plan files may exist for compatibility, but they are not required v1.2 outputs.

## Supporting Contracts

| Contract | File |
|---|---|
| Workspace artifact contract | `references/workspace_protocol.md` |
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
