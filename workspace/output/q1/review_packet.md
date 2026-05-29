# q1 Review Packet

## question card

| 字段 | 内容 |
|---|---|
| q id | `q1` |
| title | 综合性能与稳定性指标构造 |
| source | `workspace/problem/problem.md` 第一阶段问题 1 |
| goal | 建立后续全流程统一使用的综合性能评价指标，并设计至少一组具有比较意义的稳定性相关指标 |
| direct asks | 1. 判断只用电导率是否足够；2. 结合 pH 与电化学曲线构造更合理指标；3. 给出稳定性相关指标及其物理/工程意义 |
| inputs | `problem.md`、`A_data.json`、`README.txt` |
| outputs | 综合性能分数、稳定性 proxy 指标、与电导率单指标的差异分析、指标定义表 |
| constraints | 仅能使用现有短时实验数据；不能把短时电化学稳定性 proxy 夸大为循环寿命结论；实现语言锁定 Python |
| evaluation metric | 指标可解释性、排名区分度、与物理直觉一致性、对后续 `q2` 预测的可建模性、对样本异常的辨识能力 |
| downstream interface | 为 `q2` 提供预测目标字段；为 `q3` 提供解释对象；为 `q5`/`q6` 提供候选优先级口径 |

## upstream context

- 当前问题为 `q1`，无上游 `q*` 依赖。
- 已读取的上游级材料仅包括：
  - `workspace/output/problem_audit.md`
  - `workspace/output/material_index.md`
  - `workspace/output/question_index.md`

## candidate model matrix

| candidate | kept/rejected | task fit | data need | implementation risk | validation route | paper interpretability | reason |
|---|---|---|---|---|---|---|---|
| 电导率单指标排序 | 保留为 baseline | 只能回答“只看电导率是否足够”的对照问题，不能覆盖 pH 与稳定性 | 仅需 `conductivity` | 低 | 与综合指标做 Spearman 排名相关、Top-k 重叠、反例分析 | 高 | 必须保留，用于证明单指标不足 |
| 门槛约束-CRITIC-TOPSIS 综合评价模型 | 保留并作为主路线 | 能同时整合导电性、pH 适宜性与电化学稳定性 proxy，并输出单一综合分数 | 需 `conductivity`、`pH`、`derived_quantities`，必要时读取 `V/i/t` 做曲线核对 | 低到中 | 权重敏感性、标准化敏感性、与 baseline/PCA 的排名一致性比较 | 高 | 兼顾可解释性、可实现性、后续可预测性和论文表达力 |
| PCA 潜在因子综合评分 | 保留为 robust alternative | 可检验综合评分是否强依赖主观权重，但解释性弱于主路线 | 需同主路线 | 中 | 与主路线做载荷解释、排名一致性和异常样本差异分析 | 中 | 适合做权重依赖性对照，不适合作为主输出 |

## selected route

主路线采用“门槛约束-CRITIC-TOPSIS 综合评价模型”，并同步输出两类稳定性 proxy 指标。

选择理由：

1. 题意明确要求比较多个性能维度，而不是简单排序，故需要综合评价框架。
2. `A_data.json` 已包含电导率、pH 及可直接计算稳定窗口的派生量，足以支撑低风险实现。
3. TOPSIS 适合把“越大越好”与“区间最优/偏离受罚”的指标统一到一个贴近理想解的分数上，便于后续 `q2` 建模。
4. CRITIC 权重能利用指标离散度与相关冲突度，减少完全手工权重的任意性。
5. 为防止权重主导结论，Build 阶段保留 PCA 作为鲁棒对照，并保留电导率单指标作为最低透明基线。

## model specification

### 1. 原始指标定义

- 导电性指标：`kappa = conductivity`
- pH 适宜性指标：`S_pH`
  - 先用工作区间评分而非直接使用原始 pH 值
  - 推荐默认区间：`[6.5, 8.5]`
  - 区间内记高分，偏离区间按距离递减
- Tafel 稳定窗口：`W_T = V_c^T - V_a^T`
  - 其中 `V_c^T = TAFEL CATHODE V`
  - `V_a^T = TAFEL ANODE V`
- 1mA/cm^2 实用稳定窗口：`W_1 = V_c^1 - V_a^1`
  - 其中 `V_c^1 = 1mA/cm^2 CATHODE V`
  - `V_a^1 = 1mA/cm^2 ANODE V`
- 稳定窗口保留率：`R_W = W_1 / W_T`

### 2. 稳定性相关指标

- 指标 A：`W_1`
  - 物理意义：在给定电流密度门槛下，配方可承受的实用电化学稳定窗口
  - 工程意义：越大表示在实际负载下越不容易过早触发析氢/析氧等副反应
- 指标 B：`R_W`
  - 物理意义：Tafel onset 窗口到实用窗口的保留比例
  - 工程意义：越大表示从“理论 onset”到“实际工作点”损失越小，动力学 reserve 越充足

### 3. 综合性能分数

- 输入指标向量：`z = [kappa, S_pH, W_1, R_W]`
- 标准化方式：优先采用稳健标准化或区间归一化，保留正向指标方向一致性
- 权重：主路线采用 CRITIC 自动生成；同时保存等权与 PCA 对照
- 输出分数：`PI`，取 TOPSIS 贴近度

### 4. 回答“只看电导率是否足够”的比较框架

- 排名相关性：计算 `rank(kappa)` 与 `rank(PI)` 的 Spearman 相关
- Top-k 稳定性：比较电导率前 10 与综合指标前 10 的重叠率
- 反例筛查：识别“高电导但 pH/稳定性偏弱”的样本，以及“电导率中等但综合表现优”的样本

### 5. 预期 `result.json` 字段

```text
status
question_id
metric_definitions
weight_scheme
indicator_summary
overall_score_summary
top_formulations
baseline_comparison
stability_indicator_summary
claim_eligibility
source_command
```

## assumptions and notation

### 假设表

| assumption id | 内容 | 来源 | 风险 | validation / sensitivity hook |
|---|---|---|---|---|
| H1 | 现有 `fast_assessment` 电化学曲线可作为短时稳定性 proxy | 数据字段与题意“电化学测试曲线” | 不能代表长期循环寿命 | 在 `warnings.md` 中持续标记；摘要与论文中只写 proxy 结论 |
| H2 | pH 的最优区间可先按近中性工作带处理，默认 `[6.5, 8.5]` | 水系体系的一般工程直觉与题意中对 pH 的关注 | 区间设定会影响综合排序 | 在 Stage 4 做 pH 带宽敏感性分析 |
| H3 | `derived_quantities` 与原始 `V/i/t` 曲线语义一致，可直接用于窗口构造 | `README.txt` 和字段命名 | 若派生量计算口径与原曲线不一致，会影响指标解释 | Build 时抽样回看原曲线，核对阈值位置 |
| H4 | 用单一综合分数表示“好配方”是合理的，但必须保留分项指标 | 题面要求建立“评价指标”并支持后续建模 | 过度压缩会隐藏 trade-off | 输出分项指标、综合分数和反例样本三类结果 |

### 符号表

| 符号 | 含义 | 单位 | 方向 |
|---|---|---|---|
| `kappa` | 电导率 | 以原数据为准 | 越大越好 |
| `pH` | 酸碱度 | 无量纲 | 需转为区间适宜性 |
| `S_pH` | pH 适宜性得分 | 无量纲 | 越大越好 |
| `V_c^T` | Tafel 阴极阈值电位 | V | 越大越好 |
| `V_a^T` | Tafel 阳极阈值电位 | V | 越小越好 |
| `V_c^1` | 1mA/cm^2 阴极电位 | V | 越大越好 |
| `V_a^1` | 1mA/cm^2 阳极电位 | V | 越小越好 |
| `W_T` | Tafel 稳定窗口 | V | 越大越好 |
| `W_1` | 实用稳定窗口 | V | 越大越好 |
| `R_W` | 稳定窗口保留率 | 无量纲 | 越大越好 |
| `PI` | 综合性能分数 | 无量纲 | 越大越好 |

## data reconstruction plan

| source | transformation | output / role | risk |
|---|---|---|---|
| `A_data.json` / `conductivity` | 直接抽取并做量纲核对 | `kappa` | 低 |
| `A_data.json` / `pH` | 转换为区间适宜性得分 `S_pH` | 综合指标输入 | 中；依赖区间设定 |
| `A_data.json` / `derived_quantities` | 计算 `W_T`、`W_1`、`R_W` | 稳定性 proxy 与综合指标输入 | 中；需核对字段含义 |
| `A_data.json` / `electrochemistry.V,i,t` | 对抽样样本回看曲线形态、核对派生量合理性 | 审计与反例解释 | 中；不是每条都需全文曲线积分 |
| `A_data.json` / `electrolyte.*` | 暂仅保留 GUID 与配方组成用于输出前列样本解释 | Top 配方描述 | 低 |

计划生成的中间数据：

- `workspace/output/q1/results/indicator_table.csv`
- `workspace/output/q1/results/top_formula_snapshot.csv`

## toy demo plan

- 最小输入：任选 5 条样本，成功抽取 `kappa`、`pH`、`W_T`、`W_1`
- 最小输出：5 条样本的 `S_pH`、`R_W` 与 `PI`
- 成功信号：
  - 所有窗口值为正且量级合理
  - 电导率单指标与综合指标至少能产生 1 个排序差异样本
  - PCA 对照能运行并给出可比较排序
- 失败信号：
  - `derived_quantities` 缺字段或语义不一致
  - `S_pH` 的评分方式导致绝大多数样本同分
  - 综合分数完全退化为电导率单调变换
- 阻塞性判断：若稳定性字段不可用，则当前主路线 blocked，需降级到“电导率 + pH”有限结论并在 Manual 模式重新审查

## validation and sensitivity plan

- 验证 1：比较 `rank(kappa)` 与 `rank(PI)` 的 Spearman 相关和 Top-k 重叠率
- 验证 2：抽取极端样本，人工核查高分与低分样本在 pH / 稳定窗口上的差别是否符合物理直觉
- 验证 3：抽样核对原始 `V/i/t` 与 `derived_quantities` 是否一致
- 灵敏度 1：将 pH 工作区间从 `[6.5, 8.5]` 改为 `[6.0, 8.0]`、`[7.0, 9.0]`
- 灵敏度 2：权重方案在 CRITIC、等权、PCA 因子权重之间切换
- 灵敏度 3：综合指标中是否纳入 `W_T` 或仅保留 `W_1` 与 `R_W`
- 关键观测：Top-10 配方重叠率、综合分数分布变化、反例样本是否稳定

## red-team notes

- 数学风险：CRITIC-TOPSIS 仍可能受到强相关指标影响，需用 PCA 对照检验
- 数据风险：稳定性只是一类短时 proxy，不能推出寿命和循环稳定性
- 计算风险：若 `derived_quantities` 与曲线口径不一致，需回退到直接曲线阈值提取
- 论文审查风险：若直接把 `PI` 称为“最终性能真值”，会过度声明；应写为“基于现有数据的综合评价指标”
- fallback：
  - 一级 fallback：保留 `kappa + S_pH + W_1` 三指标综合评价
  - 二级 fallback：仅回答“电导率单指标不足”，并把稳定性部分降级为字段级描述

## build entry checklist

| 检查项 | 状态 | 说明 |
|---|---|---|
| 题意目标清晰 | pass | 三个显式要求已拆开并映射到具体输出 |
| 数据路径明确 | pass | 主数据与字段说明已定位 |
| 基线 / 主模型 / 鲁棒替代齐备 | pass | baseline、主路线、PCA 对照已定义 |
| 变量与输出字段明确 | pass | 已定义 `PI`、`W_1`、`R_W` 等字段和预期结果结构 |
| 风险已可见 | pass | 稳定性 proxy 与 pH 区间假设已写入警告与假设表 |
| toy demo 可执行 | pass | 5 条样本即可验证主路线是否可跑通 |
| Manual 审查已准备 | pass | 当前文件、`warnings.md`、`review_note.md` 已生成 |
| 是否可进入 Stage 3 | pending manual approval | 需用户明确同意后才能 Build |

## review material paths

- `workspace/output/q1/review_packet.md`
- `workspace/output/q1/warnings.md`
- `workspace/output/q1/review_note.md`
