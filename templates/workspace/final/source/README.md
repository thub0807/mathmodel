# Final Source Directory 模板

## 文件用途

说明 `workspace/output/final/source/` 中论文生成使用的源文件、图片、表格、LaTeX 资源和复制资产。

## 对应 stage

Stage 8 Paper Generation

## 必填字段

| 字段 | 填写规则 |
|---|---|
| source item | 列出文件或目录 |
| origin path | 写原始来源路径 |
| paper use | 写在论文中如何使用 |
| traceability row | 指向 `traceability.md` 对应行或 claim |
| status | 写 `included`、`excluded`、`failed` |

## 来源字段

`paper.md`、`paper.tex`、`traceability.md`、图表索引、表格索引。

## 可追溯要求

复制到 `source/` 的每个数据图、表格或辅助文件必须能追溯到原始路径。

## 禁止空泛表达

不要写“相关源文件”。必须逐项列出路径和用途。

## 模板正文

| source item | origin path | paper use | traceability row | status |
|---|---|---|---|---|
| `<path>` | `<origin>` | `<use>` | `<claim or row id>` | `<included/excluded/failed>` |
