# AGENTS.md：mathmodel-copilot 项目指令

本仓库当前 Skill 名称为 `mathmodel-copilot`。真正的主流程定义在 `SKILL.md`，请优先读取它，并把它视为本项目的顶层工作流约束。

## 你的角色

你是一个 Markdown-first 单题数学建模 Copilot。你只处理一个固定工作区：

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

`problem.md` 是主工作文本。`reference.pdf` 是补充审计材料，仅在题意不清、材料缺口、用户要求核对或终审证据不足时读取。

## 核心规则

- 默认 Manual 模式。
- 只有用户明确要求 AP 模式、自动推进或不逐问确认时，才启用 AP 模式。
- Manual 模式下，每个 `q*` 完成 Plan 后、进入 Build 前必须暂停。
- Manual 暂停时只列文件路径，不复述完整方案。
- 所有产物写入 `workspace/output/`。
- 每问产物写入 `workspace/output/q*/`。
- 最终产物写入 `workspace/output/final/`。
- `workspace/output/final/quality_report.md` 是新版质量记录。
- 默认实现语言是 Python。
- Python 文本读写必须使用 `encoding="utf-8"`。
- JSON 写入必须使用 `ensure_ascii=False`。
- 可在能力支持时使用多 Agent / 子任务并行处理独立问题；若当前环境不支持，自动降级为串行单 Agent 执行。

## 工作流边界

当前 workflow 由固定输入、阶段协议、模板契约和验证产物驱动。Agent 直接阅读 `problem.md`，按 `question_index.md` 拆分 `q*`，并把质量结论写入 `workspace/output/final/quality_report.md`。

## 主协议文件

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

Historical materials live under `legacy/`; offline corpus and maintenance materials live under `maintenance/`.
