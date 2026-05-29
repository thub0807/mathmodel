# q5 Sensitivity

## Key Parameters

- 邻域生成步长：`0.1`, `0.2`
- 候选混合策略：`top5=3 exploit + 2 explore`，`top10=6 exploit + 4 explore`

## Main Findings

1. 如果只做 exploit，候选会过于集中在少数高 trust 模式附近，探索价值不足。
2. 如果把 trust 约束完全放松，候选虽然更新奇，但平均预测综合性能会明显回落。
3. 当前混合策略因此更适合作为一轮有限实验预算下的平衡方案。
