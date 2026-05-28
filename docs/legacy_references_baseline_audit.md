# Legacy References Baseline Audit

Date: 2026-05-28

Scope: audit only. This report compares `legacy/references/` with the active `references/` layer and does not modify active references, `SKILL.md`, workflow files, or legacy files.

## Summary

`mathmodel-md-copilot/legacy/references/` is confirmed as the original dense references snapshot, not the previously simplified legacy layer.

Evidence:
- Every file in `mathmodel-md-copilot/legacy/references/`, including `papers/`, has an identical SHA256 hash to the corresponding file in `refs-mathmodel-skill/references/`.
- The legacy layer keeps the original dense stage files, feedback layers, `harness_compat.md`, and `papers/` notes.
- Legacy file sizes are consistently larger than active references, especially model catalog, rubrics, critic/panel layers, writing, robustness, and subproblem-loop guidance.

Line counts below use physical lines, including blank lines. Nonblank counts are included where useful for density checks.

## Legacy References File Inventory

| File | Lines | Nonblank lines |
|---|---:|---:|
| `feedback_layer1_critic.md` | 393 | 325 |
| `feedback_layer2_backtrack.md` | 183 | 139 |
| `feedback_layer3_panel.md` | 387 | 303 |
| `feedback_layer4_calibration.md` | 202 | 149 |
| `harness_compat.md` | 139 | 97 |
| `model_catalog.md` | 332 | 249 |
| `papers/_DOWNLOAD_REPORT.md` | 25 | 17 |
| `papers/README.md` | 50 | 36 |
| `rubrics.md` | 270 | 200 |
| `stage_00_kickoff.md` | 238 | 180 |
| `stage_01_problem_selection.md` | 181 | 131 |
| `stage_02_analysis.md` | 194 | 143 |
| `stage_03_model_selection.md` | 214 | 156 |
| `stage_04_foundation.md` | 173 | 125 |
| `stage_05_subproblem_loop.md` | 359 | 270 |
| `stage_06_robustness.md` | 231 | 172 |
| `stage_07_evaluation.md` | 192 | 146 |
| `stage_08_writing.md` | 348 | 245 |
| `stage_09_review.md` | 249 | 190 |

## Focus File Line Counts

| Legacy focus file | Legacy lines | Active corresponding file | Active lines | Assessment |
|---|---:|---|---:|---|
| `model_catalog.md` | 332 | `model_catalog.md` | 158 | Active is much thinner. |
| `rubrics.md` | 270 | `rubrics.md` | 138 | Active is much thinner. |
| `feedback_layer1_critic.md` | 393 | `feedback_layer1_critic.md` | 143 | Active is much thinner. |
| `feedback_layer2_backtrack.md` | 183 | `feedback_layer2_backtrack.md` | 113 | Active is thinner. |
| `feedback_layer3_panel.md` | 387 | `feedback_layer3_panel.md` | 179 | Active is much thinner. |
| `feedback_layer4_calibration.md` | 202 | `feedback_layer4_calibration.md` | 122 | Active is thinner. |
| `stage_02_analysis.md` | 194 | no exact active file; closest `stage_02_per_question_plan.md` | 143 | Active stage was redesigned and is thinner. |
| `stage_03_model_selection.md` | 214 | no exact active file; closest `stage_02_per_question_plan.md` / `stage_03_per_question_build.md` | 143 / 133 | Active model-selection guidance is much thinner and split. |
| `stage_05_subproblem_loop.md` | 359 | closest `stage_03_per_question_build.md` / `stage_06_per_question_summary.md` | 133 / 119 | Active loses much of the recursive Qi loop detail. |
| `stage_06_robustness.md` | 231 | `stage_04_verification_sensitivity.md` | 147 | Active is thinner. |
| `stage_08_writing.md` | 348 | `stage_08_paper_generation.md` | 144 | Active is much thinner. |
| `stage_09_review.md` | 249 | `stage_09_final_review.md` | 157 | Active is thinner. |

## Active Files That Are Clearly Thinner Than Legacy

Largest gaps:
- `feedback_layer1_critic.md`: active 143 lines vs legacy 393 lines.
- `feedback_layer3_panel.md`: active 179 lines vs legacy 387 lines.
- `stage_08_paper_generation.md`: active 144 lines vs legacy `stage_08_writing.md` 348 lines.
- `stage_03_per_question_build.md` / `stage_06_per_question_summary.md`: active equivalents are much thinner than legacy `stage_05_subproblem_loop.md` at 359 lines.
- `model_catalog.md`: active 158 lines vs legacy 332 lines.
- `rubrics.md`: active 138 lines vs legacy 270 lines.
- `stage_04_verification_sensitivity.md`: active 147 lines vs legacy `stage_06_robustness.md` 231 lines.
- `stage_09_final_review.md`: active 157 lines vs legacy `stage_09_review.md` 249 lines.

The active layer is cleaner and better aligned to v1.2's single-workspace Markdown-first architecture, but it has shed substantial reusable modeling, review, writing, and calibration knowledge.

## Old State-Machine Dependencies Found In Legacy

Search terms audited: `decision_log`, `cwd/state`, `score_artifact`, `question_manifest`, `stage.1.selected`, `problem selection`, `A-E`, `A-F`.

| Dependency | Legacy files containing it |
|---|---|
| `decision_log` | `feedback_layer1_critic.md`, `feedback_layer2_backtrack.md`, `feedback_layer3_panel.md`, `feedback_layer4_calibration.md`, `harness_compat.md`, `rubrics.md`, `stage_00_kickoff.md`, `stage_01_problem_selection.md`, `stage_02_analysis.md`, `stage_03_model_selection.md`, `stage_04_foundation.md`, `stage_05_subproblem_loop.md`, `stage_06_robustness.md`, `stage_07_evaluation.md`, `stage_08_writing.md`, `stage_09_review.md` |
| `cwd/state` | `feedback_layer3_panel.md`, `harness_compat.md`, `stage_00_kickoff.md` |
| `score_artifact` | `feedback_layer1_critic.md`, `harness_compat.md`, `rubrics.md`, `stage_05_subproblem_loop.md` |
| `question_manifest` | none found |
| `stage.1.selected` | `stage_02_analysis.md` |
| `problem selection` | no exact phrase found; concept appears in `stage_01_problem_selection.md` |
| `A-E` | `stage_00_kickoff.md`, `stage_01_problem_selection.md` |
| `A-F` | `stage_00_kickoff.md`, `stage_01_problem_selection.md`, `papers/_DOWNLOAD_REPORT.md` |

Also legacy-only or old-harness signals:
- `harness_compat.md` is explicitly old harness compatibility material and should remain isolated unless selectively mined for agent portability concepts.
- `stage_00_kickoff.md` asks for year, deadline, team size, and initializes `state/decision_log.json`, which conflicts with current v1.2 requirements.
- `stage_01_problem_selection.md` is multi-problem selection logic and conflicts with the fixed `workspace/problem/problem.md` input contract.
- `rubrics.md` and feedback files depend on old scorer conventions such as dim whitelist, score artifacts, and stage-numbered JSON state.

## Legacy Content Suitable For Migration

Recommended to migrate after adapting to v1.2 file contracts:
- Modeling methods: `model_catalog.md`, especially model-family map, hybrid model patterns, and concrete model applicability notes.
- Model selection: `stage_03_model_selection.md`, especially candidate generation, decision matrix, toy-demo validation, naming variants, and red-team model attacks.
- Subproblem solve loop: `stage_05_subproblem_loop.md`, especially model completion, solve implementation, result validation, local sensitivity, physical interpretation, per-question refinement, and Qi-level handoff.
- Robustness and sensitivity: `stage_06_robustness.md`, especially parameter selection, perturbation tiers, joint perturbation, visualization, stability table, and failure warnings.
- Writing methods: `stage_08_writing.md`, especially section-by-section writing prompts, summary-last discipline, formula/result traceability, appendix code presentation, and anti-empty prose rules.
- Review methods: `stage_09_review.md`, especially anti-pattern pass, visual polish pass, panel review, bottleneck mapping, and final readiness criteria.
- Rubric: `rubrics.md`, especially stage quality dimensions, threshold concepts, empirical anchors, and competition-quality criteria after removing old scorer interfaces.
- Critic / panel / calibration: `feedback_layer1_critic.md`, `feedback_layer3_panel.md`, `feedback_layer4_calibration.md`, especially review lenses, issue severity, panel personas, calibration questions, and anti-packaging checks.
- Backtrack method: `feedback_layer2_backtrack.md`, but only as artifact-consistency review rather than old `decision_log` rollback.

## Legacy Content That Should Not Be Migrated

Do not migrate directly:
- Old state machine: `decision_log`, `state/decision_log.json`, stage-numbered JSON mutation, `stage.1.selected`.
- Multi-topic / multi-problem selection: `stage_01_problem_selection.md`, `A-E`, `A-F`, problem-letter comparison, rejected-alternative scoring.
- Old scoring interface: `scripts/score_artifact.py`, dim whitelist coupling, JSON scorer contracts, aggregate Qi script calls.
- Old harness compatibility: `harness_compat.md`, `cwd/state`, cross-harness state transfer, old Claude/Codex harness assumptions.
- Startup questions forbidden by v1.2: year, deadline, team size, division of labor.
- Any flow that makes `reference.pdf` a source of truth rather than audit-only material.

## Recommended Migration Priority

1. Highest priority: `model_catalog.md` and `stage_03_model_selection.md`.
   These restore the modeling and selection depth most directly missing from the active knowledge layer.

2. Highest priority: `stage_05_subproblem_loop.md`.
   Migrate the recursive per-question solve/verify/refine loop into the current per-question build and summary stages without bringing back `decision_log` or scorer scripts.

3. High priority: `stage_06_robustness.md`.
   Fold robust/sensitivity detail into `stage_04_verification_sensitivity.md` and the active verification gate.

4. High priority: `stage_08_writing.md` and `stage_09_review.md`.
   Restore the practical writing and final-review craft into `stage_08_paper_generation.md` and `stage_09_final_review.md`.

5. Medium priority: `rubrics.md`, `feedback_layer1_critic.md`, `feedback_layer3_panel.md`, `feedback_layer4_calibration.md`.
   Migrate review dimensions and calibration methods after defining the active v1.2 issue/result contracts.

6. Low priority / mostly quarantine: `stage_00_kickoff.md`, `stage_01_problem_selection.md`, `harness_compat.md`.
   These are useful for historical context but are dominated by old state-machine and multi-problem assumptions.

## Baseline Verdict

Legacy snapshot status: confirmed original dense snapshot.

Largest active knowledge gaps:
- `feedback_layer1_critic.md`
- `feedback_layer3_panel.md`
- `stage_05_subproblem_loop.md`
- `stage_08_writing.md`
- `model_catalog.md`
- `rubrics.md`
- `stage_06_robustness.md`
- `stage_09_review.md`

Next stage recommendation: begin selective migration from modeling and model-selection knowledge first, then subproblem loop and robustness. Each migration should rewrite legacy references into the active v1.2 protocol: fixed `workspace/problem/problem.md`, Markdown-first artifacts, Python language lock, no `submit.zip`, no old state machine, no regex-based question detection, and no old scorer/harness dependency.
