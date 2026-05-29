# q4 Validation

## Core Checks

| item | observation | verdict | implication |
|---|---|---|---|
| 结构簇误差异质性 | 最差结构簇/目标组合为 cluster `0` 的 `conductivity`，误差倍率 `1.87` | pass | 随机 OOF 不能代表所有区域 |
| 簇外推误差 | leave-one-cluster-out 最差组合为 cluster `2` 的 `conductivity`，MAE `25.9864` | pass | 跨区域外推比区域内预测更难 |
| trust tier 分层 | high trust 的 PI MAE `0.0232`，low trust 为 `0.0597` | pass | 可信域分层有实际区分度 |

## Validation Verdict

**PASS**

可信域划分与结构簇 holdout 都给出了稳定信号：模型可用，但只在 high / medium trust 邻域内适合做较强结论。
