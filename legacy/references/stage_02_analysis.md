---
stage: 2
name: per_question_analysis_and_data_recon
inputs: [workspace/output/question_index.md, workspace/output/material_index.md, workspace/problem/problem.md]
outputs: [workspace/output/q*/analysis.md, workspace/output/q*/data_recon.md]
loads_reference: [references/per_question_plan.md, references/workspace_protocol.md]
next: stage_03_model_selection
---

# Stage 2：Per-Question Plan - 题意分析与数据重构

## 目标

为每个 `q*` 形成可审查的问题分析和数据使用计划，作为后续候选模型、假设、符号和构建阶段的基础。

## 输入

```text
workspace/problem/problem.md
workspace/output/question_index.md
workspace/output/material_index.md
workspace/output/problem_audit.md
```

## 输出

```text
workspace/output/q*/analysis.md
workspace/output/q*/data_recon.md
```

## `analysis.md` 必须包含

- 子问题目标。
- 原题对应标记。
- 输入。
- 输出。
- 依赖关系。
- 对应附件或图片。
- 评价目标与评价指标。
- 是否依赖其他 `q*` 的结果。
- 题意疑点和需要后续核对的材料。

## `data_recon.md` 必须包含

- 数据来源。
- 附件使用方式。
- 图片或表格信息的使用方式。
- 预处理计划。
- 缺失值处理计划。
- 异常值处理计划。
- 单位、符号、字段含义的核对事项。
- 不可用材料对本问题的影响。

## 规则

- 只基于 `problem.md` 和已索引材料工作。
- 仅在 `problem.md` 信息不足时，按 `workspace_protocol.md` 读取 `reference.pdf` 的相关部分。
- 不使用 Python 或正则脚本做问题识别。
- 不写入任何集中式状态文件。
- 不依赖旧阶段评分或题型字段。

## 退出条件

- 每个 `q*` 均有 `analysis.md`。
- 每个 `q*` 均有 `data_recon.md`。
- 依赖、附件、评价指标和材料缺口已写清楚。
