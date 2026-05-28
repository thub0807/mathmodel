# 图表协议

每个 `q*` 必须生成：

```text
workspace/output/q*/figures/
workspace/output/q*/tables/
```

建议结构：

```text
figures/
├── figure_index.md
├── fig_1_source.py
├── fig_1.png
└── fig_1_check.md

tables/
├── table_index.md
├── table_1.csv
└── table_1.md
```

## 规则

- 数据图必须来自代码、附件数据、`result.json`、`validation.md` 或 `sensitivity.md`。
- 概念图允许存在，但必须标记为 `conceptual`。
- 每张图表必须说明来源、用途和对应结论。
- 不能伪造数据图。
- 进入论文的图表必须在 `final_figures_index.md` 和 `final_tables_index.md` 中再次登记。
