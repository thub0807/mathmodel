# Final Results 模板

## 文件用途

汇总所有可进入论文的最终结果，并标注每条结果的来源、状态和限制。

## 对应 stage

Stage 7 Final Integration

## 必填字段

| 字段 | 填写规则 |
|---|---|
| result id | 给每条最终结果稳定编号 |
| source question | 指向 `q*` |
| source files | 指向 `result.json`、`validation.md`、`sensitivity.md` 或 summary |
| result status | 写 `pass`、`partial`、`fail` |
| paper use | 写摘要、正文、附录或不使用 |
| limitation | 写限制；无则写 `none` |

## 来源字段

`q*/q*_summary.md`、`q*/results/result.json`、`q*/validation.md`、`q*/sensitivity.md`。

## 可追溯要求

每条最终结果必须能进入 `traceability.md` 的 paper claim trace 表。

## 禁止空泛表达

不要写“结果较好”。必须给出结果内容、来源文件和状态。

## 模板正文

| result id | result statement | source question | source files | result status | paper use | limitation |
|---|---|---|---|---|---|---|
| `<R1>` | `<result>` | `<q*>` | `<paths>` | `<pass/partial/fail>` | `<abstract/body/appendix/exclude>` | `<note or none>` |
