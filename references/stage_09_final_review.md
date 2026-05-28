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
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_formats.md
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

1. Run or simulate Layer 1 local critic.
   - Check final paper, final results, traceability, validation, sensitivity, figure/table indexes, and report completeness.
   - Record findings in `review_report.md` and blocking verdict issues in `quality_report.md`.
2. Run or simulate Layer 2 backtrack.
   - Check whether final paper claims contradict earlier assumptions, notation, model choices, results, validation, or sensitivity.
   - If a claim is unsupported, remove it, limit it, or mark it blocking.
3. Run or simulate Layer 3 panel review.
   - Review from mathematical rigor, model fitness, evidence correctness, writing presentation, and judge perspective.
   - Use independent parallel review if available; otherwise run the panel views serially.
4. Run or simulate Layer 4 calibration.
   - Check whether polished writing is stronger than the evidence.
   - Downgrade overconfident claims and abstract eligibility when needed.
5. Check CUMCM abstract quality.
   - Compare against `competitions/cumcm/abstract_template.md`.
   - Ensure the abstract contains concrete methods and hard results when evidence allows.
   - Abstract numbers must be traceable and must not have validation status `fail`.
6. Check result and visual quality.
   - Key results should include hard numbers, units, and source fields.
   - Figures and tables must serve conclusions, not just decorate the paper.
   - Captions, notes, and references should follow `distilled_formats.md`.
7. Check model and formula consistency.
   - Model names should be clear and consistent.
   - Formulas and variables should match notation and paper text.
   - Units and symbol meanings should not drift across sections.
8. Check anti-patterns and quick judge readability.
   - Compare against `competitions/cumcm/anti_patterns.md`.
   - Ask whether a judge can grasp the contribution in 30 seconds from title, abstract, figures, and final results.
9. Write `anonymity_report.md`.
   - Check personal, school, team, local path, metadata, source comment, and hidden identifier risks.
10. Write `review_report.md`.
   - Include question coverage, paper consistency, panel findings, anti-pattern hits, figure/table issues, traceability issues, and required fixes.
11. Write `quality_report.md`.
   - Include stage completeness, result status, validation status, sensitivity status, figure/table citation, paper traceability, anonymity, feedback-layer findings, and final verdict.
12. Mark final verdict as `PASS`, `PARTIAL`, or `FAIL`.

## Output Contract

`review_report.md` must include:

```text
question coverage
paper consistency
L1 local critic findings
L2 backtrack findings
L3 panel findings
L4 calibration findings
anti-pattern hits
figure and table issues
required fixes
```

`anonymity_report.md` must include:

```text
checked artifacts
identifier risks
metadata or path risks
required user action
```

`quality_report.md` must include:

```text
stage completeness
result status summary
validation and sensitivity status
traceability verdict
paper quality verdict
anonymity verdict
feedback-layer verdicts
final verdict: PASS / PARTIAL / FAIL
blocking issues
```

## Quality Gate

Final `PASS` requires:

- no unsupported hard numbers in abstract or body;
- no validation-failed claim used as a conclusion;
- every figure/table claim traces to a source;
- model names, formulas, variables, and units are consistent;
- high anti-pattern hits are fixed;
- anonymity risks are cleared or explicitly reported;
- feedback-layer findings are resolved or carried into final verdict.

## Exit Conditions

- All required final review reports exist.
- `quality_report.md` states the final verdict and blocking issues.
- Any remaining unverified or untraceable claim is removed, limited, or explicitly reported.

## Failure Handling

- If anonymity risk cannot be fixed automatically, report it and ask for user action.
- If paper traceability fails, mark final verdict `PARTIAL` or `FAIL` and identify affected claims.
- If feedback layers find unresolved high issues, mark final verdict `PARTIAL` or `FAIL`.
- If the judge-perspective review cannot identify the contribution quickly, require abstract or final-result revision.

## Manual Mode Behavior

Final checkpoint: list review report, anonymity report, quality report, and paper artifact paths.

## AP Mode Behavior

Same as Manual for final reporting; AP mode does not suppress final review findings.
