# Reviewer Summary After Knowledge Recovery

## Purpose

This summary helps a reviewer understand what changed after the knowledge-layer recovery work and where to inspect the active Skill.

No behavior is defined here. The authoritative runtime files remain `SKILL.md`, `references/`, `competitions/`, and `templates/`.

## Problems Addressed

This recovery pass addressed five main problems:

1. The new Skill had become mostly a workflow skeleton.
   - Stage files defined inputs and outputs, but the modeling, writing, and review knowledge from the original Skill was not active.

2. `templates/workspace/` was carrying too much responsibility.
   - It is now positioned as an artifact contract library, not a modeling method library, writing guide, or formal LaTeX template source.

3. Original modeling knowledge had been misclassified as legacy.
   - Model catalog, rubrics, feedback layers, and old stage knowledge were restored into active `references/` with workspace-output semantics.

4. `competitions/cumcm/` was not connected strongly enough to active workflow.
   - It is now the active CUMCM writing-quality layer for Stage 8 and Stage 9.

5. The CUMCM LaTeX template was missing.
   - `templates/latex/cumcm/cumcmthesis/` now contains `cumcmthesis.cls`, `example.tex`, and README.

## Active Three-Layer Structure

### 1. Workflow Control Layer

Controls stage order, fixed paths, modes, and artifact lifecycle.

```text
SKILL.md
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
references/stage_00_workspace_audit.md
...
references/stage_09_final_review.md
```

### 2. Modeling And Quality Layer

Provides model selection, rubrics, feedback review, traceability, and quality gates.

```text
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
references/result_traceability.md
references/quality_gate.md
```

### 3. Competition And Output Layer

Provides CUMCM writing-quality knowledge, formal LaTeX assets, and output artifact contracts.

```text
competitions/cumcm/
templates/latex/cumcm/cumcmthesis/
templates/workspace/
```

## Execution Chain From `problem.md` To `paper.pdf`

| Stage | Key inputs | Knowledge read | Key outputs |
|---|---|---|---|
| Stage 0 Workspace Audit | `workspace/problem/problem.md`, `reference.pdf`, images, attachments | `workspace_protocol.md` | `problem_audit.md`, `material_index.md` |
| Stage 1 Question Decomposition | `problem.md`, audit, material index | stage reference, rubrics as needed | `question_index.md`, `workspace/output/q*/` |
| Stage 2 Per-Question Plan | question index, audit, material index | `model_catalog.md`, `rubrics.md`, Layer 1 critic | `analysis.md`, `candidates.md`, `model.md`, `assumptions.md`, `notation.md`, `data_recon.md`, optional warnings/review note |
| Stage 3 Per-Question Build | Plan files | rubrics, Layer 1 critic | `code/`, `result.json`, `run.log` |
| Stage 4 Verification And Sensitivity | result, run log, model, assumptions, notation | rubrics, Layer 1 critic, Layer 2 backtrack | `validation.md`, `sensitivity.md` |
| Stage 5 Figures And Tables | result, validation, sensitivity, code | CUMCM formats, winning patterns, anti-patterns | figure and table indexes |
| Stage 6 Per-Question Summary | Plan, result, validation, sensitivity, visual indexes | rubrics, Layer 1 critic, CUMCM writing anchors | `q*_summary.md` |
| Stage 7 Final Integration | all summaries, result files, visual indexes, assumptions, notation | traceability, quality gate, Layer 2 backtrack | `final_results.md`, final visual indexes, `traceability.md` |
| Stage 8 Paper Generation | summaries, final results, traceability, visual indexes | CUMCM paper skeleton, abstract template, winning patterns, phrase bank, anti-patterns, distilled structures/formats | `paper.md`, `paper.tex`, `paper.pdf`, `source/` |
| Stage 9 Final Review | paper artifacts, traceability, final results, validation/sensitivity | rubrics, all feedback layers, CUMCM anti-patterns, empirical materials | `review_report.md`, `anonymity_report.md`, `quality_report.md` |

## Original Skill Capabilities Restored

Restored active capabilities:

- `model_catalog`: model family catalog, task-to-model mapping, candidate model strategy.
- `rubrics`: quality dimensions and pass/partial/fail review standards.
- Feedback layers: local critic, cross-artifact backtrack, panel review, calibration.
- Model selection: at least three candidates or explicit shortage reason, comparison matrix, naming variants, toy demo plan.
- Robustness: sanity checks, baseline comparison, boundary tests, parameter perturbation, joint perturbation, instability boundary.
- Writing: CUMCM skeleton, abstract strategy, phrase bank, distilled structures and formats.
- Review: anti-pattern checks, panel review, calibration, judge-perspective review.
- CUMCM materials: high-score patterns, anti-patterns, empirical thresholds, formatting habits.
- LaTeX template: formal `cumcmthesis` assets restored.

## Old Workflow Removed Or Isolated

Removed from active workflow or isolated under `legacy/`:

- `decision_log`
- `cwd/state`
- `score_artifact` as active dependency
- multi-problem or multi-question selection flow
- problem recommendation behavior
- old harness compatibility workflow

Legacy files remain as historical snapshots for migration audit only.

## Recommended Review Order

1. `SKILL.md`
2. `references/workflow.md`
3. `references/stage_02_per_question_plan.md`
4. `references/stage_08_paper_generation.md`
5. `references/stage_09_final_review.md`
6. `references/model_catalog.md`
7. `references/rubrics.md`
8. `references/feedback_layer3_panel.md`
9. `competitions/cumcm/README.md`
10. `templates/latex/cumcm/cumcmthesis/README.md`
11. `templates/workspace/README.md`
12. `docs/final_knowledge_recovery_audit.md`

## Highest-Value Files To Inspect First

1. `SKILL.md`
2. `references/workflow.md`
3. `references/stage_02_per_question_plan.md`
4. `references/stage_08_paper_generation.md`
5. `references/stage_09_final_review.md`

These five files reveal whether the Skill entry, workflow map, model planning, paper generation, and final review are coherent.

## Remaining Risks

### Needs Manual Dry Run

- Run Stage 0-9 on a small `workspace/problem/problem.md`.
- Confirm Manual mode pause behavior is ergonomic.
- Confirm `result.json`, `run.log`, validation, sensitivity, and traceability are easy to fill.

### Possibly Thin Templates

- Some `templates/workspace/q/*` files may still be structurally correct but sparse.
- The final quality, review, and traceability templates should be checked against a real paper draft.

### Possibly Thin Stages

- Stage 5-7 should be tested with real figures, tables, summaries, and cross-question dependencies.
- Stage 8 should be tested with a complete CUMCM-style draft.
- Stage 9 should be tested for whether feedback layers produce useful actionable reports.

### Validation Script Decision

The workflow currently defines `result.schema.json`, traceability requirements, and quality gates. A future pass could add an optional validation script for:

- `result.json` schema validation;
- required output presence;
- traceability row completeness;
- stale or missing `run.log` records.

This should remain optional unless the project decides scripts should become active workflow tools.

