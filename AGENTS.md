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

## 禁止事项

- 不使用集中式状态机 JSON。
- 不要求在阅读 `problem.md` 前运行预检脚本。
- 不使用 Python 对 `problem.md` 做语义拆题。
- 不使用正则脚本识别问题。
- 不把 `question_manifest.json` 作为必需文件。
- 不做多题选题、多题对比或多题评分。
- 不询问年份、题号、队员、分工、团队规模或截止时间。
- 不生成提交包或 `submit.zip`。

## 主协议文件

按需懒加载以下新版协议：

- `references/workspace_protocol.md`
- `references/workflow.md`
- `references/modes_ap_manual.md`
- `references/per_question_plan.md`
- `references/per_question_build.md`
- `references/verification_protocol.md`
- `references/figures_tables_protocol.md`
- `references/paper_generation_protocol.md`
- `references/final_review_protocol.md`

旧知识层如 `references/model_catalog.md`、`references/rubrics.md`、`references/feedback_layer*.md` 与 `competitions/` 可以作为知识参考，但不是新版主流程骨架。
