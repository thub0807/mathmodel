# q2 配方到性能的预测模型

## question goal

- `q id`: `q2`
- `problem objective`: 仅利用配方组成信息及其派生特征，预测 `conductivity`、`pH`、`W_1`、`R_W` 与 `PI`
- `required output`: 各目标的预测模型、与线性/潜变量对照的比较、OOF 预测结果、误差分区分析、可供 `q3`/`q4`/`q5` 复用的不确定性与特征重要性 hook
- `evaluation metric`: OOF 的 MAE、RMSE、`R^2`、排序保持性、高低性能区与稀有模式切片误差
- `relation to other q*`: 为 `q3` 提供解释入口，为 `q4` 提供可信域诊断，为 `q5`/`q6` 提供预测均值与 uncertainty hook
- `paper section role`: 对应后续论文中的“问题二模型建立、模型比较、验证与灵敏度分析”部分

## model motivation

题面要求由配方组成信息直接预测电导率、pH 以及 `q1` 中构造的综合性能与稳定性相关指标，这意味着模型既要容纳配方组分之间的非线性和协同效应，又要在仅有 251 条记录的小样本条件下保持可审计性。基于 `q2` Plan 与返工 probe，本文采用配方结构增强的目标自适应树路线：先构造由比例、存在性、浓度/质量 proxy、全局聚合特征和配方结构 dummy 组成的统一特征库，再在 `RandomForest`、`ExtraTrees`、`HistGB` 及其简单融合之间进行 OOF 对比，并按照目标差异决定最终路线。为了满足 `Q2-W05` 的反泄漏约束，正式 Build 没有使用“看测试折调权”的自由融合，而是使用预先固定的简单融合 `Blend_RF_ET` 与 `Blend_Tree3`。

这一路线的选择理由有三点。第一，`q1` 已经表明单独使用电导率不足以表征“好配方”，因此 `PI/W_1/R_W` 需要与 `conductivity/pH` 一起被学习。第二，返工 probe 显示简单三树融合在 `conductivity`、`pH` 和 `PI` 三个关键目标上都优于最佳单树，说明融合收益是真实存在的。第三，树路线不仅能输出预测值，还能生成 OOF 残差、切片误差、局部密度和 permutation importance，为 `q3` 到 `q6` 提供直接接口。

## core assumptions and notation

1. `PI`、`W_1`、`R_W` 的定义完全沿用 `q1`，因此它们仍然是建立在短时电化学曲线上的 proxy 标签，而不是长期寿命真值。
2. 配方中未出现的组分被记为 `0.0 structural zero`，代表结构性缺失，而不是随机漏测。
3. 通过 `volume * density * molality` 构造的 proxy 特征只用于近似投料强度和离子强度，不被解释为严格热力学状态量。

关键符号如下：

- `x_i`: 第 `i` 条配方的特征向量
- `ratio_j`: 第 `j` 种母液的体积分数
- `present_j`: 第 `j` 种组分是否出现的结构零指示量
- `\hat y_i^{(k)}`: 第 `k` 个目标的预测值
- `u_i^{(k)}`: 由树间预测离散度和局部密度组合得到的 heuristic uncertainty hook
- `\widehat{PI}^{recon}`: 由预测的 `conductivity/pH/W_1/R_W` 通过 `q1` 固定权重重构得到的 `PI`

## core formulas

对每个目标 `k`，本文先训练三类树基学习器：

\[
f_k^{RF}(x), \qquad f_k^{ET}(x), \qquad f_k^{GB}(x).
\]

对于 `conductivity`、`pH`、`W_1` 和 `PI`，正式 Build 采用预先固定的简单三树融合：

\[
\hat y_i^{(k)}=\frac{1}{3}\left(f_k^{RF}(x_i)+f_k^{ET}(x_i)+f_k^{GB}(x_i)\right),
\qquad
k\in\{\text{conductivity},\text{pH},W_1,PI\}.
\]

对于 `R_W`，由于单树 `RandomForest` 已优于融合候选，因此保留

\[
\hat y_i^{(R_W)} = f_{R_W}^{RF}(x_i).
\]

为了检查综合目标量的自洽性，本文还构造

\[
\widehat{PI}^{recon}_i = g(\hat \kappa_i,\hat pH_i,\widehat{W_1}_i,\widehat{R_W}_i),
\]

其中 `g(\cdot)` 使用 `q1` 固定的 pH 适宜性评分与 CRITIC-TOPSIS 权重口径。若 `\widehat{PI}` 与 `\widehat{PI}^{recon}` 偏差过大，则说明直接头虽然精度较高，但解释链条较弱。

## algorithm or solve process

1. 读取 `A_data.json`，为每条配方构造比例特征、存在性特征、`mass_proxy_*`、`mol_proxy_*`、`ionic_strength_proxy`、`weighted_density`、`pattern_key` 及其 dummy，共得到 `73` 个输入特征。
2. 读取 `q1/results/indicator_table.csv`，按 `GUID` 合并 `conductivity`、`pH`、`W_1`、`R_W` 与 `PI` 五个目标。
3. 在 5 折 OOF 下分别训练 `ElasticNet`、`PLSRegression`、`RandomForest`、`ExtraTrees`、`HistGB` 及两个固定融合，并比较 OOF 的 MAE、RMSE、`R^2` 和 Spearman。
4. 根据目标差异确定最终路线：`conductivity/pH/W_1/PI -> Blend_Tree3`，`R_W -> RandomForest`。
5. 基于最终路线生成 `oof_predictions.csv`、`slice_error_summary.csv`、`pi_consistency_summary.csv`、`sensitivity_probe.csv` 和 permutation importance 结果，再把关键硬数字写入 `result.json`。

## main results with source fields

正式 Build 的最终路线为：`conductivity/pH/W_1/PI` 使用 `Blend_Tree3`，`R_W` 使用 `RandomForest`。
来源：`workspace/output/q2/results/result.json` -> `main_result.cv_summary.selected_routes`

在五个目标上的 OOF MAE 分别为：`conductivity = 7.8566`、`pH = 0.1740`、`W_1 = 0.04431`、`R_W = 0.01562`、`PI = 0.03467`。
来源：`workspace/output/q2/results/result.json` -> `main_result.target_model_selection.*.selected_mae`

相对于 `ElasticNet`，上述主路线在五个目标上的 MAE 改进分别约为 `2.16%`、`10.86%`、`13.56%`、`18.78%` 和 `24.18%`。这表明树路线对 `PI` 和稳定性相关指标的提升尤其明显。
来源：`workspace/output/q2/results/result.json` -> `main_result.target_model_selection.*.gain_vs_elasticnet_mae`

在关键目标的模型比较中，`Blend_Tree3` 对 `conductivity`、`pH`、`PI` 的 MAE 都优于最佳单树：`conductivity 7.8566 < 8.4225`，`pH 0.1740 < 0.1822`，`PI 0.03467 < 0.03606`。这说明简单树融合的收益不是偶然的。
来源：`workspace/output/q2/results/model_probe.csv`

对于 `PI` 的双路径检查，direct head 的 overall MAE 为 `0.03467`，低于 recon 的 `0.03911`；但二者的 overall Spearman 仍达到 `0.9662`。这说明 direct 头更偏精度，而 recon 头保留了更强的解释入口。
来源：`workspace/output/q2/results/result.json` -> `main_result.pi_consistency_summary`

从特征重要性看，`conductivity` 和 `PI` 都主要受 `ionic_strength_proxy`、硫酸盐/高氯酸盐相关比例以及锂/钠体系比例影响；`pH` 的首要特征则转向 `lithium_ratio` 与 `ratio_NaClO4`；`W_1`、`R_W` 对 `NaBr` 相关特征更敏感。这些结果为后续 `q3` 的机理讨论提供了定量入口。
来源：`workspace/output/q2/results/feature_importance_summary.csv`

## validation conclusion

验证结果表明，`q2` 的实现链路是稳定可用的：251 条样本全部成功生成 OOF 预测，没有出现未处理 NaN、负电导率、越界 pH、负 `W_1` 或超出 `[0,1]` 的 `PI` 预测；toy demo 也在 60 样本下成功复现了树路线相对线性基线的优势。更重要的是，`PI` 直接头与重构头保持了 `0.9662` 的高 Spearman 相关，不确定性 hook 与误差也存在中等正相关，这意味着主路线既能提供预测值，也能提供后续可信度线索。

不过，验证同时揭示了三个不能隐藏的限制。第一，`conductivity` 头虽然在整体 MAE 上优于 `ElasticNet`，但在高 `PI` Top10 切片上的 MAE 为 `6.7864`，高于线性基线的 `4.1390`；因此它不是“所有局部区域都更好”的模型。第二，`R_W` 头是五个目标中最弱的一头，整体 `R^2 = 0.7006`，且在 `R_W > 1` 切片上的误差接近整体的 `3` 倍。第三，`PI` 的 Top10 只与真实 Top10 重合 `7/10`，说明它适合候选筛选，但不能被写成“精确复原了真实榜单”。基于这些事实，本问整体 validation verdict 为 **PASS**，但局部区域和局部目标的 claim 必须显式降级。

## sensitivity conclusion

灵敏度分析表明，**proxy block 是当前主路线最关键的特征组**。当删除 `mass_proxy_*`、`mol_proxy_*`、`weighted_density`、`ionic_strength_proxy` 等 proxy 特征后，`conductivity` 的 MAE 从 `7.8566` 上升到 `9.5179`，升幅约 `21.2%`；`PI` 也从 `0.03467` 升到 `0.03765`，升幅约 `8.6%`。这说明模型确实利用了“配方强度”信息，而不是仅靠比例和结构 dummy 在拟合。

相比之下，CV 折叠随机种子从 `42` 改为 `7` 时，五个目标的 MAE 只发生小幅波动，没有推翻主路线。`Blend_Tree3` 也在 `conductivity`、`pH` 和 `PI` 上持续优于最佳单树，因此“简单树融合有稳定收益”这一结论是稳健的。

真正的失稳边界来自局部区域而不是折叠随机性。以 `PI` 为例，`low_PI_bottom10` 切片上的 MAE 为 `0.1042`，约为整体的 `3.01` 倍；稀有模式切片上的 MAE 也达到整体的 `1.53` 倍。若进一步叠加“低 `PI` + 稀有模式”这类 stress 场景，模型误差会明显放大。因此，本问最稳健的结论不是“模型全空间都很好”，而是“模型在高分区与已见邻域内更可信，在低分区和稀有模式区应谨慎使用”。

## figures and tables for paper use

- 图 1 `workspace/output/q2/figures/figure_q2_model_mae_comparison.png`
  - 支撑 claim：`Blend_Tree3` 在关键目标上的 MAE 优于单树与线性对照
- 图 2 `workspace/output/q2/figures/figure_q2_pi_parity_and_recon.png`
  - 支撑 claim：`PI` direct head 与 recon head 总体一致，但在极端切片存在差异
- 图 3 `workspace/output/q2/figures/figure_q2_slice_error_ratio.png`
  - 支撑 claim：低 `PI` 区域与稀有模式区域更难预测
- 图 4 `workspace/output/q2/figures/figure_q2_feature_importance_heatmap.png`
  - 支撑 claim：不同目标受不同配方因子主导
- 表 1 `workspace/output/q2/tables/table_q2_main_model_summary.csv`
  - 支撑 claim：五个目标的最终路线与路由权重
- 表 3 `workspace/output/q2/tables/table_q2_slice_error_summary.csv`
  - 支撑 claim：误差具有明显区域异质性
- 表 4 `workspace/output/q2/tables/table_q2_pi_consistency_summary.csv`
  - 支撑 claim：`PI` direct/recon 的一致性与差异
- 表 5 `workspace/output/q2/tables/table_q2_feature_importance_top.csv`
  - 支撑 claim：为 `q3` 提供重要特征入口

## paper-ready subsection draft

针对题目中“由配方组成信息预测其性能”的要求，本文构建了一个配方结构增强的目标自适应树路线。具体而言，我们首先从 `A_data.json` 中提取母液比例、是否出现、浓度/质量 proxy、离子强度 proxy 和配方结构 dummy，共形成 73 个输入特征；随后分别对 `conductivity`、`pH`、`W_1`、`R_W` 与 `PI` 建立 OOF 预测模型。考虑到样本规模仅有 251 条，且必须避免融合权重信息泄漏，正式实现没有采用基于测试折回填权重的自由 stacking，而是使用了预先固定的简单树融合 `Blend_Tree3` 与 `Blend_RF_ET`，再结合目标差异选择最终路线。

OOF 结果表明，`conductivity/pH/W_1/PI` 四个目标都更适合由 `Blend_Tree3` 预测，而 `R_W` 保留单树 `RandomForest` 即可。对应的 OOF MAE 分别为 `7.8566`、`0.1740`、`0.04431`、`0.01562` 和 `0.03467`。相较于 `ElasticNet`，上述主路线在五个目标上的 MAE 都得到降低，其中对综合目标 `PI` 的改善最为明显，降幅约为 `24.18%`。这说明由配方组成到综合性能的映射确实包含不能被单一线性关系充分解释的非线性与交互效应。

为了避免把 `PI` 仅当作一个黑箱分数，本文进一步构造了由预测的 `conductivity/pH/W_1/R_W` 重构得到的 `PI_recon`。结果显示，direct head 的 overall MAE 更低，但它与 `PI_recon` 的 Spearman 相关仍达到 `0.9662`。因此，`PI` 可以继续作为 `q3` 到 `q6` 的统一目标量：若更强调预测精度，可优先使用 direct head；若更强调解释链条，则应同时引用 recon 结果。

验证与灵敏度分析进一步表明，模型的可信度具有明显区域差异。一方面，删除 proxy block 会使 `conductivity` 的 MAE 由 `7.8566` 升至 `9.5179`，说明模型对浓度强度相关特征具有真实依赖；另一方面，`low_PI_bottom10` 和 `rare_pattern` 切片上的误差显著高于整体均值，`R_W > 1` 的异常切片更会使 `R_W` 头明显失稳。由此可见，本文建立的预测模型更适合在已知配方邻域内进行高分区筛选和比较，而不应被润色成“全空间均匀可信”的万能代理。

## traceable claims table

| claim | source file | source field | status | paper use | limitation note |
|---|---|---|---|---|---|
| `conductivity/pH/W_1/PI` 采用 `Blend_Tree3`，`R_W` 采用 `RandomForest` | `workspace/output/q2/results/result.json` | `main_result.cv_summary.selected_routes` | pass | full | 无 |
| 五个目标的 OOF MAE 分别为 `7.8566`、`0.1740`、`0.04431`、`0.01562`、`0.03467` | `workspace/output/q2/results/result.json` | `main_result.target_model_selection.*.selected_mae` | pass | full | 无 |
| `PI` 头相对 `ElasticNet` 的 MAE 降幅约为 `24.18%` | `workspace/output/q2/results/result.json` | `main_result.target_model_selection.PI.gain_vs_elasticnet_mae` | pass | full | 无 |
| `PI` direct head 与 recon head 的 overall Spearman 为 `0.9662` | `workspace/output/q2/results/result.json` | `main_result.pi_consistency_summary.direct_vs_recon_spearman` | pass | full | 解释时需说明二者不完全等价 |
| 删除 proxy block 后，`conductivity` MAE 升到 `9.5179` | `workspace/output/q2/results/sensitivity_probe.csv` | `scenario=drop_proxy_block, target=conductivity` | pass | full | 说明 proxy block 对电导率预测至关重要 |
| `PI` 在 `low_PI_bottom10` 切片上的 MAE 为整体的 `3.01` 倍 | `workspace/output/q2/results/slice_error_summary.csv` | `target=PI, slice=low_PI_bottom10` | partial | limited | 只能作为“区域异质性”证据，不能当作总体精度代表 |
| `R_W` 头在 `R_W > 1` 切片上的 MAE 约为整体的 `2.98` 倍 | `workspace/output/q2/results/slice_error_summary.csv` | `target=R_W, slice=RW_gt_1` | partial | limited | 涉及 `R_W` 的强结论应降级 |

## limitations and improvements

1. 当前标签体系仍继承自 `q1` 的短时稳定性 proxy，若未来获得循环寿命或更长时间窗的稳定性数据，需要重建 `W_1/R_W/PI` 的语义。
2. 低 `PI` 区域和稀有模式区域误差显著增大，说明后续更适合把这些区域视为“探索区”，而不是用当前模型直接做开发决策。
3. `conductivity` 头在高 `PI` Top10 和稀有模式切片上并未优于 `ElasticNet`，后续若专门面向这一局部区域建模，可以尝试局部模型或分区模型。
4. permutation importance 只能提供解释入口；进入 `q3` 时还需要结合配方统计和局部对比做更严格的机理讨论。

## status

`pass`
