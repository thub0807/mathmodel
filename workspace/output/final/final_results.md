# Final Results

## q1

- status: `pass`
- model: 门槛约束-CRITIC-TOPSIS 综合评价模型
- validation: `PASS`
- sensitivity: `stable`
- paper claim: 综合性能评价需要同时考虑电导率、pH 适宜性和短时稳定性 proxy，单独使用电导率会遗漏一部分高稳定性或近中性样本。
- limitation: 稳定性相关指标仅能表征基于 fast_assessment 电化学曲线的短时稳定性 proxy，不能外推为长期循环寿命结论。

## q2

- status: `pass`
- model: 配方结构增强的目标自适应受限加权树集成预测模型
- validation: `PASS`
- sensitivity: `stable`
- paper claim: 配方结构增强的树集成主路线在 `conductivity`、`pH`、`W_1`、`R_W` 和 `PI` 五个目标上均优于线性基线 `ElasticNet`。
- limitation: `PI`、`W_1`、`R_W` 仍然继承自 `q1` 的短时稳定性 proxy 口径，不能写成长期寿命预测。

## q3

- status: `pass`
- model: 关键组分与交互作用的分区解释模型
- validation: `PASS`
- sensitivity: `stable`
- paper claim: 导电率与综合性能并不是由同一组因素完全主导；离子强度 proxy、硫酸盐/高氯酸盐比例和锂钠体系平衡共同塑造了结果。
- limitation: q3 的解释证据建立在 q2 已验证的预测模型与 permutation importance 上，因此属于数据驱动解释，而不是严格机理定律。

## q4

- status: `pass`
- model: 结构簇-可信域联合验证模型
- validation: `PASS`
- sensitivity: `conditional`
- paper claim: 随机训练/测试切分不足以全面评价模型可用性，因为不同结构区域的误差存在显著异质性。
- limitation: q4 的可信域仍然来自有限样本上的结构聚类与 OOF 误差，不代表真实工艺边界。

## q5

- status: `pass`
- model: 可信域约束下的开发-探索联合候选设计模型
- validation: `PASS`
- sensitivity: `conditional`
- paper claim: 下一轮实验不应只盯着当前最高分样本附近继续微调，而应在开发型与探索型候选之间保持平衡。
- limitation: q5 给出的候选只是一轮实验优先级建议，尚未经过真实实验反馈验证。

## q6

- status: `pass`
- model: 候选配方邻域稳健性判别模型
- validation: `PASS`
- sensitivity: `stable`
- paper claim: 推荐候选中既存在稳定高分盆地，也存在对小幅扰动敏感的孤立高分点。
- limitation: q6 的稳健性仍然是模型预测意义上的局部稳健性，不等于真实工艺鲁棒性。
