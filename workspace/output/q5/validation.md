# q5 Validation

## Core Checks

| item | observation | verdict | implication |
|---|---|---|---|
| top5 平均 pred_PI | `0.8204`，比随机基线高 `0.0170` | pass | 推荐方案优于随机挑点 |
| top10 平均 pred_PI | `0.8219`，比随机基线高 `0.0181` | pass | 扩展候选仍保持优势 |
| trust mix | top10 中 `high/medium/low = {'high': 6, 'low': 3, 'medium': 1}` | pass | 候选集兼顾开发与探索 |
| 基本物理门槛 | 候选筛选已要求 `pred_S_pH >= 0.50` 且 `pred_W_1` 不低于 40% 分位 | pass | 没有把明显差候选推入推荐表 |

## Validation Verdict

**PASS**

`q5` 的核心结论是“有约束的主动推荐优于随机选点”，而不是“这些候选已经被真实实验确认最佳”。
