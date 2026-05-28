---
stage: 3
name: per_question_candidates_and_model
inputs: [workspace/output/q*/analysis.md, workspace/output/q*/data_recon.md]
outputs: [workspace/output/q*/candidates.md, workspace/output/q*/model.md, workspace/output/q*/warnings.md]
loads_reference: [references/per_question_plan.md, references/model_catalog.md]
next: stage_04_foundation
---

# Stage 3：Per-Question Plan - 候选路线与模型选型

## 目标

为每个 `q*` 比较候选建模路线，确定当前采用的模型、公式、目标函数 / 指标、约束与算法流程。

## 输入

```text
workspace/output/q*/analysis.md
workspace/output/q*/data_recon.md
references/model_catalog.md      # 可选知识参考
```

## 输出

```text
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/warnings.md    # 如有
```

## `candidates.md` 必须包含

- 至少若干条结构上不同的候选路线。
- 每条候选路线的适用条件。
- 每条候选路线的数据需求。
- 每条候选路线的优点、风险和放弃原因。
- 最终选择理由。

## `model.md` 必须包含

- 采用的模型名称。
- 核心变量。
- 目标函数或评价指标。
- 约束条件。
- 算法流程。
- 与输入 / 输出的对应关系。
- 预期产出到 `result.json` 的字段。

## `warnings.md` 触发条件

存在以下情况时必须写入：

- 强假设。
- 关键材料缺失。
- 数据质量风险。
- 模型路线依赖前序问题但前序结果尚未验证。
- 结果可能只能达到 `partial`。

## 规则

- 可以参考 `references/model_catalog.md`，但不得依赖旧题型字段或旧状态文件。
- 不写入任何集中式状态文件。
- 不调用旧评分脚本作为选型门禁。

## 退出条件

- 每个 `q*` 均有候选路线比较。
- 每个 `q*` 均有确定模型。
- 风险项已写入 `warnings.md` 或明确说明暂无。
