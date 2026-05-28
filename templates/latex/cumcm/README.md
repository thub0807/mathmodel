# CUMCM LaTeX Rendering Assets

`templates/latex/cumcm/` 是当前 active workflow 的 CUMCM final rendering asset。

Stage 8 Paper Generation 生成正式 CUMCM 论文时，优先使用：

```text
templates/latex/cumcm/cumcmthesis/
```

## 三层架构位置

本目录属于 CUMCM competition and output layer：

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
templates/workspace/
```

职责分工：

- `competitions/cumcm/`：CUMCM 写作质量、摘要、反模式、图表格式、经验材料。
- `templates/workspace/`：`workspace/output/` 的 artifact contract。
- `templates/latex/cumcm/`：最终 LaTeX 渲染资产。

## 文件说明

| 文件 | 用途 |
|---|---|
| `cumcmthesis/cumcmthesis.cls` | CUMCM 排版类文件，提供国赛论文格式、封面、摘要、目录和正文样式。 |
| `cumcmthesis/example.tex` | 模板使用示例，可作为生成 `workspace/output/final/paper.tex` 或正式 LaTeX 源文件时的结构参考。 |
| `cumcmthesis/README.md` | 原模板说明，记录模板使用方式和维护信息。 |
| `cumcmthesis/.gitignore` | 忽略 LaTeX 编译中间文件。 |

## Stage 8 使用规则

Stage 8 应先生成 Markdown 中间稿：

```text
workspace/output/final/paper.md
```

再将已通过 traceability 检查的内容写入基于 `cumcmthesis` 的 LaTeX 源文件。

论文正文中的硬数字、图表、表格和摘要结论必须来自：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

## Fallback Scaffold

`templates/workspace/final/paper.tex` 只是 fallback scaffold，用于正式模板不可用时的临时 LaTeX 输出。

它不是 CUMCM 正式排版模板。只要 `templates/latex/cumcm/cumcmthesis/` 可用，Stage 8 应优先使用本目录。

## Legacy 边界

历史 LaTeX 模板已移动到 `legacy/templates/latex/`。它们不属于当前 active workflow。
