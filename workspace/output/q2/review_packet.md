# q2 Review Packet

## question card

| 字段 | 内容 |
|---|---|
| q id | `q2` |
| title | 配方到性能的预测模型 |
| source | `workspace/problem/problem.md` 第一阶段问题 2 |
| goal | 仅利用配方组成信息预测电导率、pH 以及 `q1` 中构造的综合性能与稳定性相关指标，并比较不同模型在精度、稳定性和可解释性上的差异 |
| direct asks | 1. 由配方组成预测一个或多个目标量；2. 比较多种模型的预测精度、稳定性、可解释性；3. 分析高性能区、低性能区和特殊样本上的表现差异及原因 |
| inputs | `problem.md`、`A_data.json`、`README.txt`、`q1` summary/result/validation/sensitivity/warnings/review_note |
| outputs | 每个目标量的预测模型、模型比较表、OOF 预测结果、误差分区分析、可供 `q3` 与 `q5` 复用的特征重要性与不确定性 hook |
| constraints | 预测输入只能来自配方组成信息及其派生特征；`PI`、`W_1`、`R_W` 的定义必须继承 `q1`；所有实现锁定 Python |
| evaluation metric | MAE、RMSE、`R^2`、高性能区误差、排序保持性、模型解释性、对下游问题的可复用性 |
| downstream interface | 为 `q3` 提供特征重要性与局部解释入口；为 `q4` 提供 OOF 残差和区域误差；为 `q5`/`q6` 提供预测均值与不确定性 hook |

## upstream context

已读取以下上游产物：

- `workspace/output/q1/q1_summary.md`
- `workspace/output/q1/results/result.json`
- `workspace/output/q1/validation.md`
- `workspace/output/q1/sensitivity.md`
- `workspace/output/q1/review_packet.md`
- `workspace/output/q1/warnings.md`
- `workspace/output/q1/review_note.md`

当前上游状态与对 `q2` 的影响如下：

1. `q1` 的整体 verdict 为 `PASS`，因此 `conductivity`、`pH`、`W_1`、`R_W` 与 `PI` 可以作为 `q2` 的数值标签使用。
2. `q1` 明确规定 `W_1`、`R_W` 和 `PI` 中的稳定性部分仅代表**短时稳定性 proxy**，因此 `q2` 预测这些标签时，只能声称“预测短时 proxy 指标”，不能写成长期寿命预测。
3. `q1` 的精确 Top1/Top10 排名对 pH 区间 `[6.5, 8.5]` 的设定敏感，因此 `q2` 中的 `PI` 标签默认绑定该区间定义。后续若调整 pH 区间，应视为换标签而非单纯换模型。
4. `q1` 的 `R_W` 存在少量大于 `1.0` 的样本，说明该指标可作为预测目标，但其物理解释强度弱于 `W_1`，Build 阶段需要单独关注该目标的异常残差。

## candidate model matrix

| candidate | kept/rejected | task fit | data need | implementation risk | validation route | paper interpretability | reason |
|---|---|---|---|---|---|---|---|
| 稀疏配方特征 ElasticNet 基线回归 | 保留为 baseline | 能为各目标提供透明下界，并暴露线性近似在强交互任务上的不足 | 需要统一特征表、标准化和显式零填补 | 低 | 5 折 OOF 误差、系数稀疏性、残差图、高低性能区对比 | 高 | 必须保留，用于判断复杂模型是否真的带来收益 |
| 配方结构增强的目标自适应受限加权树集成预测模型 | 保留并作为主路线 | 能在 251 条小样本表格数据中兼顾非线性、交互作用和分区异质性，并通过受限凸组合降低单一家族偶然偏置 | 需要组成特征、浓度 proxy 特征、结构零处理、目标标签表和折内加权规则 | 中 | OOF 误差、目标分区误差、折内权重稳定性、树间离散度与局部密度诊断 | 中高 | 初始 probe 已显示树模型明显优于线性 baseline；返工 probe 进一步显示简单三树融合优于单树，因此值得升级为受限加权融合 |
| 潜变量 PLS 鲁棒对照回归 | 保留为 robust alternative | 适合样本较小、特征强共线的数据，可检验主路线收益是否来自真实非线性而非单纯过拟合 | 需要标准化后特征与交叉验证选取潜变量数 | 低到中 | 潜变量数敏感性、OOF 误差、与 baseline/主路线的误差分布对比 | 中 | 作为树模型外的化学数据常见对照，可测试“潜变量线性结构是否已足够” |

### 计划阶段轻量 probe 结果

在统一的组成特征表上进行一次轻量 5 折探针后，得到如下信号：

- `conductivity`：`RandomForest` 的 MAE 约 `7.60`，显著优于 `ElasticNet` 的 `12.82`
- `pH`：`ExtraTrees` 的 MAE 约 `0.182`，优于 `ElasticNet` 的 `0.348`
- `PI`：`ExtraTrees` 的 MAE 约 `0.0329`，优于 `ElasticNet` 的 `0.0544`
- `W_1`：树模型 MAE 约 `0.043-0.044`，优于 `ElasticNet` 的 `0.0557`
- `R_W`：树模型 MAE 约 `0.0146-0.0148`，优于 `ElasticNet` 的 `0.0204`

该 probe 不作为正式结果写入论文，但足以证明主路线选用树集成是可防御的。

### 返工轻量 probe（针对树集成优化）

在保持同一特征表与 5 折协议的前提下，额外比较了单树、简单树融合和线性残差修正。关键观察如下：

- `conductivity`：`Blend_Tree3 = (RF + ET + HistGB) / 3` 的 MAE 约 `7.41`，优于 `RandomForest` 的 `7.92` 与 `ExtraTrees` 的 `8.08`
- `pH`：`Blend_Tree3` 的 MAE 约 `0.1728`，优于 `ExtraTrees` 的 `0.1803`
- `PI`：`Blend_Tree3` 的 MAE 约 `0.03379`，优于 `ExtraTrees` 的 `0.03495`
- `ElasticNet + 树残差修正` 在上述 3 个关键目标上都未稳定优于三树融合，因此保留为 fallback/ablation，而不升级为主路线

该返工 probe 只用于路线筛选，不进入正式论文硬数字；但它说明“单树二选一”仍有改进空间，升级为受限加权树集成是有证据支撑的。

## selected route

主路线采用**配方结构增强的目标自适应受限加权树集成预测模型**。

其核心思想分为三层：

1. 共享特征层：使用同一套配方结构增强特征，保持目标间输入口径一致。
2. 基学习器层：对每个目标并行训练 `RandomForestRegressor`、`ExtraTreesRegressor` 与浅层 `HistGradientBoostingRegressor`。
3. 受限融合层：在每个外层训练折内，依据内层误差生成非负归一化权重；若权重高度集中或融合无增益，则自动退化为单一最佳树模型。

当前默认优先级不再是“预先指定某一个家族”，而是：

- `conductivity`：优先尝试 `RF + ET + HistGB` 受限融合；若无增益则回退 `RandomForest`
- `pH`：优先尝试 `RF + ET + HistGB` 受限融合；若无增益则回退 `ExtraTrees`
- `W_1`：先比较 `RandomForest`、`ExtraTrees` 与三树融合；若提升不足 `1%` MAE，则保留单树以减少复杂度
- `R_W`：同 `W_1`，优先稳定性与可审计性，而非极小数值增益
- `PI`：优先尝试 `RF + ET + HistGB` 受限融合，并继续执行“直接预测 vs 重构”一致性检查

若 Build 阶段正式 OOF 结果与上述返工 probe 不一致，则以正式 OOF 结果为准，并把融合权重或回退决策写回 `review_note.md`。

选择理由：

1. 题面明确强调“非线性作用和协同效应”，而数据只有 251 条，说明路线必须既能容纳交互，又不能依赖大样本黑箱。
2. 组成模式只有 23 种主组合结构，且不同目标间相关性不一致：例如 `conductivity` 与 `pH` 相关系数约为 `-0.514`，`PI` 与 `W_1` 约为 `0.520`。这意味着不能假设一套线性关系同时覆盖全部目标。
3. 初始轻量 probe 显示树模型对 `conductivity`、`pH`、`PI`、`W_1`、`R_W` 全部优于线性 baseline，而返工 probe 进一步说明关键目标上的简单三树融合优于单树，因此主路线不应停留在“`RF/ET` 二选一”。
4. 受限加权融合在小样本下比完全自由 stacking 更稳健，因为它既允许利用模型互补性，又能在无增益时自动退化为单树。
5. 树集成可以输出特征重要性、单树离散度和局部邻域差异，为 `q3` 的机理解释与 `q5` 的候选筛选提供直接接口。
6. 为避免树模型成为单一依赖，Build 阶段仍保留 `ElasticNet` 和 `PLS` 对照，并对 `PI` 增加“直接预测 vs 由原始目标重构”的一致性检查。

## model specification

### 1. 预测任务定义

对每个样本 `i` 构造输入特征向量 `x_i`，并分别预测：

- `y_i^(1) = conductivity`
- `y_i^(2) = pH`
- `y_i^(3) = W_1`
- `y_i^(4) = R_W`
- `y_i^(5) = PI`

其中 `W_1`、`R_W` 与 `PI` 的定义完全沿用 `q1`。

### 2. 共享特征库

输入只允许来自配方组成信息的派生量，计划采用以下四类特征：

1. **比例特征**：每种母液在总配方中的体积分数 `ratio_j`
2. **存在性特征**：每种非水组分的结构零指示量 `present_j`
3. **浓度/质量 proxy**：`vol_j * density_j * molality_j` 等近似量，用于刻画不同母液的有效投料强度
4. **全局聚合特征**：`total_volume`、`active_count`、`water_ratio`、`ionic_strength_proxy`、`weighted_density`

### 3. 模型结构

对每个目标 `k`，先训练三个树基学习器：

\[
f_k^{RF}(x), \qquad f_k^{ET}(x), \qquad f_k^{GB}(x),
\]

其中 `GB` 表示浅层 `HistGradientBoostingRegressor`。随后构造受限融合主模型：

\[
\hat y_i^{(k)} = \sum_{m \in \{RF, ET, GB\}} w_{k,m} f_k^{m}(x_i), \qquad
w_{k,m} \ge 0,\quad \sum_m w_{k,m} = 1.
\]

其中 `w_{k,m}` 只允许由外层训练折内部的误差指标决定，默认采用“逆 MAE 归一化”或“离散候选组合择优”两种受限策略之一，禁止用测试折信息反向调权。

若某个目标上融合相对最佳单树的改进不足，或权重在不同折之间高度不稳定，则该目标自动退化为最佳单树模型，以控制复杂度和解释损失。

### 4. PI 一致性检查

除直接预测 `PI` 外，还额外定义一个重构值：

\[
\widehat{PI}^{\,recon}_i = g(\hat \kappa_i,\hat pH_i,\widehat{W_1}_i,\widehat{R_W}_i),
\]

其中 `g(\cdot)` 即 `q1` 固定下来的 pH 评分与 CRITIC-TOPSIS 口径。若 `PI` 直接头与重构头差异过大，则说明 `PI` 的预测可解释性不足，需要在 Stage 4 降级相关 claim。

### 5. 预期 `result.json` 字段

```text
status
question_id
feature_schema
target_list
target_model_selection
base_model_cv_summary
ensemble_weight_summary
cv_summary
oof_predictions_path
slice_error_summary
uncertainty_hooks
pi_consistency_summary
paper_claims
source_command
```

## assumptions and notation

### 假设表

| assumption id | 内容 | 来源 | 风险 | validation / sensitivity hook |
|---|---|---|---|---|
| H1 | `q1` 中定义的 `PI`、`W_1`、`R_W` 在 `q2` 中视为固定标签，不重新修改 pH 区间与权重口径 | `q1` summary / validation / sensitivity | 若后续调整 `q1` 口径，则 `q2` 标签体系整体改变 | Build 时记录标签版本；Stage 4 检查 `PI` 直接头与重构头一致性 |
| H2 | 附件中未出现的组分视为结构零，而不是随机缺失 | `A_data.json` 的字典式配方记录 | 若误把结构零当缺失，会引入错误补值 | 数据构建时显式写零填补并在 `run.log` 记录 |
| H3 | 由体积、密度、母液质量摩尔浓度构造的 proxy 特征足以近似配方强度差异 | 题面与 `README.txt` 字段结构 | 这些 proxy 不是严格热力学状态量 | 在 Stage 4 做特征块消融，验证其必要性 |
| H4 | 当前模型只对已有 8 种组分体系及其邻域内配方有效 | 题面与材料边界 | 超出已见组分或极端比例时易外推失真 | 在 `q4` 中识别低可信区域，在 `q5` 中限制候选空间 |
| H5 | 稳定性相关标签属于短时 proxy，可被学习为数值目标，但论文措辞必须保留 proxy 限制 | `q1` warnings / review_note | 若遗漏该限制，会把预测问题写成寿命预测 | `warnings.md` 和 downstream traceability 持续保留限制 |

### 符号表

| 符号 | 含义 | 单位 / 类型 | 说明 |
|---|---|---|---|
| `x_i` | 第 `i` 条配方的共享特征向量 | 数值向量 | 由组成信息派生 |
| `ratio_j` | 第 `j` 种母液体积分数 | 无量纲 | 比例特征 |
| `present_j` | 第 `j` 种非水组分是否出现 | 0/1 | 结构零标记 |
| `c_j` | 第 `j` 种母液的浓度 proxy | 相对量 | 由体积、密度、母液质量摩尔浓度构造 |
| `\hat y_i^{(k)}` | 第 `k` 个目标的预测值 | 目标同单位 | 由主模型输出 |
| `u_i^{(k)}` | 第 `k` 个目标的不确定性 hook | 相对量 | 由树间离散度与局部密度构造 |
| `\widehat{PI}^{recon}` | 由原始目标重构的综合分数 | 无量纲 | 用于一致性检查 |

## data reconstruction plan

| source | transformation | output / role | risk |
|---|---|---|---|
| `A_data.json` / `electrolyte.volumes` | 抽取每种母液体积并计算 `ratio_j` | 主输入特征 | 低 |
| `A_data.json` / `source molalities`, `source densities` | 构造 `molality_proxy_j`、`weighted_density`、`ionic_strength_proxy` | 强度与浓度 proxy 特征 | 中；是 proxy 而非严格状态量 |
| `A_data.json` / 组分是否出现 | 生成 `present_j` 与 `active_count` | 结构信息特征 | 低 |
| `q1/results/indicator_table.csv` | 通过 `GUID` 合并 `conductivity`, `pH`, `W_1`, `R_W`, `PI` | 监督学习标签表 | 中；继承 `q1` 口径 |
| 空缺组分列 | 明确以 `0.0` 填补，并标记为结构零 | 统一特征矩阵 | 低；需在 `run.log` 公开 |

计划生成的中间数据：

- `workspace/output/q2/results/feature_table.csv`
- `workspace/output/q2/results/target_table.csv`
- `workspace/output/q2/results/model_probe.csv`
- `workspace/output/q2/results/oof_predictions.csv`
- `workspace/output/q2/results/slice_error_summary.csv`

## toy demo plan

- 最小输入：抽取 60 条样本，构造完整特征表，只先预测 `conductivity`、`pH` 和 `PI`
- 最小输出：
  - 基线 `ElasticNet` 的 OOF 误差
  - 单树基学习器与三树融合的 OOF 误差对比
  - `PI` 直接头与 `PI` 重构头的一致性指标
- 成功信号：
  - 特征表不含未处理的 NaN
  - 三树融合在 `PI` 或 `pH` 上优于 baseline，且不劣于最佳单树
  - `conductivity` 预测值量级合理，不出现大面积负值或极端爆炸
  - `PI` 直接头与重构头至少保持中高相关
- 失败信号：
  - 特征构建后仍存在未解释 NaN
  - 树模型在所有目标上都不优于 baseline
  - 融合权重在不同折之间剧烈摆动，且性能未优于单树
  - `PI` 直接头与重构头明显分离，导致解释链断裂
  - `R_W` 预测频繁落到不合理区间
- 阻塞性判断：
  - 若 `PI` 头严重不一致，则保留原始目标预测，`PI` 改为仅用重构方式产生 limited result
  - 若三树融合无稳定增益，则回退到最佳单树；若树模型全面失效，则回退到 `PLS`/`ElasticNet` 的有限路线并重新审查

## validation and sensitivity plan

### Stage 4 预定验证

- 验证 1：对每个目标计算 OOF 的 MAE、RMSE、`R^2`
- 验证 2：比较 baseline、最佳单树、受限加权主路线、鲁棒替代的误差矩阵与优势目标
- 验证 3：分析高性能区、低性能区、稀有组分模式区的误差差异
- 验证 4：对 `PI` 比较直接头与重构头的一致性
- 验证 5：抽取特殊样本（高电导低 `PI`、高 `PI` 中等电导、`R_W > 1` 异常样本）做局部残差解释

### Stage 4 预定灵敏度

- 灵敏度 1：移除浓度 proxy 特征块，观察各目标误差变化
- 灵敏度 2：比较 `RandomForest`、`ExtraTrees`、`HistGB`、`RF+ET` 与 `RF+ET+HistGB` 的性能差异
- 灵敏度 3：交叉验证折叠随机种子变化对融合权重与误差排序的影响
- 灵敏度 4：高性能区阈值从前 `10%` 改为前 `20%` 时，结论是否改变
- 灵敏度 5：`PI` 直接头与重构头差异是否集中于某些稀有模式

## red-team notes

- 数学风险：251 条样本对应 23 种主组合结构，若特征过多、融合过自由或模型过深，容易在稀有模式上过拟合
- 数据风险：`PI`、`W_1`、`R_W` 都继承自 `q1` 口径，若把它们视为绝对物理真值，会夸大标签质量
- 计算风险：全量多目标多模型交叉验证很容易超时，因此 Build 需要先做轻量 probe，再进入正式 OOF，并允许对 `W_1`、`R_W` 自动退化为单树
- 验证风险：若融合权重直接根据全量 OOF 或测试折表现回填，会产生信息泄漏并夸大主路线收益
- 论文审查风险：若只报告平均误差而不讨论高性能区或特殊样本，无法满足题面对“不同性能目标与特殊样本差异”的要求
- 不确定性风险：树间离散度和局部密度只能提供 heuristic uncertainty，不等价于严格后验方差
- fallback：
  - 一级 fallback：`conductivity`、`pH`、`PI` 保留三树融合尝试，`W_1`、`R_W` 先退化为最佳单树
  - 二级 fallback：若某个目标的融合权重不稳定或无增益，则该目标固定为最佳单树
  - 三级 fallback：若 `R_W` 目标过于不稳，则把 `R_W` 标为 limited target，并在 `PI` 解释中保留限制
  - 四级 fallback：若树模型在某个目标上整体不稳定，则该目标切换到 `PLS` 或 `ElasticNet` 的 limited route

## build entry checklist

| 检查项 | 状态 | 说明 |
|---|---|---|
| 题意目标清晰 | pass | 已覆盖电导率、pH、`q1` 指标、多模型比较和特殊样本分析 |
| 上游依赖已读取 | pass | `q1` 的 summary/result/validation/sensitivity/warnings/review_note 已读取并写入影响 |
| 基线 / 主模型 / 鲁棒替代齐备 | pass | `ElasticNet`、目标自适应受限加权树集成、`PLS` 三类路线已定义 |
| 共享特征库明确 | pass | 比例、存在性、浓度 proxy 和全局特征已规划 |
| 风险已可见 | pass | `PI` 口径继承、短时 proxy、稀有模式过拟合风险均已写明 |
| toy demo 可执行 | pass | 60 条样本、3 个目标即可做最小可行性验证 |
| Build 后输出字段明确 | pass | 已定义 feature schema、OOF 预测、slice error、uncertainty hooks 等字段 |
| 是否可进入 Stage 3 | pending manual approval | 需用户明确同意后才能 Build |

## review material paths

- `workspace/output/q2/review_packet.md`
- `workspace/output/q2/warnings.md`
- `workspace/output/q2/review_note.md`
