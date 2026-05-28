# Stage 1: Question Decomposition

## Purpose

Decompose the single problem into semantic subquestions `q1`, `q2`, `q3`, and so on.

## Required Inputs

```text
workspace/problem/problem.md
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## Required Outputs

```text
workspace/output/question_index.md
workspace/output/q*/
```

## Templates

```text
templates/workspace/root/question_index.md
```

## Entry Conditions

- Stage 0 outputs exist.
- `problem_audit.md` does not contain a blocking material gap.

## Procedure

1. Identify each explicit or implicit question from `problem.md` by reading the problem semantics.
2. Assign stable IDs `q1`, `q2`, `q3`, etc.
3. For each `q*`, record goal, required inputs, expected outputs, dependencies, attachments, and likely task type.
4. Prepare the corresponding `workspace/output/q*/` directory contract.

## Exit Conditions

- `question_index.md` defines every `q*` needed to answer the problem.
- Each `q*` has clear dependencies and expected deliverables.
- Ambiguous decompositions are either resolved or recorded for user confirmation.

## Failure Handling

- If decomposition has multiple plausible interpretations, pause and ask the user to confirm the intended split.
- If material gaps prevent decomposition, update `problem_audit.md` and stop before Stage 2.

## Manual Checkpoint Behavior

Usually continue without pause. Pause only when decomposition choices materially change the modeling path.

## AP Mode Behavior

Choose the most defensible decomposition and write uncertainty into `question_index.md`.
