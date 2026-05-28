# 新主流程

`mathmodel-copilot` 使用 10 个阶段完成单题建模工作区：

```text
Stage 0  Workspace Reading & Problem Understanding
Stage 1  Question Decomposition
Stage 2  Per-Question Plan
Stage 3  Per-Question Build
Stage 4  Per-Question Verification
Stage 5  Figures and Tables
Stage 6  Per-Question Summary
Stage 7  Final Integration
Stage 8  Paper Generation with Template
Stage 9  Final Review
```

## 执行策略

主流程允许能力感知并行：

- 独立子问题、独立验证、图表检查和终审检查可以在环境支持时并行。
- 并行任务必须以文件为边界交付结果，统一写入 `workspace/output/`。
- 如果环境没有可靠并行能力，自动降级为串行单 Agent 执行。
- 串行降级不改变任何输出路径和质量要求。

## Stage 0：Workspace Reading & Problem Understanding

输入：

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

输出：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

职责：

- 确认 `problem.md` 与 `reference.pdf` 存在。
- 读取并理解 `problem.md`。
- 索引图片、附件和数据文件。
- 记录缺失文件、路径错误和材料疑点。
- 不默认全文审计 PDF。

## Stage 1：Question Decomposition

输出：

```text
workspace/output/question_index.md
workspace/output/q1/
workspace/output/q2/
...
```

职责：

- 根据 `problem.md` 语义拆分子问题。
- 支持“问题一 / 问题1 / Q1 / 第一问 / 任务一 / 隐含问题”等表达。
- 不使用 Python 正则脚本拆题。
- 不使用 `question_manifest.json` 作为必需文件。
- 不做多题选择或评分。

## Stage 2：Per-Question Plan

每问输出：

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # 如有
workspace/output/q*/review_note.md     # AP 模式或必要时
```

Manual 模式下，Stage 2 完成后必须暂停，只列出文件路径。

本流程不要求额外生成统一的 `solution_plan.md`。每问 Plan 由上述文件集共同构成；Manual checkpoint 只列这些文件路径。

## Stage 3：Per-Question Build

每问输出：

```text
workspace/output/q*/code/
workspace/output/q*/results/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

`result.json` 是硬数字进入论文的门禁。

## Stage 4：Per-Question Verification

每问输出：

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

`validation.md` 至少覆盖约束、边界、稳定性、baseline、ablation 或 cross-method comparison、失败情形和 PASS / PARTIAL / FAIL 结论。

`sensitivity.md` 至少覆盖敏感参数、扰动范围、结果变化、结论稳定性和对论文结论的影响。

## Stage 5：Figures and Tables

每问输出：

```text
workspace/output/q*/figures/
workspace/output/q*/tables/
```

图表必须说明来源、用途和对应结论。数据图不得伪造；概念图必须标记为 `conceptual`。

## Stage 6：Per-Question Summary

每问输出：

```text
workspace/output/q*/q*_summary.md
```

内容包括问题目标、建模路线、核心公式、求解过程、主要结果、验证结论、灵敏度结论、图表索引和可写入论文的段落草稿。

## Stage 7：Final Integration

输出：

```text
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

`traceability.md` 是最终论文证据链总表，说明关键结论、硬数字、图表、假设和符号分别来自哪些文件。

## Stage 8：Paper Generation with Template

默认中文 CUMCM 风格论文。

输出：

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

论文必须基于 `q*/q*_summary.md`、`final_results.md` 和 `traceability.md`，不得引入未验证的新结果。

## Stage 9：Final Review

输出：

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

`quality_report.md` 是新版质量记录。
