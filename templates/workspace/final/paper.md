# Paper Markdown 模板

## 文件用途

生成 `workspace/output/final/paper.md`，作为论文正文的 Markdown 中间稿结构契约。

本文件只规定中间稿字段和追溯要求，不提供 CUMCM 写作方法。写作质量、摘要结构、句式、反模式和格式经验应参考 `competitions/cumcm/`。

正式 LaTeX 排版不由本文件承担，应优先使用 `templates/latex/cumcm/cumcmthesis/`。

## 对应 stage

Stage 8 Paper Generation

## 必填字段

| 字段 | 填写规则 |
|---|---|
| 标题 | 简洁描述模型主题 |
| 摘要 | 只使用 `traceability.md` 允许进入摘要的 claim |
| 关键词 | 3-5 个模型或方法关键词 |
| 问题重述 | 基于 `problem.md` 和 `problem_audit.md` |
| 模型假设 | 引用各 `assumptions.md` |
| 符号说明 | 引用各 `notation.md` |
| 模型建立与求解 | 来自 `q*_summary.md` |
| 结果分析 | 来自 `final_results.md` 和 validated artifacts |
| 灵敏度与验证 | 来自 `validation.md` 和 `sensitivity.md` |
| 优缺点与改进 | 必须具体对应模型限制 |
| 参考与附录 | 列出 source 与代码说明 |

## 来源字段

`q*_summary.md`、`final_results.md`、`traceability.md`、`final_figures_index.md`、`final_tables_index.md`。

## 可追溯要求

正文中的硬数字、图表、表格和摘要结论必须出现在 `traceability.md`。

## 禁止空泛表达

不要写不可验证的泛泛评价，如“模型具有较高准确性”。必须给出来源和验证状态。

## 模板正文

# `<论文标题>`

## 摘要

`<仅写 allowed in abstract = yes 的结论。>`

## 关键词

`<关键词1>`；`<关键词2>`；`<关键词3>`

## 1 问题重述

`<基于 problem.md 的重述。>`

## 2 模型假设

`<引用 assumptions.md。>`

## 3 符号说明

`<引用 notation.md。>`

## 4 模型建立与求解

`<按 q* 写论文正文。>`

## 5 结果分析

`<引用 final_results.md 和 traceability.md。>`

## 6 验证与灵敏度分析

`<引用 validation.md 和 sensitivity.md。>`

## 7 模型评价与改进

`<具体优点、限制和改进。>`

## 参考文献

`<参考文献或资料来源。>`

## 附录

`<代码、数据和 source 说明。>`
