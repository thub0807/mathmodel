# Feedback Layer 1: Local Quality Critic

## Purpose

Layer 1 checks one artifact set at a time. It catches local quality issues before they spread into later stages.

Use it as an Agent or human review prompt. It writes findings into workspace artifacts; it does not call any external scoring tool.

## When To Call

Call Layer 1 after each of these moments:

| Moment | Primary target |
|---|---|
| After Stage 2 Plan for a `q*` | plan files before Build |
| After Stage 3 Build | `result.json` and run evidence |
| After Stage 4 Verification | validation and sensitivity completeness |
| After Stage 6 Summary | paper-ready per-question summary |
| During Stage 8 Paper Generation | draft paper sections |
| During Stage 9 Final Review | final reports and paper artifacts |

## Read Files

For a `q*` review, read the files that exist among:

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
```

For final paper review, read:

```text
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

Also consult:

```text
references/rubrics.md
references/model_catalog.md          # for Plan and model fitness checks
competitions/cumcm/anti_patterns.md  # when doing CUMCM-style final review
```

## Write Or Update Files

Depending on the stage, write findings into:

```text
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

Do not create hidden review state. Findings must be visible in workspace output files.

## Local Critic Checklist

### Plan Critic

- Does `analysis.md` state target, input, output, dependency, and evaluation criterion?
- Does `candidates.md` compare structurally different routes?
- Does `model.md` define variables, objective or metric, constraints, algorithm, and expected `result.json` fields?
- Are assumptions source-backed and impact-aware?
- Are symbols unique, unit-aware, and used consistently?
- Is data preprocessing auditable?
- Is there a baseline or sanity-check route?

### Build Critic

- Does `run.log` identify commands, inputs, outputs, and failures?
- Does `result.json` contain every hard number intended for later use?
- Is `result.json.status` justified by the run and validation plan?
- Are random seeds, solver settings, or heuristic choices reproducible?
- Do results respect declared units and constraints?

### Validation And Sensitivity Critic

- Are constraints, boundary cases, and dimensions checked?
- Is there a baseline, ablation, cross-method comparison, or manual calculation?
- Are sensitivity parameters important rather than arbitrary?
- Are perturbation ranges plausible?
- Does sensitivity state paper impact: stable, conditionally stable, or unstable?

### Writing Critic

- Are paper claims traceable to final traceability rows?
- Does the abstract avoid unsupported hard numbers?
- Are limitations from `partial` results preserved?
- Do figures and tables support specific conclusions?
- Does the self-evaluation state weaknesses with consequences and possible fixes?

## Issue Record Format

Use this table shape:

```text
| issue id | severity | file | finding | required fix | paper impact | status |
|---|---|---|---|---|---|---|
```

Severity must be `High`, `Medium`, or `Low`.

## Triggering Rework

Layer 1 triggers rework when:

- a high issue invalidates a selected model route;
- a result is not reproducible or not present in `result.json`;
- validation contradicts the claimed status;
- sensitivity makes a conclusion unusable;
- final paper contains untraceable or overstated claims.

Rework should update the source artifact first, then all downstream summaries and traceability records.

## Manual And AP Behavior

Manual mode:

- Pause when a high issue changes the model route, invalidates a result, or blocks paper use.
- List only the affected file paths and the required decision.

AP mode:

- Continue only if the issue is explicitly recorded in `review_note.md`, `warnings.md`, `validation.md`, or final reports.
- Mark paper-facing limitations in `traceability.md` and `quality_report.md`.
