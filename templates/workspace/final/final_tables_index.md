# Final Tables Index 模板

## 文件用途

整合所有可用于论文的表，并记录表格来源、字段、验证状态和论文用途。

## 对应 stage

Stage 7 Final Integration

## 必填字段

| 字段 | 填写规则 |
|---|---|
| table id | 使用稳定编号 |
| source question | 指向 `q*` |
| table path | 指向表文件或表格索引 |
| source field | 指向 `result.json` 字段、数据列或 summary 小节 |
| validation status | 写 `pass`、`partial`、`fail` |
| paper use | 写正文、附录或不使用 |

## 来源字段

`q*/tables/table_index.md`、`q*/results/result.json`、`q*/validation.md`、表格生成代码。

## 可追溯要求

表格中的硬数字必须追溯到 `result.json` 或已验证的数据源。

## 禁止空泛表达

不要写“汇总数据”。必须说明字段来源和对应结论。

## 模板正文

| table id | source question | table path | source field | validation status | paper use | related claim |
|---|---|---|---|---|---|---|
| `<Tab-1>` | `<q*>` | `<path>` | `<field>` | `<pass/partial/fail>` | `<body/appendix/exclude>` | `<claim>` |
