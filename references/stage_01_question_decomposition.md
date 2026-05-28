# Stage 1: Question Decomposition

## Purpose

Decompose the single problem into semantic subquestions `q1`, `q2`, `q3`, and so on, using direct reading of `workspace/problem/problem.md`.

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

1. Perform a three-pass reading audit of `problem.md`.
   - Pass 1: read for surface tasks. Mark explicit asks, deliverables, and required answer forms.
   - Pass 2: read for structure. Identify action verbs, objects, constraints, data interfaces, and evaluation metrics.
   - Pass 3: read for hidden work. Identify implicit preprocessing, estimation, validation, visualization, or explanation tasks.
2. Extract a task inventory.
   - Action verbs: predict, optimize, classify, evaluate, simulate, compare, design, explain, verify.
   - Objects: entities, time ranges, regions, networks, products, teams, resources, indicators.
   - Constraints: capacity, budget, time, physical law, policy rule, data availability, precision.
   - Data interfaces: tables, images, attachments, measured variables, derived variables, external assumptions.
   - Evaluation metrics: objective value, error, rank, stability, feasibility, cost, benefit, risk.
3. Identify explicit and implicit subquestions.
   - Explicit subquestions come from numbered or named asks in `problem.md`.
   - Implicit subquestions are required support work, such as data reconstruction, parameter estimation, baseline creation, robustness checks, or result explanation.
   - Do not create a separate `q*` for a tiny support task if it naturally belongs inside another `q*`.
4. Build a dependency graph.
   - Record which `q*` depends on earlier data cleaning, model output, parameter estimate, or scenario result.
   - Mark dependency type as `data`, `parameter`, `result`, `method`, or `writing`.
   - Avoid circular dependencies; if one appears, rewrite the decomposition or record the ambiguity.
5. Map materials to subquestions.
   - Link each image, attachment, table, or data file from `material_index.md` to the relevant `q*`.
   - If a material is referenced but missing, update `material_index.md` and `problem_audit.md`.
   - If a material is unused, record whether it is optional, audit-only, or unexplained.
6. Write `question_index.md`.
   - Assign stable IDs `q1`, `q2`, `q3`, etc.
   - For each `q*`, record title, goal, inputs, outputs, dependencies, material links, likely task type, expected result form, and known risk.
7. Prepare the corresponding `workspace/output/q*/` directory contract.

## Output Contract

`workspace/output/question_index.md` must include:

```text
q id
title
explicit or implicit
source lines or source section from problem.md
goal
input materials
expected output
evaluation metric
dependencies
data attachments
known ambiguity or risk
```

When needed, update:

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

Updates must explain what changed and why the change affects decomposition.

## Quality Gate

Before Stage 2:

- every explicit ask in `problem.md` must map to at least one `q*`;
- every `q*` must have a clear expected output;
- every material needed by a `q*` must be indexed or marked missing;
- dependencies must be acyclic or explicitly recorded as ambiguous;
- no subquestion should be created only to mimic a template if it does not help solve the problem.

## Exit Conditions

- `question_index.md` defines every `q*` needed to answer the problem.
- Each `q*` has clear dependencies and expected deliverables.
- Ambiguous decompositions are either resolved or recorded for user confirmation.

## Failure Handling

- If decomposition has multiple plausible interpretations, pause and ask the user to confirm the intended split.
- If material gaps prevent decomposition, update `problem_audit.md` and stop before Stage 2.
- If an implicit subquestion is necessary but uncertain, include it in `question_index.md` with a risk note instead of hiding it.

## Manual Mode Behavior

Usually continue without pause. Pause only when decomposition choices materially change the modeling path.

## AP Mode Behavior

Choose the most defensible decomposition and write uncertainty into `question_index.md`, `problem_audit.md`, or `material_index.md` as appropriate.
