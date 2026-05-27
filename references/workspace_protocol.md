# Workspace Protocol

The active workspace has two roots:

- `workspace/problem/`
- `workspace/output/`

## Problem Root

- `workspace/problem/problem.md` is the working problem text and the default source for semantic understanding.
- `workspace/problem/images/` stores problem figures that the agent may inspect directly.
- `workspace/problem/attachments/` stores datasets, spreadsheets, archives, and other supporting files.
- `workspace/problem/reference.pdf` is audit-only. It is used to compare against `problem.md`, not to replace it.

## Output Root

- `workspace/output/` stores project-level audit, decomposition, integration, paper, and review artifacts.
- `workspace/output/q1/`, `workspace/output/q2/`, and later question workspaces store per-question planning, build, verification, figures, tables, and summaries.

## Audit Rules

- The agent reads `problem.md` directly before any setup script or manifest requirement.
- When `problem.md` and `reference.pdf` differ, record the conflict in `workspace/output/problem_audit.md`.
- Do not introduce a required state machine or required manifest file for active workflow control.

## Material Index

`workspace/output/material_index.md` should include at least these fields:

| path | type | role | used_by | notes |
|---|---|---|---|---|
| `workspace/problem/problem.md` | problem text | primary source | project | working text |

Use this table shape for all audited materials. Keep it minimal and update it as materials are actually used.
