# CUMCM LaTeX Template

本目录保存 CUMCM 正式排版资产。Stage 8 生成 CUMCM 论文时，正式排版应优先使用：

```text
templates/latex/cumcm/cumcmthesis/
```

## 文件说明

| 文件 | 用途 |
|---|---|
| `cumcmthesis/cumcmthesis.cls` | CUMCM 排版类文件，提供国赛论文格式、封面、摘要、目录和正文样式。 |
| `cumcmthesis/example.tex` | 官方模板使用示例，可作为生成 `workspace/output/final/paper.tex` 或最终 LaTeX 源文件时的结构参考。 |
| `cumcmthesis/README.md` | 原模板说明，记录模板使用方式和维护信息。 |
| `cumcmthesis/.gitignore` | 忽略 LaTeX 编译中间文件。 |

## Stage 8 使用方式

Stage 8 Paper Generation 应将已经通过 traceability 检查的论文内容写入基于 `cumcmthesis/example.tex` 结构的 LaTeX 源文件，并使用 `cumcmthesis.cls` 作为正式排版类。

论文正文中的硬数字、图表、表格和摘要结论仍必须来自 `workspace/output/final/traceability.md` 允许使用的内容。

## Fallback Scaffold

`templates/workspace/final/paper.tex` 只是 workspace 中间产物或 fallback scaffold，用于缺少正式模板、快速检查 LaTeX 结构或生成临时草稿。

它不应被视为 CUMCM 竞赛正式排版模板。

## 未恢复文件

原版目录中的 `cumcmthesis/example.pdf` 是编译后的示例输出，体积约 445 KB。本阶段未恢复该 PDF；需要预览时可由 `example.tex` 重新编译生成。
