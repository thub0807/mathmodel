---
name: mathmodel-copilot
description: 固定工作区、CUMCM-only、Markdown-first 的单题数学建模 Skill。默认 Manual 模式，读取 workspace/problem/problem.md，输出 workspace/output/。
---

# mathmodel-copilot

`mathmodel-copilot` 是固定工作区、单题、Markdown-first、Agent-first 的数学建模 Skill。当前 active competition style 仅为 CUMCM。

## v1.2 核心控制流

默认采用 question-major execution loop，而不是按 Stage 批量处理全部 `q*`。

固定顺序：

```text
Stage 0 workspace audit
Stage 1 question decomposition
q1: Plan -> Review Gate -> Build -> Verification/Sensitivity -> Figures/Tables -> Summary -> Review Gate
q2: Plan -> Review Gate -> Build -> Verification/Sensitivity -> Figures/Tables -> Summary -> Review Gate
...
Stage 7 final integration
Stage 8 paper generation
Stage 9 final review
```

规则：

- 每个 `q*` 必须按编号顺序完成完整闭环后，才能进入下一个 `q*`。
- 后续 `q*` 必须读取已完成上游问题的 `q*_summary.md`、`results/result.json`、`validation.md`、`sensitivity.md`、`review_packet.md`、`warnings.md` 和 `review_note.md`。
- 对链式依赖问题，主求解流程必须串行。只有局部 critic、图表自检、最终 panel review 等无上游依赖任务可在能力可用时并行；否则串行执行。
- AP 模式只跳过人工确认，不跳过 Plan、Build、Verification、Sensitivity、Summary、traceability 或 review notes。

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
- 每问主要 Markdown 审查入口最多为三类：`review_packet.md`、`q*_summary.md`、`warnings.md` / `review_note.md`。不得再把 `analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 作为必需产物；这些内容必须合并到 `review_packet.md` 的固定章节中。

## 默认模式

默认使用 Manual 模式。

Manual 模式下：

- Stage 2 每个 `q*` Plan 完成后必须生成 `workspace/output/q*/review_packet.md`，进入 Build 前必须暂停并得到用户同意；
- 每个 `q*` 完成 Build、Verification、Sensitivity 和 Summary 后必须再次暂停，供用户审查是否进入下一问；
- 暂停时只返回生成的文件路径，供用户审阅；
- 每次返工后必须在 `review_note.md` 写明本轮改进内容、影响的结论、仍保留的限制和审查材料位置；
- Stage 7 完成后，进入 Stage 8 前必须暂停，供用户审阅 final integration 文件。

AP 模式只在用户明确要求自动推进时启用。AP 模式仍必须逐问完整执行，并写入 `review_packet.md`、review notes、warnings、traceability 和 quality reports。

## 启动时读取

启动时先读取：

```text
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
```

运行某个阶段前，再按 `references/workflow.md` 读取对应 stage reference、knowledge layer 和必要资产。输出契约由 stage reference 直接定义，不再使用 `templates/workspace/`。

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

### CUMCM competition and rendering layer

提供 CUMCM 写作质量材料和正式 LaTeX 资产：

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
```

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

禁止生成 `submit.zip`。禁止恢复多题评分。禁止新增 `detect_questions.py`、`create_question_dirs.py` 或必需的 `question_manifest.json`。不得要求 `init_workspace.py` 或 `check_materials.py` 先于 Agent 读取 `problem.md`。

## Legacy 边界

`legacy/` 是开发迁移档案，不属于 active workflow。不要把 `legacy/` 作为运行时输入、知识源、模板、脚本或工具。

## Active Runtime Helpers

Stage 8 may use:

```bash
python scripts/render_workspace_paper.py <workspace>
```

Stage 9 may use:

```bash
python scripts/validate_workspace.py <workspace> --strict
```

Keep script details in `scripts/README.md` and the stage references. `SKILL.md` remains the control surface.
