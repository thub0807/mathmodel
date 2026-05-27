# Legacy Reference: Startup and Material Readiness

This file is no longer an active workflow entrypoint in `v1.2-alpha`.

Use it as supporting guidance for:
- `workflow.md`
- `workspace_protocol.md`
- `modes_ap_manual.md`

## What Still Matters

- Start from actual materials, not from a questionnaire.
- Confirm the project can read `workspace/problem/problem.md`, images, attachments, and `reference.pdf`.
- Lock the implementation language and mode early in `workspace/output/project_contract.md`.
- Keep tool readiness practical: confirm the chosen language, core libraries, and PDF toolchain only when they are needed.
- Record naming conventions, file organization, and reproducibility expectations in project artifacts rather than hidden state.

## Useful Startup Checks

- Can the agent read `problem.md` directly without a setup script.
- Are the attachments understandable enough to plan the first pass.
- Does `reference.pdf` materially disagree with `problem.md`.
- Is the chosen implementation language realistic for the problem and available tools.
- Are there obvious risks around missing data, unreadable files, or unsupported compilation tools.

## What Was Removed

- questionnaire-style startup
- competition, team-size, deadline, and topic-number intake
- required `decision_log.json` initialization
- any requirement to bootstrap the workflow through scripts or harness-specific UI
