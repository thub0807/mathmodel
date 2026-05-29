# Stage 0 Workspace Audit

## 审计结论

| 项目 | 状态 | 说明 |
|---|---|---|
| `workspace/problem/problem.md` | 可读 | 已直接阅读，足以完成题意理解与拆题。 |
| `workspace/problem/reference.pdf` | 存在 | 按协议视为 audit-only 材料；当前未作为题意主来源。 |
| `workspace/problem/images/` | 存在但为空 | 题面未显式引用图片，不构成阻塞。 |
| `workspace/problem/attachments/` | 可读 | 包含 `A_data.json` 与 `README.txt`，足以支撑后续建模。 |
| 是否存在阻塞性材料缺口 | 否 | 可以继续进入 Stage 1 与 `q1` 的 Stage 2。 |

## 题目范围摘要

- 题目为“水系电解液配方”单题建模任务，显式包含 6 个子问题。
- 第一阶段聚焦评价指标构造、性能预测、机理解释。
- 第二阶段聚焦模型可信度、实验候选设计、配方稳健性。
- 已知唯一核心数据源为 `workspace/problem/attachments/A_data.json`，其中包含 251 条配方实验记录。

## 已确认材料事实

- `A_data.json` 顶层字段包括 `conductivity`、`pH`、`electrolyte`、`electrochemistry`、`temperature` 等。
- `electrolyte` 内含 `volumes`、`source molalities`、`source densities`。
- `electrochemistry` 内含全曲线数组 `i`、`V`、`t`，以及 `derived_quantities`。
- 当前样本均包含 `conductivity` 与 `pH`；电化学测试名统一为 `fast_assessment`。

## 非阻塞歧义与默认处理

| ambiguity id | 来源 | 竞争解释 | 影响问题 | 建模影响 | 推荐默认 | 需用户确认 |
|---|---|---|---|---|---|---|
| A01 | 题面“稳定性相关指标” | 可理解为长循环寿命，也可理解为短时电化学稳定性 proxy | `q1` `q2` `q3` `q5` `q6` | 若误当成长寿命，会过度声明证据强度 | 默认限定为“基于现有电化学曲线的短时稳定性/稳定窗口 proxy” | 否 |
| A02 | 题面“已知部分实验结果” | 可理解为标签缺失预测，也可理解为完整样本上的监督学习泛化 | `q2` `q4` | 影响训练/验证协议设计 | 默认按完整样本监督学习处理，再通过结构化验证检验泛化 | 否 |
| A03 | 题面“下一轮实验候选方案” | 可在全连续空间搜索，也可限制在现有母液体系与可混配区域内搜索 | `q5` `q6` | 影响候选空间与可落地性 | 默认限制在已有 8 种组分及其可行配方邻域内搜索 | 否 |
| A04 | 题面“小幅扰动” | 绝对体积扰动、相对比例扰动或浓度扰动 | `q6` | 影响稳健性定义 | 默认采用“组分比例的局部相对扰动并重新归一化” | 否 |

## 后续处理建议

- Stage 1 采用显式 6 问拆分，不额外创建独立支持问；共享支持任务合并入各问的 Plan 中。
- `q1` 先建立“综合性能指标 + 稳定性 proxy 指标”的统一口径，为 `q2` 到 `q6` 提供目标量与约束语义。
- 后续若发现 `reference.pdf` 中对电化学曲线含义、单位或实验边界有额外约束，再回补审计说明。
