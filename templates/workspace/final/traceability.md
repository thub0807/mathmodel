# Traceability 模板

## 文件用途

追踪最终论文中的 claim、硬数字、图表、表格、假设和符号来源。

## 对应 stage

Stage 7 Final Integration

## 必填字段

| 字段 | 填写规则 |
|---|---|
| paper claim | 写论文中将出现的结论、数字或图表主张 |
| source question | 写 `q1`、`q2` 等来源问题 |
| source file | 写可审计来源路径 |
| source field | 写 `result.json` 字段、表格列名或 Markdown 小节 |
| validation status | 写 `pass`、`partial`、`fail` 或验证结论 |
| allowed in abstract | 只能写 `yes` 或 `no` |
| limitation note | 写限制；无则写 `none` |

## 来源字段

`result.json`、`validation.md`、`sensitivity.md`、`q*_summary.md`、`final_results.md`、图表索引和表格索引。

## 可追溯要求

论文摘要、正文、图表标题和结论中的硬数字必须在本表中有记录。

## 禁止空泛表达

不要写“来源见前文”。必须写具体文件和字段。

## Paper Claim Trace Table

| paper claim | source question | source file | source field | validation status | allowed in abstract | limitation note |
|---|---|---|---|---|---|---|
| `<claim>` | `<q*>` | `<path>` | `<field or section>` | `<pass/partial/fail>` | `<yes/no>` | `<note or none>` |

## Figure Trace Table

| figure id | paper claim | source question | source file | source field | validation status | allowed in abstract | limitation note |
|---|---|---|---|---|---|---|---|
| `<Figure 1>` | `<claim>` | `<q*>` | `<figure path or index>` | `<field>` | `<pass/partial/fail>` | `<yes/no>` | `<note or none>` |

## Table Trace Table

| table id | paper claim | source question | source file | source field | validation status | allowed in abstract | limitation note |
|---|---|---|---|---|---|---|---|
| `<Table 1>` | `<claim>` | `<q*>` | `<table path or index>` | `<field>` | `<pass/partial/fail>` | `<yes/no>` | `<note or none>` |

## Assumption and Notation Trace

| item | type | source question | source file | source field | paper use | limitation note |
|---|---|---|---|---|---|---|
| `<assumption or symbol>` | `<assumption/notation>` | `<q*>` | `<path>` | `<field>` | `<where used>` | `<note or none>` |
