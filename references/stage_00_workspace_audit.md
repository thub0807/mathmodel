# Stage 0: Workspace Audit

## Purpose

Confirm the fixed workspace inputs, read `problem.md` directly, and create the material audit that all later stages use.

## Required Inputs

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

## Required Outputs

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## Templates

```text
templates/workspace/root/problem_audit.md
templates/workspace/root/material_index.md
```

## Entry Conditions

- The user is working on one fixed-workspace mathematical modeling problem.
- The current workspace is accessible.

## Procedure

1. Read `workspace/problem/problem.md` as the primary source.
2. Confirm whether `workspace/problem/reference.pdf` exists as supporting audit material.
3. Index referenced images, attachments, data files, and missing paths.
4. Record problem scope, known requirements, uncertainties, and blocking material gaps.

## Exit Conditions

- `problem_audit.md` states whether the required inputs exist and whether the problem can proceed.
- `material_index.md` lists available, referenced, missing, and audit-only materials.
- Any ambiguity that may affect decomposition is recorded.

## Failure Handling

- If `problem.md` is missing, stop the full workflow and ask for the fixed input.
- If `reference.pdf` is missing, record the missing audit material and pause before full workflow execution.
- If optional images or attachments are missing, record them unless they block problem understanding.

## Manual Checkpoint Behavior

Do not pause after Stage 0 unless a required file is missing or the problem cannot be understood from available materials.

## AP Mode Behavior

AP mode follows the same audit requirements and continues only when blocking issues are absent or explicitly recorded.
