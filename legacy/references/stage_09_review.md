---
stage: 9
name: final_review
inputs: [workspace/output/final/paper.md, workspace/output/final/paper.tex, workspace/output/final/paper.pdf, workspace/output/final/traceability.md, workspace/output/q*/results/result.json]
outputs: [workspace/output/final/review_report.md, workspace/output/final/anonymity_report.md, workspace/output/final/quality_report.md]
loads_reference: [references/final_review_protocol.md, competitions/cumcm/anti_patterns.md]
next: done
---

# Stage 9：Final Review

## 目标

对最终论文、证据链、匿名性和质量进行终稿审查，形成可审查的最终报告。

## 输入

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/traceability.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/
workspace/output/q*/tables/
```

## 输出

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

## `review_report.md` 检查

- 是否回答所有子问题。
- 是否存在材料缺口。
- 是否存在未解决的 `problem.md` / `reference.pdf` 疑问。
- 每问是否有 Plan、Build、Verification、Figures/Tables、Summary。
- 每问是否有 `result.json`。
- `partial` / `fail` 是否标记。
- 图表是否被正文引用。
- 论文是否引入未验证结果。
- `paper.pdf` 是否生成成功。

## `anonymity_report.md` 检查

- 队伍、学校、姓名、联系方式。
- 路径用户名。
- PDF 元数据。
- 其他匿名风险。

## `quality_report.md` 记录

- 每个 `q*` 的完整性检查。
- 每个 `q*` 的 `result.json.status`。
- 每个 `q*` 的 validation / sensitivity 状态。
- 全局符号一致性。
- 全局单位一致性。
- 图表引用完整性。
- 论文模板合规性。
- 反模式检查。
- 匿名检查摘要。
- 最终质量结论。

## 退出条件

- 三个终审报告均已生成。
- 所有 `partial` / `fail` 已明确标注。
- 所有硬数字均可追溯。
- 匿名风险已记录。
- 最终质量结论已写入 `quality_report.md`。
