# q1 Code

- 模型名：门槛约束-CRITIC-TOPSIS 综合评价模型
- 对应问题：`q1`
- 输入：`workspace/problem/attachments/A_data.json`、`workspace/problem/attachments/README.txt`
- 主要输出：
  - `workspace/output/q1/results/result.json`
  - `workspace/output/q1/results/run.log`
  - `workspace/output/q1/results/indicator_table.csv`
  - `workspace/output/q1/results/top_formula_snapshot.csv`
  - `workspace/output/q1/figures/*.png`
  - `workspace/output/q1/tables/*.csv`
- 运行方式：

```bash
python workspace/output/q1/code/q1_build.py
```

- 说明：
  - 代码参考 `templates/shared/code_starter/evaluation.py` 的评价类结构实现。
  - 主路线采用 CRITIC 赋权与 TOPSIS 排序。
  - 基线为单纯电导率排序。
  - 鲁棒对照为基于第一主成分的综合得分。
