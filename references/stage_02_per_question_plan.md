# Stage 2: Per-Question Plan

## Purpose

为当前 `q*` 建立可审阅、可实现、可验证的建模方案。v1.2 起，本阶段只为“当前问题”工作，不批量规划所有问题；所有 Plan 内容汇总到一个审查入口：

```text
workspace/output/q*/review_packet.md
```

不得把 `analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 作为 v1.2 必需审查入口。分析、候选模型、模型规格、假设、符号和数据重构内容必须合并到 `review_packet.md`。

## Required Inputs

```text
workspace/problem/problem.md
workspace/output/question_index.md
workspace/output/problem_audit.md
workspace/output/material_index.md
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
```

若当前问题依赖上游问题，必须同时读取已完成上游产物：

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
```

## Required Outputs

```text
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode, rework, or risk notes
```

## Output Contract

`review_packet.md` 是唯一 Plan 审查入口。`warnings.md` 只记录会影响 Build、验证或论文 claim 的风险。`review_note.md` 记录 AP 自动推进说明、Manual 返工说明和审查材料位置。

## Entry Conditions

- Stage 1 has produced `workspace/output/question_index.md`。
- 上一个 `q*` 已完成 Stage 6 Summary，或当前是 `q1`。
- 当前 `q*` 的 inputs、outputs、dependencies 和 materials 已在 `question_index.md` 中定义。
- 题意歧义若会影响模型选择，已在 `problem_audit.md` 中解决或标记默认处理。

## Procedure

1. 直接重读 `problem.md` 中与当前 `q*` 有关的题意，不用脚本语义解析题面，不用 regex 检测问题。
2. 在 `review_packet.md` 写 question card：来源、目标、输入、输出、约束、评价指标、上游依赖、下游交付接口。
3. 若有上游依赖，写 upstream context：读取了哪些上游文件、采用了哪些结果、上游 `partial` / `fail` 如何影响当前问题。
4. 生成候选模型比较：至少包含 baseline、main model、robust alternative；若不足 3 个，写明原因和补强验证方式。
5. 选择最终模型路线：说明模型名、模型族、适配题意、数据可得性、Python 可实现性、可验证性、论文表达方式和 fallback。
6. 写模型规格：变量、参数、单位、定义域、目标函数或评价指标、约束、算法步骤、预期 `result.json` 字段。
7. 写假设和符号：只保留会被模型、代码、验证或论文使用的内容；每条假设必须有来源、风险和验证/灵敏度 hook。
8. 写数据重构计划：材料路径、字段、预处理、缺失值、异常值、单位转换、派生变量、输出中间文件。
9. 写 toy demo / 最小可行性检查：输入、预期输出、成功信号、失败信号、失败后是否阻塞 Build。
10. 写 red-team 风险回应：数学风险、数据风险、计算风险、论文审查风险、fallback 或降级策略。
11. 运行 Layer 1 Plan critic，并把 high issue 写入 `warnings.md` 或 `review_note.md`。
12. 写 Build entry checklist：只有 checklist 明确通过或风险被 Manual 接受 / AP 降级记录后，才能进入 Stage 3。

## Output Contract

`review_packet.md` 必须包含以下章节：

```text
question card
upstream context
candidate model matrix
selected route
model specification
assumptions and notation
data reconstruction plan
toy demo plan
validation and sensitivity plan
red-team notes
build entry checklist
review material paths
```

Manual mode：完成 `review_packet.md` 后必须暂停，只返回审查材料路径，不进入 Stage 3。

AP mode：不暂停，但必须写 `review_note.md`，说明自动采用当前路线的理由、被拒候选、保留风险和后续验证方式。

## Quality Gate

进入 Stage 3 前：

- 当前 `q*` 的上游依赖已读取并记录；
- 候选比较具体，不是泛泛列模型名；
- 所选模型匹配题意、数据、约束和论文表达；
- 公式、变量、约束明确到可实现；
- 假设与来源、风险、验证 hook 相连；
- 数据计划说明预处理、缺失、异常和派生变量；
- toy demo 能检验最小可行性；
- red-team high risk 已回应；
- `review_packet.md` 已生成；
- Manual mode 已暂停并等待用户同意 Build。

## Failure Handling

- 如果无法选择模型路线，写出竞争选项和风险，Manual mode 暂停。
- 如果数据或材料不足，写 `warnings.md`，不得隐藏限制。
- 如果上游结果为 `partial` 或 `fail`，当前问题必须降级、fallback 或暂停确认。
- 如果模型命名只能靠夸张词汇支撑，重写为机制性命名。
- 如果 Plan 无法支撑 CUMCM 表达，补充模型解释、验证计划或图表计划。
