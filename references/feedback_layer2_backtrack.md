# Feedback Layer 2：跨产物回溯

## 目的

Layer 2 检查后续证据是否推翻了早期分析、假设、符号、模型选择、数据处理、结果或论文 claim。它执行有目标的回溯，而不是默认重启整个流程。

Layer 2 由矛盾触发。核心问题是：哪个早期产物现在变得错误、不完整或过强？哪些下游文件必须同步变化？

## 触发时机

在以下时机调用 Layer 2：

- `workspace/output/q*/validation.md` 写完后；
- `workspace/output/q*/sensitivity.md` 写完后；
- 单个 `q*` summary 被提升到 final integration 前；
- 写入或更新 `workspace/output/final/traceability.md` 前；
- `final_results.md`、traceability 和论文文本不一致时；
- 最终 review 中 panel 或 calibration finding 暴露矛盾时。

## 读取文件

对单个 `q*`：

```text
workspace/output/q*/review_packet.md
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/review_note.md
workspace/output/q*/q*_summary.md
```

对跨问题和最终检查：

```text
workspace/output/question_index.md
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## 写入或更新文件

Layer 2 findings 写入：

```text
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
```

如果源产物发生变化，所有重复旧 claim 的下游产物都必须更新，或明确标记为 obsolete。

## 回溯触发矩阵

| 后续发现 | 回溯到 active stage | 需检查源产物 | 可能需要同步的文件 |
|---|---|---|---|
| 验证发现约束失败 | Stage 2 Plan 或 Stage 3 Build | `review_packet.md`、`results/result.json` | `validation.md`、`review_note.md`、`q*_summary.md`、`traceability.md`、论文 |
| 灵敏度推翻结论 | Stage 2 Plan、Stage 4 Verification | `review_packet.md`、`sensitivity.md`、`results/result.json` | `q*_summary.md`、`final_results.md`、`traceability.md`、论文 |
| 单位或维度不一致 | Stage 2 Plan | `review_packet.md`、`result.json` | 代码输出、图表、summary、论文公式 |
| build 中出现隐藏假设 | Stage 2 Plan | `review_packet.md`、代码说明 | `review_note.md`、`validation.md`、`sensitivity.md`、论文限制 |
| 数据预处理改变结果含义 | Stage 2 Plan 或 Stage 3 Build | `review_packet.md`、`run.log`、`result.json` | `validation.md`、`q*_summary.md`、final traceability |
| 模型族不再适合数据 | Stage 2 Plan | `review_packet.md` | 所选模型、build 产物、summary |
| 基线优于主模型 | Stage 2 Plan 或 Stage 3 Build | `review_packet.md`、`validation.md`、`result.json` | 模型理由、final wording、claim eligibility |
| 运行失败后期才发现 | Stage 3 Build | `run.log`、`result.json` | 所有含结果的 summary 和论文 claim |
| 最终论文新增 claim | Stage 7 Integration 或 Stage 8 Paper | `traceability.md`、source `result.json` | 论文文本、final reports |
| 图表支撑了无证据 claim | Stage 5 Figures/Tables 或 Stage 8 Paper | visual source、`traceability.md` | caption、论文文本、review report |
| 两个 `q*` 符号冲突 | Stage 2 Plan 或 Stage 7 Integration | `review_packet.md`、`final_results.md` | 论文公式、notation table |
| result status 变成 partial/fail | Stage 3 Build 或 Stage 4 Verification | `result.json`、`validation.md`、`sensitivity.md` | summary、final results、traceability、abstract |
| final review 发现 overclaim | Stage 8 Paper 或更早源 stage | paper、`traceability.md`、source artifact | paper wording、quality report、source review note |

## 回溯决策等级

| 等级 | 适用情形 | 动作 |
|---|---|---|
| Note | 不一致较小且不影响结论 | 记录到 `review_note.md` 或 final report |
| Patch | 源产物需要局部修正 | 编辑源产物并同步下游 |
| Rebuild | 模型/代码/结果不可靠 | 回到受影响 `q*` 的 Plan 或 Build |
| Downgrade | 证据可用但弱于当前 claim | 标记 `PARTIAL`，弱化措辞，更新 traceability |
| Remove claim | 证据不能支撑论文使用 | 从论文移除并写入 final reports |
| Block | 必答答案缺失或被反驳 | 修复前 final verdict 不能 `PASS` |

## 回溯 Issue 格式

在 `review_note.md` 或 final reports 中使用：

```text
| issue id | severity | conflict type | evidence files | backtrack target | affected files | required action | status |
|---|---|---|---|---|---|---|---|
```

增加同步 checklist：

```text
source artifact changed:
old claim:
new claim:
files updated:
files requiring manual/user review:
claim eligibility after patch: full | limited | not eligible
```

## Claim 撤回与降级规则

出现以下情况时撤回 claim：

- 支撑它的 `result.json` 缺失、失败或被反驳；
- 验证显示不可行或重大约束违规；
- 灵敏度显示合理扰动下结论反转；
- 图表无法复现；
- claim 只在论文 prose 中出现。

出现以下情况时降级 claim：

- 证据支持方向，但不支持精确量级；
- 验证 partial 但不矛盾；
- 灵敏度只在较窄范围内稳定；
- 数据重构合理但不确定；
- 模型更适合作情景分析，而非确定预测。

替换措辞示例：

| 过强表述 | 回溯后表述 |
|---|---|
| “模型证明最优方案为...” | “在给定约束和可用数据下，模型推荐...” |
| “预测是准确的。” | “在可用验证集上误差可接受，但预测期风险仍存在。” |
| “排序是稳定的。” | “在测试权重范围内，头部方案稳定；较低排名敏感。” |
| “该方法普遍适用。” | “该方法适用于满足本文假设和数据结构的情景。” |

任何 downgrade 必须同步到：

```text
workspace/output/q*/review_note.md
workspace/output/q*/q*_summary.md
workspace/output/final/traceability.md
workspace/output/final/quality_report.md
```

如果论文已生成，也必须同步修改论文。

## Partial 与 Fail 传播规则

`PARTIAL` 传播：

- 只带限制保留在 `final_results.md`；
- traceability eligibility 标为 limited；
- 除非限制可见，否则不要作为摘要 headline；
- 在受影响论文 claim 附近写出限制；
- 在 `quality_report.md` 记录 unresolved risk。

`FAIL` 传播：

- 除非 rebuild，否则从 final conclusions 移除；
- 阻断所有依赖它的 hard claim；
- 在 `quality_report.md` 标明受影响 `q*`；
- 如果失败结果对应必答任务，final verdict 不能是 `PASS`；
- 保留 failure 记录，不要隐藏。

跨问题传播：

- 如果 `q2` 依赖变化后的 `q1` 结果，重新检查 `q2` 输入和结论；
- 如果共享假设变化，重新检查所有使用它的模型；
- 如果符号变化，更新所有公式、summary 和 final paper；
- 如果 final aggregate 变化，更新所有包含它的图表。

## 常见回溯案例

### 符号漂移

症状：`x_i` 在一个文件中是 0-1 选择变量，在另一个文件中是连续评分。

回溯：

- 修正 `review_packet.md` 的 assumptions and notation；
- 更新代码注释、论文公式、最终 notation table；
- 只有代码变量含义改变时才需要 rerun。

### 隐藏假设

症状：代码设置上限、填补缺失或固定参数，但 `review_packet.md` 没记录。

回溯：

- 增加假设或预处理说明；
- 如果影响结果，补敏感性；
- 更新 summary limitation。

### 模型族不匹配

症状：选择线性模型，但验证残差显示阈值或非线性结构。

回溯：

- 返回 `review_packet.md` 的 candidate model matrix；
- 增加非线性或分段替代；
- 重建，或把线性结果降为 baseline。

### 鲁棒性失败

症状：小扰动导致排名、路径或政策反转。

回溯：

- 标记结论 unstable 或 conditionally stable；
- 可行时增加鲁棒替代；
- 最终论文避免硬推荐。

### 论文过度 claim

症状：论文使用“证明”“普适”“精确影响”等超出证据的措辞。

回溯：

- 更新 traceability eligibility；
- 用边界化语言重写；
- 重要过度 claim 写入 quality report。

### 图表 claim 不匹配

症状：图表只是情景仿真，但 caption 把它写成经验事实。

回溯：

- 修改 caption 和正文；
- 增加 source 和 scenario label；
- 更新 traceability row。

## 与 Layer 1 的区别

Layer 1 问：这个产物局部质量是否足够？

Layer 2 问：后续证据出现后，这个产物是否仍然为真？

当后续产物削弱、推翻或矛盾于早期产物时使用 Layer 2。不要用最终论文编辑替代源产物修复。

## Manual 与 AP 行为

Manual mode：

- 遇到 `Rebuild`、`Remove claim` 或 `Block` 时暂停；
- 所选模型改变时暂停；
- 返回受影响文件路径和所需决策。

AP mode：

- 证据明确时自动执行 `Note`、`Patch`、`Downgrade` 和清楚的 `Remove claim`；
- `Rebuild` 仅在 fallback 路线已定义时继续；
- 在 final reports 中记录所有 downgrade 和 unresolved issue。

## 退出条件

Layer 2 完成条件：

- 每个 high contradiction 已修复、降级、移除或标记阻塞；
- 没有下游文件重复 obsolete claim；
- `traceability.md` 反映每个 claim 当前来源和 eligibility；
- `quality_report.md` 记录剩余风险和 final verdict impact。

## 迁移说明

本层保留 legacy 的跨阶段一致性回检思想，但通过 active workspace 产物、定向同步和 claim eligibility 规则实现。
