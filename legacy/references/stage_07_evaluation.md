---
stage: 7
name: per_question_summary_and_final_integration
inputs: [workspace/output/q*/q*_summary.md, workspace/output/q*/results/result.json, workspace/output/q*/validation.md, workspace/output/q*/sensitivity.md, workspace/output/q*/figures, workspace/output/q*/tables]
outputs: [workspace/output/q*/q*_summary.md, workspace/output/final/final_results.md, workspace/output/final/traceability.md]
loads_reference: [references/workflow.md, references/final_review_protocol.md]
next: stage_08_writing
---

# Stage 7：Per-Question Summary 与 Final Integration

## 目标

为每个 `q*` 形成可写入论文的总结，并把各问题的结果、图表和证据来源整合到最终结果与追溯报告。

## 每问输入

```text
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/
workspace/output/q*/tables/
```

## 每问输出

```text
workspace/output/q*/q*_summary.md
```

`q*_summary.md` 必须包含：

- 问题目标。
- 建模路线。
- 核心公式。
- 求解过程。
- 主要结果。
- 验证结论。
- 灵敏度结论。
- 图表索引。
- 可写入论文的段落草稿。
- 局限性与改进方向。

## 最终整合输出

```text
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

## `traceability.md` 必须说明

- 论文关键结论来自哪个 `q*`。
- 硬数字来自哪个 `result.json` / `validation.md` / `sensitivity.md`。
- 图来自哪个 `q*/figures/`。
- 表来自哪个 `q*/tables/`。
- 假设来自哪个 `assumptions.md`。
- 符号来自哪个 `notation.md`。
- `partial` 或 `fail` 的限制如何影响最终论文。

## 规则

- 不读取旧集中式状态。
- 不写入任何集中式状态文件。
- 不把 `fail` 结果写成论文结论。
- `partial` 结果必须带限制说明。

## 退出条件

- 每个 `q*` 均有 `q*_summary.md`。
- `final_results.md` 已生成。
- `final_figures_index.md` 与 `final_tables_index.md` 已生成。
- `traceability.md` 已生成并覆盖硬数字来源。
