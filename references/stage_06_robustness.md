---
stage: 6
name: per_question_verification
inputs: [workspace/output/q*/results/result.json, workspace/output/q*/model.md, workspace/output/q*/assumptions.md, workspace/output/q*/notation.md]
outputs: [workspace/output/q*/validation.md, workspace/output/q*/sensitivity.md]
loads_reference: [references/verification_protocol.md]
next: stage_07_evaluation
---

# Stage 6：Per-Question Verification

## 目标

对每个 `q*` 的模型、代码和结果进行验证与灵敏度分析，形成论文证据链所需的可靠性依据。

## 输入

```text
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

## 输出

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

## `validation.md` 至少覆盖

- 约束满足检查。
- 边界条件检查。
- 数值稳定性。
- baseline 对比。
- ablation 或 cross-method comparison。
- 失败情形。
- PASS / PARTIAL / FAIL 结论。

## `sensitivity.md` 至少覆盖

- 敏感参数。
- 扰动范围。
- 结果变化。
- 结论稳定性。
- 对论文结论的影响。

## 规则

- 验证结论应与 `result.json.status` 保持一致；如不一致，必须说明原因。
- 跨问题和跨阶段一致性不再依赖旧状态机，应在后续 `traceability.md`、`review_report.md` 和 `quality_report.md` 中完成。
- 不写入任何集中式状态文件。
- 不把未验证结果推进到论文强结论。

## 退出条件

- 每个 `q*` 均有 `validation.md`。
- 每个 `q*` 均有 `sensitivity.md`。
- 验证结论与结果状态关系明确。
