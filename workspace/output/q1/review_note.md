# q1 Review Note

## Layer 1 Local Critic

Reviewed artifacts:

- `workspace/output/q1/review_packet.md`
- `workspace/output/q1/results/result.json`
- `workspace/output/q1/results/run.log`
- `workspace/output/q1/validation.md`
- `workspace/output/q1/sensitivity.md`
- `workspace/output/q1/figures/figure_index.md`
- `workspace/output/q1/tables/table_index.md`
- `workspace/output/q1/q1_summary.md`
- `workspace/output/q1/warnings.md`

Local verdict: PASS

| issue id | severity | artifact | finding | evidence | required patch | downstream impact | status |
|---|---|---|---|---|---|---|---|
| `Q1-C01` | Medium | `result.json`, `validation.md` | 稳定性指标能够回答题目中的“稳定性相关指标”，但只能作为短时 proxy 使用。 | 数据只提供 `fast_assessment` 曲线与 4 个派生阈值字段。 | 在 summary 和后续引用中固定为“短时稳定性 proxy”。 | 若省略该限定，会夸大 `q5`、`q6` 的证据强度。 | open-limitation |
| `Q1-C02` | Medium | `sensitivity.md`, `q1_summary.md` | pH 适宜区间是当前指标体系最敏感的设定项。 | pH 区间改为 `[6.0, 8.0]` 后，Top10 与基准只重合 `6/10`，相关系数降到 `0.6936`。 | 将“精确 Top10 / Top1 配方”降级为条件稳定结论。 | 影响后续候选配方直接继承 `q1` 排名时的措辞。 | open-limitation |
| `Q1-C03` | Low | `validation.md` | `R_W` 存在少量大于 1 的样本，说明派生阈值口径并非严格保持 `W_1 <= W_T`。 | `7` 条样本 `R_W > 1.0`，其中 `5` 条 `R_W > 1.05`，最大值 `1.0726`。 | 作为数据级轻微异常记录，不单独回退模型。 | 影响 `R_W` 的物理解释精度，但不推翻主流程。 | noted |
| `Q1-C04` | Low | `validation.md`, `q1_summary.md` | 主路线与 PCA 载荷对照保持正相关，说明结论不完全依赖单一权重方案。 | `PI` 与 PCA 对照的 Spearman 相关为 `0.8796`。 | 保留 PCA 作为鲁棒对照，无需返工。 | 有助于支撑 `q1` 主路线的可解释性与稳健性。 | accepted |
| `Q1-C05` | Low | `result.json`, `q1_summary.md` | “单独使用电导率不足”的核心主张证据充分。 | `conductivity` 排名与 `PI` 排名的 Spearman 相关仅 `0.4154`，Top10 重合数 `0/10`。 | 可作为 full claim 进入后续论文侧。 | 为 `q2` 到 `q6` 提供统一目标量和评价口径。 | accepted |

## 审查结论

- `q1` 已形成可追溯的 Build、Validation、Sensitivity、Figure/Table 和 Summary 闭环。
- 当前无需回到 Stage 2 或 Stage 3 重建主路线。
- 允许进入下一问，但后续引用 `q1` 时必须沿用本文件和 `warnings.md` 中的限制措辞。

## Remaining Limitations

- `q1` 的稳定性指标是短时 proxy，不等价于长期循环寿命。
- 精确榜首配方对 pH 适宜区间设定敏感，应写成条件稳定结论。
- `R_W` 的少量异常值提示后续若要做更强的机理解释，最好重新核对派生阈值算法。

## review material paths

- `workspace/output/q1/q1_summary.md`
- `workspace/output/q1/results/result.json`
- `workspace/output/q1/validation.md`
- `workspace/output/q1/sensitivity.md`
- `workspace/output/q1/warnings.md`
- `workspace/output/q1/review_note.md`
