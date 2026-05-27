# Output Workspace

This directory holds all generated modeling artifacts.

## Inputs

- `workspace/problem/problem.md`: the main working text
- `workspace/problem/images/`: problem images used during reading and audit
- `workspace/problem/attachments/`: data files, appendices, or structured inputs
- `workspace/problem/reference.pdf`: audit-only comparison source

## Modes

- Manual mode: after writing `solution_plan.md` and related plan files for a question, the agent returns file paths only for review.
- AP mode: the agent continues automatically and writes `review_note.md` and `warnings.md` inside each question workspace.

## Typical Output Shape

- `workspace/output/project_contract.md`
- `workspace/output/problem_audit.md`
- `workspace/output/material_index.md`
- `workspace/output/question_index.md`
- `workspace/output/q1/`
- `workspace/output/q2/`
- `workspace/output/final/final_results.md`
- `workspace/output/final/locked_numbers.md`
- `workspace/output/final/paper.md`
- `workspace/output/final/review_report.md`
