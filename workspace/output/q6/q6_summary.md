# q6 候选配方稳健性建模
## main results with source fields

- 在半径 `0.1` 的邻域审查下，stable basin 有 `0` 个，isolated peak 有 `5` 个。来源：`main_result.robustness_overview`
- 最优稳健候选为 `q5cand_0252`，稳健性得分 `0.7420`。来源同上。
- 半径放大到 `0.2` 后，候选平均 `PI` 变化的均值为 `-0.0076`。来源：`metrics.mean_radius_drop`

## paper-ready subsection draft

候选配方是否值得继续开发，不能只看中心点预测分数，还必须看其邻域内的表现是否稳定。我们以 `q5` 的 10 组候选为中心，对每组配方构造半径 `0.1` 与 `0.2` 的局部扰动邻域，并比较邻域平均 `PI`、最小 `PI`、标准差以及 pH 可接受率。结果显示，在半径 `0.1` 下共有 `0` 个候选可归入 stable high-performance basin，而另有 `5` 个候选虽然中心分数较高，但对局部扰动更敏感，更像 isolated peak。  
因此，最终推荐不应简单地“挑最高分”，而应优先选择落在稳定高分盆地内的候选，把孤立尖峰保留为补充探索对象。这一结论与 `q4` 的可信域分析是一致的：高中心分数只有在局部邻域也稳定时，才更适合进入开发优先序列。

## status

`pass`
