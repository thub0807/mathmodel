# q1 Validation

## Reviewed Artifacts

- `workspace/output/q1/review_packet.md`
- `workspace/output/q1/results/result.json`
- `workspace/output/q1/results/run.log`
- `workspace/output/q1/results/indicator_table.csv`
- `workspace/output/q1/tables/table_q1_top10_formulations.csv`
- `workspace/output/q1/tables/table_q1_counterexamples.csv`

## Sanity Check

| check item | expected behavior | observed value | pass/partial/fail | implication |
|---|---|---|---|---|
| 样本完整性 | 输入记录数与输出记录数一致，关键字段不缺失 | `251 -> 251`，`conductivity/pH/W_T/W_1/R_W/S_pH/PI` 缺失数均为 `0` | pass | 可以直接进入排序与统计比较 |
| 电化学窗口方向 | `W_T` 与 `W_1` 应保持正值 | `W_T`、`W_1` 正值率均为 `100%` | pass | 稳定窗口定义在数据层面可计算 |
| 评分边界 | `S_pH` 应落在 `[0,1]`，`PI` 应为有限值 | `S_pH` 范围 `[0,1]`，`PI` 范围 `[0.1781, 0.8671]` | pass | 综合分数可比较且无数值爆炸 |
| pH 边界惩罚 | 极端 pH 样本应被显著惩罚 | `S_pH=0` 的样本共 `5` 条，`S_pH=1` 的样本共 `142` 条 | pass | 指标能区分近中性与偏酸/偏碱样本 |
| `R_W` 物理一致性 | 大多数样本应满足 `R_W` 近似不超过 `1` | `R_W > 1.0` 有 `7` 条，`R_W > 1.05` 有 `5` 条，最大值 `1.0726` | partial | 少量派生量口径差异需要作为轻微异常保留 |

## Baseline Comparison

### baseline 方法

- baseline: 按 `conductivity` 单指标降序排序
- main route: 基于 `conductivity`、`S_pH`、`W_1`、`R_W` 的 CRITIC-TOPSIS 综合分数 `PI`
- robust alternative: PCA 载荷加权综合分数

### 对比结果

| comparison item | main model vs baseline | observed value | judgment | implication |
|---|---|---|---|---|
| 排名相关性 | `PI` 与电导率排序不应完全一致，否则综合模型退化为单指标 | Spearman `0.4154` | better | 说明多指标模型显著改变了排序结构 |
| Top10 重合度 | 若电导率已足够，Top10 应高度重合 | `0/10` | better | 强力支持“单独使用电导率不足”这一核心结论 |
| Top10 的 pH 特征 | 综合评价应优先保留近中性样本 | `PI` 前 10 的平均 pH 为 `7.833`；电导率前 10 的平均 pH 为 `5.879` | better | 单纯追求电导率会明显偏向酸性样本 |
| Top10 的稳定窗口 | 综合评价应优先保留较大 `W_1` | `PI` 前 10 的平均 `W_1` 为 `2.5366`；电导率前 10 的平均 `W_1` 为 `1.7432` | better | `PI` 更契合题目对稳定性相关指标的要求 |
| PCA 对照一致性 | 主路线不应完全依赖单一赋权方式 | `PI` 与 PCA 对照的 Spearman 为 `0.8796`，Top10 重合 `4/10` | comparable | 主结论稳定，但精确榜单仍有权重依赖 |

## Constraint Satisfaction

| item | audit result | pass/partial/fail | note |
|---|---|---|---|
| 指标方向一致性 | 所有进入 TOPSIS 的指标均按“越大越好”方向统一 | pass | `conductivity`、`S_pH`、`W_1`、`R_W` 已统一为正向 |
| 权重归一化 | CRITIC 权重和等权 / PCA 对照权重均归一化到 1 | pass | 主权重为 `0.2254, 0.2703, 0.3306, 0.1737` |
| 输出字段契约 | `result.json` 包含 Stage 3 约定字段，且 hard numbers 可追踪 | pass | `status`, `main_result`, `metrics`, `warnings`, `limitations`, `trace` 均存在 |
| 显式异常处理 | 异常值处理不得隐藏 | pass | `run.log` 已记录无缺失、无非正窗口，以及 `R_W` 轻微异常需在验证阶段说明 |

## Boundary Conditions

| boundary case | expected behavior | observed value | pass/partial/fail | implication |
|---|---|---|---|---|
| 代表性 5 样本 toy demo | 最小可行样本应能跑通并出现与单纯电导率不同的排序 | `rank_difference_detected = true` | pass | 证明主路线在小样本上也能激活区分机制 |
| 全等指标矩阵 | 若所有样本四个指标完全相同，模型不应伪造排名差异 | `TOPSIS scores = [0.0, 0.0, 0.0]` | pass | 模型在“无信息差异”情形下会正确退化为并列 |
| 极端 pH 样本 | 偏离工作区间较远时应被显著降权 | 极端 pH 样本的 `S_pH` 降到 `0`，且多条高电导酸性样本在 `PI` 排名中跌出前 200 | pass | pH 惩罚机制真正参与了综合评价 |

## Consistency With Assumptions And Notation

- 与 `review_packet.md` 一致使用 `W_T = V_c^T - V_a^T`、`W_1 = V_c^1 - V_a^1`、`R_W = W_1 / W_T`。
- `S_pH` 的实现与 Plan 中的“区间得满分、偏离按距离递减”一致。
- 未发现代码中新增且未在 `review_packet.md` 公开的隐藏假设。

## Failure Cases

- 若后续任务把 `R_W` 直接解释为严格物理保留率，而忽略其 `7` 条轻微超 1 样本，则会过度声明该指标的物理精确性。
- 若后续任务把当前 Top1 配方视为绝对最优，而忽略 pH 区间敏感性，则会夸大 `q1` 排名的稳定性。

## Validation Verdict

**PASS**

理由：

1. 指标构造、计算与输出链路完整，且不存在阻断性缺失或数值异常。
2. “电导率单指标不足”的核心论断得到强证据支持：相关系数仅 `0.4154`，Top10 重合为 `0/10`。
3. 主路线与 PCA 对照保持较强正相关，说明结论不完全依赖单一权重方案。

## Affected Claims

| claim | status | paper claim eligibility | note |
|---|---|---|---|
| 单独使用电导率不足以定义“好配方” | PASS | full | 可直接进入正文核心结论 |
| 应同时考虑 `conductivity`、`S_pH`、`W_1`、`R_W` 构造综合性能指标 | PASS | full | 可直接作为 `q2` 的目标量定义 |
| 当前 Top10 / Top1 配方名单可被视为绝对最优排序 | PARTIAL | limited | 需结合 `sensitivity.md` 中的 pH 区间限制表达 |
| `R_W` 可以被解释为严格的物理保留率 | PARTIAL | limited | 需保留阈值派生量轻微异常说明 |

## Required Downgrade Or Backtrack

- 不需要回退到 Stage 2 或 Stage 3。
- 需要在 `q1_summary.md` 和后续下游问题中，将“具体榜首配方”降级为条件稳定结论。
