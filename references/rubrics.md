# 新版质量 Rubrics

本文件服务 `mathmodel-copilot` 的 Markdown-first 单题工作流。评分或评审结果不写入旧状态机，统一汇总到：

```text
workspace/output/final/quality_report.md
```

必要时同步写入：

```text
workspace/output/final/review_report.md
workspace/output/q*/warnings.md
```

## 总体原则

- 评分只辅助审查，不作为隐藏状态。
- 所有证据必须指向 `workspace/output/` 下的文件。
- 硬数字必须能追溯到 `result.json`、`validation.md` 或 `sensitivity.md`。
- `partial` 和 `fail` 必须在最终报告中标注限制。

## 质量维度

| 维度 | 满分标准 | 主要证据 |
|---|---|---|
| 工作区材料完整性 | 必需文件存在，材料疑点和缺失路径已记录 | `problem_audit.md`, `material_index.md` |
| 问题拆分完整性 | 每个子问题有输入、输出、依赖和附件映射 | `question_index.md` |
| 每问 Plan 完整性 | analysis / candidates / model / assumptions / notation / data_recon 齐全 | `workspace/output/q*/` |
| 模型与题意匹配 | 模型目标、变量和约束对应题面任务 | `model.md`, `analysis.md` |
| 假设与符号质量 | 假设有依据，符号有含义、单位、类型和来源 | `assumptions.md`, `notation.md` |
| 结果门禁 | `result.json.status` 合法，硬数字来源清楚 | `result.json` |
| 验证充分性 | 覆盖约束、边界、稳定性、baseline、对比和失败情形 | `validation.md` |
| 灵敏度充分性 | 覆盖敏感参数、扰动范围、结果变化和结论影响 | `sensitivity.md` |
| 图表可信度 | 图表有来源、用途和对应结论，无伪造数据图 | `figure_index.md`, `table_index.md` |
| 追溯完整性 | 结论、硬数字、图表、假设和符号可追踪 | `traceability.md` |
| 论文模板合规性 | 默认中文 CUMCM 风格，结构完整，未引入未验证结果 | `paper.md`, `paper.tex` |
| 匿名风险 | 队伍、学校、姓名、联系方式、路径用户名和 PDF 元数据已检查 | `anonymity_report.md` |
| 反模式检查 | 空泛假设、伪图表、过度包装、未验证结论已排查 | `quality_report.md` |

## 建议等级

| 结论 | 建议标准 |
|---|---|
| PASS | 关键文件齐全，硬数字可追溯，验证与灵敏度支持论文结论 |
| PARTIAL | 主要流程完成，但存在材料缺口、验证不足或部分结果限制 |
| FAIL | 缺少关键结果、验证失败、硬数字不可追溯或论文结论不可信 |

## `quality_report.md` 建议结构

```markdown
# Quality Report

## 总体结论

## 工作区与材料

## 子问题完整性

| 问题 | Plan | Build | Verification | Figures/Tables | Summary | result.json.status |
|---|---|---|---|---|---|---|

## 证据链与硬数字

## 验证与灵敏度

## 图表引用与来源

## 论文模板合规性

## 匿名检查摘要

## 反模式检查

## 遗留风险
```

## 禁止事项

- 不写入旧状态文件。
- 不要求运行旧评分脚本。
- 不把脚本输出作为唯一质量来源。
- 不使用隐藏 JSON 状态替代 `quality_report.md`。
