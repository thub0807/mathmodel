# mathmodel-copilot

`mathmodel-copilot` 是固定工作区、CUMCM-only、Markdown-first、Agent-first 的单题数学建模 Skill。

它从：

```text
workspace/problem/problem.md
```

读取题目，并把全部过程产物写入：

```text
workspace/output/
```

## 固定工作区

输入材料：

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

输出结构：

```text
workspace/output/
workspace/output/q*/
workspace/output/final/
```

规则：

- `problem.md` 是主工作文本。
- `reference.pdf` 是 audit-only 支持材料；缺失时记录审计风险，不阻止 Agent 直接读取 `problem.md`。
- 每问产物进入 `workspace/output/q*/`。
- 最终论文、traceability 和质量报告进入 `workspace/output/final/`。
- 默认 `implementation_language` 为 `python`，所有求解、验证、图表和数据处理代码使用锁定语言。

## Active Scope

当前 active workflow 默认且仅支持 CUMCM。

Active CUMCM 层：

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
templates/workspace/
```

历史 MCM / Diangong 材料已移动到 `legacy/`，仅作为历史或未来扩展材料，不属于当前 active workflow。

## 三层架构

| Layer | Role | Paths |
|---|---|---|
| Workflow control layer | 固定路径、阶段顺序、Manual/AP 模式、产物生命周期 | `SKILL.md`; `references/workspace_protocol.md`; `references/workflow.md`; `references/modes_ap_manual.md`; `references/stage_00...stage_09...` |
| Modeling and quality layer | 建模目录、rubric、反馈层、traceability、quality gate | `references/model_catalog.md`; `references/rubrics.md`; `references/feedback_layer1_critic.md`; `references/feedback_layer2_backtrack.md`; `references/feedback_layer3_panel.md`; `references/feedback_layer4_calibration.md`; `references/result_traceability.md`; `references/quality_gate.md` |
| CUMCM competition and output layer | CUMCM 写作质量材料、正式 LaTeX 资产、workspace artifact contract | `competitions/cumcm/`; `templates/latex/cumcm/cumcmthesis/`; `templates/workspace/` |

## 主流程

启动时读取：

```text
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
```

阶段：

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

每个阶段运行前读取对应 `references/stage_*.md`，并按 `references/workflow.md` 中列出的 knowledge layer、templates/assets 和 outputs 执行。

## 默认模式

默认 Manual 模式。

- Stage 2 每个 `q*` Plan 完成后暂停，用户审阅后进入 Build。
- Stage 2 暂停前必须生成 `workspace/output/q*/solution_plan.md`，作为统一审阅入口。
- Stage 7 完成后暂停，用户审阅 `final_results.md`、`traceability.md`、`final_figures_index.md`、`final_tables_index.md` 后进入 Paper Generation。
- AP 模式只在用户明确要求自动推进时启用。

## 证据规则

论文 hard numbers 和 final claims 只能来自：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

`partial` 结果必须限制表达。`fail` 结果不能作为论文 claim。

## Legacy 与 Maintenance

`legacy/` 是开发迁移档案，不属于 active workflow。
`maintenance/` 是离线维护材料，不属于用户建模运行时 workflow。
`scripts/` 当前没有必需 active runtime scripts。
