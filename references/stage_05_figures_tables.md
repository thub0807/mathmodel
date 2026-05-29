# Stage 5: Figures and Tables

## Purpose

建立每个 `q*` 的图表索引，使每张图、每张表都服务明确论文 claim，并能追溯到数据、代码、结果字段、验证状态和论文位置。

图表不是“登记路径”的附件清单。每个 visual artifact 必须回答：它支撑哪个结论？来源是什么？验证状态如何？会进入论文哪个小节？

## Required Inputs

```text
workspace/output/q*/review_packet.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/code/
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
competitions/cumcm/distilled_formats.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
references/rubrics.md
references/feedback_layer1_critic.md
```

默认按 CUMCM 论文风格组织图表；不得引入其他竞赛的图表格式要求作为 active 默认。

## Required Outputs

```text
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/figures/
workspace/output/q*/tables/
workspace/output/q*/warnings.md        # if visual limitations appear
workspace/output/q*/review_note.md     # if L1 finds visual issues
```

## Output Contract

`figures/figure_index.md` 和 `tables/table_index.md` 必须记录 artifact path、source file、source field、source command、linked claim、validation status、paper section、include in paper、caption note 和 limitation。

实际图表文件必须保存在对应 `figures/` 或 `tables/` 目录，不能只在索引中写占位路径。

## Entry Conditions

- Stage 4 已产生 `validation.md` 和 `sensitivity.md`，或已记录验证缺失/失败限制。
- `result.json`、代码输出或源材料中存在可支撑图表的数据。
- 当前 `q*` 的 paper-facing claims 已在 summary 前具备初步方向。
- 任何 visual 都能被绑定到 `q*`、source file 和 source field；否则不得进入论文。

## Procedure

1. 先决定图表的论文作用。

   每个图表必须至少服务一种作用：

   - 支撑核心结果 claim；
   - 解释模型结构、变量关系或算法流程；
   - 诊断结果可信度；
   - 展示灵敏度、鲁棒性或失稳边界；
   - 汇总最终答案。

   仅装饰、重复正文数字、无法解释的图表应排除。

2. 分类每张图。

   在 `figure_index.md` 中使用以下类别：

   ```text
   data figure
   diagnostic figure
   conceptual figure
   final paper figure
   ```

   分类规则：

   - `data figure`：来自源数据、预处理数据或 `result.json` 字段，用于展示数据分布、趋势、空间关系、输入结构；
   - `diagnostic figure`：用于验证拟合、残差、收敛、约束残差、baseline 对比、敏感性或鲁棒性；
   - `conceptual figure`：解释模型结构、流程、依赖图、机制，必须明确标注 conceptual，不得伪装为数据证据；
   - `final paper figure`：计划进入最终论文的正式图，可由 data、diagnostic 或 conceptual 图提升而来。

3. 分类每张表。

   在 `table_index.md` 中标注：

   - input data table；
   - parameter table；
   - result table；
   - validation table；
   - sensitivity table；
   - final answer table。

   表格应服务比较、结果汇总、参数说明、验证或灵敏度，不要把原始数据整表倾倒进论文。

4. 绑定 source 和 claim。

   每张图表必须记录：

   ```text
   visual id
   type
   q*
   source file
   source field
   generation code or manual source
   supported claim
   claim type
   validation status
   result status
   paper section
   body citation location
   include in paper: yes | no
   limitation note
   ```

   source field 优先指向：

   ```text
   workspace/output/q*/results/result.json
   workspace/output/q*/validation.md
   workspace/output/q*/sensitivity.md
   workspace/output/q*/code/
   workspace/problem/attachments/
   workspace/problem/images/
   ```

5. 根据 validation status 决定图表表达强度。

   - `PASS`：可支撑正式 claim；
   - `PARTIAL`：图表可进入正文，但 caption 和正文必须写限制；
   - `FAIL`：不得作为论文 claim，只能在必要时作为失败诊断或附加说明，并标明不可用于结论。

6. 使用 CUMCM 图题、表题和注释格式。

   参考 `competitions/cumcm/distilled_formats.md`：

   - 图题和表题应简洁说明变量、对象、范围或结论；
   - 表注说明单位、数据来源、缩写和限制；
   - 图注说明读者应观察的趋势或比较；
   - 编号、引用、公式/图/表格式保持一致；
   - caption 不写空泛“结果图”“分析表”。

7. 参考 CUMCM 高质量图表模式。

   使用 `competitions/cumcm/winning_patterns.md` 检查：

   - 图表是否揭示模型结构、结果比较、敏感性或答案逻辑；
   - 是否有清楚的单位、标签、图例和解释；
   - 是否能帮助评委快速找到答案；
   - 是否比文字重复更有信息密度。

8. 检查反模式。

   使用 `competitions/cumcm/anti_patterns.md` 标记：

   - 无 source 的图表；
   - 默认样式且无解释；
   - 坐标、单位、图例缺失；
   - caption 支撑了图表不能支撑的 claim；
   - 图表编号和正文引用不一致；
   - 用 failed/partial 结果当作强结论；
   - conceptual figure 伪装成数据证据。

9. 生成或记录图表。

   - 若图表已经生成，记录路径、代码、source field；
   - 若图表尚未生成，但 Stage 8 需要，记录 intended visual 和生成计划；
   - 若无法生成，记录原因和论文影响；
   - 不可追踪图表必须标记 `include in paper: no`。

10. 运行 Layer 1 图表检查。

   使用 `references/feedback_layer1_critic.md` 检查：

   - 图表是否有 claim；
   - claim 是否可追踪；
   - validation status 是否正确；
   - caption 是否诚实；
   - partial/fail 限制是否可见。

## Output Contract

`figure_index.md` 和 `table_index.md` 必须记录：

```text
visual id
type: data figure / diagnostic figure / conceptual figure / final paper figure
q*
title or caption
supported claim
source file
source field
generation code or manual source
validation status
result status
intended paper section
body citation location
limitations or notes
include in paper: yes / no
```

每个进入 `tables/` 的表必须包含：

```text
source
column meaning
units
supported conclusion
validation status
limitation note
```

## Quality Gate

进入 Stage 6 前：

- 每个 included visual 都绑定 claim、source file、source field、`q*`、paper section 和 validation status；
- 每个 data figure/table 能追溯到结果、验证、灵敏度、源材料或代码输出；
- 每个 diagnostic visual 说明它回答哪个可靠性问题；
- 每个 conceptual figure 明确标注 conceptual；
- partial/fail 结果对应图表已降级表达；
- 图题、表题、注释符合 CUMCM 格式倾向；
- 触发反模式的图表已修复或排除；
- 没有不可追踪图表进入论文候选。

## Exit Conditions

- 每个图表都有 source path、source field、supported claim、intended paper use 和 validation status。
- 被拒绝或无法生成的图表被记录，而不是静默遗漏。
- Stage 6 可直接引用 include in paper 的图表，并把限制写入 `q*_summary.md`。

## Failure Handling

- source 不清的图表不得进入最终论文。
- 图表缺失影响解释时，写入 `warnings.md` 或 `review_note.md`。
- 如果图表支撑的 claim 后续变为 `PARTIAL` 或 `FAIL`，更新索引并把限制传递到 Stage 6-9。
- 如果 caption 或正文引用夸大图表证据，触发 Layer 2 backtrack 或 Stage 9 final review 修正。

## Manual Mode Behavior

通常继续。若图表选择会改变科学结论、结果表达强度或最终摘要可用性，则暂停并列出：

```text
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/warnings.md
```

## AP Mode Behavior

继续使用 source-backed visuals。所有 visual limitations 必须进入后续 `q*_summary.md`、`traceability.md`、`review_report.md` 或 `quality_report.md`。
