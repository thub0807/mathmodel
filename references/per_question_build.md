# Per-Question Build

Stage 3 turns the approved plan into reproducible implementation artifacts.

## Language Lock

- Use the `implementation_language` locked in `workspace/output/project_contract.md`.
- The default is `python`.
- All solve, verify, figure, and data-processing code for the run must use the same locked language.

## Required Outputs

For each question workspace, write:
- `code/`
- `results/result.json`
- `results/run.log`

## Build Expectations

- `code/` contains the runnable implementation for the question.
- `results/run.log` records the executed command, environment notes if relevant, and a concise run trace.
- `results/result.json` is the source of hard numbers for later integration and writing.

## `result.json` Minimum Schema

```json
{
  "schema_version": "1.0",
  "question_id": "q1",
  "status": "ok",
  "implementation_language": "python",
  "model_name": "example model",
  "run_command": "python code/solve_q1.py",
  "main_result": {},
  "metrics": {},
  "parameters": {},
  "figures": [],
  "tables": [],
  "warnings": []
}
```

## Evidence Rule

- `result.json` is the canonical hard-number source for build outputs.
- If a number matters to the paper, it must later be traceable to `result.json`, `validation.md`, or `locked_numbers.md`.
