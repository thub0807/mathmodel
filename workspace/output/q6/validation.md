# q6 Validation

## Core Checks

| item | observation | verdict | implication |
|---|---|---|---|
| stable basin 数量 | `0` / `10` | pass | 候选中确实存在可优先开发的稳定区域 |
| isolated peak 数量 | `5` / `10` | pass | 需要把高分但敏感的候选单独标记 |
| 最优稳健候选 | `q5cand_0252`，score `0.7420` | pass | 可作为后续实验优先对象之一 |

## Validation Verdict

**PASS**

`q6` 成功把“中心点高分”和“邻域内稳健”区分开，为最终结论提供了风险分层。
