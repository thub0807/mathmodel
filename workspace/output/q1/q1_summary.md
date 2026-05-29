# q1 综合性能与稳定性指标构造

## question goal

- `q id`: `q1`
- `problem objective`: 建立能够同时反映导电性、酸碱适宜性和电化学稳定性的综合性能指标，并回答“只用电导率是否足够”
- `required output`: 综合性能分数 `PI`、稳定性相关指标 `W_1` 与 `R_W`、与电导率单指标的比较结论
- `evaluation metric`: 指标可解释性、排序区分度、与物理直觉一致性、对后续 `q2` 预测的可建模性
- `relation to other q*`: 为 `q2` 提供预测目标量，为 `q3` 提供解释对象，为 `q5` 和 `q6` 提供候选筛选口径
- `paper section role`: 对应后续论文中的“问题一模型建立、结果分析与灵敏度检验”部分

## model motivation

单独使用电导率只能刻画离子传导能力，却无法区分“高电导但酸性过强、实用稳定窗口偏窄”的配方。题面又明确要求结合 pH 与电化学测试曲线讨论更合理的性能表征，因此本问必须把三个维度统一到同一评价框架中。基于此，本文采用门槛约束-CRITIC-TOPSIS 综合评价模型：先把 pH 转换为工作区间适宜性得分，再利用电化学派生量构造稳定窗口指标，最后用 CRITIC 赋权和 TOPSIS 聚合理想解距离。与仅按电导率排序的 baseline 相比，该模型能够直接回答“什么样的配方可以被认为是好的”，并把结果压缩成后续预测问题可用的单一目标量。

## core assumptions and notation

1. 现有 `fast_assessment` 曲线及其派生量只用于构造短时稳定性 proxy，不将其外推为长期循环寿命。
2. 默认把 pH 工作区间设为 `[6.5, 8.5]`；区间内记满分，区间外按偏离距离线性递减。
3. 评价指标只基于现有 251 条实验记录构造，因此它代表“当前数据支持下的综合性能口径”，而非普适真值。

关键符号如下：

- `kappa`: 电导率
- `S_pH`: pH 适宜性得分
- `W_T = V_c^T - V_a^T`: Tafel 稳定窗口
- `W_1 = V_c^1 - V_a^1`: `1 mA/cm^2` 条件下的实用稳定窗口
- `R_W = W_1 / W_T`: 稳定窗口保留率
- `PI`: 综合性能分数

## core formulas

本文先对 pH 定义区间适宜性分数：

\[
S_{pH}=\max \left(0,\, 1-\frac{d_{pH}}{1.0}\right),
\quad
d_{pH}=\max(0,\, 6.5-pH,\, pH-8.5).
\]

电化学稳定性由两类指标共同表征：

\[
W_T = V_c^T - V_a^T,\qquad
W_1 = V_c^1 - V_a^1,\qquad
R_W = \frac{W_1}{W_T}.
\]

设归一化后的第 `j` 个指标标准差为 `\sigma_j`，相关系数为 `r_{jk}`，则 CRITIC 信息量为

\[
C_j = \sigma_j \sum_k (1-r_{jk}), \qquad
w_j = \frac{C_j}{\sum_j C_j}.
\]

将指标向量 `z_i=[kappa_i,S_{pH,i},W_{1,i},R_{W,i}]` 做 TOPSIS 聚合，得到样本 `i` 的综合性能分数

\[
PI_i=\frac{D_i^-}{D_i^+ + D_i^-},
\]

其中 `D_i^+` 与 `D_i^-` 分别表示样本到正理想解和负理想解的距离。`PI` 越大，样本的综合性能越优。

## algorithm or solve process

1. 读取 `A_data.json` 的 251 条记录，抽取 `conductivity`、`pH`、`derived_quantities` 和配方组成信息。
2. 由派生量计算 `W_T`、`W_1` 和 `R_W`，并按 `[6.5, 8.5]` 生成 `S_pH`。
3. 对四个正向指标构造评价矩阵，使用 CRITIC 计算客观权重。
4. 以 TOPSIS 计算综合性能分数 `PI`，再与电导率单排序、PCA 载荷加权对照进行比较。
5. 将完整中间结果写入 `indicator_table.csv`，将可追溯 hard numbers 写入 `result.json`。

## main results with source fields

主路线得到的 CRITIC 权重依次为：`W_1 = 0.3306`、`S_pH = 0.2703`、`conductivity = 0.2254`、`R_W = 0.1737`。
来源：`workspace/output/q1/results/result.json` -> `main_result.weight_scheme.critic_weights`

这说明在当前数据下，**实用稳定窗口 `W_1` 的信息贡献最高**，而 pH 适宜性的重要性也高于单纯电导率。换言之，若只看电导率，就会忽略题面明确要求讨论的酸碱环境和稳定性维度。

进一步比较 `conductivity` 排序与 `PI` 排序可知，两者的 Spearman 相关系数仅为 `0.4154`，且前 10 名样本的重合数为 `0/10`。
来源：`workspace/output/q1/results/result.json` -> `main_result.baseline_comparison.spearman_cond_vs_PI`, `main_result.baseline_comparison.top10_overlap_count`

这种差异不是偶然的。综合评分前 10 样本的平均电导率为 `163.37`，虽然低于单纯电导率前 10 的 `186.37`，但其平均 pH 为 `7.833`，显著优于后者的 `5.879`；同时其平均 `W_1` 达到 `2.5366`，也明显高于电导率前 10 的 `1.7432`。
来源：`workspace/output/q1/validation.md` -> `Baseline Comparison`

因此，本问的核心结论不是“电导率越高越好”，而是：**高质量配方应同时具备较高电导率、近中性的 pH 和较大的实用稳定窗口**。在默认 pH 区间 `[6.5, 8.5]` 下，当前综合评分最高的样本为 `NaNO3:5.00; NaClO4:1.00`，其 `conductivity = 170.5`、`pH = 7.54`、`W_1 = 2.5464`、`PI = 0.8671`。不过这一条具体榜首结论只应视为**条件稳定**结果，而不应写成绝对最优。
来源：`workspace/output/q1/results/result.json` -> `main_result.top_formulations[0]`

## validation conclusion

验证结果表明，当前指标体系在数值层面是自洽的：251 条样本全部成功生成 `W_T`、`W_1`、`R_W`、`S_pH` 和 `PI`，没有缺失值；`W_T` 与 `W_1` 全部为正，`S_pH` 落在 `[0,1]`，`PI` 落在 `[0.1781, 0.8671]`。同时，边界测试表明当四项指标完全相同时，TOPSIS 会退化为并列分数，而不会伪造排序差异；代表性 5 样本 toy demo 也能稳定地产生与单纯电导率不同的排序。

需要保留的验证限制有两点。第一，`R_W` 存在 `7` 条略高于 `1.0` 的样本，其中 `5` 条高于 `1.05`，最大值为 `1.0726`，这提示派生阈值口径并非严格满足 `W_1 <= W_T`。第二，稳定性相关指标的物理含义仍应限定为短时 proxy，不能借此直接推出长期寿命。基于这些事实，本问整体 validation verdict 为 **PASS**，但物理解释强度和精确排名主张需要保留限制。

## sensitivity conclusion

灵敏度分析表明，**pH 工作区间是当前模型最主要的敏感源**。当区间由 `[6.5, 8.5]` 改为 `[6.0, 8.0]` 时，Top10 与基准只保留 `6/10`，排序相关系数降到 `0.6936`，榜首样本也发生变化；当区间改为 `[7.0, 9.0]` 时，Top10 仍保留 `9/10`，榜首不变。相较之下，权重混合系数 `alpha` 在 `[0.6, 1.0]` 内变化时，Top10 至少保留 `9/10`，Spearman 相关均高于 `0.99`，说明排序对赋权方式并不脆弱。

若只保留 `W_1` 而移除 `R_W`，Top1 样本仍保持不变，但 Top10 只保留 `7/10`。这说明 `R_W` 更多承担“高分样本细排序”的作用，而不是决定是否进入高分区。综合来看，**“必须采用多指标综合评价”是稳定结论；“哪一条具体配方排第一”则是条件稳定结论**。

## figures and tables for paper use

- 图 1 `workspace/output/q1/figures/figure_q1_score_vs_conductivity.png`
  - 支撑 claim：`PI` 与电导率排序存在显著差异
- 图 2 `workspace/output/q1/figures/figure_q1_weight_comparison.png`
  - 支撑 claim：`W_1` 和 `S_pH` 在主路线中具有实质权重
- 图 3 `workspace/output/q1/figures/figure_q1_sensitivity_overlap.png`
  - 支撑 claim：精确排名对 pH 区间敏感，但对权重混合不敏感
- 表 2 `workspace/output/q1/tables/table_q1_top10_formulations.csv`
  - 支撑 claim：默认口径下高分样本的共同结构
- 表 3 `workspace/output/q1/tables/table_q1_counterexamples.csv`
  - 支撑 claim：存在“高电导但综合评分低”的反例样本
- 表 4 `workspace/output/q1/tables/table_q1_sensitivity_summary.csv`
  - 支撑 claim：pH 区间是主要敏感项

## paper-ready subsection draft

针对题目中“什么样的配方可以被认为是好的”这一问题，本文认为单独采用电导率作为评价标准并不充分。电导率只能表征离子传导能力，而题面同时强调了 pH 环境与电化学稳定性的重要性，因此我们构造了由电导率 `kappa`、pH 适宜性 `S_pH`、实用稳定窗口 `W_1` 与窗口保留率 `R_W` 组成的综合评价体系。其中，`S_pH` 用于刻画配方是否处于近中性的可用工作区间，`W_1` 与 `R_W` 则分别反映实用电流密度下的稳定窗口大小及其相对于 Tafel 窗口的保留程度。

在赋权与聚合方面，本文采用 CRITIC 赋权与 TOPSIS 排序相结合的门槛约束-CRITIC-TOPSIS 综合评价模型。该模型首先根据各指标的离散程度和冲突程度确定客观权重，再通过样本到正负理想解的距离计算综合性能分数 `PI`。计算结果表明，四项指标的权重依次为 `W_1 = 0.3306`、`S_pH = 0.2703`、`conductivity = 0.2254`、`R_W = 0.1737`，说明在当前数据中，实用稳定窗口和 pH 适宜性对“好配方”的识别作用并不弱于电导率，反而更能区分那些高电导但不适宜实际应用的样本。

进一步将综合排序与电导率单排序比较，可见两者的 Spearman 相关系数仅为 `0.4154`，且前 10 名样本完全不重合。这说明如果只按电导率从高到低筛选配方，将明显偏向酸性较强的样本。事实上，综合评分前 10 样本的平均 pH 为 `7.833`，平均实用稳定窗口 `W_1` 为 `2.5366`；而电导率前 10 样本的平均 pH 仅为 `5.879`，平均 `W_1` 也只有 `1.7432`。因此，从工程可用性的角度看，电导率高并不等于综合性能优。

验证与灵敏度分析进一步表明，该综合指标体系在方法层面是可信的，但其精确排名仍具有条件稳定性。一方面，251 条样本均能稳定生成 `PI`，且窗口指标整体保持正值；另一方面，少量样本的 `R_W` 略高于 `1`，提示该指标应被理解为短时 proxy 而非严格机理量。此外，当 pH 工作区间由 `[6.5, 8.5]` 放宽到 `[6.0, 8.0]` 时，Top10 与基准只保留 `6/10`，榜首样本也会变化。因此，本文建议把“需要构造多指标综合评价体系”作为稳健结论写入论文正文，而把“具体哪一条配方排第一”保留为带条件的结果。

## traceable claims table

| claim | source file | source field | status | paper use | limitation note |
|---|---|---|---|---|---|
| `W_1` 的 CRITIC 权重最高，达到 `0.3306` | `workspace/output/q1/results/result.json` | `main_result.weight_scheme.critic_weights.W_1` | pass | full | 无 |
| `PI` 与电导率排序的 Spearman 相关系数仅为 `0.4154` | `workspace/output/q1/results/result.json` | `main_result.baseline_comparison.spearman_cond_vs_PI` | pass | full | 无 |
| 电导率前 10 与综合评分前 10 的重合数为 `0/10` | `workspace/output/q1/results/result.json` | `main_result.baseline_comparison.top10_overlap_count` | pass | full | 无 |
| 综合评分前 10 的平均 pH 为 `7.833`，电导率前 10 的平均 pH 为 `5.879` | `workspace/output/q1/validation.md` | `Baseline Comparison` | pass | full | 无 |
| 当 pH 区间改为 `[6.0, 8.0]` 时，Top10 与基准只保留 `6/10` | `workspace/output/q1/sensitivity.md` | `Single-Parameter Perturbation` | partial | limited | 说明精确排名对 pH 区间敏感 |
| 默认口径下榜首样本为 `NaNO3:5.00; NaClO4:1.00` | `workspace/output/q1/results/result.json` | `main_result.top_formulations[0]` | pass | limited | 仅在默认 pH 区间 `[6.5, 8.5]` 下成立 |

## limitations and improvements

1. 当前稳定性指标只基于短时电化学曲线构造，若未来有循环寿命或长期腐蚀数据，应把它们纳入新的稳定性维度。
2. pH 工作区间的设定对精确排名较敏感，后续可以结合更明确的实验安全窗口或工程工况重新标定区间。
3. `R_W` 的少量异常值提示派生阈值提取算法仍值得复核，若能直接从原始曲线重构阈值位置，可进一步增强指标的物理一致性。

## status

`pass`
