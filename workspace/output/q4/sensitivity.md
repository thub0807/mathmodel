# q4 Sensitivity

## Key Parameters

- 聚类数当前固定为 `4`
- trust tier 由局部密度、`uncertainty_hook_PI` 与 rare_pattern 共同定义

## Main Findings

1. 可信等级差异比“是否随机分到测试折”更能解释误差高低。
2. 结构簇 holdout 的结果强化了 `q2` 已经给出的结论：低 `PI`、稀有模式和远离已见邻域的样本更难预测。
3. 因此，q4 的核心稳定结论不是“模型整体精度够高”，而是“模型的适用范围可以被分层刻画”。
