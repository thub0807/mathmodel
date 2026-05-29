# q2 Code Notes

- 对应问题：`q2` 配方到性能的预测模型
- 主路线：配方结构增强的目标自适应受限加权树集成预测模型
- 锁定语言：`python`
- 主要输入：
  - `workspace/problem/problem.md`
  - `workspace/problem/attachments/A_data.json`
  - `workspace/problem/attachments/README.txt`
  - `workspace/output/q1/results/indicator_table.csv`
  - `workspace/output/q1/results/result.json`
- 主要输出：
  - `workspace/output/q2/results/result.json`
  - `workspace/output/q2/results/run.log`
  - `workspace/output/q2/results/feature_table.csv`
  - `workspace/output/q2/results/target_table.csv`
  - `workspace/output/q2/results/model_probe.csv`
  - `workspace/output/q2/results/oof_predictions.csv`
  - `workspace/output/q2/results/slice_error_summary.csv`
  - `workspace/output/q2/results/pi_consistency_summary.csv`
  - `workspace/output/q2/results/sensitivity_probe.csv`

运行命令：

```bash
python workspace/output/q2/code/q2_build.py
```

说明：

- 主路线候选模型包含 `RandomForestRegressor`、`ExtraTreesRegressor`、`HistGradientBoostingRegressor` 及两个预先固定的简单融合：`Blend_RF_ET`、`Blend_Tree3`。
- 为避免融合权重信息泄漏，正式 Build 使用预先固定的简单融合，而不是根据测试折表现回填权重。
- `PI` 同时保留“直接预测头”和“由预测的 `conductivity/pH/W_1/R_W` 重构得到的 `PI_recon`”，供 Stage 4 做一致性检查。
