# Feedback Layer 4：校准与反包装检查

## 目的

Layer 4 检查作品是否真的由证据支撑，而不是只是看起来完整、措辞漂亮。它防止过度自信表达、装饰性验证、夸大型模型命名，以及“表面通过 checklist 但实质薄弱”的最终报告。

Layer 4 不是奖项预测器。它不得伪造分位、奖项或排名判断，只能做质量倾向判断，并给出具体改进建议。

## 触发时机

在以下情况调用 Layer 4：

- Layer 1 和 Layer 2 几乎没有 finding，但作品仍显得薄弱；
- Layer 3 返回 `PASS` 或轻微 `PARTIAL` 后；
- `workspace/output/final/quality_report.md` 给出 final `PASS` 前；
- 论文措辞强于 `result.json`、验证或灵敏度证据时；
- 摘要、模型命名或图表看起来很强但支撑证据偏薄时。

## 读取文件

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/q*/review_note.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
references/rubrics.md
references/model_catalog.md
competitions/cumcm/empirical.json
competitions/cumcm/empirical_notes.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
```

## 写入或更新文件

```text
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
```

如果 calibration 降低某个 claim 的可信度，必须更新 final traceability 和论文措辞。如果弱点来自源产物，触发 Layer 2。

## 与 CUMCM 经验材料的关系

`competitions/cumcm/empirical.json` 和 `competitions/cumcm/empirical_notes.md` 只能作为校准参考，不能作为自动评分真值。

允许的使用方式：

- 对照论文特征与经验材料中的质量倾向；
- 判断摘要、图表、验证、模型命名是否偏薄；
- 决定哪类改进最可能提升质量；
- 标记看起来低于竞赛风格 baseline 的薄弱段落；
- 支持“偏薄”“可接受”“强于最低要求”“需要更多证据”等定性判断。

禁止的使用方式：

- 伪造缺失经验值；
- 声称精确分位、获奖概率或奖项等级；
- 把经验 anchor 当作硬性 pass/fail 阈值；
- 用经验材料覆盖题目本身的证据；
- 因为论文像强模板而升级弱结果。

如果经验材料缺失或不适用，应在 `quality_report.md` 中说明，并仅按直接证据校准。

## Calibration 输出格式

在 `review_report.md` 或 `quality_report.md` 中增加：

```text
## Layer 4 Calibration

Calibration basis:
- direct evidence files:
- CUMCM empirical references used:
- unavailable references:

| calibration point | evidence | tendency | severity | required adjustment | affected files | status |
|---|---|---|---|---|---|---|
```

Tendency 可使用：

```text
strong | adequate | thin | overstated | unsupported
```

除非经验来源中明确存在且直接适用，否则不要写数值分位。即使存在，也只能作为背景，不能预测奖项。

## 核心校准问题

### 证据真实度

- 结论放在简单基线旁边是否仍可信？
- 最重要的数字是否进入 `result.json`？
- 验证是否测试真实失败模式？
- 灵敏度是否扰动真正驱动结论的参数？
- failed 或 partial 结果是否可见？
- 不确定性、不可行性、重构限制是否靠近 claim？

需要降级的情况：

- 论文声称稳定或最优，但检查很浅；
- 硬数字只出现在 prose；
- 验证只是重复答案；
- limitation 只出现在最终自评。

### 建模真实度

- 模型是否不只是一个漂亮名称？
- 模型名是否描述变量、机制、目标或数据关系？
- 假设是否必要且有后果？
- 候选拒绝理由是否可信？
- 所选模型相对基线的优势是否在论文中可见？
- 模型是否直接回答题目？

需要降级的情况：

- 通用方法被包装成创新；
- 方程不影响实现；
- 假设装饰化；
- 所选模型复杂度超过证据支撑。

### 写作真实度

- 摘要是否陈述已验证的方法和结果？
- 摘要中的硬数字是否 traceability 允许？
- 最终答案是否易找？
- 图表是否有意义，而非装饰？
- claim 是否与证据成比例？
- limitation 是否放在读者需要看到的位置？

需要降级的情况：

- 摘要承诺质量而非报告发现；
- 图表漂亮但无支撑；
- 措辞暗示证明、普适或最优，却无证据；
- 论文用自信语气遮住不确定性。

### CUMCM 风格真实度

- 问题分析是否自然引出模型选择？
- 假设是否少、清楚、有用？
- 符号和公式是否可读？
- 结果是否解释了实际、物理或管理意义？
- 验证和灵敏度是否达到正式建模论文的实质要求？
- 图表信息密度是否足够？
- 自评是否写出真实弱点和可行改进？

需要降级的情况：

- 论文像通用 scaffold；
- 模型段缺少“建立-求解-验证-解释”结构；
- 结果段缺少简洁答案表；
- 鲁棒性讨论表面化。

## 具体校准点

### 1. 摘要硬数字

检查：

- 至少说明核心方法和核心结果；
- 每个数字都出现在 `traceability.md`；
- 数字有单位和语境；
- limited result 不被写成确定结论。

强：

- 摘要包含任务相关硬数字、方法名、稳定性或验证信号。

薄：

- 摘要只有背景和泛泛结论。

过度：

- 摘要使用无来源精确值或忽略 partial status。

必要调整：

- 移除 unsupported numbers；
- 从 `result.json` 加入已验证结果数字；
- 证据 partial 时加入 limitation phrase。

### 2. 模型命名

检查：

- 名称描述方法族和作用；
- hybrid 名称反映子模型之间真实数据流；
- 创新措辞与证据成比例。

较强示例：

- 容量约束混合整数分配模型；
- 熵权-TOPSIS 综合评价模型；
- 回归校准的状态演化模型；
- Monte Carlo 情景压力测试模型。

较弱示例：

- 改进模型；
- 综合模型；
- 数学模型；
- 智能优化模型。

必要调整：

- 把泛化模型名改为机制相关名称；
- 没有技术改变时移除 novelty wording；
- 解释所选模型为什么适合任务。

### 3. 图表密度

检查：

- 图表支撑具体 claim；
- caption 说明比较对象和结论；
- 单位、标签可读；
- 正文引用图表；
- 条件允许时至少有一个图表总结最终答案或鲁棒性。

强：

- 图表清楚展示比较、灵敏度、趋势、流量或最终答案。

薄：

- 默认图或原始表，没有解释。

无支撑：

- 图表无 source artifact 或与 `result.json` 矛盾。

必要调整：

- 增加 source note 和 traceability row；
- 重写 caption，说明被支撑的结论；
- 用答案图或鲁棒性图替换装饰图；
- 移除 unsupported visual claim。

### 4. 验证深度

检查：

- 验证至少包含一个独立诊断；
- 诊断匹配模型风险；
- result status 跟随验证证据；
- failed checks 触发 downgrade。

强诊断示例：

- 优化：约束残差；
- 预测：基线和残差分析；
- 评价：权重/排名稳定性；
- 分类：混淆矩阵和阈值检查；
- 仿真：重复情景和收敛；
- 微分模型：单位、边界、稳定性；
- 网络模型：连通性和边权敏感性。

薄：

- 验证只说“合理”，没有测试证据。

必要调整：

- 增加最匹配模型族的诊断；
- 报告检查的数值结果；
- 更新 claim eligibility。

### 5. 灵敏度与鲁棒性

检查：

- 参数重要；
- 范围合理；
- 输出影响被量化；
- 结论影响被说明；
- 单参数测试可能误导时，加入联合扰动或情景压力测试。

强：

- 灵敏度表包含 baseline、low、high、output change、claim impact。

薄：

- 只扰动一个任意参数且无解释。

过度：

- 测试范围很小或无关，却声称 robust。

必要调整：

- 扰动核心参数；
- 增加稳定性类别：stable、conditionally stable、unstable；
- 不稳定时降级推荐。

### 6. Result Traceability

检查：

- 论文每个 hard claim 都映射到 source artifact；
- trace row 说明 eligibility；
- partial 和 failed evidence 不被当作 full conclusion；
- final result table 与 summaries 一致。

强：

- 评审者能从 paper claim 一行追到 source result。

薄：

- traceability 只列文件，不说明 claim eligibility。

无支撑：

- 论文含 traceability 缺失的 claim。

必要调整：

- 增加 trace rows；
- 移除 unsourced claims；
- 标记 limited claims。

### 7. 自评与限制

检查：

- 弱点具体；
- 每个弱点有后果；
- 改进可行；
- 限制不只藏在结尾。

强：

- “在熵权扰动下，第 4-6 名排序变化，因此论文只使用 top-3 稳定结论。”

弱：

- “模型可能存在误差，后续可改进。”

必要调整：

- 把 limitation 改成证据相关语句；
- 将关键 limitation 移到受影响结果附近。

## 反包装信号

以下信号应视为 Medium 或 High issue：

| 信号 | 风险 | 常见修复 |
|---|---|---|
| prose 精致但源证据弱 | 写作超过工作本身 | 移除 claim 或重建证据 |
| 方程很多但检查很少 | 数学装饰 | 增加诊断或简化 |
| 模型名很新但方法普通 | 贡献夸大 | 诚实改名或增加真实方法细节 |
| 灵敏度重复结果表 | 无鲁棒性证据 | 扰动重要参数并报告影响 |
| 摘要含无支撑硬数字 | headline 误导 | 移除或补 trace |
| limitation 只在结论中出现 | 风险被隐藏 | 移到受影响 claim 附近 |
| 图表漂亮但不可追踪 | 视觉 overclaim | 增加 source 或移除 |
| final verdict 忽略 partial local result | 报告不一致 | 更新 quality report 和 traceability |

## Verdict 调整

Layer 4 可以执行以下 downgrade：

- `PASS` 降为 `PARTIAL`：证据可用但表述过强；
- `PARTIAL` 降为 `FAIL`：主结论缺少验证支撑；
- claim eligibility 从 full 降为 limited；
- unsupported hard claim 的 abstract eligibility 从 yes 降为 no。

Layer 4 不应升级 verdict，除非缺失证据已经真实补齐，且下游文件已同步更新。

Downgrade record：

```text
claim:
old eligibility:
new eligibility:
evidence causing downgrade:
files updated:
remaining risk:
```

## Manual 与 AP 行为

Manual mode：

- 如果 calibration 会移除中心结论、要求模型 rebuild 或改变 final verdict，则暂停；
- 返回受影响文件路径和 proposed downgrade。

AP mode：

- 证据明确时自动应用保守措辞、limitation label 和 traceability downgrade；
- 将 unresolved calibration risk 写入 `quality_report.md`；
- calibration 暴露源产物矛盾时触发 Layer 2。

## 退出条件

Layer 4 完成条件：

- 每个 calibration point 都是 strong、adequate 或明确 limited；
- 摘要和最终 claim 中没有 unsupported hard number；
- 模型名诚实；
- validation 和 sensitivity claim 匹配真实检查；
- CUMCM 经验材料如被使用，只作为定性校准 anchor；
- `quality_report.md` 写明 final verdict impact。

## 迁移说明

本层保留 legacy 的反 gaming 和 calibration 意图，但使用可见产物、CUMCM 经验材料的定性 anchor，以及保守 claim 调整，替代隐藏评分操控。
