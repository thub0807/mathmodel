# mathmodel-copilot

`mathmodel-copilot` 是一个 Markdown-first、Agent-first、固定工作区的单题数学建模 Skill。它从 `workspace/problem/problem.md` 出发，完成问题审计、子问题拆分、逐问建模、求解、验证、图表索引、最终整合、论文生成和终审。

## 固定工作区

输入材料放在：

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/
    └── attachments/
```

规则：

- `problem.md` 是主工作文本。
- `reference.pdf` 是补充审计材料。
- `images/` 和 `attachments/` 按 `problem.md` 中相对路径读取。
- 材料审计结果写入 `workspace/output/problem_audit.md` 和 `workspace/output/material_index.md`。

## 输出结构

所有流程产物写入：

```text
workspace/output/
```

每问产物写入：

```text
workspace/output/q*/
```

最终产物写入：

```text
workspace/output/final/
```

关键最终文件包括：

- `workspace/output/final/final_results.md`
- `workspace/output/final/traceability.md`
- `workspace/output/final/paper.md`
- `workspace/output/final/paper.tex`
- `workspace/output/final/paper.pdf`
- `workspace/output/final/review_report.md`
- `workspace/output/final/anonymity_report.md`
- `workspace/output/final/quality_report.md`

## 主流程

新版流程共 10 阶段：

```text
Stage 0  Workspace Audit
Stage 1  Question Decomposition
Stage 2  Per-Question Plan
Stage 3  Per-Question Build
Stage 4  Verification and Sensitivity
Stage 5  Figures and Tables
Stage 6  Per-Question Summary
Stage 7  Final Integration
Stage 8  Paper Generation
Stage 9  Final Review
```

默认模式是 Manual。每个问题完成 Plan 后，Agent 只列出 Plan 文件路径并等待用户确认。AP 模式只有在用户明确要求自动推进时启用。

## 协议文件

启动时读取：

- `references/workspace_protocol.md`
- `references/workflow.md`
- `references/modes_ap_manual.md`

按阶段读取：

- `references/stage_00_workspace_audit.md`
- `references/stage_01_question_decomposition.md`
- `references/stage_02_per_question_plan.md`
- `references/stage_03_per_question_build.md`
- `references/stage_04_verification_sensitivity.md`
- `references/stage_05_figures_tables.md`
- `references/stage_06_per_question_summary.md`
- `references/stage_07_final_integration.md`
- `references/stage_08_paper_generation.md`
- `references/stage_09_final_review.md`

Supporting contracts:

- `references/result_traceability.md`
- `references/quality_gate.md`
- `templates/workspace/`

## Legacy 和 Maintenance

历史迁移材料位于 `legacy/`，仅用于迁移审计或人工参考。离线资料维护脚本和论文资料位于 `maintenance/`，不属于用户建模运行时 workflow。

`scripts/` 只保留可选 runtime helper；主流程推进以 `SKILL.md`、active references 和 `templates/workspace/` 为准。
