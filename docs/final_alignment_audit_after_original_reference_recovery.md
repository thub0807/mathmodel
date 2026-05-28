# Final Alignment Audit After Original Reference Recovery

审计日期：2026-05-28

审计范围：

```text
SKILL.md
AGENTS.md
README.md
references/
competitions/cumcm/
templates/workspace/
templates/latex/cumcm/
legacy/
scripts/
config/    # 如存在
tests/     # 如存在
```

## 总体判断

总体判断：`PASS`

当前 active workflow 已完成以下对齐：

- active knowledge layer 已从摘要版补强为可执行知识层；
- Stage 1-9 已吸收 legacy 原版的分析、建模、求解、验证、图表、写作、终审和反馈层细节；
- active workflow 默认且仅启用 CUMCM；
- MCM / Diangong 材料已隔离到 `legacy/`；
- 旧评分配置、旧测试夹具、旧脚本已隔离到 `legacy/`；
- `templates/workspace/` 定位为 artifact contract，未替代 CUMCM 写作层或 LaTeX 渲染层；
- 未发现旧状态机作为 active workflow 输入、输出、脚本或默认竞赛选项。

## Active Knowledge Layer 对齐情况

| 文件 | 状态 | 行数 | 判断 |
|---|---:|---:|---|
| `references/model_catalog.md` | exists | 207 | 已补强，不是摘要空壳。 |
| `references/rubrics.md` | exists | 288 | 已补强，不是摘要空壳。 |
| `references/feedback_layer1_critic.md` | exists | 278 | 已补强，不是摘要空壳。 |
| `references/feedback_layer2_backtrack.md` | exists | 200 | 已补强，不是摘要空壳。 |
| `references/feedback_layer3_panel.md` | exists | 205 | 已补强，不是摘要空壳。 |
| `references/feedback_layer4_calibration.md` | exists | 273 | 已补强，不是摘要空壳。 |

覆盖内容：

- `model_catalog.md` 覆盖模型族、适用条件、数据需求、输出形式、可解释性、失败模式、CUMCM 命名和 code starter 对应关系。
- `rubrics.md` 覆盖题意理解、模型选择、求解实现、验证灵敏度、论文表达、图表质量、CUMCM 风格和 final verdict。
- L1-L4 feedback layers 覆盖局部 critic、跨产物回溯、终局 panel、校准与反包装检查。

## Stage References 对齐情况

| Stage | 文件 | 行数 | 对齐判断 |
|---|---|---:|---|
| Stage 1 | `references/stage_01_question_decomposition.md` | 216 | 已包含题意精读、动词/对象/约束/数据接口识别、显式/隐式子问题、依赖图和歧义记录。 |
| Stage 2 | `references/stage_02_per_question_plan.md` | 271 | 已包含 question card、候选模型、比较矩阵、模型选择、toy demo 和 red-team。 |
| Stage 3 | `references/stage_03_per_question_build.md` | 243 | 已包含子问题求解循环、公式到代码、数据预处理、异常处理、result schema、run.log 和 code starter。 |
| Stage 4 | `references/stage_04_verification_sensitivity.md` | 290 | 已包含 sanity check、baseline、约束、边界、单/联合扰动、失稳边界和 L2 backtrack 触发条件。 |
| Stage 5 | `references/stage_05_figures_tables.md` | 189 | 已包含图表服务 claim、图表类型、source field、paper section、validation status 和 CUMCM 图表质量检查。 |
| Stage 6 | `references/stage_06_per_question_summary.md` | 191 | 已明确 `q*_summary.md` 是论文小节草稿，并限制 hard numbers 来源。 |
| Stage 7 | `references/stage_07_final_integration.md` | 282 | 已包含统一符号、统一单位、统一模型命名、跨题依赖、结果冲突和 Stage 8 前 Manual checkpoint。 |
| Stage 8 | `references/stage_08_paper_generation.md` | 237 | 已接入 CUMCM 写作材料、Markdown 中间稿契约和 `cumcmthesis` 正式模板优先级。 |
| Stage 9 | `references/stage_09_final_review.md` | 286 | 已接入 L1/L2/L3/L4、多轮 review、匿名性、traceability 和 CUMCM 风格终审。 |

定向关键词抽查显示各 Stage 的 legacy 恢复要点均有命中，例如：

- Stage 1：三遍精读、依赖图、歧义；
- Stage 2：候选模型、比较矩阵、toy demo、red-team；
- Stage 3：code starter、`result.schema.json`、`run.log`、fallback；
- Stage 4：baseline、单参数、联合扰动、失稳边界；
- Stage 8：`paper_skeleton`、`abstract_template`、`phrase_bank`、`cumcmthesis`；
- Stage 9：L1/L2/L3/L4、panel、calibration、匿名性、traceability。

## CUMCM-only 情况

结论：`PASS`

active 目录状态：

```text
competitions/cumcm/
templates/latex/cumcm/
```

已不存在 active：

```text
competitions/mcm/
competitions/diangong/
templates/latex/mcm/
templates/latex/diangong/
```

历史材料已移动到：

```text
legacy/competitions/mcm/
legacy/competitions/diangong/
legacy/templates/latex/mcm/
legacy/templates/latex/diangong/
```

`SKILL.md`、`README.md`、`AGENTS.md` 和 `references/workflow.md` 均声明当前 active workflow 默认且仅支持 CUMCM。

## Legacy Isolation 情况

结论：`PASS`

确认：

- `legacy/references/` 是原版 references 高密度快照；与 `refs-mathmodel-skill/references/` 对应文件 SHA256 对比无差异输出。
- active workflow 不读取 `legacy/references/`。
- `legacy/config/` 存放旧评分配置：`dim_weights.json`。
- `legacy/tests/fixtures/` 存放旧评分/旧脚本测试夹具。
- `legacy/scripts/extract_diff.py` 存放旧 critique patch 工具。
- active workflow 不依赖 `legacy/`。

active 旧评分/旧脚本目录状态：

```text
config/    missing
tests/     missing
scripts/   only scripts/README.md
```

`scripts/README.md` 已说明当前没有 active runtime scripts。

## 旧关键词残留表

搜索 active 区域：

```text
SKILL.md
AGENTS.md
README.md
references/
competitions/cumcm/
templates/workspace/
templates/latex/cumcm/
scripts/
```

| 关键词 | 命中情况 | 判断 |
|---|---:|---|
| `decision_log` | 0 | 通过 |
| `cwd/state` | 0 | 通过 |
| `score_artifact` | 0 | 通过 |
| `question_manifest` | 0 | 通过 |
| `stage.1.selected` | 0 | 通过 |
| `problem selection` | 0 | 通过 |
| `A-E` | 0 | 通过 |
| `A-F` | 0 | 通过 |
| `MCM` | 多处 | 允许。主要来自 `CUMCM` 正常词、`cumcmthesis` 模板内部宏名、`mcm.edu.cn` 官网链接，以及 `SKILL.md`/`README.md` 中的 legacy isolation 说明。未作为 active 竞赛入口。 |
| `Diangong` | 2 | 允许。仅在 `SKILL.md` 和 `README.md` 中说明历史材料已移动到 `legacy/`，不属于 active workflow。 |
| `电工杯` | 0 | 通过 |

更精确路径检查：

- 未发现 `competitions/mcm` 或 `competitions/diangong` 被 active references 引用；
- 未发现 `templates/latex/mcm` 或 `templates/latex/diangong` 被 active references 引用；
- 未发现 `extract_diff.py` 或 `score_artifact.py` 作为 active tool；
- 未发现 `config/` 或 `tests/fixtures/` 作为 active dependency。

## Templates / Workspace 定位

结论：`PASS`

确认：

- `templates/workspace/` 是 `workspace/output/` 的 artifact contract；
- `templates/workspace/` 没有替代 `competitions/cumcm/`；
- `templates/workspace/` 没有替代 `templates/latex/cumcm/`；
- `templates/workspace/final/paper.md` 是 Markdown 中间稿契约；
- `templates/workspace/final/paper.tex` 是 fallback scaffold；
- CUMCM 正式排版优先使用 `templates/latex/cumcm/cumcmthesis/`；
- `competitions/cumcm/` 是 CUMCM writing-quality layer。

## 仍需人工审查的问题

非阻塞：

- `templates/latex/cumcm/cumcmthesis/` 内部包含 `mcm` 宏名和 `mcm.edu.cn` 链接，这是 CUMCM 模板原生内容，不是 active MCM 入口。
- `competitions/cumcm/topic_specs.json` 保留历史题型经验，并声明不用于自动路由；如未来希望更严格，可将其进一步标注为人工参考。
- 当前审计确认 references 和入口文档一致，但尚未运行一次真实 `workspace/problem/problem.md` 端到端 smoke test。

## 推荐下一轮任务

1. 做一次最小 CUMCM workspace smoke test：放入一个小型 `workspace/problem/problem.md`，验证 Stage 0-9 是否能按文件契约产出。
2. 检查 `templates/shared/code_starter/*.py` 是否与 Stage 3 的 result schema、run.log 契约完全一致。
3. 检查 `templates/workspace/q/results/result.schema.json` 是否覆盖 `pass/partial/fail`、source field、claim eligibility、warnings、limitations。
4. 对 `competitions/cumcm/topic_specs.json` 做一次人工参考定位审查，确认不会被误用为自动题号路由。
5. 在 README 或 docs 中补一份“如何运行一次 Manual 模式”的最小示例。
