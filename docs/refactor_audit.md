# mathmodel-copilot Step 0 仓库审计报告

## 1. 审计范围与结论

本报告审计当前 `mathmodel-md-copilot` 仓库是否已经形成稳定的 `workspace/problem/problem.md` 与 `workspace/problem/reference.pdf` 驱动的单题 Markdown-first 数学建模 Skill。

本次审计只读取文件，不修改除本报告以外的任何仓库文件。

总体结论：

- 当前根目录 `SKILL.md` 已经是主要 active workflow 入口，名称为 `mathmodel-copilot`。
- 当前仓库只剩一个 `SKILL.md`，嵌套 shim 已移除。
- `references/` 中已经存在新版协议文件和 Stage 0-9 文档，但 active workflow 引用关系仍不够硬约束。
- `templates/workspace/` 已经有较完整的输出模板，但 `SKILL.md` 尚未明确把它作为强约束文件契约库加载。
- `scripts/` 仍保留旧脚本，文档已标注 legacy / optional，但脚本本体仍是旧 `decision_log` 路径假设。
- `competitions/` 与部分知识参考文件仍包含旧流程词汇，当前应视为 legacy / knowledge reference，而不是 active workflow。
- 当前最大问题不是单点文字残留，而是 active / legacy / maintenance 边界尚未通过目录结构和引用图彻底固化。

## 2. 当前文件树摘要

高层结构：

```text
.
├── SKILL.md
├── AGENTS.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── workspace_protocol.md
│   ├── modes_ap_manual.md
│   ├── per_question_plan.md
│   ├── per_question_build.md
│   ├── verification_protocol.md
│   ├── figures_tables_protocol.md
│   ├── paper_generation_protocol.md
│   ├── final_review_protocol.md
│   ├── stage_00_kickoff.md
│   ├── stage_01_problem_selection.md
│   ├── stage_02_analysis.md
│   ├── stage_03_model_selection.md
│   ├── stage_04_foundation.md
│   ├── stage_05_subproblem_loop.md
│   ├── stage_06_robustness.md
│   ├── stage_07_evaluation.md
│   ├── stage_08_writing.md
│   ├── stage_09_review.md
│   ├── feedback_layer*.md
│   ├── rubrics.md
│   ├── model_catalog.md
│   ├── harness_compat.md
│   └── papers/
├── templates/
│   ├── workspace/
│   ├── shared/
│   └── latex/
├── scripts/
├── competitions/
│   ├── cumcm/
│   ├── mcm/
│   └── diangong/
├── config/
└── tests/
```

当前 `git status --short` 显示有若干未提交改动，其中包括若干 `templates/latex/cumcm/cumcmthesis/` 文件删除。这些删除不是本次 Step 0 审计产生的变更，后续重构前应单独确认是否为用户有意修改。

## 3. Active workflow 文件引用图

当前入口关系：

```text
agents/openai.yaml
  └─ default_prompt: 使用 $mathmodel-copilot

AGENTS.md
  └─ 指向 SKILL.md 作为主流程定义

SKILL.md
  ├─ 启动优先读取
  │  ├─ references/workspace_protocol.md
  │  ├─ references/workflow.md
  │  └─ references/modes_ap_manual.md
  ├─ 按阶段懒加载
  │  ├─ references/per_question_plan.md
  │  ├─ references/per_question_build.md
  │  ├─ references/verification_protocol.md
  │  ├─ references/figures_tables_protocol.md
  │  ├─ references/paper_generation_protocol.md
  │  └─ references/final_review_protocol.md
  ├─ 新版阶段文档
  │  ├─ references/stage_00_kickoff.md
  │  ├─ references/stage_01_problem_selection.md
  │  ├─ references/stage_08_writing.md
  │  └─ references/stage_09_review.md
  └─ 可按需参考旧知识层
     ├─ references/model_catalog.md
     ├─ references/rubrics.md
     ├─ references/feedback_layer*.md
     └─ competitions/*
```

重要断点：

- `SKILL.md` 的“新版阶段文档”只列出 Stage 0、Stage 1、Stage 8、Stage 9，没有列出 Stage 2-7 文档。
- `references/workflow.md` 描述了 Stage 0-9，但它没有强制每个 stage 文档的进入条件、退出条件和失败处理。
- `templates/workspace/` 已经存在强模板，但 active workflow 没有明确规定“生成产物必须匹配这些模板”。
- `references/harness_compat.md` 仍是旧兼容说明，未被 SKILL 主动加载，但仍在 references 根目录，容易被误读为当前协议。

## 4. legacy / active / ambiguous 文件分类表

| 路径 | 分类 | 原因 |
|---|---|---|
| `SKILL.md` | active | 根 Skill 入口，定义当前主流程。 |
| `AGENTS.md` | active | Codex 项目指令，指向 `SKILL.md`。 |
| `agents/openai.yaml` | active | Skill UI 元数据与默认 prompt。 |
| `README.md` | active | 项目说明。 |
| `references/workflow.md` | active | 新版主流程总览。 |
| `references/workspace_protocol.md` | active | 固定输入工作区协议。 |
| `references/modes_ap_manual.md` | active | Manual / AP 模式协议。 |
| `references/per_question_plan.md` | active | 每问 Plan 文件契约。 |
| `references/per_question_build.md` | active | 每问 Build 与 result.json 契约。 |
| `references/verification_protocol.md` | active | validation / sensitivity 契约。 |
| `references/figures_tables_protocol.md` | active | 图表来源与索引契约。 |
| `references/paper_generation_protocol.md` | active | 论文生成契约。 |
| `references/final_review_protocol.md` | active | 终审与质量记录契约。 |
| `references/stage_00_kickoff.md` | active | 已改为 Stage 0 工作区审计。 |
| `references/stage_01_problem_selection.md` | active | 已改为 Stage 1 子问题拆分，但文件名仍保留旧名称。 |
| `references/stage_02_analysis.md` 到 `references/stage_07_evaluation.md` | ambiguous | 内容已向新版契约靠拢，但 `SKILL.md` 没有明确把它们纳入 active stage 文档列表。 |
| `references/stage_08_writing.md` | active | Stage 8 论文生成。 |
| `references/stage_09_review.md` | active | Stage 9 终审。 |
| `references/feedback_layer*.md` | ambiguous | 已改写为输出到 `workspace/output/`，但 `SKILL.md` 仍称其为旧知识层参考，没有明确 active 质量门禁调用点。 |
| `references/rubrics.md` | ambiguous | 已服务 `quality_report.md`，但仍在“旧知识层可参考”列表里，定位不够稳定。 |
| `references/model_catalog.md` | legacy / knowledge | 仍有旧“stage 1 选题”用法说明；可保留为模型知识库。 |
| `references/harness_compat.md` | legacy | 明确残留旧 `decision_log` / `cwd/state` 兼容内容。 |
| `references/papers/` | maintenance | 论文资料维护说明，仍有年份、题号下载说明，不应进入 active workflow。 |
| `templates/workspace/` | active | 新版文件契约模板库。 |
| `templates/shared/` | ambiguous | 表格与 code starter 可复用，但未被新版契约明确加载。 |
| `templates/latex/` | active / maintenance | 论文生成可用，但 CUMCM 模板字段和部分文件状态需确认。 |
| `scripts/README.md` | active documentation | 已标注旧脚本为 optional / legacy。 |
| `scripts/score_artifact.py` | legacy | 脚本本体仍依赖旧 `decision_log`。 |
| `scripts/render_paper.py` | legacy / optional | 脚本本体仍有旧 `decision_log` 自动检测。 |
| `scripts/extract_diff.py` | optional | 可作为维护辅助，不是主流程。 |
| `scripts/ingest_papers.py` 与 `scripts/download_cumcm_papers.py` | maintenance | 资料维护工具。 |
| `competitions/cumcm/` | knowledge / ambiguous | 论文模板与短语库有用，但部分文件仍有旧 `decision_log` 描述。 |
| `competitions/mcm/` 与 `competitions/diangong/` | knowledge / legacy | 当前不是本轮优化重点，仍有旧 team_size / topic_specs 等概念。 |
| `config/dim_weights.json` | legacy | 服务旧评分脚本，不属于新版质量门禁。 |
| `tests/fixtures/` | legacy / maintenance | 多数 fixture 验证旧 `score_artifact.py`。 |

## 5. 当前流程断点清单

1. Stage 2-7 文档存在，但没有被 `SKILL.md` 的阶段文档列表直接列为 active stage contract。
2. `references/workflow.md` 是阶段总览，但没有统一模板说明每个阶段的 `Purpose / Required inputs / Required outputs / Entry conditions / Exit conditions / Failure handling / Manual checkpoint behavior`。
3. `templates/workspace/` 模板已经较完整，但 `SKILL.md`、`workflow.md` 和各 stage 文档没有明确声明“输出文件应使用这些模板结构”。
4. `feedback_layer*.md` 已经脱离旧状态机，但没有接入明确的 Stage 4、Stage 7、Stage 9 质量门禁调用点。
5. `rubrics.md` 已经改为新版质量 rubrics，但 `SKILL.md` 仍将它放在旧知识层参考列表，可能削弱其 active quality gate 地位。
6. `references/harness_compat.md` 仍在 `references/` 根目录，包含旧状态机说明，容易被误加载。
7. `model_catalog.md` 仍有“stage 1 选题 + stage 3 模型选型”旧用法说明，需要隔离或加 migration note。
8. `scripts/score_artifact.py` 与 `scripts/render_paper.py` 仍有旧路径假设；文档已标注 legacy，但脚本路径上没有隔离。
9. CUMCM LaTeX 模板目录当前有被删除的跟踪文件，需确认是否为预期。
10. active workflow 仍较依赖“禁止事项”文字，尚未通过目录隔离和引用图完全避免旧流程被加载。

## 6. references 缺口清单

| 缺口 | 影响 | 建议 |
|---|---|---|
| 缺统一阶段契约格式 | 各阶段文档粒度不一致，执行者可能漏掉进入条件和失败处理 | 后续 Step 将 `workflow.md` 或各 stage 文档统一为固定字段。 |
| Stage 2-7 未在 SKILL 阶段文档列表中列出 | active stage contract 不够明确 | 后续更新 `SKILL.md` 的 active reference map。 |
| `harness_compat.md` 未隔离 | 旧 `decision_log` 说明可能被误读 | 移入 `legacy/` 或 `maintenance/`。 |
| `model_catalog.md` 含旧用法 | 作为模型知识库仍有价值，但入口说明旧 | 添加 migration note 或拆出纯模型目录。 |
| feedback layers 没有明确触发阶段 | 质量反馈思想存在，但 gate 接入点不稳 | 在目标架构中定义 Layer 1-4 对应阶段和输出文件。 |
| rubrics 定位 ambiguous | 可作为新版 quality gate，但目前像参考资料 | 后续纳入 active quality gate 或移至 `references/quality/`。 |

## 7. templates 缺口清单

`templates/workspace/` 当前已有以下能力：

- Stage 0：`problem_audit.md`、`material_index.md`
- Stage 1：`question_index.md`
- 每问 Plan：`analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md`、`warnings.md`、`review_note.md`
- 每问 Build：`results/result.json`
- 每问 Verification：`validation.md`、`sensitivity.md`
- 图表：`figures/figure_index.md`、`tables/table_index.md`
- Final：`final_results.md`、`final_figures_index.md`、`final_tables_index.md`、`traceability.md`、`review_report.md`、`anonymity_report.md`、`quality_report.md`

仍有缺口：

| 缺口 | 影响 | 建议 |
|---|---|---|
| 缺 `run.log` 模板 | Build 阶段要求 `run.log`，模板库未提供 | 增加 `templates/workspace/q/results/run.log`。 |
| 缺 `paper.md`、`paper.tex`、`source/` 说明模板 | Stage 8 输出契约未完全模板化 | 增加 final paper 相关模板或占位说明。 |
| 模板未被 active workflow 强制引用 | 模板存在但执行者不一定使用 | 在 `SKILL.md` / `workflow.md` 声明模板库为文件契约。 |
| `q_summary.md` 与目标文件名 `q*_summary.md` 存在命名差异 | 模板复制时需要改名，容易不一致 | 目标架构中明确模板名是复制源，输出名为 `q1_summary.md` 等。 |

## 8. scripts 与新版流程不匹配之处

| 脚本 | 当前问题 | 当前建议 |
|---|---|---|
| `scripts/score_artifact.py` | 脚本本体仍读取和写入旧 `decision_log`，服务旧 L1 评分体系 | 保留为 legacy utility，不进入 active workflow。 |
| `scripts/render_paper.py` | 仍可从旧 `decision_log` 自动检测 competition，默认路径假设与 `workspace/output/final/` 不完全一致 | 标注 optional；后续如要启用，改造成读取 `workspace/output/final/`。 |
| `scripts/extract_diff.py` | 可作为辅助 diff 工具，但不是阶段契约的一部分 | 保留 optional。 |
| `scripts/ingest_papers.py` | 维护期论文蒸馏工具，与运行时无关 | 移入 maintenance 或保留并标注维护用途。 |
| `scripts/download_cumcm_papers.py` | 维护期下载工具，与运行时无关 | 移入 maintenance 或保留并标注维护用途。 |

## 9. 旧流程残留摘要

主入口中旧概念主要以“禁止事项”出现，不是 active workflow 要求。

仍有旧流程内容的主要路径：

- `references/harness_compat.md`：旧 harness 互通、`cwd/state/decision_log.json`、`single source of truth`。
- `references/model_catalog.md`：旧 stage 1 选题用法。
- `references/papers/README.md`：维护下载说明包含年份、题号。
- `competitions/cumcm/*`：部分文件包含旧 `decision_log`、选题摇摆、score_artifact 说明。
- `competitions/mcm/*`、`competitions/diangong/*`：保留旧 `topic_specs`、`team_size` 等配置。
- `config/dim_weights.json`：旧评分权重配置。
- `tests/fixtures/*`：旧 score_artifact fixture。
- `scripts/score_artifact.py`、`scripts/render_paper.py`：旧状态路径逻辑。

这些文件目前应视为 legacy / knowledge / maintenance，不应出现在 active execution path。

## 10. 建议的重构顺序

1. 先写 `docs/target_architecture.md`，定义正向目标架构和 active / legacy / maintenance 判定标准。
2. 更新 `SKILL.md` 的 active reference map，让 Stage 0-9、feedback、rubrics、templates/workspace 的引用关系清晰且完整。
3. 统一 `references/workflow.md` 与 stage 文档格式，为每阶段补齐进入条件、退出条件、失败处理和 Manual checkpoint 行为。
4. 将 `references/harness_compat.md`、旧脚本说明、旧评分配置等移入 `legacy/` 或 `maintenance/`，并从 active workflow 引用图中移除。
5. 把 `templates/workspace/` 升级为强约束文件契约库，补齐 `run.log`、paper 相关模板，并在 stage 文档中引用。
6. 重新整理 `references/model_catalog.md`，去掉旧选题用法或移入 migration note。
7. 梳理 `competitions/`：CUMCM 保留为默认论文知识库，MCM / Diangong 标注为可选知识，不进入默认 active workflow。
8. 最后再评估是否需要改造 `render_paper.py` 为新版 workspace 工具；当前不应作为主流程必需脚本。

## 11. Step 0 结论

当前 Skill 已经具备新版单题 Markdown-first 工作流的核心雏形，但还没有形成“固定工作区、阶段契约、强模板、证据链、质量门禁”驱动的稳定架构。主要短板在于引用图不够强、legacy 文件未隔离、模板未作为硬契约接入、旧脚本仍在原目录中制造歧义。

下一步应先创建目标架构文档，再按架构逐步修改主入口、references、templates 和 legacy 隔离目录。
