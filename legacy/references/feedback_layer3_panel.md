# Feedback Layer 3：终稿 Panel Review

Layer 3 用于终稿多视角审查。它保留 panel review 思想，但所有结果写入最终报告，不再写入旧状态目录。

## 检查对象

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
```

## 输出位置

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## 建议 Panel 视角

- 数学严谨：公式、约束、边界条件、单位。
- 模型合理：路线选择、假设支撑、结果解释。
- 代码与复现：结果来源、运行日志、可复核性。
- 写作呈现：摘要、章节、图表、引用、语言。
- 评委视角：30 秒内是否能抓住核心贡献和可信证据。

## 建议记录格式

```markdown
## Panel Review

| 视角 | 结论 | 主要问题 | 必修项 | 可选优化 |
|---|---|---|---|---|
```

## 规则

- 如果环境支持多 Agent，可并行执行不同视角审查。
- 如果不支持并行，串行完成，不影响流程。
- 不输出到旧状态目录。
- 不要求生成 panel JSON 文件。
- 所有 must-fix 必须写入 `review_report.md` 或 `quality_report.md`。
