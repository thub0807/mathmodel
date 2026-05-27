# Scripts

No script is required before agent-led modeling.

## Current Layout

- `extract_diff.py`
  - optional active helper for refining an existing Markdown artifact after critique

- `dev/`
  - development-time corpus tools
  - not part of the active modeling workflow

- `legacy/`
  - old migration references
  - retained only for historical compatibility and later adaptation

## Rules

- scripts are optional utilities only
- no script is required before the agent reads `workspace/problem/problem.md`
- scripts must not replace agent-led problem understanding or question decomposition
