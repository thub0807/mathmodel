# Legacy Materials

`legacy/` 是开发迁移档案，不属于 active workflow。active workflow 不读取、不依赖、不执行 `legacy/` 下的任何材料。

当前 active workflow 入口是：

```text
SKILL.md
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
references/stage_00_workspace_audit.md
references/stage_01_question_decomposition.md
references/stage_02_per_question_plan.md
references/stage_03_per_question_build.md
references/stage_04_verification_sensitivity.md
references/stage_05_figures_tables.md
references/stage_06_per_question_summary.md
references/stage_07_final_integration.md
references/stage_08_paper_generation.md
references/stage_09_final_review.md
references/result_traceability.md
references/quality_gate.md
competitions/cumcm/
templates/workspace/
templates/latex/cumcm/
```

## 目录说明

| 路径 | 含义 | Active workflow 是否使用 |
|---|---|---|
| `legacy/references/` | 原版 references 高密度快照，供开发迁移参考。 | 否 |
| `legacy/config/` | 旧评分权重快照。 | 否 |
| `legacy/tests/fixtures/` | 旧评分/旧脚本测试夹具。 | 否 |
| `legacy/scripts/score_artifact.py` | 旧评分脚本。 | 否 |
| `legacy/scripts/render_paper.py` | 旧渲染脚本。 | 否 |
| `legacy/scripts/extract_diff.py` | 旧 critique patch 工具。当前 active workflow 不使用。 | 否 |
| `legacy/competitions/mcm/` | 历史竞赛材料，未来可迁移扩展。 | 否 |
| `legacy/competitions/diangong/` | 历史竞赛材料，未来可迁移扩展。 | 否 |
| `legacy/templates/latex/mcm/` | 历史 LaTeX 模板，未来可迁移扩展。 | 否 |
| `legacy/templates/latex/diangong/` | 历史 LaTeX 模板，未来可迁移扩展。 | 否 |

## Active CUMCM-only 边界

当前 active competition and output layer 只包含：

```text
competitions/cumcm/
templates/latex/cumcm/
templates/workspace/
```

历史 MCM 和 Diangong 材料没有删除，只移动到 `legacy/`。如果未来要恢复为 active workflow，必须先迁移到新版 workspace/output 契约、traceability、quality gate 和 CUMCM-only 之外的新入口说明。

## 使用规则

- active stage reference 不得把 `legacy/` 当作输入、输出、模板、工具或知识源。
- 维护者可以人工阅读 `legacy/` 做迁移审计。
- 用户建模运行时不得要求先执行 `legacy/scripts/`。
- active workflow 的质量判断来自 `references/`、`competitions/cumcm/`、`templates/workspace/` 和 `templates/latex/cumcm/`。
