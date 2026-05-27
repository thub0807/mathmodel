# Generic Agent Compatibility Notes

This file is now a lightweight compatibility note for ChatGPT, Codex, Claude, and similar agent environments. It is no longer a harness-specific workflow contract.

## Core Principle

The active workflow must be recoverable from repository files and workspace artifacts, not from hidden conversation state or harness-only UI features.

## Compatibility Rules

- Root `SKILL.md` is the active skill entrypoint.
- `AGENTS.md` stores compact internal constraints for the active workflow.
- The agent should read `workspace/problem/problem.md` directly rather than relying on harness-specific ingestion helpers.
- Parallel work is optional and capability-aware.
- Final integration and final review stay serial even if earlier question work can parallelize.

## Tooling Expectations

- File reads, searches, and edits may be implemented differently by each environment.
- Script execution is optional support, not the workflow entrypoint.
- Image inspection, PDF inspection, and attachment handling may vary by environment, but the file protocol remains the same.

## Path Discipline

- Input root: `workspace/problem/`
- Output root: `workspace/output/`
- Per-question workspaces: `workspace/output/q1/`, `workspace/output/q2/`, and later question directories as needed

## What Was Removed

- Friendly Mode rules
- `AskUserQuestion` binding
- plugin or shim discovery rules
- `decision_log` cross-harness state model
