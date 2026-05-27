# Modes: AP and Manual

The project contract locks one active mode for the run.

## Manual Mode

- Generate the per-question planning files first.
- Stop after planning for that question is complete.
- Return review file paths only. Do not restate the full plan in the reply.
- Apply user review comments before entering build.
- Enter build only after explicit user confirmation.

## AP Mode

- Continue automatically after planning unless a hard blocker is found.
- Write `review_note.md` in the question workspace to summarize what was reviewed before build.
- Write `warnings.md` in the question workspace to record unresolved concerns, assumptions to watch, and evidence risks.

## Parallelism

- If the environment supports multiple agents safely, per-question work may run in parallel.
- If that capability is unavailable or uncertain, fall back to serial execution without changing the file protocol.
- Final integration, evidence lock, paper assembly, and final review remain serial.

## Shared Rule

- In both modes, the active workflow stays rooted in the same `workspace/problem/` and `workspace/output/` structure.
