# Feedback Layer 4: Calibration And Anti-Packaging Check

## Purpose

Layer 4 checks whether the work is genuinely supported by evidence rather than merely looking polished. It protects against overconfident writing, decorative validation, and rubric gaming.

Use it as a final calibration pass, especially when the draft appears to pass all checklists too easily.

## When To Call

Call Layer 4:

- after Layer 1 and Layer 2 have few or no findings but the result feels weak;
- after Layer 3 returns `PASS` or mild `PARTIAL`;
- before final `PASS` in `quality_report.md`;
- whenever a paper section sounds stronger than its evidence.

## Read Files

```text
workspace/output/q*/analysis.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
references/rubrics.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/anti_patterns.md
```

## Write Or Update Files

```text
workspace/output/q*/review_note.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
workspace/output/final/traceability.md
```

If calibration reduces confidence in a claim, update paper text or traceability eligibility.

## Calibration Questions

### Evidence Reality

- Would the same conclusion still hold if a simple baseline were shown beside it?
- Are the most important numbers in `result.json` and validated?
- Does sensitivity test the parameters that actually drive the conclusion?
- Are uncertainty, infeasibility, or failure cases visible?

### Modeling Reality

- Is the chosen model more than a named formula?
- Are assumptions necessary and defensible?
- Does the model answer the question, or only produce an impressive-looking computation?
- Is there a clear reason the rejected candidates were worse?

### Writing Reality

- Does the abstract state verified results rather than promise quality?
- Are claims proportional to evidence?
- Are limitations written where a reader will see them?
- Does final paper structure help a judge locate each answer quickly?

### CUMCM Quality Reality

- Are figures and tables dense with meaning, not decorative?
- Does the paper explain physical, managerial, or practical meaning of results?
- Is model evaluation honest about weaknesses and cost of improvements?
- Does the conclusion avoid unsupported generalization?

## Anti-Packaging Signals

Treat these as medium or high issues:

| Signal | Risk | Typical fix |
|---|---|---|
| polished paper, weak `result.json` | writing outruns evidence | remove unsupported claims or rebuild result |
| many formulas, few constraints checked | mathematical decoration | add validation or simplify |
| sensitivity section repeats result | no robustness evidence | vary important parameters and report impact |
| abstract has hard numbers absent from traceability | unsupported headline | remove or trace |
| model name sounds novel but method is generic | presentation-only innovation | rename honestly or add real method detail |
| limitations appear only in final paragraph | risk hidden from reader | place limitation near affected claim |

## Finding Format

Add a calibration table:

```text
| claim or artifact | calibration question | finding | severity | required adjustment | status |
|---|---|---|---|---|---|
```

## Verdict Adjustment

Layer 4 may downgrade:

- `PASS` to `PARTIAL` when evidence is usable but overstated;
- `PARTIAL` to `FAIL` when the main conclusion lacks verified support;
- abstract eligibility from `yes` to `no` for any unsupported hard claim.

Layer 4 should not upgrade a verdict unless the missing evidence is actually supplied and downstream files are updated.

## Manual And AP Behavior

Manual mode:

- Pause if a downgrade would remove a central conclusion or require model rebuild.
- List affected files and the proposed downgrade.

AP mode:

- Apply conservative wording and limitation labels automatically when evidence is clear.
- Record every downgrade and unresolved risk in `quality_report.md`.
