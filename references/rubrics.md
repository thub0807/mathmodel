# Quality Rubrics

## Purpose

This file defines active human/Agent review standards for the workspace workflow. It supports:

```text
workspace/output/q*/review_note.md
workspace/output/q*/validation.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

It is not a scoring program. Use it to write concrete findings, limitations, and required fixes.

## Verdict Scale

Use the workflow's final verdict words:

| Verdict | Meaning |
|---|---|
| `PASS` | Evidence is complete enough for the next stage or final paper use. |
| `PARTIAL` | Work is usable only with stated limitations. The limitation must appear in downstream files. |
| `FAIL` | Work cannot support paper claims until corrected or replaced. |

For local checks, use severity:

| Severity | Meaning | Required action |
|---|---|---|
| High | Could invalidate result, traceability, anonymity, or core answer | Stop or pause; fix before promotion |
| Medium | Weakens confidence or presentation but may be recoverable | Record and fix when practical |
| Low | Polish, clarity, or small completeness issue | Record in review notes or final report |

## Core Quality Dimensions

| Dimension | PASS signal | PARTIAL / FAIL signal | Record in |
|---|---|---|---|
| Problem understanding | Each `q*` maps to a clear task, input, output, and dependency | unclear decomposition, missing material, ambiguous target | `problem_audit.md`, `question_index.md`, `analysis.md` |
| Model fitness | selected model matches task type and data; rejected candidates have reasons | model chosen by habit, no baseline, no feasibility check | `candidates.md`, `model.md`, `review_note.md` |
| Assumptions and notation | assumptions are source-backed; symbols have units and domains | hidden assumptions, duplicate symbols, missing units | `assumptions.md`, `notation.md` |
| Data discipline | source files, preprocessing, missing values, and limitations are explicit | unexplained data reconstruction, silent row/column changes | `data_recon.md`, `run.log`, `validation.md` |
| Result traceability | hard numbers appear in `result.json` and flow to traceability | paper claim has no source field or validation status | `result.json`, `traceability.md`, `quality_report.md` |
| Verification | constraints, boundary cases, baseline or cross-method comparison are checked | only reports answer, no sanity check | `validation.md` |
| Sensitivity | important parameters have perturbation ranges and conclusion impact | sensitivity absent or only decorative | `sensitivity.md` |
| Figure/table quality | every visual has data source, purpose, and supported claim | chart without source, default-looking visual, unreferenced table | figure/table indexes, `review_report.md` |
| Writing quality | abstract and body use verified claims, explain meaning, and avoid vague praise | hard numbers missing, conclusions overstated, weak self-critique | `paper.md`, `paper.tex`, `review_report.md` |
| Final safety | anonymity, completeness, traceability, and verdict are explicit | hidden identifiers, unsupported claims, missing reports | `anonymity_report.md`, `quality_report.md` |

## Stage-Oriented Review Standards

### Workspace Audit

PASS when `problem.md` is understood directly, materials are indexed, and any missing image or attachment is recorded.

FAIL when a required problem file is absent or the task cannot be understood from available materials.

### Question Decomposition

PASS when every `q*` has goal, input, output, dependency, and material mapping.

PARTIAL when a question is split reasonably but an ambiguity remains and is recorded.

FAIL when a required task is omitted or two unrelated tasks are merged so later evidence cannot be traced.

### Per-Question Plan

PASS when `analysis.md`, `candidates.md`, `model.md`, `assumptions.md`, `notation.md`, and `data_recon.md` jointly define a buildable route.

Medium or high issues:

- only one model candidate is considered when alternatives are natural;
- the baseline is missing;
- the selected model cannot produce structured `result.json` fields;
- assumptions are not tied to problem text, data, or domain reasoning.

### Build And Result

PASS when code, run log, and `result.json` agree, and status is one of `pass`, `partial`, or `fail`.

High issues:

- a result appears in writing but not in `result.json`;
- random or heuristic output cannot be reproduced;
- units or dimensions conflict with `notation.md`;
- failed run is hidden instead of recorded.

### Verification And Sensitivity

PASS when validation includes constraint checks, boundary cases, and at least one baseline, ablation, cross-method comparison, or defensible manual calculation.

Sensitivity should identify important parameters, perturbation ranges, result changes, and whether the conclusion is stable.

FAIL when the main conclusion is contradicted by validation or sensitivity and downstream files still present it as reliable.

### Final Integration And Paper

PASS when `final_results.md` and `traceability.md` can support every paper-facing hard number, figure claim, table claim, assumption, and symbol.

High issues:

- abstract uses a number not allowed by `traceability.md`;
- final paper claims a `fail` result as a conclusion;
- CUMCM formal paper uses only a shallow fallback scaffold when the formal LaTeX template is available;
- limitations from `partial` results disappear in the final text.

### Final Review

PASS requires:

- all required stage artifacts exist or have a recorded limitation;
- all paper claims are traceable;
- anonymity check is complete;
- quality report states `PASS`, `PARTIAL`, or `FAIL`;
- high issues are fixed or explicitly blocking.

## CUMCM Quality Anchors

Use these as review anchors when writing a CUMCM-style paper:

- abstract contains concrete method and result signals, not only background;
- model names are specific enough to convey the contribution;
- assumptions are neither decorative nor unsupported;
- figures and tables explain result meaning, not just raw output;
- sensitivity has a real conclusion about robustness;
- model evaluation includes honest weaknesses and feasible improvements;
- appendix code or source notes are reproducible enough for audit.

## Recording Issues

Use this compact issue format in `review_note.md`, `validation.md`, `review_report.md`, or `quality_report.md`:

```text
issue id | severity | artifact | finding | required fix | downstream impact | status
```

Manual mode: pause when a high issue changes the selected route, invalidates a result, or blocks paper use.

AP mode: continue only when the issue is recorded in the relevant artifact and the downstream limitation is preserved.
