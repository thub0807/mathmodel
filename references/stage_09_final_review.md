# Stage 9: Final Review

## Purpose

Perform final completeness, anonymity, traceability, and quality review.

## Required Inputs

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

## Required Outputs

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

## Templates

```text
templates/workspace/final/review_report.md
templates/workspace/final/anonymity_report.md
templates/workspace/final/quality_report.md
```

## Entry Conditions

- Stage 8 has produced paper artifacts or recorded a PDF failure.
- `traceability.md` exists and covers paper-facing claims.

## Procedure

1. Write `review_report.md` checking question coverage, result limitations, figure/table citations, and paper consistency.
2. Write `anonymity_report.md` checking personal, school, team, path, metadata, and hidden identifier risks.
3. Write `quality_report.md` checking stage completeness, result status, validation status, sensitivity status, figure/table citation, paper traceability, anonymity, and final verdict.
4. Mark final verdict as `PASS`, `PARTIAL`, or `FAIL`.

## Exit Conditions

- All required final review reports exist.
- `quality_report.md` states the final verdict and blocking issues.
- Any remaining unverified or untraceable claim is removed, limited, or explicitly reported.

## Failure Handling

- If anonymity risk cannot be fixed automatically, report it and ask for user action.
- If paper traceability fails, mark final verdict `PARTIAL` or `FAIL` and identify affected claims.

## Manual Checkpoint Behavior

Final checkpoint: list review report, anonymity report, quality report, and paper artifact paths.

## AP Mode Behavior

Same as Manual for final reporting; AP mode does not suppress final review findings.
