# Knowledge Layer Recovery Audit

## 1. 原版目录识别结果

审计位置：`D:\postgraduate\Paper\mathmodel-md-copilot-build`

新版 Skill 根目录固定为：

```text
mathmodel-md-copilot/
```

同级候选目录扫描结果：

| 目录 | SKILL.md | references/ | competitions/ | templates/latex/ | 判定 |
|---|---:|---:|---:|---:|---|
| `refs-auto-MM/` | 否 | 否 | 否 | 否 | 非原版 Skill |
| `refs-AutoMCM-Pro/` | 否 | 否 | 否 | 否 | 非原版 Skill |
| `refs-mathmodel-skill/` | 是 | 是 | 是 | 是 | 原版 Skill |

结论：只发现一个原版 Skill 候选，原版目录为：

```text
D:\postgraduate\Paper\mathmodel-md-copilot-build\refs-mathmodel-skill
```

未出现多个候选，因此本审计继续执行。

## 2. 新版目录识别结果

新版目录为：

```text
D:\postgraduate\Paper\mathmodel-md-copilot-build\mathmodel-md-copilot
```

新版 active workflow 入口与核心索引：

```text
mathmodel-md-copilot/SKILL.md
mathmodel-md-copilot/references/workspace_protocol.md
mathmodel-md-copilot/references/workflow.md
mathmodel-md-copilot/references/modes_ap_manual.md
mathmodel-md-copilot/references/result_traceability.md
mathmodel-md-copilot/references/quality_gate.md
mathmodel-md-copilot/references/stage_00_workspace_audit.md
...
mathmodel-md-copilot/references/stage_09_final_review.md
mathmodel-md-copilot/templates/workspace/
```

新版还保留：

```text
mathmodel-md-copilot/legacy/references/
mathmodel-md-copilot/legacy/scripts/
mathmodel-md-copilot/competitions/
mathmodel-md-copilot/templates/latex/
```

关键观察：新版 active workflow 已经转向 fixed workspace、Markdown-first、result.json、traceability、quality gate；但原版的模型知识、评分量表、反馈层和写作经验多数被隔离到 `legacy/references/`，没有接入 active workflow。

## 3. 原版核心能力文件清单

以下原版材料属于有效知识层，应恢复并去状态机化，而不是作为 legacy 长期封存。

### 3.1 通用模型与评分知识

| 原版路径 | 核心能力 | 恢复判断 |
|---|---|---|
| `references/model_catalog.md` | 优化、预测、评价、分类、仿真、图论、统计、动力系统等模型族目录；候选模型生成与选型 checklist | 应恢复为 active knowledge，删除旧 stage / 题号 / decision_log 绑定 |
| `references/rubrics.md` | 三竞赛评分维度、阶段级 rubric、阈值、与 winning_patterns / anti_patterns / empirical 的对应关系 | 应恢复为 active quality layer，改写为 workspace artifact 质量门禁 |
| `references/feedback_layer1_critic.md` | 阶段级 critic、评分维度、verdict、diff-only 精修思想 | 应恢复为 active quality gate，但移除 score_artifact、decision_log 写入协议 |
| `references/feedback_layer2_backtrack.md` | 跨阶段一致性回检：符号漂移、假设隐式引入、模型族不一致、灵敏度推翻假设 | 应恢复为 active cross-artifact consistency check，改读 `workspace/output/` |
| `references/feedback_layer3_panel.md` | 终局多视角 panel：数学严谨、模型创新、代码正确、写作呈现、评委视角 | 应恢复为 final review 可选/能力感知并行检查；无并行能力时串行 |
| `references/feedback_layer4_calibration.md` | 防 rubric gaming 的校准抽查 | 可恢复为 Stage 9 或 championship-style final review 的增强检查 |

### 3.2 原版 stage 中可抽取的知识层

| 原版路径 | 可恢复知识 | 必须去掉的旧绑定 |
|---|---|---|
| `references/stage_02_analysis.md` | 题目精读、子问题分解、变量统一编号、数据 schema 扫描、子问题关系图、目标函数雏形 | `decision_log.stages.2`、旧 stage 编号依赖 |
| `references/stage_03_model_selection.md` | 按问题类型映射模型族、生成至少 3 个结构性不同候选、选型矩阵、toy demo 验证、模型族协调 | `decision_log.stages.3`、championship red-team 状态写入、旧 stage 选型流 |
| `references/stage_05_subproblem_loop.md` | 单子问题建模、求解、验证、子灵敏度、物理意义讨论、跨子问题协调 | `score_artifact.py --mode aggregate_qi`、`decision_log.stages.5`、qi_weights 状态机 |
| `references/stage_06_robustness.md` | 3-5 个参数联合扰动、扰动幅度、稳健区间、失稳预警、可视化 | `decision_log.stages.6`、L2 旧回滚记录 |
| `references/stage_08_writing.md` | 摘要最后写、论文各节写作 prompt、代码附录、摘要 5 段式、写作常见坑 | `decision_log.stages.0-7`、按 `decision_log.competition` dispatch |
| `references/stage_09_review.md` | anti-pattern 对照、视觉化润色、5 视角 panel、定向修复、终稿退出条件 | `decision_log_full`、submission_ready、旧状态写入 |

## 4. 新版已保留但未接入 active workflow 的文件清单

### 4.1 被保留在 `legacy/references/`

这些文件已存在于新版，但 `legacy/README.md` 明确声明 legacy 不属于 active workflow，因此当前不会被 active modeling 自动加载。

```text
legacy/references/model_catalog.md
legacy/references/rubrics.md
legacy/references/feedback_layer1_critic.md
legacy/references/feedback_layer2_backtrack.md
legacy/references/feedback_layer3_panel.md
legacy/references/feedback_layer4_calibration.md
legacy/references/stage_02_analysis.md
legacy/references/stage_03_model_selection.md
legacy/references/stage_05_subproblem_loop.md
legacy/references/stage_06_robustness.md
legacy/references/stage_08_writing.md
legacy/references/stage_09_review.md
```

它们不是“无用旧流程”。准确状态应是：包含旧状态机污染的高价值知识层，需要迁回 active knowledge / quality / writing 层，并移除旧状态机接口。

### 4.2 已保留在 `competitions/`，但 active workflow 引用不足

新版 `competitions/` 与原版相比，`cumcm/`、`mcm/`、`diangong/` 文件集合和内容哈希一致，未发现缺失或改动。

但新版 `SKILL.md` 和 `references/workflow.md` 没有把 `competitions/cumcm/` 明确作为默认 active writing / review knowledge 接入。当前 Stage 8 只提到 `templates/latex/cumcm/`，而该目录在新版缺失。

## 5. 被错误移动到 legacy 的文件清单

以下文件应从 legacy 中恢复为 active knowledge，但恢复时不能原样搬回，必须先去状态机化。

| 当前新版路径 | 建议目标定位 | 恢复理由 |
|---|---|---|
| `legacy/references/model_catalog.md` | `references/knowledge/model_catalog.md` 或 `references/model_catalog.md` | active Plan 阶段需要模型候选生成和选型依据 |
| `legacy/references/rubrics.md` | `references/quality/rubrics.md` 或 `references/rubrics.md` | active quality gate 需要明确评分维度 |
| `legacy/references/feedback_layer1_critic.md` | `references/quality/feedback_layer1_critic.md` | 可转化为 stage output 质量检查 |
| `legacy/references/feedback_layer2_backtrack.md` | `references/quality/feedback_layer2_consistency.md` | 可转化为 workspace artifact 一致性检查 |
| `legacy/references/feedback_layer3_panel.md` | `references/quality/feedback_layer3_panel.md` | 可用于 final review 的多视角评审 |
| `legacy/references/feedback_layer4_calibration.md` | `references/quality/feedback_layer4_calibration.md` | 可用于防止形式化评分通过但实质失败 |
| `legacy/references/stage_02_analysis.md` | 融入 `references/stage_01_question_decomposition.md` 与 `stage_02_per_question_plan.md` | 子问题分解与深度分析是 active workflow 的核心 |
| `legacy/references/stage_03_model_selection.md` | 融入 `references/stage_02_per_question_plan.md` | 候选模型生成、选型矩阵、toy demo 是 Plan 核心 |
| `legacy/references/stage_05_subproblem_loop.md` | 融入 `references/stage_03_per_question_build.md`、`stage_04_verification_sensitivity.md`、`stage_06_per_question_summary.md` | 单问求解、验证、灵敏度、解释均可复用 |
| `legacy/references/stage_06_robustness.md` | 融入 `references/stage_04_verification_sensitivity.md` | 联合扰动和稳健区间比当前 sensitivity 模板更有指导性 |
| `legacy/references/stage_08_writing.md` | 融入 `references/stage_08_paper_generation.md` 与 CUMCM writing knowledge | 当前论文生成缺少足够写作策略 |
| `legacy/references/stage_09_review.md` | 融入 `references/stage_09_final_review.md` | 当前 final review 偏契约检查，缺少评委视角与 anti-pattern 深查 |

## 6. `competitions/` 可复用材料清单

新版 `competitions/` 与原版 `competitions/` 对比结论：

- `competitions/cumcm/`：无缺失、无新增、无内容变化。
- `competitions/mcm/`：无缺失、无新增、无内容变化。
- `competitions/diangong/`：无缺失、无新增、无内容变化。

### 6.1 CUMCM 应作为默认 active 知识层接入

| 文件 | 可复用内容 | 去状态机化处理 |
|---|---|---|
| `competitions/cumcm/winning_patterns.md` | 摘要、章节结构、图表密度、模型命名、子问题复用链、假设支撑、灵敏度深度、评价节质量 | 保留为 writing / review principles |
| `competitions/cumcm/phrase_bank.md` | 中文学术句式、章节连接、公式术语、危险句式 | 保留为 writing support |
| `competitions/cumcm/abstract_template.md` | 5 段式摘要、自检项、关键词策略 | 删除 `decision_log.json` 调用说明 |
| `competitions/cumcm/paper_skeleton.md` | 国赛论文结构、页数预算、章节占位 | 删除 render_paper / decision_log 假设，改从 `workspace/output/final/traceability.md` 填充 |
| `competitions/cumcm/anti_patterns.md` | 摘要、假设、模型选型、求解、结果、灵敏度、写作反模式 | 删除 Stage 1 选题摇摆和 decision_log 修复建议，保留质量检查 |
| `competitions/cumcm/empirical.json` | 国赛优秀论文统计分位 | 不再由 `score_artifact.py` 注入；改为 quality gate 可选参考 |
| `competitions/cumcm/empirical_notes.md` | 统计分位说明、样本局限 | 保留为审计说明 |
| `competitions/cumcm/distilled_structures.md` | 章节结构记忆、结构模板卡 | 保留为 writing knowledge |
| `competitions/cumcm/distilled_phrases.md` | 蒸馏句式模板 | 保留为 writing knowledge |
| `competitions/cumcm/distilled_naming.md` | 模型命名变体 | 保留为 model naming support |
| `competitions/cumcm/distilled_formats.md` | 公式编号、图表标题、引用格式、版式检查 | 保留为 final polish / review support |
| `competitions/cumcm/rubric_overlay.json` | CUMCM 特化评分维度与 panel persona | 可保留，但不能依赖 `score_artifact.py` |
| `competitions/cumcm/topic_specs.json` | 题号体系到 task_type 的旧映射 | 不应进入 active workflow；如保留，仅维护/历史参考 |

### 6.2 MCM / Diangong 可保留为可选知识层

`competitions/mcm/*` 与 `competitions/diangong/*` 仍可复用写作模板、反模式、短语库、paper_skeleton、rubric_overlay、winning_patterns。它们不应成为默认 active path，因为 v1.2 当前目标是固定单题、默认 Python、Markdown-first，且不要求多竞赛调度。

## 7. `templates/latex/` 缺失材料清单

原版 LaTeX 模板清单：

```text
templates/latex/cumcm/cumcmthesis/README.md
templates/latex/cumcm/cumcmthesis/example.tex
templates/latex/cumcm/cumcmthesis/example.pdf
templates/latex/cumcm/cumcmthesis/cumcmthesis.cls
templates/latex/diangong/main.tex
templates/latex/mcm/main.tex
```

新版 LaTeX 模板清单：

```text
templates/latex/diangong/main.tex
templates/latex/mcm/main.tex
```

新版缺失：

```text
templates/latex/cumcm/cumcmthesis/README.md
templates/latex/cumcm/cumcmthesis/example.tex
templates/latex/cumcm/cumcmthesis/example.pdf
templates/latex/cumcm/cumcmthesis/cumcmthesis.cls
```

影响：

- 新版 `references/workflow.md` Stage 8 写明使用 `templates/latex/cumcm/`。
- 新版 `references/stage_08_paper_generation.md` 也引用 `templates/latex/cumcm/`。
- 但新版实际没有 `templates/latex/cumcm/`，导致默认 CUMCM 论文生成路径断裂。

结论：CUMCM LaTeX 模板应恢复。恢复时应注意 `cumcmthesis.cls` 中仍有 A-E 题号填写字段，这是官方模板字段，不等同于 active workflow 的多题选题；不得由 Agent 自动选题或推荐题号。

## 8. `templates/workspace/` 过度承担职责的问题清单

`templates/workspace/` 在新版中是必要的文件契约库，但当前承担了过多知识与流程职责。

| 问题 | 表现 | 建议 |
|---|---|---|
| 模板同时承担 schema、流程指令和质量规则 | 多数模板包含“文件用途 / 对应 stage / 必填字段 / 来源字段 / 可追溯要求 / 禁止空泛表达 / 模板正文” | 保留模板为输出结构；把流程策略放到 stage reference，把质量规则放到 quality reference |
| Plan 知识被压进模板 | `analysis.md`、`candidates.md`、`model.md` 定义了输出形状，但缺少来自 `model_catalog.md` 的候选模型知识 | 恢复 model_catalog，并在 Stage 2 明确读取 |
| 验证方法被模板孤立承载 | `validation.md` 要求 baseline、ablation 或 cross-method comparison，但 active reference 缺少足够方法指导 | 将旧 Stage 5 / Stage 6 的验证与稳健性方法迁入 Stage 4 |
| 论文结构由 `paper.md` 模板单独决定 | 当前 Stage 8 缺少 CUMCM writing knowledge 接入，导致 `paper.md` 模板承担写作骨架职责 | 接入 `competitions/cumcm/paper_skeleton.md`、`abstract_template.md`、`winning_patterns.md` |
| final review 偏文件完整性 | `quality_report.md` 检查文件和 traceability，但缺少评委视角与反模式深查 | 恢复 rubrics、feedback_layer3_panel、anti_patterns |
| Manual mode 产物口径不一致 | 项目硬要求为 Manual mode 生成 `solution_plan.md` 并返回路径；当前 `modes_ap_manual.md` 说明不要求统一 `solution_plan.md` | 后续应统一 Manual checkpoint contract；本审计不修改 |
| 模板库成为 active workflow 的唯一强约束 | `SKILL.md` 强调 templates 是 contract，但知识层没有同等强度接入 | 建议形成三层：stage contract、knowledge reference、workspace template |

## 9. 需要删除、替换或隔离的旧内容

以下材料不应作为 active workflow 恢复。

| 旧内容 | 当前位置/表现 | 处理建议 |
|---|---|---|
| `decision_log` | `legacy/references/*`、`legacy/scripts/score_artifact.py`、部分 `competitions/*` 文案 | 从 active references 中删除；知识文件恢复时替换为 `workspace/output/*` 产物 |
| `cwd/state` | `legacy/references/harness_compat.md`、`legacy/scripts/*` | 保留在 legacy 审计材料，不进入 active workflow |
| `score_artifact.py` active 依赖 | `legacy/scripts/score_artifact.py`，以及 competitions / old feedback 文案中引用 | 不恢复为 active dependency；如需评分，改为 Agent 质量检查或新版 workspace-aware optional tool |
| 多题选题 | 原版 Stage 1、Quick Start、topic_specs | 不恢复；新版只读取已给定 `problem.md` |
| A-E / A-F 题推荐 | 原版 Quick Start、topic_specs、competition README | 不恢复为 Agent 行为；官方 LaTeX 的题号字段可保留为空/用户提供 |
| question selection / problem selection | `stage_01_problem_selection.md`、旧 SKILL 文案 | 不恢复；新版 Stage 1 是 question decomposition，不是选题 |
| old harness state machine | `harness_compat.md`、`cwd/state/decision_log.json` 互通协议 | 继续隔离在 legacy |
| team size / deadline / division of labor 询问 | 原版 Quick Start | 不恢复 |
| submit.zip / submission packaging | 原版提交导向材料如有残留 | 不恢复；v1.2 不生成 submit.zip |
| `topic_specs.json` 作为 task_type 自动路由 | `competitions/*/topic_specs.json` | 仅历史/维护参考，不接入 active workflow |

## 10. 建议恢复顺序

1. 恢复 `templates/latex/cumcm/cumcmthesis/`，修复 Stage 8 当前引用的缺失路径。
2. 恢复 `model_catalog.md` 为 active model knowledge，删除旧 stage / 题号 / decision_log 说明，并接入 Stage 2 Per-Question Plan。
3. 恢复 `rubrics.md` 与 `feedback_layer1_critic.md` 为 active quality layer，改读 `workspace/output/`，不调用 `score_artifact.py`。
4. 将 `stage_03_model_selection.md` 的候选模型生成、选型矩阵、toy demo 内容迁入新版 `stage_02_per_question_plan.md`。
5. 将 `stage_05_subproblem_loop.md` 与 `stage_06_robustness.md` 中的验证、子灵敏度、联合扰动、稳健区间迁入新版 `stage_03_per_question_build.md` 和 `stage_04_verification_sensitivity.md`。
6. 将 `stage_08_writing.md` 的写作顺序、摘要策略、章节 prompt，与 `competitions/cumcm/{paper_skeleton,abstract_template,phrase_bank,winning_patterns,distilled_*}.md` 接入新版 Stage 8。
7. 将 `stage_09_review.md`、`feedback_layer3_panel.md`、`feedback_layer4_calibration.md`、`competitions/cumcm/anti_patterns.md` 接入新版 Stage 9。
8. 最后统一 `templates/workspace/` 职责边界：模板只定义输出形状，stage references 定义执行流程，knowledge / quality references 提供专业判断。

## 11. 关键结论

- 原版目录已唯一识别为 `refs-mathmodel-skill/`。
- 新版目录已形成固定工作区与证据链主流程，但知识层恢复不足。
- `model_catalog.md`、`rubrics.md`、`feedback_layer*.md` 和若干旧 stage 文件不是纯 legacy；它们是被旧状态机污染的有效知识层。
- `competitions/cumcm/*` 已完整保留，但没有被 active workflow 充分接入。
- `templates/latex/cumcm/cumcmthesis/*` 在新版缺失，且 Stage 8 当前仍引用 CUMCM LaTeX 路径，这是明确断点。
- 不应恢复 `decision_log`、`cwd/state`、`score_artifact.py` active 依赖、多题选题、题号推荐、旧 harness state machine。

