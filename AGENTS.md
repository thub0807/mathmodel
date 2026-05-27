# mathmodel-md-copilot

Internal implementation constraints for the active skill:

- Fixed input path: `workspace/problem/problem.md`.
- Read images from `workspace/problem/images/` and attachments from `workspace/problem/attachments/`.
- Treat `workspace/problem/reference.pdf` as audit-only; `problem.md` is the working source.
- The agent performs semantic problem understanding and question decomposition directly from the materials.
- Do not rely on regex question detection, required manifests, or mandatory setup scripts before the agent reads the problem.
- Default `implementation_language` is `python`; lock it in `workspace/output/project_contract.md` before formal modeling.
- All solve, verify, figure, and data-processing code must use the locked implementation language.
- `scripts/` are optional utilities only and must not become the main workflow entrypoint.
- Do not use questionnaire-style startup inputs unrelated to solving the current problem.
- Do not generate packaging or competition submission artifacts.
- Manual mode returns review file paths only.
- AP mode may continue automatically and should write `review_note.md` and `warnings.md`.
- Parallelism is capability-aware and optional; final integration remains serial.
