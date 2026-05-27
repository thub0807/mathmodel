# Scripts

Scripts in this directory are optional utilities only. They are not the active entrypoint for `mathmodel-md-copilot v1.2-alpha`, and they must not replace agent-led reading, decomposition, planning, or review.

## Current Classification

### Active Scripts

- none required in `v1.2-alpha`
- the active workflow is agent-led and Markdown-first
- any script use is optional

### Keep As Optional Utilities

- `extract_diff.py`
  - Use: turn critique notes into section-level patch instructions for an existing Markdown artifact.
  - Role: optional local editing helper.

- `download_cumcm_papers.py`
  - Use: offline corpus maintenance for competition assets.
  - Role: development-time helper, not modeling workflow.

- `ingest_papers.py`
  - Use: offline corpus processing and empirical reference generation.
  - Role: development-time helper, not modeling workflow.

### Legacy Scripts Retained For Migration Reference

- `legacy/render_paper.py`
  - Intended role: optional paper-compilation helper for `paper.tex` and `paper.pdf`.
  - Current issue: still carries legacy competition and `decision_log` assumptions.
  - `v1.2-alpha` status: retained for migration reference only.

- `legacy/score_artifact.py`
  - Intended role: optional quality helper.
  - Current issue: still centered on legacy `decision_log`, competition overlays, and stage-scoring logic.
  - `v1.2-alpha` status: retained for migration reference only. Later work may adapt it into `quality_gate.py` or a lighter review helper.

## Not Allowed As Active Workflow Dependencies

- scripts must not parse `workspace/problem/problem.md` semantically
- scripts must not detect question boundaries automatically
- scripts must not create required question manifests
- scripts must not be required before the agent reads the problem
- scripts must not generate competition submission packages

## Future Optional Utilities

Possible follow-up utilities include:
- `compile_pdf.py`
- `anonymity_scan.py`
- `quality_gate.py`
