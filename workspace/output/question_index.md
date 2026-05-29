# Stage 1 Question Decomposition

## Question List

| q id | title | explicit or implicit | source section | 目标输出 | blocking upstream |
|---|---|---|---|---|---|
| `q1` | 综合性能与稳定性指标构造 | explicit | 第一阶段问题 1 | 综合性能得分、稳定性 proxy 指标、与电导率单指标的对比结论 | 无 |
| `q2` | 配方到性能的预测模型 | explicit | 第一阶段问题 2 | 对电导率、pH、`q1` 指标的预测模型与比较报告 | `q1` |
| `q3` | 关键组分与交互作用解释 | explicit | 第一阶段问题 3 | 重要组分、交互作用、稳定适用范围的解释结论 | `q1` `q2` |
| `q4` | 模型可信度与适用范围分析 | explicit | 第二阶段问题 4 | 分区域验证方案、误差异质性和可信区域结论 | `q1` `q2` |
| `q5` | 下一轮实验候选设计 | explicit | 第二阶段问题 5 | 5 组/10 组候选配方方案、探索-开发平衡原则、对比基线 | `q1` `q2` `q4` |
| `q6` | 候选配方稳健性建模 | explicit | 第二阶段问题 6 | 扰动稳健性定义、敏感配方识别、推荐候选的稳健性判断 | `q1` `q2` `q4` `q5` |

## 依赖图

| from q* | to q* | dependency type | dependency description | blocking if missing |
|---|---|---|---|---|
| `q1` | `q2` | result | `q2` 需要预测 `q1` 中定义的综合性能与稳定性指标 | yes |
| `q1` | `q3` | result | `q3` 需要解释 `q1` 指标的驱动因素 | yes |
| `q2` | `q3` | method | `q3` 依赖 `q2` 的可解释预测模型、特征重要性或局部解释 | yes |
| `q1` | `q4` | result | `q4` 的验证对象包括 `q1` 指标 | yes |
| `q2` | `q4` | result | `q4` 需要对 `q2` 预测模型做结构化验证 | yes |
| `q1` | `q5` | result | `q5` 的优化目标必须继承 `q1` 指标定义 | yes |
| `q2` | `q5` | result | `q5` 候选筛选依赖 `q2` 的预测值与不确定性 | yes |
| `q4` | `q5` | result | `q5` 需避开低可信区域或对其单独标记风险 | yes |
| `q1` | `q6` | result | `q6` 需沿用 `q1` 的性能/稳定性口径 | yes |
| `q2` | `q6` | result | `q6` 需使用预测模型评估局部扰动表现 | yes |
| `q4` | `q6` | result | `q6` 需参考不同区域的可信度差异 | yes |
| `q5` | `q6` | data | `q6` 只评估 `q5` 推荐候选及其邻域 | yes |

## 材料映射

| material path | used by q* | expected role | risk if missing |
|---|---|---|---|
| `workspace/problem/problem.md` | `q1`-`q6` | 题意主来源 | High |
| `workspace/problem/attachments/A_data.json` | `q1`-`q6` | 输入数据、验证样本、候选搜索基础 | High |
| `workspace/problem/attachments/README.txt` | `q1`-`q6` | 字段说明、单位与结构辅助说明 | Medium |
| `workspace/problem/reference.pdf` | `q1`-`q6` | audit-only 备查 | Low |
| `workspace/problem/images/` | 暂无 | optional / unused | Low |

## 执行顺序

```text
q1 -> q2 -> q3 -> q4 -> q5 -> q6
```

- 当前题目是强链式依赖问题，主 Plan / Build / Verification / Summary 不适合跨问并行。
- 可并行的任务仅限各问内部的局部 critic、图表自检和终审 panel；若当前环境不启用并行能力，则默认串行。

## Per-Question Cards

### `q1` 综合性能与稳定性指标构造

- `explicit or implicit`: explicit
- `source section from problem.md`: 第一阶段问题 1
- `action verb`: 分析、构造、比较、说明
- `object`: 电导率、pH、电化学测试曲线、稳定性
- `goal`: 定义后续全流程统一使用的综合性能指标和稳定性 proxy 指标，并证明“只看电导率”不足
- `expected output`: 指标定义、标准化/赋权方案、稳定性 proxy 指标、与电导率单指标的差异案例
- `evaluation metric`: 排名区分度、与物理直觉一致性、对后续预测任务的可建模性、对特殊样本的可解释性
- `constraints`: 只能使用现有短时电化学曲线与派生量；不得把 proxy 夸大为长寿命结论
- `input materials`: `problem.md`, `A_data.json`, `README.txt`
- `data interface`: 原始字段 `conductivity`, `pH`, `electrochemistry.V/i/t`, `derived_quantities`
- `dependencies`: 无上游依赖
- `early variables and symbols`: `kappa`, `pH`, `V_c^T`, `V_a^T`, `V_c^1`, `V_a^1`, `W_T`, `W_1`, `S_pH`, `PI`, `SI`
- `known ambiguity or risk`: 稳定性仅能定义为电化学稳定窗口/动力学 reserve 的 proxy
- `next-stage planning focus`: 指标体系、候选赋权路线、pH 门槛、稳定性 proxy 的物理解释与可验证性
- `stage 2 contract`:
  - `workspace/output/q1/review_packet.md`
  - `workspace/output/q1/warnings.md`
  - `workspace/output/q1/review_note.md`

### `q2` 配方到性能的预测模型

- `explicit or implicit`: explicit
- `source section from problem.md`: 第一阶段问题 2
- `action verb`: 预测、比较、分析
- `object`: 电导率、pH、`q1` 构造指标
- `goal`: 用配方组成信息预测多个目标量，并比较不同模型的精度、稳定性和可解释性
- `expected output`: 多目标预测模型、模型对比、在不同性能区域的表现差异分析
- `evaluation metric`: 回归误差、排名保持性、高低性能区表现、解释性、稳定性
- `constraints`: 实现语言锁定 Python；目标定义必须继承 `q1`
- `input materials`: `problem.md`, `A_data.json`, `README.txt`, `q1` summary/result artifacts
- `data interface`: 组分体积、母液质量摩尔浓度、密度、派生配方特征与 `q1` 标签
- `dependencies`: `q1` results
- `early variables and symbols`: `x_j`, `m_j`, `rho_j`, `y_kappa`, `y_pH`, `y_PI`, `y_SI`, `f_theta`
- `known ambiguity or risk`: 样本量较小且组分组合有限，复杂模型可能过拟合
- `next-stage planning focus`: 特征重构、基线回归、非线性主模型、鲁棒替代、误差分区
- `stage 2 contract`:
  - `workspace/output/q2/review_packet.md`
  - `workspace/output/q2/warnings.md`
  - `workspace/output/q2/review_note.md`

### `q3` 关键组分与交互作用解释

- `explicit or implicit`: explicit
- `source section from problem.md`: 第一阶段问题 3
- `action verb`: 解释、识别、讨论、验证
- `object`: 电导率、稳定性相关指标、组分交互作用
- `goal`: 提炼关键组分、特征重要性与协同效应，并判断规律是否具有范围稳定性
- `expected output`: 重要组分排名、交互作用证据、局部与全局稳定性讨论
- `evaluation metric`: 解释一致性、跨模型一致性、在样本子区间中的稳定性
- `constraints`: 解释必须建立在 `q2` 已验证模型或数据统计证据上
- `input materials`: `problem.md`, `A_data.json`, `q1` outputs, `q2` outputs
- `data interface`: 特征重要性、SHAP/偏依赖或替代解释、分层统计
- `dependencies`: `q1`, `q2`
- `early variables and symbols`: `I_j`, `I_{jk}`, `Delta y`, `region_g`
- `known ambiguity or risk`: 交互作用可能受样本稀疏区放大，需要区域稳定性检查
- `next-stage planning focus`: 解释方法选择、交互项抽取、局部稳定性检验
- `stage 2 contract`:
  - `workspace/output/q3/review_packet.md`
  - `workspace/output/q3/warnings.md`
  - `workspace/output/q3/review_note.md`

### `q4` 模型可信度与适用范围分析

- `explicit or implicit`: explicit
- `source section from problem.md`: 第二阶段问题 4
- `action verb`: 评价、设计、比较、划分
- `object`: 训练测试划分、配方结构、聚类区域、误差分布
- `goal`: 给出比随机切分更强的验证协议，并识别高可信与低可信区域
- `expected output`: 结构化验证方案、区域误差图谱、可信度分层结论
- `evaluation metric`: 误差均匀性、区域覆盖度、外推风险显著性、验证设计的防泄漏能力
- `constraints`: 不能只给随机切分结论；需显式结合配方区域
- `input materials`: `problem.md`, `A_data.json`, `q1` outputs, `q2` outputs
- `data interface`: 聚类标签、复杂度指标、区域验证折、误差统计
- `dependencies`: `q1`, `q2`
- `early variables and symbols`: `g`, `e`, `CV_g`, `density_x`, `complexity_x`
- `known ambiguity or risk`: 区域划分方式本身会影响可信区结论
- `next-stage planning focus`: 聚类方案、分层验证、误差热区与适用边界定义
- `stage 2 contract`:
  - `workspace/output/q4/review_packet.md`
  - `workspace/output/q4/warnings.md`
  - `workspace/output/q4/review_note.md`

### `q5` 下一轮实验候选设计

- `explicit or implicit`: explicit
- `source section from problem.md`: 第二阶段问题 5
- `action verb`: 设计、平衡、比较、推荐
- `object`: 候选配方、候选区域、探索与开发策略
- `goal`: 在同时考虑电导率、pH、稳定性指标的条件下，推荐少量新增实验候选
- `expected output`: 5 组与 10 组候选方案、采样原则、与随机选点的优势和风险对比
- `evaluation metric`: 预期性能、预测不确定性、区域覆盖增益、可实施性
- `constraints`: 候选需受限于现有组分体系与可实现配比；必须显式平衡 exploit/explore
- `input materials`: `problem.md`, `A_data.json`, `q1` outputs, `q2` outputs, `q4` outputs
- `data interface`: 预测均值、预测不确定性、样本密度、候选生成规则
- `dependencies`: `q1`, `q2`, `q4`
- `early variables and symbols`: `x_new`, `mu(x)`, `sigma(x)`, `rho(x)`, `A(x)`
- `known ambiguity or risk`: 无真实实验反馈，候选优先级只能作为数据驱动建议
- `next-stage planning focus`: 候选空间生成、采集函数、随机基线与风险标记
- `stage 2 contract`:
  - `workspace/output/q5/review_packet.md`
  - `workspace/output/q5/warnings.md`
  - `workspace/output/q5/review_note.md`

### `q6` 候选配方稳健性建模

- `explicit or implicit`: explicit
- `source section from problem.md`: 第二阶段问题 6
- `action verb`: 定义、预测、判断、比较
- `object`: 高性能区域、孤立样本、局部扰动、模型准确度
- `goal`: 判断候选是否处于稳定高性能区域，并定义/预测稳健性
- `expected output`: 稳健性指标、扰动敏感样本识别、推荐候选的稳健性结论
- `evaluation metric`: 扰动后性能保持率、局部梯度敏感性、邻域一致性、模型在扰动样本上的误差稳定性
- `constraints`: 扰动必须遵守配方可行性；需区分“性能高”与“稳健性高”
- `input materials`: `problem.md`, `A_data.json`, `q1` outputs, `q2` outputs, `q4` outputs, `q5` outputs
- `data interface`: 局部扰动样本、邻域搜索、预测误差对比、复杂度指标
- `dependencies`: `q1`, `q2`, `q4`, `q5`
- `early variables and symbols`: `delta`, `R(x)`, `G(x)`, `N_eps(x)`, `err_delta`
- `known ambiguity or risk`: “小幅扰动”口径需要在 Stage 2 固化
- `next-stage planning focus`: 扰动机制、稳健性定义、候选区域与孤立高分样本区分
- `stage 2 contract`:
  - `workspace/output/q6/review_packet.md`
  - `workspace/output/q6/warnings.md`
  - `workspace/output/q6/review_note.md`

## Decomposition Check

- `problem.md` 中 6 个显式任务已全部映射到 `q1`-`q6`。
- 共享支撑任务没有单独拆为新问，而是在各问 Plan 中显式处理，以避免虚增问题数量。
- 依赖图无循环；当前最强主链为 `q1 -> q2 -> q4 -> q5 -> q6`，`q3` 作为解释分支依赖 `q1` 与 `q2`。
