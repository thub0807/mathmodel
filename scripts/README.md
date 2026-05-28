# Optional Runtime Scripts

The active `mathmodel-copilot` workflow is file-contract first. It reads `workspace/problem/problem.md` directly and writes Markdown-first artifacts under `workspace/output/`.

Scripts in this directory are optional helpers only. They are not required to start the workflow, read the problem, decompose questions, build models, verify results, generate paper artifacts, or run final review.

## Available helper

### `extract_diff.py`

Optional helper for local diff extraction or manual maintenance work. It is not a stage gate and is not referenced by the active workflow.

## Moved materials

Historical scoring and paper rendering utilities were moved to `legacy/scripts/`.

Offline paper ingestion and download utilities were moved to `maintenance/scripts/`.

## Encoding

Python text I/O should use explicit UTF-8, and JSON writing should use `ensure_ascii=False`.
