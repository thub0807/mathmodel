# Maintenance Materials

Maintenance files are not part of the user-facing modeling workflow.

Use this area for offline paper collection, corpus distillation, reference material refreshes, or one-off repository upkeep. These files must not be required before the Agent can read `workspace/problem/problem.md`, decompose the problem, build models, verify results, or generate `workspace/output/` artifacts.

Current maintenance areas:

```text
maintenance/scripts/
maintenance/papers/
```

If a maintenance script reads or writes text, keep UTF-8 explicit in the script implementation. If it writes JSON, use `ensure_ascii=False`.
