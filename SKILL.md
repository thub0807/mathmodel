---
name: mathmodel-copilot
description: 固定工作区、CUMCM-only、Markdown-first 的单题数学建模 Skill。默认 Manual 模式，读取 workspace/problem/problem.md，输出 workspace/output/。
---

# mathmodel-copilot

`mathmodel-copilot` 是固定工作区、单题、Markdown-first、Agent-first 的数学建模 Skill。当前 active competition style 仅为 CUMCM。

## 固定工作区

输入：

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

输出：

```text
workspace/output/
```

规则：

- `workspace/problem/problem.md` 是主工作文本，Agent 必须直接阅读和理解。
- `workspace/problem/reference.pdf` 是 audit-only 支持材料，不自动作为题意来源；缺失时记录审计风险，但不得阻止 Agent 读取 `problem.md`。
- 所有阶段产物写入 `workspace/output/`。
- 每问产物写入 `workspace/output/q*/`。
- 最终产物写入 `workspace/output/final/`。
- 默认 `implementation_language` 为 `python`。所有 solve、verify、figure 和 data-processing code 必须使用锁定语言。

## 默认模式

默认使用 Manual 模式。

Manual 模式下：

- Stage 2 每个 `q*` Plan 完成后必须生成 `workspace/output/q*/solution_plan.md`，进入 Build 前必须暂停；
- 暂停时只返回生成的文件路径，供用户审阅；
- Stage 7 完成后，进入 Stage 8 前必须暂停，供用户审阅 final integration 文件。

AP 模式只在用户明确要求自动推进时启用。AP 模式仍必须写入 review notes、warnings、traceability 和 quality reports。

## 启动时读取

启动时先读取：

```text
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
```

运行某个阶段前，再按 `references/workflow.md` 读取对应 stage reference、knowledge layer 和 templates/assets。

## 三层架构

### Workflow control layer

控制固定路径、阶段顺序、模式行为和产物生命周期：

```text
SKILL.md
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
references/stage_00_workspace_audit.md
references/stage_01_question_decomposition.md
references/stage_02_per_question_plan.md
references/stage_03_per_question_build.md
references/stage_04_verification_sensitivity.md
references/stage_05_figures_tables.md
references/stage_06_per_question_summary.md
references/stage_07_final_integration.md
references/stage_08_paper_generation.md
references/stage_09_final_review.md
```

### Modeling and quality layer

提供建模目录、质量 rubric、反馈层、traceability 和 final gate：

```text
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
references/result_traceability.md
references/quality_gate.md
```

### CUMCM competition and output layer

提供 CUMCM 写作质量材料、正式 LaTeX 资产和 workspace 产物契约：

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
templates/workspace/
```

`templates/workspace/` 是 artifact contract。
`competitions/cumcm/` 是 CUMCM writing-quality layer。
`templates/latex/cumcm/` 是 final rendering asset。

## Active Competition Scope

当前 active workflow 默认且仅支持 CUMCM。

MCM 和 Diangong 材料已移动到 `legacy/`，仅作为历史或未来扩展材料，不属于当前 active workflow，也不是启动选项。

## 证据规则

论文硬数字和结论只能来自：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

`result.json.status` 只能是：

```text
pass
partial
fail
```

`partial` 结果必须带限制进入正文。`fail` 结果不能作为论文 claim。

## Legacy 边界

`legacy/` 是开发迁移档案，不属于 active workflow。不要把 `legacy/` 作为运行时输入、知识源、模板、脚本或工具。
