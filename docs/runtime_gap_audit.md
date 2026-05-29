# Runtime Gap Audit

Stage: Stage 0 audit only. This document records current runtime gaps before adding active helpers.

## Current Script Availability

`scripts/render_workspace_paper.py`:

```text
missing before Stage 1
```

`scripts/validate_workspace.py`:

```text
missing before Stage 2
```

`scripts/README.md` currently states that the active workflow has no required runtime scripts. That is accurate for the pre-fix state, but it leaves Stage 8 and Stage 9 without executable helpers.

## Stage 8 Execution Gap

Stage 8 describes paper generation and says the formal CUMCM template should be preferred. However, before Stage 1 there is no active helper that:

- reads final integration outputs;
- builds `paper.md` before LaTeX;
- copies formal CUMCM template dependencies into `source/`;
- maps generated paper content into `MathModel.tex` / `gmcmthesis.cls`;
- copies final figure/table assets;
- compiles or records PDF failure;
- writes `latex_compile.log` and `render_report.json`.

As a result, Stage 8 is documented but not truly connected to an executable formal-template render path.

## Stage 9 Execution Gap

Stage 9 describes final review, traceability, anonymity, CUMCM quality, and report consistency checks. However, before Stage 2 there is no active validator that:

- checks the workspace contract stage by stage;
- validates `result.json` structure and status values;
- checks final report contradictions;
- verifies Stage 8 render outputs;
- distinguishes warnings from blocking errors;
- provides a machine-readable JSON validation result.

As a result, Stage 9 is documented but not truly connected to an executable workspace validator.

## Time Risk For Real Data Problems

Real data tasks may be slow because:

- q-level result files may depend on large attachments;
- result, baseline, ablation, and sensitivity runs may be expensive;
- figure/table generation may depend on heavy data preprocessing;
- Stage 8 PDF compilation may fail late due to missing fonts, class files, image formats, or LaTeX engine availability;
- Stage 9 manual review is broad and can become costly without a structural validator.

The validator should avoid rerunning modeling code. It should inspect files, schemas, paths, and consistency only.

## Recommended Fix Order

1. Add `docs/cumcm_latex_template_interface.md` and this runtime gap audit.
2. Add `scripts/render_workspace_paper.py` as the active Stage 8 helper.
3. Add `scripts/validate_workspace.py` as the active Stage 9 helper.
4. Update `scripts/README.md`.
5. Wire Stage 8, Stage 9, `workflow.md`, `quality_gate.md`, `result_traceability.md`, `SKILL.md`, `README.md`, and `AGENTS.md` to the two helpers.
6. Keep `templates/latex/cumcm/cumcmthesis/` unchanged and keep `legacy/` isolated.
