# 电工杯实测分布 (SEED v0.1)

> **此目录数据为种子版本 (seed_v0.1), 未做真 PDF 烘焙。**
> 阈值取自历年电工杯题目题量分析 + 公开评审标准估算 + 国赛 D 题部分类比。
> 后续若提交 30+ 篇电工杯一等奖 PDF, 可用 `scripts/ingest_papers.py` 重新烘焙覆盖。

## 数据缺口提示

`empirical.json` 中所有 `min` / `max` / `mean` 字段填的是估算值。Stage 8/9 或 feedback layers 使用这些字段时, 必须把它们标为 seed reference, 避免误导。

## 阈值出处

| 阈值 | 来源 |
|------|------|
| 摘要 600-1000 字 | 工程类摘要常见区间, 比国赛 5 段式略短 |
| 论文 25-30 页 | 历年获奖论文目测 |
| 子问数 6-8 | 历年题目结构稳定 |
| 图 12-25 | 工程类图表多, 含等高线 / 时序曲线 / 单线图 |
| 公式 18-50 | 中等密度 |
| 引用 10-22 | 电力 / 能源类期刊为主 |

## 与 cumcm 的差异

电工杯的"工程实用性"维度国赛没有显式对应。本 overlay 加了 3 个工程化维度 (engineering_practicality / physical_meaning / data_completeness), 可供 Stage 8/9 写作与质量审查参考。

电工杯的子问数中位数 7, 比国赛 4 多近一倍。建议在 workspace workflow 中更早记录风险:
- Stage 1-4: 明确子问题依赖、模型路线和验证计划
- Stage 5-7: 优先保证关键结果、图表和 traceability
- Stage 8-9: 把工程实用性和物理意义作为终稿重点
