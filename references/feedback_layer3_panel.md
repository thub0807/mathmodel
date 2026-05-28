# Feedback Layer 3: Final Panel Review

## Purpose

Layer 3 performs a multi-view final review. It is used near the end of Stage 9 to find issues that a single linear checklist may miss.

If independent sub-agents or parallel review capability are available, run the panel views independently and merge findings. Otherwise run them serially with separated notes.

## When To Call

Call Layer 3 after a draft final paper and traceability set exist:

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

It may also be called after a major rewrite of paper sections.

## Read Files

```text
workspace/output/problem_audit.md
workspace/output/question_index.md
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
references/rubrics.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/winning_patterns.md
```

## Write Or Update Files

Panel output is merged into:

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

If a panel finding changes claim eligibility, update:

```text
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
```

## Panel Views

### 1. Mathematical Rigor

Checks:

- variables, constraints, assumptions, and units;
- derivation clarity;
- boundary cases and feasibility;
- whether the conclusion follows from the model.

Typical high issues:

- objective and constraints do not match the stated question;
- a formula uses undefined or conflicting symbols;
- result magnitude is implausible and not explained.

### 2. Model Innovation And Fitness

Checks:

- whether the model is appropriate for the data and task;
- whether candidate rejection is credible;
- whether the chosen model has a clear advantage over baseline;
- whether model naming and framing are specific.

Typical high issues:

- model is generic and mismatched;
- no baseline or alternative route is present;
- claimed innovation is only wording, not method or insight.

### 3. Code And Evidence Correctness

Checks:

- code outputs match `result.json`;
- run logs explain inputs and failures;
- figures and tables are reproducible;
- validation and sensitivity support the result status.

Typical high issues:

- paper number does not appear in `result.json`;
- validation contradicts final claim;
- figure or table has no data source.

### 4. Writing And Presentation

Checks:

- abstract contains verified method and result signals;
- sections follow a readable CUMCM-style structure;
- figures and tables are introduced and interpreted;
- limitations are honest and visible.

Typical high issues:

- abstract overclaims;
- final paper hides `partial` limitations;
- paper relies on vague phrases rather than evidence.

### 5. Judge Perspective

Checks:

- whether a reviewer can understand contribution in the first read;
- whether answers to all sub-questions are easy to find;
- whether the paper avoids common CUMCM anti-patterns;
- whether the final verdict is honest.

Typical high issues:

- answer to a required sub-question is missing;
- final results are scattered and not traceable;
- paper would look incomplete under quick review.

## Panel Finding Format

Each panel view should produce:

```text
panel view | verdict | top issues | must fix | nice to fix | affected files
```

Verdict values:

```text
PASS
PARTIAL
FAIL
```

Merge findings into a single table in `review_report.md`:

```text
| panel | verdict | issue | severity | affected files | required fix | status |
|---|---|---|---|---|---|---|
```

## Aggregation Rule

Final panel verdict:

- `FAIL` if any panel finds an unresolved high issue that invalidates a required answer, traceability, or anonymity.
- `PARTIAL` if high issues are limited and explicitly carried into paper limitations or final reports.
- `PASS` only when all panel views are pass or low-risk partial with no unsupported claims.

## Manual And AP Behavior

Manual mode:

- Pause when the panel requests removal of a conclusion, major paper rewrite, model rebuild, or anonymity action.
- List affected final report and paper paths.

AP mode:

- Apply clear claim removals or limitation labels automatically.
- Record all unresolved panel issues in `quality_report.md`; AP mode must not suppress final findings.
