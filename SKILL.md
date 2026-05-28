---
name: mathmodel-copilot
description: markdown-first single-problem mathematical modeling copilot for fixed workspace/problem/problem.md workflows. Use when the user wants to solve one mathematical modeling problem from a prepared workspace, decompose the problem into subquestions, build models, run code, verify results, generate figures/tables, write a CUMCM-style paper, and perform final review. Defaults to Manual mode and Chinese CUMCM-style output; AP mode and MCM English output require explicit user request.
---

# mathmodel-copilot：Markdown-first 单题数学建模 Copilot

`mathmodel-copilot` 面向一个已经准备好的单题建模工作区。它以 `workspace/problem/problem.md` 为主工作文本，把所有过程状态沉淀为 `workspace/output/` 下可审查的 Markdown / JSON 文件，默认产出中文 CUMCM 风格论文。

本 Skill 不做多题选题，不询问年份、题号、队员、分工或截止时间，不生成 `submit.zip`，不依赖 `decision_log.json`。

## 固定输入工作区

必须使用以下固定结构：

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/          # 可不存在或为空
    └── attachments/     # 可不存在或为空
```

硬性规则：

- `workspace/problem/problem.md` 必须存在。
- `workspace/problem/reference.pdf` 必须存在。
- 如果任一必需文件缺失，提示用户补充，不能进入完整建模流程。
- `problem.md` 是主工作文本，Agent 必须直接阅读并理解。
- `reference.pdf` 是补充审计材料，不是默认全文审计对象。
- 不使用 Python 对 `problem.md` 做语义解析。
- 不使用正则脚本拆题。
- 不要求先运行任何初始化或材料检查脚本。

仅在以下场景读取 `reference.pdf`：

- `problem.md` 表述不完整或存在歧义。
- 图片说明不足。
- 附件来源不清。
- 单位、符号、编号、表格含义疑似缺失。
- 用户明确要求核对 PDF。
- 最终 review 发现题意依据不足。

`images/` 与 `attachments/` 按 `problem.md` 中的相对路径读取。若 `problem.md` 引用了不存在的图片或附件，记录到：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## 默认模式

默认运行模式是 **Manual**。

只有用户显式说“AP 模式”“自动推进”“不逐问确认”等含义时，才启用 **AP 模式**。

Manual 模式规则：

- 每个 `q*` 完成 Per-Question Plan 后，进入 Build 前必须暂停。
- 暂停时不要复述完整方案内容，避免浪费 token。
- 只列出该问题已经生成的完整解决材料保存路径。
- 用户确认后，才进入该问题 Build 阶段。

Manual checkpoint 示例：

```text
q1 的 Plan 材料已生成，请审查：

workspace/output/q1/analysis.md
workspace/output/q1/candidates.md
workspace/output/q1/model.md
workspace/output/q1/assumptions.md
workspace/output/q1/notation.md
workspace/output/q1/data_recon.md
workspace/output/q1/warnings.md   # 如有

确认后进入 q1 Build。
```

AP 模式规则：

- 不逐问等待用户确认。
- 每个问题仍必须生成完整 Plan 文件。
- 如存在强假设、材料缺口或路线风险，写入 `workspace/output/q*/review_note.md` 与 `workspace/output/q*/warnings.md`。

## 新主流程

启动时优先读取：

- `references/workspace_protocol.md`
- `references/workflow.md`
- `references/modes_ap_manual.md`

按阶段懒加载：

- 每问计划：`references/per_question_plan.md`
- 每问构建：`references/per_question_build.md`
- 验证：`references/verification_protocol.md`
- 图表：`references/figures_tables_protocol.md`
- 论文：`references/paper_generation_protocol.md`
- 终审：`references/final_review_protocol.md`

10 个阶段如下：

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

新版阶段文档：

- `references/stage_00_kickoff.md`
- `references/stage_01_problem_selection.md`
- `references/stage_08_writing.md`
- `references/stage_09_review.md`

旧知识层可以按需参考，例如：

- `references/model_catalog.md`
- `references/rubrics.md`
- `references/feedback_layer*.md`
- `competitions/cumcm/*`
- `competitions/mcm/*`
- `competitions/diangong/*`

这些文件是知识参考，不再作为主流程骨架。

## Agent 执行策略

本 Skill 是 Agent-first 流程。复杂子问题、验证、图表检查和终审检查可以使用能力感知并行：

- 如果当前环境支持可靠的多 Agent / 子任务并行，可并行处理相互独立的 `q*` 分析、验证或审查任务。
- 并行任务必须各自写入对应的 `workspace/output/q*/` 或 `workspace/output/final/` 文件，不共享隐式状态。
- 如果当前环境不支持并行能力，自动降级为串行单 Agent 执行。
- 不得因为缺少并行能力而阻塞流程。

## 输出协议

所有流程产物严格写入：

```text
workspace/output/
```

每问产物严格写入：

```text
workspace/output/q*/
```

最终产物严格写入：

```text
workspace/output/final/
```

`workspace/output/final/quality_report.md` 是新版质量记录，替代旧的集中式评分或状态记录。

## 实现语言与编码

默认：

```text
implementation_language = python
```

所有求解、验证、绘图、制表和数据处理代码必须使用锁定实现语言。

Python 文本读写必须显式使用：

```python
encoding="utf-8"
```

JSON 写入必须使用：

```python
ensure_ascii=False
```

不要引入 GBK、ANSI 或 Latin-1 编码假设。

## 禁止事项

- 不创建或要求 `decision_log.json`。
- 不读写 `cwd/state/decision_log.json`。
- 不恢复多题选题、多题评分或 A-E/A-F 题推荐。
- 不询问年份、题号、队员、分工、团队规模或截止时间。
- 不新增 `detect_questions.py`。
- 不新增 `create_question_dirs.py`。
- 不把 `init_workspace.py` 或 `check_materials.py` 作为主流程依赖。
- 不把 `question_manifest.json` 作为必需文件。
- 不生成 `submit.zip`。
- 不新增提交包逻辑。
- 没有 `result.json` 的硬数字不得进入最终论文。
- `status = partial` 或 `status = fail` 的结果必须在追溯报告和终审报告中标明限制。
