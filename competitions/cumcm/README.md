# CUMCM Active Writing-Quality Layer

本目录是 CUMCM 国赛的 active writing-quality layer，供 Stage 8 Paper Generation 和 Stage 9 Final Review 读取。这里保存竞赛经验、写作风格、反模式、优秀论文结构与经验阈值。

本目录不定义 workspace 文件契约。过程产物和输出文件契约位于：

```text
templates/workspace/
```

Stage 8/9 应把本目录作为写作与质量判断参考，并把所有硬结果追溯到：

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
```

| 字段 | 值 |
|------|-----|
| 竞赛代码 | `cumcm` |
| 官方名 | 全国大学生数学建模竞赛 |
| 时长 | 72 小时 (3 天) |
| 语言 | 中文 |
| LaTeX 编译器 | xelatex |
| LaTeX 模板 | `templates/latex/cumcm/cumcmthesis/` |
| 引用格式 | GB/T 7714 |
| 默认子问题数 | 4 (IQR [3, 5]) |
| 数据状态 | **stable** — 91 篇真烘焙 (2023-2025) |

## 文件清单

| 文件 | 用途 | 加载阶段 |
|------|------|---------|
| `topic_specs.json` | 题型经验与历史映射参考，不作为 active workflow 路由 | 人工参考 |
| `rubric_overlay.json` | 国赛特化质量维度和 panel persona | Stage 8/9 |
| `empirical.json` | 91 篇优秀论文 p25/p50/p75 经验分位 | Stage 8/9 质量参考 |
| `empirical_notes.md` | 实测数据人读说明 + 样本出处 | 文档参考 |
| `winning_patterns.md` | 一等奖共性 10 条 | Stage 8/9 |
| `phrase_bank.md` | 中文学术句式库 | Stage 8 |
| `anti_patterns.md` | 反模式清单 | Stage 9 |
| `distilled_phrases.md` | 段落模板 | Stage 8 |
| `distilled_naming.md` | 命名变体 | Stage 2/8 |
| `distilled_structures.md` | 章节结构模板 | Stage 8 |
| `distilled_formats.md` | 格式细节 | Stage 8/9 |
| `abstract_template.md` | 5 段式摘要模板 + 完整示例 | Stage 8 |
| `paper_skeleton.md` | CUMCM 论文骨架 | Stage 8 |

## 数据来源

- 教育部"中国大学生在线"数学建模论文展廊 (2023-2025, 32 篇)
- GitHub `zhanwen/MathModel/国赛论文/2023年优秀论文/` (58 篇，覆盖多个题型)
- GitHub `Jackyleo-Zhao/cumcm-2025` (1 篇国二 C 题)

烘焙时间 2026-05-05; 烘焙脚本已存档于 `scripts/ingest_papers.py`。

## 与 references/ 通用层的关系

- Stage 8 读取本目录完成 paper skeleton、摘要、句式、格式与高分写作质量检查。
- Stage 9 读取本目录完成 anti-pattern、panel review、calibration 与最终质量判断。
- 通用模型清单 `references/model_catalog.md` 跨竞赛复用。
- 通用反馈层 `references/feedback_layer*.md` 可结合本目录的 `empirical.json`、`winning_patterns.md` 和 `anti_patterns.md` 做人工/Agent 审查。
