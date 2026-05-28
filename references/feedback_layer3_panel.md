# Feedback Layer 3：终局 Panel Review

## 目的

Layer 3 是多视角最终审阅。它让不同专家视角审阅同一组最终产物，用来发现单一 checklist 容易漏掉的问题。

如果当前环境支持独立 sub-agent 或并行 review，可以让各 panel 独立运行再合并 findings。若不支持，则串行执行，但每个视角必须保留独立笔记，避免互相污染。

## 触发时机

在完整草稿集存在后调用：

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

发生重大改写、模型 rebuild、claim downgrade 或 final integration 改动后，应再次调用。

## 读取文件

```text
workspace/problem/problem.md
workspace/output/question_index.md
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
references/rubrics.md
references/model_catalog.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/empirical_notes.md
```

## 写入或更新文件

Panel findings 合并到：

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

如果 finding 改变 claim eligibility，更新：

```text
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/q*/review_note.md
```

## Panel 运行规则

- 每个 panel 视角先独立审阅，再聚合；
- 每个 panel 必须输出 `PASS`、`PARTIAL` 或 `FAIL`；
- 每个 panel 必须区分 must-fix 与 nice-to-fix；
- finding 必须点名受影响文件和 required fix；
- aggregator 必须保留不同意见，不能用平均分抹平；
- 单个 unresolved high issue 可以阻止 final `PASS`。

## Panel 输出格式

每个 panel 输出：

```text
panel:
verdict: PASS | PARTIAL | FAIL
top strengths:
must fix:
nice to fix:
claim downgrades:
affected files:
recommended next action:
```

合并到 `review_report.md`：

```text
| panel | verdict | severity | issue | evidence | affected files | required fix | status |
|---|---|---|---|---|---|---|---|
```

汇总到 `quality_report.md`：

```text
Layer 3 panel verdict:
Blocking issues:
Limited claims:
Claims removed:
Final verdict impact:
```

## Panel 视角

### 1. 建模专家

角色：审查数学建模形式、模型匹配度、假设和贡献表达。

检查问题：

- 每个 `q*` 的模型族是否匹配任务类型？
- 变量、约束、目标、方程或评价指标是否完整？
- 假设是否必要，并进入模型？
- 模型是否回答真实题目，而不是方便的 proxy？
- 候选模型拒绝理由是否可信？
- 模型名是否具体且诚实？
- 论文是否解释为什么选择该模型？
- 是否有清楚的基线或比较？
- 模型限制是否在结论附近可见？

High issue：

- 目标或指标不匹配题目要求；
- 主结论依赖无支撑假设；
- 所选模型弱于明显基线且无解释；
- 公式段落装饰化，和实现脱节。

推荐修复：

- 回到 `candidates.md` 增加替代路线；
- 在 `model.md` 中补 model contract；
- 如果路线只能作情景分析，则降级论文 claim；
- 增加基线比较或解释基线不足。

### 2. 数值与算法专家

角色：审查实现正确性、可复现性、求解器行为、数值稳定性和计算证据。

检查问题：

- `run.log` 是否记录命令、输入、输出和失败？
- `result.json` 是否包含论文使用的硬数字？
- 求解器设置、随机种子、收敛准则、启发式参数是否记录？
- 求解后是否检查约束？
- 单位和维度是否一致？
- 是否测试边界或 edge cases？
- 结果对初始化、求解 tolerance 或扰动是否稳健？
- 图表是否匹配计算输出？
- failed 或 partial computation 是否可见？

High issue：

- 结果不可复现；
- 论文数字没有进入 `result.json`；
- 忽略不可行、残差过大或 solver gap；
- 验证与最终 claim 矛盾；
- 灵敏度不稳定但论文仍声称稳定。

推荐修复：

- 重新运行并记录 command/output；
- 增加 constraint residual table；
- 求解证据不足时把结果标为 `PARTIAL`；
- 移除或重标不受支撑的图表 claim。

### 3. 评委与论文表达专家

角色：审查 CUMCM 风格读者能否快速理解贡献、证据和答案。

检查问题：

- 摘要是否写出具体方法和已验证结果？
- 评委能否快速找到每个 `q*` 的答案？
- 问题分析、模型建立、求解、验证和结论是否连贯？
- 模型名是否有表达力且不夸大创新？
- 图表是否被引入、解释并连到 claim？
- 假设和符号是否简洁而非堆砌？
- 限制是否诚实且靠近相关 claim？
- 自评是否写出后果和改进，而非空泛表态？
- 论文是否避免通用模板语言？

High issue：

- final result section 缺少必答答案；
- 摘要含无支撑硬数字；
- 论文隐藏 limited 或 failed 结果；
- 图表装饰化或未解释；
- 结论过度泛化。

推荐修复：

- 重构最终答案表；
- 在 traceability audit 后重写摘要；
- 把 limitation 移到受影响模型/结果段；
- 增加图表解释段。

### 4. 数据与可复现性专家

角色：审查数据 lineage、预处理、来源纪律、traceability 和可审计性。

检查问题：

- 题目附件、图片和数据源是否全部 accounted for？
- `data_recon.md` 是否说明清洗、填补、过滤、归一化和重构字段？
- 行数、列含义、单位转换是否记录？
- 每个最终硬数字是否追踪到 `result.json`？
- 图表能否从记录输出复现？
- 附件限制是否进入模型限制？
- 匿名性和文件输出要求是否遵守？
- traceability 是否诚实标记 claim eligibility？

High issue：

- 静默预处理改变结果含义；
- 重构数据驱动结论但没有 limitation；
- 最终论文包含无来源数字；
- 图表没有 source artifact；
- traceability row 指向弱或失败来源。

推荐修复：

- 增加 data lineage table；
- 降级 claim eligibility；
- 更新 traceability 和 captions；
- 在 final paper 与 quality report 中增加 limitation。

### 5. 校准与怀疑读者

角色：判断作品是真强，还是只是包装得好。

检查问题：

- 结论放在简单基线旁边是否仍可信？
- 最好看的图是否真的支撑 claim？
- 验证和灵敏度是否选择了诊断性检查？
- 是否具备 CUMCM 风格质量信号：摘要硬数字、清晰模型名、实质鲁棒性、可读最终答案？
- claim 是否与证据成比例？
- 是否用自信措辞隐藏弱点？
- 如果评委只读摘要、最终结果和图表，会得到准确印象吗？

High issue：

- polished writing 超过证据；
- 模型命名暗示不存在的创新；
- 灵敏度装饰化；
- 摘要 headline 依赖 limited evidence；
- final verdict 相对 unresolved issues 过于乐观。

推荐修复：

- 调用 Layer 4 calibration；
- 降级自信 claim；
- 增加直接 limitation table；
- 强化最有诊断价值的验证检查。

## 合议规则

Aggregator 应执行：

1. 收集所有 panel findings。
2. 按 affected claim 或 file 合并重复问题。
3. 对同一问题保留最高 severity。
4. 识别 blocking issues。
5. 识别 claim downgrades 和 removals。
6. 更新 `review_report.md`。
7. 更新 `quality_report.md` 中的最终 verdict 和 limitation summary。
8. 如果 finding 需要源产物回溯，触发 Layer 2。
9. 如果 finding 暗示“包装强但证据弱”，触发 Layer 4。

Final panel verdict：

- `FAIL`：任何 unresolved high issue 使必答答案、traceability、匿名性或中心 claim 失效。
- `PARTIAL`：必答答案存在，但部分答案有限制，必须保守呈现。
- `PASS`：所有 panel 为 pass 或低风险 partial，且没有 unsupported paper claim。

不要平均 verdict。一个严重可复现性问题可以压过多个正面写作评价。

## Directed Rework Map

| Panel finding | Rework target | 常见同步文件 |
|---|---|---|
| 模型不回答题目 | `analysis.md`、`candidates.md`、`model.md` | result、validation、summary、final paper |
| 结果不可复现 | `run.log`、`result.json`、代码输出 | validation、summary、traceability |
| 摘要 overclaim | paper draft、`traceability.md` | `quality_report.md` |
| 图表无支撑 | figure/table source、`traceability.md` | caption、paper text、review report |
| data lineage 弱 | `data_recon.md` | validation、limitation、traceability |
| 灵敏度浅 | `sensitivity.md` | summary、final wording |
| 最终答案难找 | `final_results.md`、paper structure | abstract、conclusion |

## Manual 与 AP 行为

Manual mode：

- panel 建议模型 rebuild、中心 claim 移除、重大论文改写或用户决策时暂停；
- 只返回受影响路径供审阅。

AP mode：

- 自动执行清楚的 claim downgrade、limitation label 和论文措辞修复；
- panel finding 识别源产物冲突时运行 source backtrack；
- 不压制 panel 分歧，在 `quality_report.md` 记录 unresolved risk。

## 迁移说明

本层保留 legacy 的高密度多视角 panel、独立评审、聚合逻辑和定向返工行为，并将所有输出绑定到 active final reports。
