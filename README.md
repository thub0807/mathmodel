# mathmodel-md-copilot v1.2-alpha

`mathmodel-md-copilot` is a Markdown-first, agent-first skill for solving one mathematical modeling problem inside a fixed workspace. The active workflow starts from `workspace/problem/problem.md`, audits supporting materials, plans and builds per question, verifies results, and then assembles the final paper and review reports.

## Workspace

```text
workspace/
  problem/
    problem.md
    images/
    attachments/
    reference.pdf
  output/
```

- `problem.md` is the working problem text.
- `images/` stores problem figures.
- `attachments/` stores data files and supplementary materials.
- `reference.pdf` is kept for audit and conflict checking, not as the default source of truth.

## Workflow

1. Read [references/workflow.md](./references/workflow.md) and create `workspace/output/project_contract.md`.
2. Lock the implementation language, review mode, and source policy in the project contract. The default implementation language is Python.
3. Audit the problem materials, decompose the problem into question workspaces, and plan each question before coding.
4. Build, verify, and summarize each question, then lock final numbers before paper generation and final review.
5. Assemble project-level outputs under `workspace/output/final/`.

## Modes

- Manual mode stops after each question plan and returns the review file paths only.
- AP mode continues automatically and writes `review_note.md` and `warnings.md` in each question workspace.

## Reusable Assets

- `references/` provides workflow notes, modeling guidance, verification ideas, and writing support that should be loaded progressively by stage.
- `competitions/` keeps reusable winning patterns, anti-patterns, phrase banks, abstract templates, and paper skeletons for Stage 2, Stage 8, and Stage 9 support.
- `templates/latex/` contains paper templates that can be adapted during paper generation.
- `templates/workspace/` is organized into `project/`, `per_question/`, and `final/` template groups.
- `scripts/` are optional utilities. Skill packaging or plugin distribution is a separate development concern and is not part of the modeling workflow.
