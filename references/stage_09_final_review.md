# Stage 9: Final Review

## Purpose

执行最终完整性、匿名性、traceability、论文质量和 CUMCM 风格审查，并给出最终 `PASS`、`PARTIAL` 或 `FAIL` verdict。

本阶段必须进行多轮 review：本地 critic、跨产物 backtrack、panel review、calibration、匿名性检查和最终质量门。AP mode 也不得压制 final findings。

## Required Inputs

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf       # if exists
workspace/output/final/source/
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
references/rubrics.md
references/result_traceability.md
references/quality_gate.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_formats.md
competitions/cumcm/distilled_structures.md
competitions/cumcm/empirical.json
competitions/cumcm/empirical_notes.md
```

## Required Outputs

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

如果 review 需要修改论文或 traceability，应更新对应文件并在 `review_report.md` 记录。

## Templates

```text
templates/workspace/final/review_report.md
templates/workspace/final/anonymity_report.md
templates/workspace/final/quality_report.md
```

模板不足时，增加 L1/L2/L3/L4 findings、多轮 review log、abstract review、figure/table review、anonymity scan、final verdict rationale 等段落。

## Entry Conditions

- Stage 8 已生成 paper artifacts，或记录了 PDF/formal template failure。
- `traceability.md` 存在并覆盖 paper-facing claims。
- `final_results.md` 存在。
- Stage 8 generation warnings 已保留。

## Procedure

1. 建立多轮 review log。

   在 `review_report.md` 中记录：

   ```text
   review round
   reviewer/layer
   files checked
   major findings
   action taken
   unresolved issues
   verdict impact
   ```

   至少包含 L1、L2、L3、L4、匿名性、traceability、CUMCM style 轮次。

2. 执行 L1 local critic。

   使用 `references/feedback_layer1_critic.md` 检查：

   - final paper 是否有 unsupported hard numbers；
   - final results 是否覆盖所有 `q*`；
   - validation/sensitivity limitation 是否保留；
   - 图表是否支撑 claim；
   - final reports 是否完整；
   - summary 与 paper 是否一致。

   findings 写入：

   ```text
   workspace/output/final/review_report.md
   workspace/output/final/quality_report.md
   ```

3. 执行 L2 backtrack。

   使用 `references/feedback_layer2_backtrack.md` 检查 final paper 是否矛盾于：

   - assumptions；
   - notation；
   - model choices；
   - result.json；
   - validation；
   - sensitivity；
   - figure/table indexes；
   - traceability。

   发现 unsupported claim 时，必须执行：

   - remove claim；
   - downgrade claim；
   - update traceability；
   - update paper；
   - mark blocking。

   不得只在 review report 里说“有问题”而保留正文强 claim。

4. 执行 L3 panel review。

   使用 `references/feedback_layer3_panel.md`，从至少以下视角审查：

   - 建模专家；
   - 数值/算法专家；
   - 评委/论文表达专家；
   - 数据与可复现性专家；
   - 校准与怀疑读者。

   若支持并行，则各视角独立执行；否则串行但保持独立记录。

   Panel findings 写入 `review_report.md`，聚合 verdict 写入 `quality_report.md`。

5. 执行 L4 calibration。

   使用 `references/feedback_layer4_calibration.md` 和 CUMCM empirical materials：

   ```text
   competitions/cumcm/empirical.json
   competitions/cumcm/empirical_notes.md
   ```

   检查：

   - 论文是否包装强于证据；
   - 摘要 hard numbers 是否过强；
   - 模型命名是否夸大；
   - 图表密度是否足够；
   - 验证和灵敏度是否有实质；
   - limitation 是否可见。

   不得伪造分位、奖项或排名判断。只给质量倾向和改进建议。

6. 执行摘要 review。

   对照 `competitions/cumcm/abstract_template.md`：

   - 摘要是否先概述问题和方法，再给关键结果；
   - 是否包含可追踪 hard numbers；
   - 摘要数字 validation status 是否非 fail；
   - partial result 是否被限制表达；
   - 是否避免空泛背景和自夸；
   - 是否能让评委快速理解贡献。

   摘要发现写入 `review_report.md`；若影响 final verdict，写入 `quality_report.md`。

7. 执行图表 review。

   检查：

   - 每张 final figure/table 是否有 source file 和 source field；
   - 是否绑定 claim；
   - caption 是否符合 `distilled_formats.md`；
   - 图表是否服务论证；
   - partial/fail 限制是否可见；
   - 图表编号和正文引用是否一致；
   - 是否触发 `anti_patterns.md`。

8. 执行模型与变量一致性 review。

   检查：

   - 模型名在 `model.md`、summary、final_results、paper 中一致；
   - 变量含义跨章节一致；
   - 公式符号与 notation 一致；
   - 单位统一；
   - result 字段与论文数字一致；
   - 代码/算法叙述与实际 run log 一致。

9. 执行公式/符号/单位 review。

   检查：

   - 每个公式变量已定义；
   - 单位没有漂移；
   - 向量/矩阵维度足够清楚；
   - 下标、编号、公式引用一致；
   - 文本中的单位与表格/图一致。

10. 执行 CUMCM 风格 review。

   使用：

   ```text
   competitions/cumcm/winning_patterns.md
   competitions/cumcm/anti_patterns.md
   competitions/cumcm/distilled_structures.md
   competitions/cumcm/distilled_formats.md
   ```

   检查：

   - 结构是否像完整建模论文；
   - 问题分析是否引出模型；
   - 模型建立、求解、验证、灵敏度是否连贯；
   - 图表是否有信息密度；
   - 优缺点是否具体；
   - 快速评委阅读能否抓住贡献。

11. 执行匿名性 review。

   写入 `anonymity_report.md`：

   ```text
   checked artifacts
   personal identifiers
   school/team identifiers
   local path risks
   metadata risks
   source comment risks
   embedded file risks
   required user action
   anonymity verdict
   ```

   检查对象包括 paper、LaTeX source、PDF metadata、figures/tables、code comments、file paths、source directory。

12. 执行 traceability review。

   使用 `references/result_traceability.md` 检查：

   - paper claim -> source question -> source file -> source field -> validation status 是否完整；
   - 摘要数字是否允许进入摘要；
   - partial result 是否限制表达；
   - fail result 是否已从 claim 中移除；
   - figure/table claim 是否追踪到 final indexes；
   - final_results 与 traceability 是否一致。

13. 写 `review_report.md`。

   必须包含：

   ```text
   question coverage
   paper consistency
   abstract review
   figure and table review
   model/name/formula/unit review
   traceability review
   CUMCM style review
   L1 local critic findings
   L2 backtrack findings
   L3 panel findings
   L4 calibration findings
   anti-pattern hits
   required fixes
   fixed vs unresolved issues
   ```

14. 写 `quality_report.md`。

   使用 `references/quality_gate.md`，必须包含：

   ```text
   stage completeness
   modeling quality
   numerical quality
   validation quality
   writing quality
   CUMCM style quality
   traceability verdict
   anonymity verdict
   feedback-layer verdicts
   final verdict: PASS | PARTIAL | FAIL
   blocking issues
   limitations carried into paper
   next action if not PASS
   ```

15. 给出 final verdict。

   - `PASS`：无 unsupported hard numbers，无 validation-failed conclusion，traceability 完整，匿名风险清除，high issues 已修复；
   - `PARTIAL`：论文可用但存在明确限制，且限制已进入正文和报告；
   - `FAIL`：必答结论缺失、不可追踪、被验证反驳、匿名风险未清除，或 high issue 未解决。

## Output Contract

`review_report.md` 必须包含：

```text
question coverage
paper consistency
abstract review
figure and table issues
model and notation consistency
formula and unit consistency
traceability review
CUMCM style review
L1 local critic findings
L2 backtrack findings
L3 panel findings
L4 calibration findings
anti-pattern hits
required fixes
fixed vs unresolved issues
```

`anonymity_report.md` 必须包含：

```text
checked artifacts
identifier risks
metadata risks
local path risks
source/comment risks
required user action
anonymity verdict
```

`quality_report.md` 必须包含：

```text
stage completeness
modeling quality
numerical quality
validation quality
writing quality
CUMCM style quality
traceability verdict
anonymity verdict
feedback-layer verdicts
final verdict: PASS | PARTIAL | FAIL
blocking issues
```

## Quality Gate

Final `PASS` requires:

- no unsupported hard numbers in abstract or body；
- no validation-failed claim used as conclusion；
- partial claims are limited；
- every figure/table claim traces to a source；
- model names, formulas, variables, and units are consistent；
- CUMCM high anti-pattern hits are fixed；
- anonymity risks are cleared or explicitly reported as nonblocking；
- L1-L4 findings are resolved or carried into final verdict；
- quality_report final verdict matches actual evidence。

## Exit Conditions

- 所有 required final review reports 存在。
- `quality_report.md` 声明 final verdict 和 blocking issues。
- 任何剩余 unverified 或 untraceable claim 已移除、限制或明确报告。
- 用户能从 final reports 判断论文是否可交付。

## Failure Handling

- 匿名风险不能自动修复时，报告并请求用户 action。
- paper traceability fails 时，final verdict 标为 `PARTIAL` 或 `FAIL`，并列出 affected claims。
- feedback layers 发现 unresolved high issues 时，final verdict 标为 `PARTIAL` 或 `FAIL`。
- 评委视角无法快速识别贡献时，要求 revision abstract 或 final results。
- PDF/formal template failure 不应隐藏；写入 review_report 和 quality_report。

## Manual Mode Behavior

最终 checkpoint：列出 review report、anonymity report、quality report 和 paper artifact paths：

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf       # if exists
```

## AP Mode Behavior

与 Manual 一样输出最终报告路径。AP mode 不得压制 final review findings，不得把 unresolved high issue 包装为 `PASS`。
