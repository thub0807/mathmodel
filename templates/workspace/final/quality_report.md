# Quality Report 模板

## 文件用途

完成 Stage 9 最终质量门禁，记录 workflow 完整性、结果状态、验证状态、图表引用、论文追溯、匿名检查和最终结论。

## 对应 stage

Stage 9 Final Review

## 必填字段

| 字段 | 填写规则 |
|---|---|
| stage completeness | 检查 Stage 0-9 输出是否存在 |
| result status | 汇总每个 `result.json.status` |
| validation status | 汇总每个 `validation.md` 结论 |
| sensitivity status | 汇总每个 `sensitivity.md` 结论 |
| figure/table citation | 检查论文图表引用是否有索引和来源 |
| paper traceability | 检查论文 claim 是否出现在 `traceability.md` |
| anonymity | 引用 `anonymity_report.md` 结论 |
| final verdict | 只能为 `PASS`、`PARTIAL` 或 `FAIL` |

## 来源字段

`problem_audit.md`、`question_index.md`、`q*/results/result.json`、`q*/validation.md`、`q*/sensitivity.md`、`final/traceability.md`、`paper.md`、`paper.tex`、`anonymity_report.md`。

## 可追溯要求

每个质量问题必须指向具体文件和影响范围。

## 禁止空泛表达

不要写“整体较好”。必须给出检查项、状态、证据文件和处理建议。

## Stage Completeness

| stage | required output | status | evidence file | issue |
|---|---|---|---|---|
| `<Stage 0-9>` | `<output>` | `<complete/partial/missing>` | `<path>` | `<issue or none>` |

## Result Status

| question | result status | model name | evidence file | limitation |
|---|---|---|---|---|
| `<q*>` | `<pass/partial/fail>` | `<model>` | `<result.json path>` | `<note or none>` |

## Validation And Sensitivity Status

| question | validation status | sensitivity status | evidence files | limitation |
|---|---|---|---|---|
| `<q*>` | `<pass/partial/fail>` | `<stable/limited/unstable>` | `<paths>` | `<note or none>` |

## Figure And Table Citation

| item | cited in paper | index file | source file | status | issue |
|---|---|---|---|---|---|
| `<figure/table>` | `<yes/no>` | `<path>` | `<path>` | `<pass/partial/fail>` | `<issue or none>` |

## Paper Traceability

| paper claim | in traceability.md | validation status | allowed in abstract | issue |
|---|---|---|---|---|
| `<claim>` | `<yes/no>` | `<pass/partial/fail>` | `<yes/no>` | `<issue or none>` |

## Anonymity

| check item | status | evidence file | issue |
|---|---|---|---|
| `<personal/school/team/path/metadata>` | `<pass/partial/fail>` | `<path>` | `<issue or none>` |

## Final Verdict

`PASS / PARTIAL / FAIL`：`<reason>`

## Required Fixes

| priority | file | issue | required action |
|---|---|---|---|
| `<high/medium/low>` | `<path>` | `<issue>` | `<action>` |
