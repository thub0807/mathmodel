# Codex Project Instructions

This repository implements `mathmodel-md-copilot`, a Markdown-first mathematical modeling workflow Skill.

The repository must follow the v1.2 workflow exactly. Do not infer older behavior from any reference project if it conflicts with this file, `SKILL.md`, or `references/workflow.md`.

## Editable Repository

- Current repository: `mathmodel-md-copilot`

## Reference Repositories

The following repositories may be used as references only:

- AutoMCM-Pro: workflow skeleton, AP/Manual mode, verification gates, optional parallelism ideas, LaTeX compile and review tooling ideas.
- mathmodel-skill: model knowledge, competition resources, rubrics, paper templates, anti-patterns, feedback layers.
- auto-MM: evidence discipline, result.json, baseline/ablation/sensitivity, traceability, anonymity and quality review.

Do not copy reference project behavior blindly. Migrate only the parts compatible with this v1.2 Skill.

## Core Positioning

This Skill is:

- Markdown-first.
- Agent-first.
- Workspace-based.
- Per-question structured.
- Evidence-backed.
- Default Python language locked.
- Compatible with both Claude-like and Codex-like environments.
- Not dependent on multi-agent parallel execution.
- Not a submit packaging tool.

## Required Workspace Contract

The Skill must assume this input layout:

```text
workspace/
├── problem/
│   ├── problem.md
│   ├── images/
│   ├── attachments/
│   └── reference.pdf
└── output/