# Active Runtime Scripts

The active workflow is still Markdown-first and Agent-first. The Agent directly reads:

```text
workspace/problem/problem.md
```

All runtime helpers in this directory are stage helpers. They must not read `legacy/`, `decision_log`, old state, or `score_artifact.py`.

## Stage 8: `render_workspace_paper.py`

Active Stage 8 helper:

```bash
python scripts/render_workspace_paper.py <workspace>
```

Review-only command:

```bash
python scripts/render_workspace_paper.py <workspace> --no-pdf
```

This helper:

- requires each `workspace/output/q*/review_packet.md` as the Stage 2 review source;
- generates `workspace/output/final/paper.md` before LaTeX;
- prioritizes the formal CUMCM template at `templates/latex/cumcm/cumcmthesis/`;
- copies required LaTeX/template assets into `workspace/output/final/source/`;
- copies existing indexed figures/tables when referenced by final indexes;
- writes `workspace/output/final/paper.tex`;
- attempts `paper.pdf` unless `--no-pdf` is specified;
- records compile/runtime details in `latex_compile.log` and `render_report.json`.

It is not a legacy renderer. It does not read `legacy/`.

If the formal CUMCM template is unavailable, the helper may generate an internal temporary LaTeX draft and record the reason in `render_report.json`. The temporary draft is not the preferred formal CUMCM template.

## Stage 9: `validate_workspace.py`

Active Stage 9 helper:

```bash
python scripts/validate_workspace.py <workspace> --strict
```

This helper is a workspace contract validator. It checks v1.2 question-major structure, required `review_packet.md` files, `result.json` minimal schema, referenced figure/table files, render reports, upstream dependency visibility, and final report consistency.

It is not the old scorer and does not assign modeling quality scores. It does not read `legacy/`, `decision_log`, old state, or `score_artifact.py`.

Use UTF-8 text I/O and JSON `ensure_ascii=False`.
