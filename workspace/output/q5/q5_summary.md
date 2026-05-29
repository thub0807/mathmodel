# q5 下一轮实验候选设计
## main results with source fields

- 候选池共有 `663` 条，可行筛选后保留 `398` 条。来源：`main_result.candidate_pool_summary`
- top5 推荐的平均 `pred_PI` 为 `0.8204`，比随机基线高 `0.0170`。来源：`metrics.top5_gain_vs_random_mean_PI`
- top10 推荐的平均 `pred_PI` 为 `0.8219`，比随机基线高 `0.0181`。来源：`metrics.top10_gain_vs_random_mean_PI`

## paper-ready subsection draft

在实验预算有限的前提下，下一轮候选设计不能只做“局部最优微调”，也不能完全随机探索。为此，我们以 `q2` 的预测结果为收益估计，以 `q4` 的可信域为风险约束，在已观测样本邻域内生成单步与双步体积转移候选。随后把候选分成开发型与探索型两类：前者优先高 `pred_PI`、高 `W_1`、高 pH 适宜度且位于 high/medium trust 邻域；后者允许进入 medium/low trust 区，但必须保持基本性能门槛。  
结果表明，top5 推荐的平均 `pred_PI` 为 `0.8204`，比同一候选池上的随机基线高 `0.0170`；top10 推荐的平均 `pred_PI` 为 `0.8219`，也高于随机基线 `0.0181`。因此，当前推荐方案更像“有证据约束的主动实验设计”，而不是盲目穷举或纯贪心搜索。

## status

`pass`
