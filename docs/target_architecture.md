# mathmodel-copilot 目标架构说明

## 1. Design Principles

`mathmodel-copilot` 的目标不是复刻旧竞赛调度器，而是形成一个固定工作区、阶段契约、强模板、证据链和质量门禁驱动的单题数学建模 Skill。

核心设计原则：

- **fixed workspace input**：唯一固定输入为 `workspace/problem/problem.md` 与 `workspace/problem/reference.pdf`，图片与附件从 `problem.md` 中的相对路径解析。
- **single-problem modeling workflow**：只处理一个已给定的建模题，不做多题选择、题号比较或队伍调度。
- **Markdown-first artifacts**：所有过程材料优先写成 Markdown，必要的结构化结果写成 JSON。
- **explicit per-stage contracts**：每个阶段必须声明 Purpose、Required inputs、Required outputs、Entry conditions、Exit conditions、Failure handling 和 Manual checkpoint behavior。
- **Manual checkpoint by default**：默认 Manual 模式；每个 `q*` 完成 Plan 后暂停，只列文件路径，不复述方案。
- **result traceability**：所有硬数字必须追溯到 `result.json`、`validation.md`、`sensitivity.md` 或 `traceability.md`。
- **paper generation only from validated artifacts**：论文只能基于已验证的每问总结、最终结果和证据链生成。
- **active workflow 与 legacy 隔离**：active workflow 不引用 legacy 文件；旧逻辑如需保留，应移入 legacy / maintenance 或写 migration note。
- **positive architecture first**：主流程主体描述“应该如何执行”，不以反复禁止旧流程作为主要约束方式。

## 2. Active Workflow

### Stage 0：Workspace Audit

**Purpose**

确认固定工作区材料存在，读取 `problem.md`，建立问题审计和材料索引。

**Required inputs**

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

**Required outputs**

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

**Entry conditions**

- 当前工作区可访问。
- 用户意图是处理单题数学建模问题。

**Exit conditions**

- `problem.md` 与 `reference.pdf` 存在性已确认。
- `problem.md` 已被阅读并概括。
- 图片、附件和数据文件已索引。
- 缺失材料和题意疑点已记录。

**Failure handling**

- 缺少 `problem.md` 或 `reference.pdf` 时停止完整流程，并要求用户补充。
- 发现缺失图片或附件时记录到 audit / index，除非缺失材料阻断题意理解。

**Manual checkpoint behavior**

Stage 0 不需要用户确认即可进入 Stage 1，除非必需文件缺失或题意无法理解。

### Stage 1：Question Decomposition

**Purpose**

将单题问题按语义拆分为 `q1`、`q2`、`q3` 等可独立推进的子问题。

**Required inputs**

```text
workspace/problem/problem.md
workspace/output/problem_audit.md
workspace/output/material_index.md
```

**Required outputs**

```text
workspace/output/question_index.md
workspace/output/q*/
```

**Entry conditions**

- Stage 0 已完成。
- `problem_audit.md` 未标记阻断性问题。

**Exit conditions**

- 每个子问题有编号、标题、输入、输出、依赖、对应附件和核心任务类型。
- 每个 `workspace/output/q*/` 目录已准备。

**Failure handling**

- 如果 `problem.md` 无法可靠拆分，应在 `problem_audit.md` 中记录疑点，并按需核对 `reference.pdf`。

**Manual checkpoint behavior**

Stage 1 通常不暂停；若问题拆分存在多种合理解释，应向用户确认拆分方案。

### Stage 2：Per-Question Plan

**Purpose**

为每个 `q*` 生成可审查的计划文件集，包括题意分析、候选路线、模型、假设、符号和数据计划。

**Required inputs**

```text
workspace/output/question_index.md
workspace/output/material_index.md
workspace/output/problem_audit.md
```

**Required outputs**

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

**Entry conditions**

- Stage 1 已完成。
- 当前 `q*` 的输入、输出和依赖已在 `question_index.md` 中定义。

**Exit conditions**

- 当前 `q*` 的 Plan 文件集齐全。
- 建模路线和候选取舍清楚。
- 假设和符号有依据。
- 数据来源和预处理计划明确。

**Failure handling**

- 如果材料缺口影响建模，应写入 `warnings.md`。
- 如果无法确定路线，应暂停并请求用户确认或补充材料。

**Manual checkpoint behavior**

Manual 模式下，每个 `q*` 完成 Plan 后必须暂停，只列文件路径，等待用户确认后进入 Build。

### Stage 3：Per-Question Build

**Purpose**

按已确认的 Plan 编写代码、求解或计算，并生成结果门禁文件。

**Required inputs**

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
```

**Required outputs**

```text
workspace/output/q*/code/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

**Entry conditions**

- 当前 `q*` Plan 已通过 Manual checkpoint，或 AP 模式已写入 `review_note.md`。
- 必要数据和附件路径已明确。

**Exit conditions**

- `result.json.status` 为 `pass`、`partial` 或 `fail`。
- `run.log` 记录输入、运行、输出和失败信息。

**Failure handling**

- 运行失败时写入 `run.log`，并将 `result.json.status` 设为 `fail` 或 `partial`。
- 不允许把没有 `result.json` 支持的硬数字推进到论文。

**Manual checkpoint behavior**

Build 阶段通常不要求额外暂停；若 Build 输出为 `partial` 或 `fail`，应向用户说明限制。

### Stage 4：Verification and Sensitivity

**Purpose**

验证每个 `q*` 的结果可靠性，完成灵敏度分析。

**Required inputs**

```text
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
```

**Required outputs**

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

**Entry conditions**

- Stage 3 已生成 `result.json`。
- `result.json.status` 已声明。

**Exit conditions**

- `validation.md` 覆盖约束、边界、稳定性、baseline、ablation 或 cross-method comparison、失败情形和 PASS / PARTIAL / FAIL 结论。
- `sensitivity.md` 覆盖敏感参数、扰动范围、结果变化、结论稳定性和论文影响。

**Failure handling**

- 验证失败时同步修正 `result.json.status` 或在 `validation.md` 中记录不一致原因。
- `fail` 不得进入论文结论，`partial` 必须带限制。

**Manual checkpoint behavior**

通常不暂停；如果验证推翻 Plan 或 Build 结论，应暂停并提示用户选择重做或降级使用。

### Stage 5：Figures and Tables

**Purpose**

为每个 `q*` 生成图表目录、来源说明和必要的检查记录。

**Required inputs**

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/code/
```

**Required outputs**

```text
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
```

**Entry conditions**

- 当前问题至少有 `result.json`。
- 数据图来源可追溯。

**Exit conditions**

- 每张图表都有来源、用途和对应结论。
- 概念图标记为 `conceptual`。
- 数据图不包含伪造或不可追溯数据。

**Failure handling**

- 来源不明的图表不得进入最终论文。
- 缺失图表记录到 `warnings.md` 或 `review_report.md`。

**Manual checkpoint behavior**

通常不暂停；如果图表会改变论文结论表达，应在最终整合前提示用户。

### Stage 6：Per-Question Summary

**Purpose**

把每个 `q*` 的 Plan、Build、Verification 和 Figures/Tables 汇总为论文可用草稿。

**Required inputs**

```text
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
```

**Required outputs**

```text
workspace/output/q*/q*_summary.md
```

**Entry conditions**

- 当前 `q*` 至少完成 Build 和 Verification。
- 图表索引已建立或明确说明无图表。

**Exit conditions**

- Summary 包含问题目标、建模路线、核心公式、求解过程、主要结果、验证结论、灵敏度结论、图表索引、论文段落草稿、局限性与改进方向。

**Failure handling**

- 缺少验证或结果时，summary 必须标注 `partial` 或 `fail` 限制。

**Manual checkpoint behavior**

通常不暂停；若 summary 与 Plan 或 Validation 结论冲突，应暂停。

### Stage 7：Final Integration

**Purpose**

整合所有 `q*` 的结果、图表、表格、假设和符号，形成最终结果与证据链。

**Required inputs**

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
```

**Required outputs**

```text
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

**Entry conditions**

- 至少一个 `q*` 已完成 Summary。
- 所有 `partial` 和 `fail` 状态已明确。

**Exit conditions**

- `traceability.md` 可追踪结论、硬数字、图、表、假设和符号来源。
- `final_results.md` 不把 `fail` 写成结论。

**Failure handling**

- 发现不可追溯硬数字时，将其排除或标记为不可用于论文。
- 发现跨问题符号或单位冲突时写入 `review_report.md` 或 `quality_report.md`。

**Manual checkpoint behavior**

建议在进入 Paper Generation 前暂停一次，列出 final 文件路径供用户审查。

### Stage 8：Paper Generation

**Purpose**

基于已验证和可追溯产物生成默认中文 CUMCM 风格论文。

**Required inputs**

```text
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
```

**Required outputs**

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

**Entry conditions**

- Stage 7 已完成。
- 所有硬数字来源可追溯。

**Exit conditions**

- 论文没有引入未验证结果。
- 硬数字可追溯到 `result.json`、`validation.md`、`sensitivity.md` 或 `traceability.md`。
- 如果 PDF 未生成，失败原因已记录。

**Failure handling**

- LaTeX 模板需要提交字段时使用安全占位符或跳过正式封面，不打断建模流程。
- PDF 生成失败时记录到 `review_report.md` 和 `quality_report.md`。

**Manual checkpoint behavior**

论文生成后应列出 `paper.md`、`paper.tex`、`paper.pdf` 或失败记录路径。

### Stage 9：Final Review

**Purpose**

完成最终审查、匿名检查和质量门禁。

**Required inputs**

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

**Required outputs**

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

**Entry conditions**

- Stage 8 已完成或明确 PDF 失败。
- `traceability.md` 已存在。

**Exit conditions**

- 所有子问题是否回答已检查。
- `partial` / `fail` 已标注。
- 匿名风险已检查。
- `quality_report.md` 给出最终 PASS / PARTIAL / FAIL 结论。

**Failure handling**

- 若存在未验证硬数字，必须从论文结论中移除或标记。
- 若匿名风险无法自动处理，写入 `anonymity_report.md` 并提示用户。

**Manual checkpoint behavior**

Final Review 是最终 checkpoint，列出三个报告和论文路径。

## 3. File Contract Map

| 阶段 | 输出文件 |
|---|---|
| Stage 0 | `workspace/output/problem_audit.md` |
| Stage 0 | `workspace/output/material_index.md` |
| Stage 1 | `workspace/output/question_index.md` |
| Stage 2 | `workspace/output/q*/analysis.md` |
| Stage 2 | `workspace/output/q*/candidates.md` |
| Stage 2 | `workspace/output/q*/model.md` |
| Stage 2 | `workspace/output/q*/assumptions.md` |
| Stage 2 | `workspace/output/q*/notation.md` |
| Stage 2 | `workspace/output/q*/data_recon.md` |
| Stage 2 | `workspace/output/q*/warnings.md` |
| Stage 2 | `workspace/output/q*/review_note.md` |
| Stage 3 | `workspace/output/q*/code/` |
| Stage 3 | `workspace/output/q*/results/result.json` |
| Stage 3 | `workspace/output/q*/results/run.log` |
| Stage 4 | `workspace/output/q*/validation.md` |
| Stage 4 | `workspace/output/q*/sensitivity.md` |
| Stage 5 | `workspace/output/q*/figures/figure_index.md` |
| Stage 5 | `workspace/output/q*/tables/table_index.md` |
| Stage 6 | `workspace/output/q*/q*_summary.md` |
| Stage 7 | `workspace/output/final/final_results.md` |
| Stage 7 | `workspace/output/final/final_figures_index.md` |
| Stage 7 | `workspace/output/final/final_tables_index.md` |
| Stage 7 | `workspace/output/final/traceability.md` |
| Stage 8 | `workspace/output/final/paper.md` |
| Stage 8 | `workspace/output/final/paper.tex` |
| Stage 8 | `workspace/output/final/paper.pdf` |
| Stage 8 | `workspace/output/final/source/` |
| Stage 9 | `workspace/output/final/review_report.md` |
| Stage 9 | `workspace/output/final/anonymity_report.md` |
| Stage 9 | `workspace/output/final/quality_report.md` |

## 4. Active vs Legacy Policy

### Active 文件

Active 文件直接参与运行时 workflow，满足以下条件：

- 被 `SKILL.md` 或 active stage contract 明确引用。
- 描述当前 `workspace/problem/` 输入与 `workspace/output/` 输出。
- 不要求旧状态机、旧评分脚本或多题选题流程。
- 输出路径与 `templates/workspace/` 文件契约一致。

### Legacy 文件

Legacy 文件是旧流程、旧脚本、旧兼容说明或旧测试材料，满足以下任一条件：

- 仍依赖旧状态路径或旧状态机。
- 仍描述多题选题、旧评分聚合或旧 harness 互通。
- 对当前运行时 workflow 没有必要。

Legacy 文件可以保留，但 active workflow 不得引用它。若需要保留，应移动到 `legacy/` 或在文件头添加 migration note。

### Maintenance 文件

Maintenance 文件用于维护资料、下载材料、蒸馏经验或测试旧工具，满足以下条件：

- 不在用户建模运行时加载。
- 不影响 `workspace/output/` 契约。
- 可由维护者手动运行或参考。

### 引用政策

- active workflow 不引用 legacy 文件。
- 负面禁止语不得成为主流程主体；主流程必须通过正向 contract 驱动。
- 如果旧逻辑还需要保留，用 migration note 解释保留原因。
- 如果一个文件既有知识价值又有旧流程说明，应拆分为 active knowledge 与 legacy migration note。

## 5. Target Directory Layout

目标目录树建议如下。本步骤只定义目标，不实际移动文件。

```text
.
├── SKILL.md
├── AGENTS.md
├── README.md
├── agents/
│   └── openai.yaml
├── docs/
│   ├── refactor_audit.md
│   └── target_architecture.md
├── references/
│   ├── workflow.md
│   ├── stages/
│   │   ├── stage_00_workspace_audit.md
│   │   ├── stage_01_question_decomposition.md
│   │   ├── stage_02_per_question_plan.md
│   │   ├── stage_03_per_question_build.md
│   │   ├── stage_04_verification_sensitivity.md
│   │   ├── stage_05_figures_tables.md
│   │   ├── stage_06_per_question_summary.md
│   │   ├── stage_07_final_integration.md
│   │   ├── stage_08_paper_generation.md
│   │   └── stage_09_final_review.md
│   ├── contracts/
│   │   ├── workspace_protocol.md
│   │   ├── modes_ap_manual.md
│   │   ├── file_contracts.md
│   │   ├── result_json_contract.md
│   │   └── traceability_contract.md
│   ├── quality/
│   │   ├── rubrics.md
│   │   ├── feedback_layer1_local_quality.md
│   │   ├── feedback_layer2_cross_question.md
│   │   ├── feedback_layer3_panel_review.md
│   │   └── feedback_layer4_calibration.md
│   └── knowledge/
│       ├── model_catalog.md
│       └── cumcm_writing_notes.md
├── templates/
│   ├── workspace/
│   │   ├── problem_audit.md
│   │   ├── material_index.md
│   │   ├── question_index.md
│   │   ├── q/
│   │   └── final/
│   └── latex/
├── legacy/
│   ├── references/
│   │   └── harness_compat.md
│   ├── scripts/
│   │   ├── score_artifact.py
│   │   └── render_paper_legacy_notes.md
│   ├── config/
│   │   └── dim_weights.json
│   └── tests/
├── maintenance/
│   ├── scripts/
│   │   ├── ingest_papers.py
│   │   └── download_cumcm_papers.py
│   └── papers/
└── competitions/
    ├── cumcm/
    ├── mcm/
    └── diangong/
```

## 6. Step 1 后续约束

后续修改应按以下顺序推进：

1. 更新 `SKILL.md` 的 active reference map。
2. 统一 `references/workflow.md` 和 stage contracts 的字段格式。
3. 将 active contracts 与 `templates/workspace/` 明确绑定。
4. 隔离 legacy / maintenance 文件。
5. 最后再决定是否改造或替换旧脚本。

在这些步骤完成前，不应运行测试、打包 Skill 或引入提交包逻辑。
