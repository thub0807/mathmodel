# 质量 Rubric

## 目的

本文件定义 Markdown-first 工作流中的 active 定性评审标准。它是人类/Agent 使用的质量 rubric，不是评分脚本。用于把具体问题写入：

```text
workspace/output/q*/review_note.md
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
workspace/output/final/traceability.md
```

所有 verdict 必须基于可见产物。论文写得漂亮不等于证据充分；硬数字必须能追溯到 `workspace/output/q*/results/result.json`、验证和灵敏度证据。

## Verdict 标准

| Verdict | 含义 | 必须记录 |
|---|---|---|
| `PASS` | 证据足够进入下一阶段或支撑最终论文使用。 | 支撑文件和剩余低风险 |
| `PARTIAL` | 只能在明确限制下使用。 | 限制必须进入下游摘要、traceability 和论文文本 |
| `FAIL` | 不能支撑论文 claim，必须修正、替换或移除。 | 阻塞原因和下一步动作 |

Severity 与 verdict 分开使用：

| Severity | 含义 | 必要动作 |
|---|---|---|
| High | 可能使结果、traceability、匿名性、核心答案或论文结论失效 | 修复、阻塞、重建或移除 claim |
| Medium | 削弱可信度，但可能带限制继续 | 记录，并在可行时修复 |
| Low | 表达、完整性或小的清晰度问题 | 记录或顺手修复 |

## 核心评审维度

### 1. 题意理解

阅读：

```text
workspace/problem/problem.md
workspace/problem/images/
workspace/problem/attachments/
workspace/output/question_index.md
workspace/output/q*/analysis.md
```

`PASS` 信号：

- 每个 `q*` 都对应 `problem.md` 中的必要任务；
- 每个任务有目标输出、输入材料、依赖关系和成功标准；
- 相关图片和附件被引用；
- 不确定性被记录，而不是被悄悄假定；
- Agent 直接理解题面，而不是把派生产物当作唯一来源。

`PARTIAL` 信号：

- 拆解总体合理，但仍有一个不影响核心路线的歧义；
- 某个数据或图片依赖不确定，但不是核心；
- 下游任务依赖尚未完成的上游结果。

`FAIL` 信号：

- 必答任务被遗漏；
- 两个无关任务被合并，导致证据不可追踪；
- 结果回答了与题面不同的问题；
- 论文结论无法回到 `problem.md`。

发现写入 `question_index.md`、`analysis.md`，有下游影响时写入 `review_note.md`。

### 2. 模型选择

阅读：

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
references/model_catalog.md
```

`PASS` 信号：

- 条件允许时考虑了基线、主模型和鲁棒替代；
- 被拒绝候选有具体原因；
- 所选模型匹配任务类型、数据可得性和输出要求；
- 变量、参数、目标/指标、约束、算法明确；
- 模型能产生结构化 `result.json` 字段；
- 模型名具备 CUMCM 论文表达力。

`PARTIAL` 信号：

- 只有两条候选路线可行，且原因已记录；
- 所选模型可接受，但有一个明显假设或数据弱点；
- 验证路线存在但较窄。

`FAIL` 信号：

- 模型只是凭习惯或便利选择；
- 自然存在替代方案时没有基线；
- 模型不能回答该 `q*`；
- 假设无依据或被隐藏；
- 模型输出无法追踪到最终 claim。

候选比较应覆盖题意匹配、数据匹配、可实现性、可解释性、可验证性、可追踪性、鲁棒性和论文表达力。

### 3. 求解实现

阅读：

```text
workspace/output/q*/model.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

`PASS` 信号：

- 代码使用锁定实现语言；
- 输入文件、预处理、命令、库和输出均有记录；
- `result.json` 包含状态、单位、硬数字、来源命令和 claim eligibility；
- 求解器设置、随机种子、启发式参数可复现；
- 结果量级符合约束、单位和领域常识。

`PARTIAL` 信号：

- 运行成功，但某个非核心预处理记录偏弱；
- 启发式方法可复现，但缺少强最优性证据；
- 结果只适合支撑有限 claim。

`FAIL` 信号：

- 论文中的结果没有出现在 `result.json`；
- 失败运行被隐藏或覆盖；
- 单位或维度与 `notation.md` 冲突；
- 数据行列被静默改变；
- 随机或启发式输出不可复现。

实现评审必须严守证据纪律：重要数字必须进入 `result.json`。

### 4. 验证与灵敏度

阅读：

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/results/result.json
workspace/output/q*/review_note.md
```

`PASS` 信号：

- 验证检查约束、维度、边界案例和结果合理性；
- 至少有一个基线、消融、交叉方法、手算或外部 sanity check；
- 灵敏度扰动的是重要参数，不是装饰参数；
- 扰动范围有依据；
- 结论影响被标为稳定、条件稳定或不稳定；
- 限制进入 `review_note.md` 和最终 traceability。

`PARTIAL` 信号：

- 验证覆盖核心约束，但比较证据有限；
- 灵敏度较窄，但针对最重要参数；
- 结论仍能在明确限制下使用。

`FAIL` 信号：

- 主结论被验证反驳；
- 灵敏度推翻答案，但下游仍沿用旧 claim；
- 验证只是重复结果；
- 失败或不稳定发现没有进入论文侧记录。

### 5. 论文表达

阅读：

```text
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
```

`PASS` 信号：

- 摘要包含具体方法和结果信号；
- 每个硬数字、图 claim、表 claim 都可追踪；
- 假设和限制靠近相关 claim；
- 模型名能传达真实机制；
- 结论回答全部要求；
- 自评写出有意义的弱点和可行改进。

`PARTIAL` 信号：

- 表达清楚，但某个弱结果必须作为 limited claim；
- 结构完整，但图表解释需要增强；
- 因证据有限，摘要硬数字较少，但表述诚实。

`FAIL` 信号：

- 摘要包含无支撑硬数字；
- 最终论文隐藏 `PARTIAL` 或 `FAIL` 结果；
- 公式装饰化，与实现脱节；
- 最终答案分散或不完整；
- 论文新增了 `traceability.md` 中没有的 claim。

### 6. 图表质量

阅读：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/traceability.md
workspace/output/final/review_report.md
```

`PASS` 信号：

- 每个图表都有来源、用途和支撑的 claim；
- 标签、单位、图例、caption、尺度可读；
- 图表用于比较、显示不确定性、展示灵敏度或总结最终答案；
- 正文引用并解释图表；
- 表格足够紧凑，不是原始数据倾倒。

`PARTIAL` 信号：

- 来源清楚，但 caption 解释偏弱；
- 某个非关键图略装饰，但不误导。

`FAIL` 信号：

- 图表没有可复现来源；
- 图表与 `result.json` 矛盾；
- 坐标或单位缺失；
- 图表被用于它不能支撑的 claim；
- 论文依赖默认风格图，缺少解释价值。

### 7. CUMCM 风格质量

阅读：

```text
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/empirical_notes.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/quality_report.md
```

`PASS` 信号：

- 问题分析自然引出模型选择；
- 假设必要、少而有影响；
- 符号完整但不过度堆砌；
- 模型建立部分包含变量、目标/方程、求解方法和结果解释；
- 验证与灵敏度有实质内容；
- 图表解释意义，而不仅展示数据；
- 优缺点具体；
- 评委能快速定位最终答案。

`PARTIAL` 信号：

- 论文结构完整，但缺少一个高质量比较或灵敏度视图；
- 模型命名可接受但不够鲜明；
- `review_report.md` 诚实记录质量风险。

`FAIL` 信号：

- 论文像通用模板；
- 模型名夸大创新；
- 验证敷衍；
- 没有清晰结果表回答题目；
- 限制被藏在最后。

## Stage-Level Rubric

### Workspace Audit

`PASS`：

- `workspace/problem/problem.md` 存在并被直接理解；
- 图片和附件被索引；
- 缺失或不可用材料被记录；
- 如存在 `reference.pdf`，仅作 audit-only。

`FAIL`：

- 固定输入路径缺失；
- 材料缺口阻止题意理解；
- Agent 依赖派生文件而不是题面。

### Question Decomposition

`PASS`：

- `workspace/output/question_index.md` 列出所有 `q*`；
- 每个 `q*` 有目标、输入、输出、依赖和预期产物；
- 题间依赖明确。

`FAIL`：

- 任务遗漏或凭空添加；
- 拆解导致结果不可追踪。

### Per-Question Plan

`PASS`：

- `analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 构成可构建路线；
- 候选路线和 fallback 清楚；
- 数据限制在 build 前可见。

`FAIL`：

- 只有口号式模型；
- 假设或符号缺失；
- 没有通向 `result.json` 的路径。

### Build And Result

`PASS`：

- 代码/运行证据与 `result.json` 一致；
- 结果状态有依据；
- 失败被记录而不是隐藏。

`FAIL`：

- 论文侧数字没有结构化来源；
- 实现不可复现。

### Verification And Sensitivity

`PASS`：

- 验证和灵敏度测试真实模型风险；
- 不稳定结果被降级并向下游传递。

`FAIL`：

- 未经证据就把结论写成稳定；
- 已知矛盾未传播。

### Per-Question Summary

`PASS`：

- 摘要包含方法、关键结果、验证状态、灵敏度状态、限制和论文可用性；
- 只使用 `result.json` 和检查允许的 claim。

`FAIL`：

- 摘要比证据更强。

### Final Integration

`PASS`：

- `final_results.md` 汇总所有问题答案；
- `traceability.md` 连接每个硬 claim 到来源产物；
- 跨问题符号和假设统一。

`FAIL`：

- 最终答案表遗漏必答任务；
- 核心 claim 断链。

### Paper Generation

`PASS`：

- 论文结构完整；
- 摘要在验证结果存在后撰写；
- 模型、结果、验证、灵敏度和限制相互连接。

`FAIL`：

- 模板文本仍泛化；
- 论文 claim 超过证据。

### Final Review

`PASS`：

- `review_report.md` 包含 findings 和修复状态；
- `quality_report.md` 给出最终 `PASS`、`PARTIAL` 或 `FAIL`；
- high issues 已修复或明确阻塞；
- 匿名和 traceability 已检查。

`FAIL`：

- 最终质量报告压制已知限制。

## 报告写入规则

在 `review_note.md`、`review_report.md`、`quality_report.md` 中使用：

```text
| issue id | severity | verdict impact | artifact | finding | required fix | downstream impact | status |
|---|---|---|---|---|---|---|---|
```

`review_note.md` 是单个 `q*` 的局部记录，应包含：

- 被审阅产物；
- findings 表；
- local verdict；
- 必要 patch；
- 结果是否可进入论文侧。

`review_report.md` 面向最终审查，应包含：

- critic 和 panel findings；
- 跨问题一致性问题；
- 论文结构和表达问题；
- 已修复与未解决 issue 表。

`quality_report.md` 应包含：

- final verdict；
- unresolved high/medium issues；
- claim eligibility 总结；
- limitations 总结；
- 若最终 verdict 不是 `PASS`，说明降级原因和下一步。

## PASS / PARTIAL / FAIL 判定规则

局部 `q*` verdict：

- `PASS`：计划、实现、结果、验证、灵敏度均能支撑论文使用。
- `PARTIAL`：答案只能在条件、弱化 claim 或缺少非核心证据的限制下使用。
- `FAIL`：结果不能回答任务或与检查相矛盾。

最终 verdict：

- `PASS`：所有必答任务都有可用答案，traceability 完整，没有 unresolved high issue，论文 claim 与证据匹配。
- `PARTIAL`：论文可交付，但必须诚实呈现限制，且没有 unsupported core claim。
- `FAIL`：必答答案缺失、不可追踪、被反驳或不宜呈现。

## Manual 与 AP 行为

Manual mode：

- high issue 改变路线、阻塞结果、移除中心 claim 或需要用户选择时暂停；
- 返回供审阅的文件路径。

AP mode：

- 自动执行清楚的局部修复；
- 对风险选择写入 `review_note.md` 和 warnings；
- 在最终报告和论文中保留所有限制。

## 迁移说明

本 active rubric 保留 legacy 中高密度阶段质量和评审标准，但用可见 workspace 产物替代旧隐藏状态和脚本耦合评分。
