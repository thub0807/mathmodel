# q1 Warnings

| issue id | severity | verdict impact | artifact | finding | required fix | downstream impact | status |
|---|---|---|---|---|---|---|---|
| `Q1-W01` | Medium | `PARTIAL` if hidden | `review_packet.md`, `result.json`, `validation.md` | 稳定性相关指标只来自 `fast_assessment` 电化学曲线与派生量，属于短时稳定性 proxy，不能外推为循环寿命或长期工程稳定性。 | 在 `q1_summary.md`、后续 `q2`-`q6` summary 和 final traceability 中保持“短时稳定性 proxy”表述。 | 影响所有后续把 `q1` 指标当作标签或目标量的任务。 | open-limitation |
| `Q1-W02` | Medium | `PARTIAL` for exact ranking | `sensitivity.md`, `q1_summary.md` | 当 pH 适宜区间由 `[6.5, 8.5]` 改为 `[6.0, 8.0]` 时，Top10 与基准只重合 `6/10`，且榜首样本发生变化。 | 将“多指标优于单电导率”的主结论保留为 full claim；将“具体 Top10 roster / Top1 配方”降级为条件稳定结论。 | `q2` 可使用 `PI` 作为目标量，但 `q5` 和 `q6` 若直接引用单个榜首配方，需附带 pH 区间条件。 | open-limitation |
| `Q1-W03` | Low | `PASS` with note | `validation.md` | `R_W` 有 `7` 条样本略高于 `1.0`，其中 `5` 条高于 `1.05`，最大值约 `1.073`。 | 在验证与摘要中说明这更像派生量阈值差异造成的轻微异常，不作为推翻主路线的依据。 | 影响对 `R_W` 的物理解释强度，但不改变主模型结构。 | noted |
| `Q1-W04` | Low | `PASS` | `figures/figure_index.md`, `tables/table_index.md` | 图表已生成，但图中使用英文标签以规避当前运行环境的中文字体缺失。 | 在图表索引与论文图题中用中文解释图意即可，无需重画。 | 只影响展示语言，不影响证据链。 | noted |
