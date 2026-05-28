# Legacy Materials

Legacy files are not part of the active `mathmodel-copilot` workflow.

The active workflow entry points are:

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
templates/workspace/
```

Files under `legacy/` are retained only for migration audit, historical comparison, or manual reference. Do not load them during active modeling unless a maintainer is explicitly auditing the migration.

## Restored Knowledge Snapshots

Several files in `legacy/references/` are pre-refactor snapshots of knowledge that has already been restored into active `references/` with workspace-output semantics:

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

Active replacements live in:

```text
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
references/stage_01_question_decomposition.md
references/stage_02_per_question_plan.md
references/stage_03_per_question_build.md
references/stage_04_verification_sensitivity.md
references/stage_05_figures_tables.md
references/stage_06_per_question_summary.md
references/stage_07_final_integration.md
references/stage_08_paper_generation.md
references/stage_09_final_review.md
```

The legacy copies may still contain older execution assumptions, compatibility notes, old scoring utilities, or old stage names. They are intentionally preserved as historical snapshots only.

## Active Workflow Rule

Active workflow files must not reference `legacy/` as an input, output, template, tool, or knowledge source. If a restored concept is needed, use the active `references/`, `competitions/`, or `templates/` path instead.
