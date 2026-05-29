# q6 Sensitivity

## Key Parameters

- 邻域半径：`0.1`, `0.2`
- 稳健性分类：基于局部均值、局部最小值、标准差和 pH 可接受率

## Main Findings

1. 半径从 0.1 放大到 0.2 后，部分候选的平均 PI 明显下降，说明它们更像局部尖峰。
2. 真正稳健的候选在两个半径下都保持较高局部均值和较低方差。
3. 因此，最终推荐应优先 stable basin，再把 isolated peak 作为补充探索对象。
