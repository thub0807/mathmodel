---
stage: 4
name: per_question_assumptions_and_notation
inputs: [workspace/output/q*/analysis.md, workspace/output/q*/model.md, workspace/output/q*/data_recon.md]
outputs: [workspace/output/q*/assumptions.md, workspace/output/q*/notation.md]
loads_reference: [references/per_question_plan.md]
next: stage_05_subproblem_loop
---

# Stage 4：Per-Question Plan - 假设与符号

## 目标

为每个 `q*` 建立可审查的建模假设和符号表，保证后续构建、验证、图表和论文写作一致。

## 输入

```text
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/data_recon.md
```

## 输出

```text
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
```

## `assumptions.md` 必须包含

- 假设编号。
- 假设内容。
- 依据来源：题面、附件、数据观察、文献常识或工程常识。
- 假设影响范围。
- 若假设不成立，可能影响哪些结果。

## `notation.md` 必须包含

| 符号 | 含义 | 单位 | 类型 | 来源 | 使用位置 |
|---|---|---|---|---|---|

类型建议使用：

- 决策变量。
- 状态变量。
- 参数。
- 指标。
- 集合或索引。
- 中间变量。

## 跨问题一致性

- 同一个符号跨问题复用时，含义、单位和类型必须一致。
- 如果同一符号在不同问题中必须表示不同含义，应更换符号。
- Final Integration 阶段必须在 `workspace/output/final/traceability.md` 中汇总符号来源。

## 规则

- 假设必须有依据，不能只有“为简化模型”。
- 符号必须包含单位；无量纲变量写“无量纲”。
- 不写入任何集中式状态文件。

## 退出条件

- 每个 `q*` 均有 `assumptions.md`。
- 每个 `q*` 均有 `notation.md`。
- 假设有依据，符号有单位和来源。
