---
name: mathmodel-copilot
description: Fixed-workspace mathematical modeling Skill. Reads workspace/problem/problem.md as the primary problem statement, uses workspace/problem/reference.pdf only as supporting audit material, and produces Markdown-first modeling artifacts, traceability reports, quality gates, and a final paper under workspace/output/. Defaults to a Manual checkpoint workflow; AP mode requires explicit user request.
---

# mathmodel-copilot

`mathmodel-copilot` 是一个固定工作区、单题、Markdown-first 的数学建模 Skill。它以文件契约驱动建模过程：每个阶段读取明确输入，写入明确输出，最终只从已验证、可追溯的产物生成论文结论。

默认写作风格为 CUMCM 国赛中文论文。正式 CUMCM 排版优先使用 `templates/latex/cumcm/cumcmthesis/`，`templates/workspace/final/paper.tex` 仅是 fallback scaffold。

## Fixed Workspace

固定输入：

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

固定输出：

```text
workspace/output/
```

`problem.md` 是主工作文本。`reference.pdf` 是补充审计材料，只在题意不清、材料缺口、用户要求核对或终审证据不足时读取。

## Startup References

启动时读取：

```text
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
```

## Layer Structure

Workflow control layer:

```text
SKILL.md
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
references/stage_00_workspace_audit.md
...
references/stage_09_final_review.md
```

Modeling and quality layer:

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

Competition and output layer:

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
templates/workspace/
```

`templates/workspace/` 是输出文件契约库。`competitions/cumcm/` 是 CUMCM 写作与质量判断知识层。`templates/latex/cumcm/cumcmthesis/` 是正式排版资产。

## Stage Reference Map

Before running a stage, read its stage reference. As needed, also read the modeling/quality references, CUMCM competition materials, LaTeX assets, and workspace templates listed in `references/workflow.md`.

Before entering the next stage, write the required stage outputs under `workspace/output/` according to the stage reference and matching `templates/workspace/` contract.

| Stage | Reference |
|---|---|
| Stage 0 Workspace Audit | `references/stage_00_workspace_audit.md` |
| Stage 1 Question Decomposition | `references/stage_01_question_decomposition.md` |
| Stage 2 Per-Question Plan | `references/stage_02_per_question_plan.md` |
| Stage 3 Per-Question Build | `references/stage_03_per_question_build.md` |
| Stage 4 Verification and Sensitivity | `references/stage_04_verification_sensitivity.md` |
| Stage 5 Figures and Tables | `references/stage_05_figures_tables.md` |
| Stage 6 Per-Question Summary | `references/stage_06_per_question_summary.md` |
| Stage 7 Final Integration | `references/stage_07_final_integration.md` |
| Stage 8 Paper Generation | `references/stage_08_paper_generation.md` |
| Stage 9 Final Review | `references/stage_09_final_review.md` |

Supporting contracts:

```text
references/result_traceability.md
references/quality_gate.md
```

Stage-specific knowledge is loaded lazily:

- Stage 2-4 use `model_catalog.md`, `rubrics.md`, Layer 1 critic, and Layer 2 backtrack as needed.
- Stage 5-7 use traceability, quality, CUMCM figure/table and writing-quality materials as needed.
- Stage 8 reads `competitions/cumcm/` and prefers `templates/latex/cumcm/cumcmthesis/` for formal CUMCM paper generation.
- Stage 9 reads rubrics, all feedback layers, CUMCM anti-patterns, and empirical materials when present.

## Modes

Manual 是默认模式。每个 `q*` 完成 Stage 2 Plan 后，必须暂停并只列出已生成的 Plan 文件路径，等待用户确认后进入 Build。

AP 模式只在用户明确要求“AP 模式”“自动推进”或“不逐问确认”时启用。AP 模式仍必须写完整 Plan 文件，并在存在材料缺口、强假设或路线风险时写入 `review_note.md` 与 `warnings.md`。

## Evidence Rule

论文结论只能来自 validated artifacts：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

`result.json.status` 只能是 `pass`、`partial` 或 `fail`。`partial` 必须带限制进入正文，`fail` 不得作为论文结论依据。

Every hard number, table entry, figure claim, and final conclusion in `workspace/output/final/paper.*` must trace back to one of the validated artifacts above.

## Legacy Isolation

`legacy/` 中的迁移保留材料仅供历史审计和维护参考，不属于 active execution path。
