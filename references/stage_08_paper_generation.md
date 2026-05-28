# Stage 8: Paper Generation

## Purpose

Generate the final paper from validated and traceable artifacts only.

## Required Inputs

```text
workspace/output/q*/q*_summary.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/phrase_bank.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_structures.md
competitions/cumcm/distilled_formats.md
```

## Required Outputs

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf
workspace/output/final/source/
```

## Templates

```text
templates/workspace/final/paper.md
templates/workspace/final/paper.tex
templates/workspace/final/source/README.md
templates/latex/cumcm/cumcmthesis/cumcmthesis.cls
templates/latex/cumcm/cumcmthesis/example.tex
```

`templates/workspace/final/paper.md` is the Markdown intermediate draft contract.

`templates/workspace/final/paper.tex` is only a fallback scaffold for temporary LaTeX output.

CUMCM formal typesetting should prefer:

```text
templates/latex/cumcm/cumcmthesis/cumcmthesis.cls
templates/latex/cumcm/cumcmthesis/example.tex
```

## Entry Conditions

- Stage 7 outputs exist.
- `traceability.md` marks the claims allowed for paper and abstract use.
- No untraceable hard number is required for the intended paper conclusion.

## Procedure

1. Load the CUMCM writing knowledge.
   - Use `paper_skeleton.md` and `distilled_structures.md` for section structure.
   - Use `abstract_template.md` for the high-score abstract shape.
   - Use `winning_patterns.md` for quality anchors.
   - Use `phrase_bank.md` for polished Chinese academic phrasing.
   - Use `anti_patterns.md` to avoid common paper failures.
   - Use `distilled_formats.md` for formula, figure, table, citation, and caption format.
2. Draft `paper.md` as the Markdown intermediate paper.
   - It should be readable and complete before LaTeX conversion.
   - It must not introduce hard numbers outside the allowed source files.
3. Use only hard results from:

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

4. Build sections from verified artifacts.
   - Problem restatement uses `problem.md` and Stage 0/1 outputs.
   - Methods use `q*_summary.md`, assumptions, notation, and model files.
   - Results use `final_results.md` and traceability.
   - Figures and tables use final visual indexes.
   - Evaluation and limitations use validation, sensitivity, and summary limitations.
5. Write the abstract last.
   - Abstract numbers must be traceable.
   - Abstract claims must not have validation status `fail`.
   - `partial` claims may appear only with clear limitation and should normally stay out of the abstract unless central and defensible.
6. Prepare formal CUMCM LaTeX.
   - Prefer `templates/latex/cumcm/cumcmthesis/example.tex` as the structural source.
   - Use `templates/latex/cumcm/cumcmthesis/cumcmthesis.cls` as the formal class.
   - Use safe placeholders for formal fields not supplied by the user.
   - Use `templates/workspace/final/paper.tex` only as fallback when the formal template cannot be used.
7. Generate `paper.pdf` when the environment supports it.
8. Store copied paper assets under `workspace/output/final/source/`.

## Output Contract

`paper.md` must be a full Markdown intermediate draft aligned with:

```text
templates/workspace/final/paper.md
```

`paper.tex` should use the CUMCM formal template when possible. If fallback scaffold is used, record why.

`source/` must include or reference the assets needed to audit paper generation.

## Quality Gate

Before Stage 9:

- every hard number in paper text appears in `traceability.md`;
- abstract numbers are traceable and not validation-failed;
- CUMCM structure, abstract, captions, and formatting follow the competition knowledge files;
- paper text preserves `partial` limitations;
- fallback LaTeX scaffold is not treated as the formal template when `cumcmthesis` is available;
- anti-pattern hits are fixed or carried into final review.

## Exit Conditions

- `paper.md` and `paper.tex` do not introduce unsupported claims.
- Any generated `paper.pdf` corresponds to the current `paper.tex`.
- PDF generation failure is recorded for final review instead of hidden.

## Failure Handling

- If a claim is not traceable, remove it or rewrite it as a clearly limited statement.
- If PDF generation fails, record the command, error, and affected output in Stage 9 reports.
- If the formal CUMCM template cannot be used, record the reason and use fallback scaffold only as temporary output.

## Manual Mode Behavior

After generation, list `paper.md`, `paper.tex`, `paper.pdf` if present, and any failure record paths.

## AP Mode Behavior

Continue to Stage 9 with all generation warnings preserved.
