# Feedback Layer 1：局部质量 Critic

## 目的

Layer 1 是局部 critic。它审阅单个 `q*` 的产物集，或最终论文的一个产物集，在缺陷扩散到下游之前发现并修正问题。它是可作为 prompt 使用的审阅协议，不是隐藏评估器，也不调用外部评分工具。

Layer 1 必须给出可执行的局部 patch。有效 finding 应说明：源产物、证据问题、必要修改、下游影响。

## 触发时机

| 时机 | 主要审阅对象 | 主要输出 |
|---|---|---|
| 题目拆解后 | `workspace/output/question_index.md` | 必要时写入最终 review 记录 |
| 单题分析后 | `workspace/output/q*/analysis.md` | `workspace/output/q*/review_note.md` |
| 候选/模型规划后 | `candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` | `review_note.md`，必要时 `warnings.md` |
| build/result 后 | `results/result.json`、`results/run.log` | `review_note.md`，必要时调整 result 状态 |
| 验证/灵敏度后 | `validation.md`、`sensitivity.md` | `review_note.md` 和限制标记 |
| 单题 summary 后 | `q*_summary.md` | summary 可用性 finding |
| 论文生成期间 | `final_results.md`、`traceability.md`、论文草稿 | `review_report.md` |
| 最终 review 期间 | 所有 final artifacts | `quality_report.md` |

## 读取文件

对单个 `q*`，读取已存在的以下文件：

```text
workspace/output/question_index.md
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/review_note.md
workspace/output/q*/q*_summary.md
references/model_catalog.md
references/rubrics.md
```

对最终论文，读取：

```text
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/winning_patterns.md
```

## 写入或更新文件

Layer 1 findings 写入：

```text
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

如果局部 issue 改变 claim eligibility，后续必须同步更新：

```text
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
```

## Critic 输出格式

在 `review_note.md` 或最终报告中使用：

```text
## Layer 1 Local Critic

Reviewed artifacts:
- path

Local verdict: PASS | PARTIAL | FAIL

| issue id | severity | artifact | finding | evidence | required patch | downstream impact | status |
|---|---|---|---|---|---|---|---|
```

Severity：

- High：使结果、模型路线、claim eligibility、traceability 或匿名性失效。
- Medium：削弱可信度，但可带限制继续。
- Low：清晰度、表达或完整性问题。

Verdict：

- `PASS`：没有 high 或 unresolved medium issue 阻塞下游。
- `PARTIAL`：只能在明确限制或降级 claim 下使用。
- `FAIL`：修复前不能进入下游。

## 局部 Patch 协议

每个 issue 推荐最小必要 patch：

```text
patch id:
source artifact:
change type: clarify | add evidence | rerun | downgrade claim | replace model | remove claim
exact edit target:
required new evidence:
files to update after patch:
expected verdict after patch:
```

Patch 规则：

- 先修源产物，再更新 summary 和 final traces；
- 局部修正足够时不要重写整个阶段；
- 不因论文表述漂亮而保留无支撑 claim；
- 证据弱时降级 claim，不用漂亮措辞掩盖；
- `PARTIAL` 结果必须在 summary 和 final traceability 中可见。

## 单题 Critic 检查清单

### A. `analysis.md`

检查问题：

- 是否识别了正在回答的精确任务？
- 是否写清输入、输出、评价标准和依赖？
- 是否区分题目给定数据与 Agent 引入的假设？
- 是否点名相关图片和附件？
- 是否记录歧义，而不是私自补题？
- 是否说明什么情况会使答案不可用？

High issue：

- 必答任务遗漏；
- 任务目标与 `problem.md` 不同；
- 输出格式不清；
- 隐藏了对其他 `q*` 的依赖。

推荐 patch：

- 增加任务表：目标、输入、输出、依赖、成功标准；
- 增加 ambiguity note 和 downstream impact。

### B. `candidates.md`

检查问题：

- 条件允许时是否有基线、主模型、鲁棒替代？
- 候选是否结构不同，而非同一模型换名字？
- 被拒绝路线是否有具体原因？
- 每条路线是否列出数据需求、假设、实现风险、验证路线、论文表达力？
- 主路线失败时是否有 fallback？
- 所选路线是否能产生结构化 `result.json` 字段？

High issue：

- 非平凡模型没有基线；
- 所选路线无法使用现有数据；
- 候选比较忽略验证；
- 复杂路线没有比简单路线更强的解释或效果。

推荐 patch：

- 增加 candidate matrix；
- 增加一个透明基线和一个鲁棒替代；
- 说明所选路线为何优于基线。

### C. `model.md`

检查问题：

- 变量、参数、单位、域、目标/指标、约束、算法是否明确？
- 模型名是否具体且诚实？
- 方程是否与题意相连，而非符号装饰？
- 是否描述预期 `result.json` keys？
- 是否列出求解器设置、收敛预期或算法选择？
- 假设是否同步到 `assumptions.md`？
- 是否说明模型失效条件？

High issue：

- 符号未定义或冲突；
- 目标/约束不匹配题意；
- 模型不能生成声称的结果；
- 缺少实现路线。

推荐 patch：

- 增加 “model contract”：变量、参数、方程/目标、算法、输出、验证、失败触发。

### D. `assumptions.md`

检查问题：

- 每条假设是否必要？
- 假设是否来自题面、数据、领域推理或明确的建模简化？
- 是否说明违反假设的影响？
- 假设是否真的被方程或代码使用？
- 弱假设是否进入下游限制？

High issue：

- 代码或论文中出现隐藏假设；
- 中心 claim 依赖无支撑假设；
- 假设与给定数据冲突。

推荐 patch：

- 增加 assumption table：source、role、risk、validation/sensitivity hook。

### E. `notation.md`

检查问题：

- 每个符号是否只定义一次？
- 单位和定义域是否存在？
- 向量/矩阵维度是否清楚？
- 符号是否与代码变量、论文公式一致？
- 跨问题符号是否统一？

High issue：

- 同一符号表示不同含义；
- 单位冲突影响结果；
- 公式使用未定义符号。

推荐 patch：

- 修正 notation table，并把命名变化传播到 model、result、summary 和 paper。

### F. `data_recon.md`

检查问题：

- 是否列出源文件、列、图片、附件？
- 清洗、缺失填补、归一化、过滤是否明确？
- 行数或 shape 变化是否记录？
- 重构字段是否标为 reconstructed？
- 数据限制是否对应模型风险？

High issue：

- 静默数据转换；
- 未验证重构字段驱动主结论；
- 缺失值或异常值被忽略。

推荐 patch：

- 增加 data lineage table：source、transformation、output file、risk。

### G. Build 与 `result.json`

检查问题：

- `run.log` 是否记录命令、输入、输出、warning 和 failure？
- `result.json` 是否包含最终可能使用的每个硬数字？
- `result.json` 是否包含单位和状态？
- 随机种子、求解器选项、库版本是否在相关时记录？
- 结果是否符合约束和单位？
- failed 或 partial run 是否可见？

High issue：

- 论文中有数字，但 `result.json` 没有；
- 隐藏运行失败；
- `result.json` 状态比验证证据更乐观；
- 忽略 solver gap、不可行或随机种子风险。

推荐 patch：

- 重新运行或更新 result，明确 status 和 evidence fields；
- 无法支撑 claim 时降级 eligibility。

### H. `validation.md`

检查问题：

- 是否数值检查约束？
- 是否测试边界或不可能 case？
- 是否有基线、消融、交叉方法或手算？
- 是否报告残差、误差或可行性 gap？
- 是否决定 paper use 是否允许？

High issue：

- 验证与 result status 矛盾；
- 验证只是重复答案；
- 复杂路线没有基线。

推荐 patch：

- 增加至少一个独立检查，并给出 claim eligibility verdict。

### I. `sensitivity.md`

检查问题：

- 扰动参数是否真的影响结论？
- 扰动范围是否有依据？
- 必要时是否考虑单参数和联合扰动？
- 结果变化是否用可解释单位报告？
- 结论是稳定、条件稳定还是不稳定？
- 不稳定发现是否传递下游？

High issue：

- 灵敏度推翻结论但没有降级；
- 参数选择装饰化；
- 没有报告 effect size。

推荐 patch：

- 增加参数表：baseline、low/high、output change、paper impact；
- 在 `review_note.md` 中增加 limitation 或 downgrade。

### J. `q*_summary.md`

检查问题：

- 是否说明方法、关键结果、验证状态、灵敏度状态、限制和论文可用性？
- 所有硬数字是否来自 `result.json`？
- `PARTIAL` 和 `FAIL` 是否诚实呈现？
- 是否直接回答该 `q*`？

High issue：

- summary 过度强化弱结果；
- 遗漏验证或灵敏度中的限制；
- 新增硬数字。

推荐 patch：

- 围绕 verified fields 重写 summary，并增加可见 limitation。

## 最终产物 Critic 检查清单

### `final_results.md`

- 是否回答每个 `q*`？
- 方法和结果结构是否可比较？
- partial/fail 状态是否可见？
- 跨问题依赖是否已解决？

### `traceability.md`

- 每个硬数字、图、表、claim 是否有来源产物？
- 每个 claim 是否说明 eligibility？
- 被移除或降级的 claim 是否标记？
- 最终论文段落是否连到来源证据？

### 论文草稿

- 摘要是否只包含已验证硬数字？
- 结构是否便于扫描？
- 模型名是否具体？
- 图表是否先引入再解释？
- 限制是否靠近受影响 claim？
- 自评是否说明弱点后果，而非空泛谦虚？

### `review_report.md` 与 `quality_report.md`

- high issues 是否修复或明确阻塞？
- final verdict 是否匹配局部 verdict？
- unresolved limitations 是否保留？
- final verdict 不是 `PASS` 时，降级理由是否清楚？

## 局部精修提示

```text
只精修 <artifact> 的受影响段落。
保留已有有效内容。
修复：<issue>。
补充证据来源：<source files>。
更新 downstream impact note：<impact>。
不要引入无支撑 claim。
```

```text
将 claim 从 <old wording> 降级为 <new limited wording>。
原因：<validation or sensitivity finding>。
同步更新 traceability eligibility 和最终 limitation summary。
```

```text
为 <model/result> 增加基线检查。
使用 <path> 中的可用数据。
在 run log 中记录命令/输出，在 result artifact 中记录硬数字。
更新 validation verdict。
```

## Failure 与 Partial 处理

当 local verdict 为 `PARTIAL`：

- 只允许作为 limited claim 使用；
- 在 `review_note.md` 中写明 limitation；
- final traceability 标为 limited；
- 限制不可见时不要作为摘要 headline 使用。

当 local verdict 为 `FAIL`：

- 阻止受影响结果进入论文；
- 重建源产物或移除 claim；
- 记录 failure 和 next action；
- 不要把失败结果改写成含糊文字。

多个 `q*` 产物互相矛盾时：

- 调用 Layer 2 做跨产物回溯；
- 不要只 patch 最终论文。

## Manual 与 AP 行为

Manual mode：

- high issue 改变模型路线、使结果失效、需要 rebuild、移除中心结论或需要用户判断时暂停；
- 只返回受影响文件路径和所需决策；
- 当前阶段要求 manual review 时仍写入 `solution_plan.md`。

AP mode：

- 自动应用清楚的局部 patch；
- 对风险选择写入 `review_note.md` 和 `warnings.md`；
- 保守降级 unsupported claims；
- 在 `quality_report.md` 保留未解决 issue。

## 迁移说明

本层保留 legacy 中高密度局部 critic、diff-style 精修、partial 处理和反过度 claim 机制，同时把所有检查绑定到可见 workspace 产物。
