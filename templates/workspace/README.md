# workspace 模板契约库

`templates/workspace/` 是 `workspace/output/` 的 artifact contract，不是示例库，也不是建模方法库。

它属于当前三层架构中的 CUMCM competition and output layer，负责定义每个输出文件的字段、来源、追溯信息、必填项和结构。

## 职责边界

`templates/workspace/` 负责：

- 规定 `workspace/output/` 下各产物的结构；
- 规定 result、traceability、review、quality report 的字段；
- 规定 Markdown 中间稿和 fallback scaffold 的文件契约；
- 帮助 Agent 保持产物一致、可审计、可追踪。

`templates/workspace/` 不负责：

- 建模方法：读取 `references/model_catalog.md` 和 stage references；
- 质量判断：读取 `references/rubrics.md`、feedback layers、`quality_gate.md`；
- CUMCM 写作经验：读取 `competitions/cumcm/`；
- 正式 LaTeX 排版：读取 `templates/latex/cumcm/cumcmthesis/`；
- 历史迁移材料：不读取 `legacy/`。

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
| `workspace/output/q*/solution_plan.md` | `templates/workspace/q/solution_plan.md` | Stage 2 |
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
| `workspace/output/final/paper.tex` | `templates/workspace/final/paper.tex` fallback scaffold | Stage 8 |
| `workspace/output/final/source/` | `templates/workspace/final/source/README.md` | Stage 8 |
| `workspace/output/final/review_report.md` | `templates/workspace/final/review_report.md` | Stage 9 |
| `workspace/output/final/anonymity_report.md` | `templates/workspace/final/anonymity_report.md` | Stage 9 |
| `workspace/output/final/quality_report.md` | `templates/workspace/final/quality_report.md` | Stage 9 |

## 填写规则

- 每个输出文件必须保留模板中的用途、stage、必填字段、来源字段和追溯字段。
- 不知道的字段写 `待确认` 或 `不适用`，并说明原因；不要留空。
- 硬数字、图表、表格和论文结论必须能追溯到源文件和验证状态。
- `paper.md` 是 Markdown 中间稿契约。
- `paper.tex` 是 fallback scaffold；CUMCM 正式排版优先使用 `templates/latex/cumcm/cumcmthesis/`。

## run log 命名规则

模板文件：

```text
templates/workspace/q/results/run_log.md
```

实际产物：

```text
workspace/output/q*/results/run.log
```
