# Quality Gate Contract

## Purpose

定义新版 workflow 的最终质量门。质量门不只是文件存在检查，而是对建模质量、数值质量、验证质量、写作质量、CUMCM 风格、traceability、匿名性和最终 verdict 的综合判断。

质量结果写入：

```text
workspace/output/final/quality_report.md
```

必要时同步写入：

```text
workspace/output/final/review_report.md
workspace/output/q*/warnings.md
workspace/output/q*/review_note.md
```

## Gate Items

最终质量门至少包含：

```text
stage completeness
modeling quality
numerical quality
validation quality
writing quality
CUMCM style quality
traceability
anonymity
feedback layer findings
final verdict
```

每一项都必须给出：

```text
verdict: PASS | PARTIAL | FAIL
evidence files
blocking issues
limitations
required fixes
```

## Stage Completeness

检查：

- Stage 1-9 的必要产物是否存在；
- 每个 `q*` 是否至少有 plan、result、validation/sensitivity、summary；
- final layer 是否有 `final_results.md`、`traceability.md`、final figure/table indexes；
- paper artifacts 是否存在或 failure 已记录；
- final review reports 是否存在。

文件缺失不一定自动 `FAIL`，但若缺失阻断必答结论、traceability 或匿名检查，则 final verdict 不能 `PASS`。

## Modeling Quality

检查：

- question decomposition 是否覆盖全部任务；
- model choice 是否有候选比较；
- baseline 是否存在或缺失有理由；
- selected model 是否匹配题意、数据和约束；
- assumptions、notation、model name 是否清楚；
- 模型是否能支撑 CUMCM 论文表达；
- rejected candidates 是否有具体理由。

`FAIL` 信号：

- 模型回答了错误问题；
- 模型路线无候选比较；
- 假设无支撑且驱动核心结论；
- 模型名夸大不存在的创新。

## Numerical Quality

检查：

- code 和 `run.log` 是否可复现；
- `result.json` 是否包含所有 hard numbers；
- 单位、维度、字段名是否一致；
- solver status、random seed、algorithm settings 是否记录；
- 异常数据处理是否透明；
- failed/partial run 是否可见。

`FAIL` 信号：

- 论文数字不在 `result.json`；
- 运行失败被隐藏；
- 结果不可复现；
- 单位错误影响结论。

## Validation Quality

检查：

- sanity check 是否完成；
- baseline comparison 是否存在或缺失有理由；
- 约束满足和边界条件是否检查；
- sensitivity 是否测试关键参数；
- 是否有单参数和联合扰动；
- instability boundary 是否记录；
- validation verdict 是否与 result status 一致；
- partial/fail 是否传播。

`FAIL` 信号：

- validation 反驳主结论；
- sensitivity 推翻结论但论文仍强 claim；
- 没有任何独立检查；
- failed result 被当作结论。

## Writing Quality

检查：

- paper.md 是否完整；
- 摘要是否有方法和可追踪结果；
- 模型建立、求解、结果、验证、灵敏度是否连贯；
- 图表是否嵌入论证；
- limitation 是否靠近受影响 claim；
- phrase bank 是否只用于润色已有证据；
- paper.tex 与 paper.md 是否一致；
- PDF failure 是否记录。

`FAIL` 信号：

- paper 添加 unsupported claims；
- 摘要有 untraceable hard numbers；
- 结果段不回答题目；
- limitation 被隐藏。

## CUMCM Style Quality

检查：

```text
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_structures.md
competitions/cumcm/distilled_formats.md
```

重点：

- 结构是否符合 CUMCM 建模论文；
- 摘要是否有高信息密度；
- 图表格式和 caption 是否规范；
- 公式、表格、引用是否一致；
- 反模式是否修复或报告；
- 快速评委视角能否识别贡献。

## Traceability

使用 `references/result_traceability.md` 检查：

- paper claim -> source question -> source file -> source field -> validation status 是否完整；
- 摘要数字是否 allowed in abstract；
- partial result 是否标 limitation；
- fail result 是否从论文 claim 中移除；
- figure/table claim 是否追踪到 source field；
- final_results 与 traceability 是否一致。

`FAIL` 信号：

- 中心 claim 不可追踪；
- fail result 仍作为结论；
- 摘要数字 source 缺失；
- 图表 claim 没有 source field。

## Anonymity

检查：

- paper.md；
- paper.tex；
- paper.pdf metadata if exists；
- source files；
- figures/tables；
- code comments；
- local paths；
- user/team/school identifiers；
- hidden metadata。

匿名性风险必须写入：

```text
workspace/output/final/anonymity_report.md
```

未清除的 high anonymity risk 会阻止 final `PASS`。

## Feedback Layers

Final review should run or simulate:

```text
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
```

Findings must be summarized in:

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

要求：

- L1：局部质量 issue；
- L2：跨产物矛盾和 claim downgrade；
- L3：panel verdict 和 must-fix；
- L4：calibration、反包装、CUMCM 质量倾向。

Unresolved high feedback issue 会阻止 final `PASS`。

## Final Verdict

最终 verdict 只能为：

```text
PASS
PARTIAL
FAIL
```

`PASS` 条件：

- 所有必答任务有可用答案；
- hard claims 可追踪；
- validation/sensitivity 不反驳结论；
- partial limitations 已表达；
- no fail result used as claim；
- anonymity high risks 清除；
- L1-L4 high findings 已修复；
- CUMCM style 无 high anti-pattern。

`PARTIAL` 条件：

- 论文可交付但有明确限制；
- 某些结果 limited，但正文已诚实表达；
- traceability 对中心 claims 完整；
- 无未披露 high risk。

`FAIL` 条件：

- 必答答案缺失或不可用；
- 中心 claim 不可追踪；
- validation failed result 被用作结论；
- 匿名 high risk 未清除；
- unresolved high issue 影响核心质量；
- paper 无法支撑 final results。

## Failure Handling

任何缺失或失败都必须写入 `quality_report.md`。不可追溯硬数字必须从论文结论中移除，或标记为 not allowed。不得用写作润色掩盖质量门失败。

若 final verdict 不是 `PASS`，`quality_report.md` 必须包含：

```text
blocking issues
affected claims
required fixes
whether paper can be submitted with limitations
next action
```
