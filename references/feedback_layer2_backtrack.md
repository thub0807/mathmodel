# Feedback Layer 2: Cross-Artifact Backtrack

## Purpose

Layer 2 checks whether earlier assumptions, notation, model choices, data handling, and results remain consistent after later evidence appears.

It performs targeted rework. It should not restart the whole workflow unless a high issue affects most artifacts.

## When To Call

Call Layer 2:

- after Stage 4 Verification and Sensitivity for each `q*`;
- before Stage 7 Final Integration;
- after Stage 7 if traceability reveals contradictions;
- during Stage 9 Final Review when the paper, traceability, and validation disagree.

## Read Files

For one `q*`:

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
```

For cross-question and final checks:

```text
workspace/output/question_index.md
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## Write Or Update Files

Layer 2 findings go into:

```text
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

If a source artifact changes, downstream summaries and traceability must be updated.

## Backtrack Matrix

| Later finding | Earlier artifact to check | Possible fix |
|---|---|---|
| validation fails a constraint | `model.md`, `assumptions.md`, `result.json` | revise model, mark result limited, or rerun |
| sensitivity overturns conclusion | `model.md`, `q*_summary.md`, `traceability.md` | weaken claim, change conclusion status, add limitation |
| unit mismatch appears | `notation.md`, `result.json`, figure/table indexes | fix units and regenerate affected outputs |
| hidden assumption appears during Build | `assumptions.md`, `review_note.md` | add assumption and rerun affected checks |
| model family no longer fits data | `candidates.md`, `model.md` | select alternative or record route risk |
| figure/table supports unsupported claim | figure/table index, `traceability.md`, paper | remove or relabel visual |
| final paper adds new claim | `traceability.md`, source `result.json` | remove claim or add verified source |
| two questions use conflicting symbols | `notation.md`, `final_results.md`, paper | harmonize notation and update text |

## Issue Record Format

Use this table:

```text
| issue id | severity | conflict type | evidence files | affected files | required rework | user confirmation | status |
|---|---|---|---|---|---|---|---|
```

## Rework Levels

| Level | Meaning | Action |
|---|---|---|
| Note | contradiction is minor and does not affect conclusions | record in `review_note.md` or final report |
| Patch | one or a few artifacts need edits | update source artifact and downstream traces |
| Rebuild | model or code output is unreliable | return to Plan or Build for the affected `q*` |
| Remove claim | evidence cannot support paper use | remove from paper and mark in `traceability.md` |

## Manual And AP Behavior

Manual mode:

- Pause for user confirmation when rework level is `Rebuild`, when a selected model changes, or when a paper conclusion must be removed.
- List affected paths and the required decision.

AP mode:

- Apply `Note`, `Patch`, or `Remove claim` when evidence is clear.
- For `Rebuild`, continue only if the route is unambiguous; otherwise write `review_note.md` and preserve the limitation in final reports.

## Exit Criteria

Layer 2 is complete when:

- every high contradiction is fixed, downgraded with evidence, or marked blocking;
- downstream files no longer present obsolete claims;
- `traceability.md` reflects the current source of each paper claim;
- `quality_report.md` records remaining risk.
