# workspace 模板契约库

`templates/workspace/` 是 `workspace/output/` 的强约束模板库，不是可选示例。Agent 生成 workflow 输出时，必须按对应模板的字段、表格、来源和追溯要求填写。

## 固定输入

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

## 固定输出

```text
workspace/output/
workspace/output/q*/
workspace/output/final/
```

## 模板覆盖表

| Workflow output | Template or schema | Stage |
|---|---|---|
| `workspace/output/problem_audit.md` | `templates/workspace/root/problem_audit.md` | Stage 0 |
| `workspace/output/material_index.md` | `templates/workspace/root/material_index.md` | Stage 0 |
| `workspace/output/question_index.md` | `templates/workspace/root/question_index.md` | Stage 1 |
| `workspace/output/q*/analysis.md` | `templates/workspace/q/analysis.md` | Stage 2 |
| `workspace/output/q*/candidates.md` | `templates/workspace/q/candidates.md` | Stage 2 |
| `workspace/output/q*/model.md` | `templates/workspace/q/model.md` | Stage 2 |
| `workspace/output/q*/assumptions.md` | `templates/workspace/q/assumptions.md` | Stage 2 |
| `workspace/output/q*/notation.md` | `templates/workspace/q/notation.md` | Stage 2 |
| `workspace/output/q*/data_recon.md` | `templates/workspace/q/data_recon.md` | Stage 2 |
| `workspace/output/q*/warnings.md` | `templates/workspace/q/warnings.md` | Stage 2 |
| `workspace/output/q*/review_note.md` | `templates/workspace/q/review_note.md` | Stage 2 |
| `workspace/output/q*/code/` | `templates/workspace/q/code/README.md` | Stage 3 |
| `workspace/output/q*/results/result.json` | `templates/workspace/q/results/result.schema.json` | Stage 3 |
| `workspace/output/q*/results/run.log` | `templates/workspace/q/results/run.log` | Stage 3 |
| `workspace/output/q*/validation.md` | `templates/workspace/q/validation.md` | Stage 4 |
| `workspace/output/q*/sensitivity.md` | `templates/workspace/q/sensitivity.md` | Stage 4 |
| `workspace/output/q*/figures/figure_index.md` | `templates/workspace/q/figures/figure_index.md` | Stage 5 |
| `workspace/output/q*/tables/table_index.md` | `templates/workspace/q/tables/table_index.md` | Stage 5 |
| `workspace/output/q*/q*_summary.md` | `templates/workspace/q/q_summary.md` | Stage 6 |
| `workspace/output/final/final_results.md` | `templates/workspace/final/final_results.md` | Stage 7 |
| `workspace/output/final/final_figures_index.md` | `templates/workspace/final/final_figures_index.md` | Stage 7 |
| `workspace/output/final/final_tables_index.md` | `templates/workspace/final/final_tables_index.md` | Stage 7 |
| `workspace/output/final/traceability.md` | `templates/workspace/final/traceability.md` | Stage 7 |
| `workspace/output/final/paper.md` | `templates/workspace/final/paper.md` | Stage 8 |
| `workspace/output/final/paper.tex` | `templates/workspace/final/paper.tex` | Stage 8 |
| `workspace/output/final/paper.pdf` | Generated from `paper.tex`; record failures in Stage 9 reports | Stage 8 |
| `workspace/output/final/source/` | `templates/workspace/final/source/README.md` | Stage 8 |
| `workspace/output/final/review_report.md` | `templates/workspace/final/review_report.md` | Stage 9 |
| `workspace/output/final/anonymity_report.md` | `templates/workspace/final/anonymity_report.md` | Stage 9 |
| `workspace/output/final/quality_report.md` | `templates/workspace/final/quality_report.md` | Stage 9 |

## 填写规则

- 每个模板必须保留文件用途、对应 stage、必填字段、来源字段、可追溯要求和禁止空泛表达。
- 不知道的字段写 `待确认` 或 `不适用`，并说明原因；不要留空。
- 硬数字、图表、表格和论文结论必须能追溯到源文件和验证状态。
