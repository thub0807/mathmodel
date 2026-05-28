# Review Report 模板

## 文件用途

检查最终论文是否回答所有子问题，并记录材料缺口、未验证结果、`partial` / `fail` 限制和 PDF 生成状态。

## 对应 stage

Stage 9 Final Review

## 必填字段

| 字段 | 填写规则 |
|---|---|
| question coverage | 每个 `q*` 是否回答 |
| artifact completeness | Plan、Build、Verification、Summary 是否齐全 |
| material gap | 指向 `problem_audit.md` 或 `material_index.md` |
| partial/fail labeling | 检查限制是否进入论文和 traceability |
| unverified result check | 检查论文 claim 是否有验证来源 |
| paper generation status | 记录 `paper.md`、`paper.tex`、`paper.pdf` 状态 |

## 来源字段

`question_index.md`、`q*/q*_summary.md`、`final/paper.md`、`final/traceability.md`、`final/final_results.md`。

## 可追溯要求

每个 review finding 必须指向具体文件路径。

## 禁止空泛表达

不要写“论文基本完整”。必须列出每个子问题和关键缺口。

## Question Coverage

| question | answer status | source summary | paper section | limitation |
|---|---|---|---|---|
| `<q*>` | `<answered/partial/missing>` | `<path>` | `<section>` | `<note>` |

## Artifact Completeness

| question | Plan | Build | Verification | Figures/Tables | Summary | limitation |
|---|---|---|---|---|---|---|
| `<q*>` | `<ok/missing>` | `<ok/missing>` | `<ok/missing>` | `<ok/missing>` | `<ok/missing>` | `<note>` |

## Material Gaps

| gap | source file | paper impact | action |
|---|---|---|---|
| `<gap>` | `<path>` | `<impact>` | `<action>` |

## Paper Generation Status

| artifact | status | path or failure note |
|---|---|---|
| `paper.md` | `<status>` | `<path/note>` |
| `paper.tex` | `<status>` | `<path/note>` |
| `paper.pdf` | `<status>` | `<path/note>` |
