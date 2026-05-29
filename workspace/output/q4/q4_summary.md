# q4 模型可信度与适用范围分析
## main results with source fields

- 最差随机 OOF 区域误差倍率为 `1.87`，说明不同结构区域的误差并不一致。来源：`main_result.cluster_validation.worst_random_oof_ratio`
- leave-one-cluster-out 最差 MAE 为 `25.9864`，比随机切分更严格地暴露了跨区域外推风险。来源：`main_result.cluster_validation.worst_holdout_mae`
- high trust 区的 `PI` MAE 为 `0.0232`，low trust 区为 `0.0597`，二者相差 `2.57` 倍。来源：`metrics.pi_mae_gap_low_vs_high`

## paper-ready subsection draft

仅靠随机划分训练集与测试集，不足以评价模型在不同配方区域中的真实可用性。我们首先在组合特征空间中把 251 条样本划分为 4 个结构簇，然后分别统计随机 OOF 和 leave-one-cluster-out 的区域误差。结果显示，最差区域的误差倍率可达到整体平均的 `1.87` 倍，而最差簇外推的 MAE 也明显高于常规随机 OOF。  
在此基础上，我们进一步把样本按局部密度、`uncertainty_hook_PI` 与 rare pattern 标记划分为 high / medium / low trust 三层。`PI` 在 high trust 区的 MAE 仅为 `0.0232`，到了 low trust 区则升至 `0.0597`。因此，`q2` 模型更适合在 high trust 邻域内做开发型推荐，而对 low trust 区域应以探索和风险标注为主。

## status

`pass`
