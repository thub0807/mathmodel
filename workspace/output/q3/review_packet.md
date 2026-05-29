# q3 Review Packet

## AP mode note

当前问题按 AP 模式自动推进，不再等待人工 Review Gate，但仍保留完整审查包、警告和 review note。

## question card

- q id: `q3`
- title: 关键组分与交互作用解释
- upstream: `q1`, `q2`
- goal: 在 `q2` 已通过验证的预测模型基础上，识别影响导电率与综合性能的关键组分、交互作用及其区域稳定性。

## upstream context

- 已读取 `q1_summary.md`、`q1/results/result.json`
- 已读取 `q2_summary.md`、`q2/results/result.json`、`q2/validation.md`、`q2/sensitivity.md`
- 继承限制：稳定性结论仍是短时 proxy；稀有模式和低 `PI` 区域解释强度较弱

## planned outputs

- `workspace/output/q3/results/driver_ranking.csv`
- `workspace/output/q3/results/interaction_summary.csv`
- `workspace/output/q3/results/stability_summary.csv`
- `workspace/output/q3/q3_summary.md`

## auto-entry verdict

`PASS`
