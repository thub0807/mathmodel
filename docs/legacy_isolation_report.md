# Legacy Isolation Report

## Scope

This report checks that restored knowledge is active under `references/` and that historical snapshots under `legacy/` do not drive the active workflow.

Active areas checked:

```text
SKILL.md
AGENTS.md
agents/openai.yaml
references/
competitions/
templates/workspace/
templates/latex/
```

## Active Legacy References

| Match | Location | Judgment | Action |
|---|---|---|---|
| `legacy/` | `SKILL.md` | brief legacy isolation note, not workflow input | kept |
| `legacy/` | `AGENTS.md` | developer/project maintenance note | kept |

No active workflow file references `legacy/` as an input, output, template, tool, or required knowledge source.

## Active Old Keyword Residue

Checked keywords:

```text
decision_log
cwd/state
score_artifact
question_manifest
A-E
A-F
problem selection
multi-question selection
harness
```

| Keyword | Active residue after cleanup | Judgment |
|---|---|---|
| `decision_log` | none | clear |
| `cwd/state` | none | clear |
| `score_artifact` | none | clear |
| `question_manifest` | none | clear |
| `A-E` | none | clear |
| `A-F` | none | clear |
| `problem selection` | none | clear |
| `multi-question selection` | none | clear |
| `harness` | none | clear |

## Rewritten Active References

The following active files had old execution wording rewritten:

```text
competitions/mcm/README.md
competitions/mcm/empirical_notes.md
competitions/mcm/empirical.json
competitions/diangong/empirical_notes.md
competitions/diangong/empirical.json
```

Changes made:

- MCM problem-letter wording no longer presents old letter ranges as an active routing mechanism.
- Seed empirical materials no longer mention old scoring tooling.
- MCM and Diangong empirical notes now instruct Stage 8/9 and feedback layers to treat seed thresholds as reference material.
- Diangong workflow timing notes were rewritten as workspace artifact risk guidance.

## Legacy Area Explanation

`legacy/README.md` now states:

- legacy files are for migration audit, historical comparison, and manual reference only;
- active workflow does not read `legacy/`;
- restored knowledge has active workspace-output versions under `references/`;
- older execution assumptions remain only as historical snapshots.

## Preserved Historical Files

No legacy files were deleted. The following restored-knowledge snapshots remain under `legacy/references/` for audit comparison:

```text
model_catalog.md
rubrics.md
feedback_layer1_critic.md
feedback_layer2_backtrack.md
feedback_layer3_panel.md
feedback_layer4_calibration.md
stage_02_analysis.md
stage_03_model_selection.md
stage_05_subproblem_loop.md
stage_06_robustness.md
stage_08_writing.md
stage_09_review.md
```

Other legacy references and scripts are also preserved as historical material.

## Items Requiring Human Judgment

- Whether `legacy/references/harness_compat.md` should remain long-term or move to a deeper archive is a maintainer decision.
- `competitions/mcm/` and `competitions/diangong/` are still seed-quality competition layers; their empirical thresholds need human caution.
- If future workflow documents intentionally mention `legacy/`, they should do so only as migration notes, not active dependencies.

