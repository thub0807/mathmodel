# Final Figures Index 模板

## 文件用途

整合所有可用于论文的图，并记录每张图的数据来源、生成代码、验证状态和论文用途。

## 对应 stage

Stage 7 Final Integration

## 必填字段

| 字段 | 填写规则 |
|---|---|
| figure id | 使用稳定编号 |
| source question | 指向 `q*` |
| figure path | 指向图文件 |
| data source | 指向 `result.json`、附件或中间数据 |
| code source | 指向生成代码；概念图写 `conceptual` |
| validation status | 写 `pass`、`partial`、`fail` |
| paper use | 写正文、附录或不使用 |

## 来源字段

`q*/figures/figure_index.md`、`q*/results/result.json`、`q*/validation.md`、生成代码。

## 可追溯要求

数据图必须追溯到数据和代码；概念图必须说明其解释对象。

## 禁止空泛表达

不要写“用于展示结果”。必须说明展示哪个结论。

## 模板正文

| figure id | source question | figure path | data source | code source | validation status | paper use | related claim |
|---|---|---|---|---|---|---|---|
| `<Fig-1>` | `<q*>` | `<path>` | `<path/conceptual>` | `<path/conceptual>` | `<pass/partial/fail>` | `<body/appendix/exclude>` | `<claim>` |
