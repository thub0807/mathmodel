# mathmodel-copilot

`mathmodel-copilot` 是一个 Markdown-first、Agent-first、单题数学建模 Copilot Skill。它不从多个赛题中选题，而是面向一个已经准备好的固定工作区，从 `workspace/problem/problem.md` 出发，拆分子问题、建模、求解、验证、生成图表、整合论文并完成终审。

本轮重构的重点是流程控制层。数学建模知识层、竞赛模板和脚本工具尽量保留，但不再作为旧式主流程状态机的一部分。

## 固定工作区

输入材料放在：

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/          # 可不存在或为空
    └── attachments/     # 可不存在或为空
```

规则：

- `problem.md` 必须存在，是主工作文本。
- `reference.pdf` 必须存在，但只是补充审计材料。
- `images/` 和 `attachments/` 按 `problem.md` 中相对路径读取。
- 若缺少 `problem.md` 或 `reference.pdf`，Agent 应提示补充，不能进入完整建模流程。

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

其中 `quality_report.md` 是新版质量记录。

## 主流程

新版流程共 10 阶段：

```text
Stage 0  Workspace Reading & Problem Understanding
Stage 1  Question Decomposition
Stage 2  Per-Question Plan
Stage 3  Per-Question Build
Stage 4  Per-Question Verification
Stage 5  Figures and Tables
Stage 6  Per-Question Summary
Stage 7  Final Integration
Stage 8  Paper Generation with Template
Stage 9  Final Review
```

默认模式是 Manual。每个问题完成 Plan 后，Agent 只列出 Plan 文件路径并等待用户确认。AP 模式只有在用户明确要求自动推进时启用。

如当前环境支持可靠的多 Agent / 子任务并行，可并行处理相互独立的子问题或审查任务；如果不支持，则自动降级为串行单 Agent 执行。

## 协议文件

新版主流程优先读取：

- `references/workspace_protocol.md`
- `references/workflow.md`
- `references/modes_ap_manual.md`
- `references/per_question_plan.md`
- `references/per_question_build.md`
- `references/verification_protocol.md`
- `references/figures_tables_protocol.md`
- `references/paper_generation_protocol.md`
- `references/final_review_protocol.md`

旧知识层仍保留，可作为参考：

- `references/model_catalog.md`
- `references/rubrics.md`
- `references/feedback_layer*.md`
- `competitions/cumcm/`
- `competitions/mcm/`
- `competitions/diangong/`
- `templates/latex/`

## 本流程不做什么

- 不做多题选题。
- 不询问年份、题号、队员、分工、团队规模或截止时间。
- 不使用集中式流程状态文件。
- 不要求先运行初始化或材料检查脚本。
- 不新增 Python 或正则拆题脚本。
- 不把 `question_manifest.json` 作为必需文件。
- 不生成 `submit.zip`。
- 不新增提交包逻辑。

## 脚本说明

`scripts/` 下脚本是可选工具，不是主流程依赖。详见 `scripts/README.md`。

如果旧脚本仍依赖旧状态文件，它们只能视为 legacy utility。当前 active workflow 不调用这些脚本作为质量门禁；新版质量记录以 `workspace/output/final/quality_report.md` 为准。
