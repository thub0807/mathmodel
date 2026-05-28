# 论文生成协议

默认生成中文 CUMCM 风格论文。

优先使用：

```text
templates/latex/cumcm/
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/phrase_bank.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/winning_patterns.md
```

只有用户明确指定 MCM 时，才使用英文 Summary / Paper。

## 输入

论文必须基于：

```text
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

## 输出

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

## 规则

- 不得引入未验证的新结果。
- 摘要、结论、表格中的硬数字必须来自 `result.json`、`validation.md` 或 `sensitivity.md`。
- 必须使用 `competitions/cumcm/anti_patterns.md` 做反向检查。
- 图表引用必须与最终图表索引一致。
- 若 `paper.pdf` 生成失败，必须记录到 `review_report.md` 与 `quality_report.md`。
