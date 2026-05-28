# workspace 模板契约库

`templates/workspace/` 是 `workspace/output/` 的输出文件契约库，不是可选示例。

本目录只定义 workspace 输出文件的字段契约、追溯字段、必填项和结构。Agent 生成 workflow 输出时，必须按对应模板的字段、表格、来源和追溯要求填写。

本目录不承担以下职责：

- 建模方法库：建模方法来自 `references/model_catalog.md`、stage references 和 feedback layers。
- 竞赛写作知识库：CUMCM 写作质量来自 `competitions/cumcm/`。
- 正式 LaTeX 模板库：CUMCM 正式排版来自 `templates/latex/cumcm/cumcmthesis/`。

`templates/workspace/final/paper.md` 是 Markdown 中间稿结构契约。

`templates/workspace/final/paper.tex` 只是 fallback scaffold，不是 CUMCM 竞赛正式模板。

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
| `workspace/output/q*/results/run.log` | `templates/workspace/q/results/run_log.md` | Stage 3 |
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

## run log 命名规则

模板文件使用 Markdown 名称：

```text
templates/workspace/q/results/run_log.md
```

实际产物文件仍写为：

```text
workspace/output/q*/results/run.log
```

也就是说，`run_log.md` 定义字段契约，`run.log` 是运行时输出文件名。

## 纸面稿与正式模板边界

`templates/workspace/final/paper.md` 只规定 Markdown 中间稿需要哪些字段和追溯信息。论文写作策略、摘要结构、句式、反模式和格式经验应读取：

```text
competitions/cumcm/
```

`templates/workspace/final/paper.tex` 只在正式模板不可用时提供 fallback scaffold。CUMCM 正式排版优先使用：

```text
templates/latex/cumcm/cumcmthesis/
```
