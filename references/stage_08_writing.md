---
stage: 8
name: paper_generation_with_template
inputs: [workspace/output/q*/q*_summary.md, workspace/output/final/final_results.md, workspace/output/final/traceability.md]
outputs: [workspace/output/final/paper.md, workspace/output/final/paper.tex, workspace/output/final/paper.pdf, workspace/output/final/source]
loads_reference: [references/paper_generation_protocol.md, competitions/cumcm/paper_skeleton.md, competitions/cumcm/abstract_template.md, competitions/cumcm/phrase_bank.md, competitions/cumcm/anti_patterns.md, competitions/cumcm/winning_patterns.md]
next: stage_09_review
---

# Stage 8：Paper Generation with Template

## 目标

基于每问总结、最终结果和证据链，生成默认中文 CUMCM 风格论文。

## 输入

```text
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

## 输出

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

## 默认模板与参考

优先使用：

```text
templates/latex/cumcm/
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/phrase_bank.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/winning_patterns.md
```

用户明确指定 MCM 时，才使用英文 Summary / Paper。

## 写作规则

- 论文必须基于 `q*/q*_summary.md`、`final_results.md` 和 `traceability.md`。
- 不得引入未验证的新结果。
- 摘要、结论和表格中的硬数字必须来自 `result.json`、`validation.md` 或 `sensitivity.md`。
- 必须使用 `anti_patterns.md` 做反向检查。
- 图表必须来自最终图表索引。
- `partial` 结果只能有限进入正文，不能作为摘要强结论数字。
- `fail` 结果不得作为论文结论依据。
- 不主动询问题号、队员、学校、联系方式或 deadline。
- 如果 LaTeX 模板需要正式提交字段，默认使用安全占位符或跳过正式提交封面。
- 不得为了填模板字段而打断建模流程。
- 只输出论文工作产物到 `workspace/output/final/`，不生成提交包。

## 建议论文结构

```markdown
# 题目

## 摘要

## 1 问题重述

## 2 问题分析

## 3 模型假设

## 4 符号说明

## 5 模型建立与求解

## 6 模型检验与灵敏度分析

## 7 模型评价与推广

## 参考文献

## 附录
```

## 退出条件

- `paper.md` 已生成。
- `paper.tex` 已生成。
- 若环境支持，`paper.pdf` 已生成；若失败，失败原因已记录。
- 论文所有硬数字可追溯。
- 论文未引入未验证结果。
