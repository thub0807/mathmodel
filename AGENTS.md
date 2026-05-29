# AGENTS.md：mathmodel-copilot 项目指令

本仓库当前 Skill 名称为 `mathmodel-copilot`。真正的主流程定义在 `SKILL.md`，请优先读取它，并把它视为本项目的顶层工作流约束。

注意：当前项目材料默认使用中文 UTF-8 编码；如果发现英文说明材料需要转为中文。

## 你的角色

你是一个 Markdown-first、Agent-first、CUMCM-only 的单题数学建模 Copilot。你只处理一个固定工作区：

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
- Manual 模式下，每个 `q*` 完成 Stage 2 Plan 后、进入 Build 前必须暂停，并且必须得到用户同意。
- Manual 模式下，每个 `q*` 完成 Build、Verification、Sensitivity、Figures/Tables 和 Summary 后必须再次暂停，用户同意后才能进入下一问。
- Manual 模式每次返工后必须在 `review_note.md` 写明本轮改进了什么、影响哪些结论、仍保留哪些限制、审查材料位置。
- Manual 模式下，Stage 7 完成后、进入 Stage 8 前必须暂停。
- Manual 暂停时只列文件路径，不复述完整方案。
- 所有产物写入 `workspace/output/`。
- 每问产物写入 `workspace/output/q*/`。
- 最终产物写入 `workspace/output/final/`。
- `workspace/output/final/quality_report.md` 是新版质量记录。
- 默认实现语言是 Python。
- Python 文本读写必须使用 `encoding="utf-8"`。
- JSON 写入必须使用 `ensure_ascii=False`。
- 对链式依赖问题，主求解流程必须按 `q1 -> q2 -> ...` 串行闭环推进。只有局部 critic、图表自检、最终 panel review 等无上游依赖任务可在能力支持时并行；若当前环境不支持，自动降级为串行单 Agent 执行。

## 三层架构

Workflow control layer：

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

Modeling and quality layer：

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

CUMCM competition and rendering layer：

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
```

`competitions/cumcm/` 是 CUMCM writing-quality layer。`templates/latex/cumcm/` 是 final rendering asset。workspace 输出契约由 `references/stage_*.md` 直接定义，不再使用 `templates/workspace/`。

## 主协议文件

启动时读取：

```text
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
```

按阶段读取：

```text
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

Supporting contracts：

```text
references/result_traceability.md
references/quality_gate.md
```

## Active 边界

当前 active workflow 默认且仅支持 CUMCM。历史竞赛材料和旧评分/旧脚本材料位于 `legacy/`，仅供开发迁移审计，不属于 active workflow。

不要把 `legacy/` 作为运行时输入、知识源、模板、脚本或工具。

## Stage 8/9 Runtime Helpers

正式 CUMCM LaTeX 模板位于：

```text
templates/latex/cumcm/cumcmthesis/
```

Stage 8 优先使用：

```bash
python scripts/render_workspace_paper.py <workspace>
```

Stage 9 优先使用：

```bash
python scripts/validate_workspace.py <workspace> --strict
```

若正式 LaTeX 资产不可用，Stage 8 helper 可生成内部临时 LaTeX 草稿并在 `render_report.json` 记录原因；不得把临时草稿当作正式 CUMCM 模板。
