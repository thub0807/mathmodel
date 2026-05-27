# v1.2-alpha 自检清单

- 只有一个 active `SKILL.md`，位于仓库根目录
- `SKILL.md` 保持 compact，并指向 active workflow references
- `references/` 下存在 active workflow protocol 文件
- Manual 模式只返回审查路径，不复述方案
- AP 模式会写入 `review_note.md` 和 `warnings.md`
- final outputs 统一位于 `workspace/output/final/`
- 模板覆盖 workflow-required 的 markdown 与 json 产物；`paper.pdf`、`results/run.log` 等生成型文件不要求静态模板
- scripts 只作为 optional utilities
- active workflow 不依赖 `decision_log`
- active workflow 不依赖 Friendly Mode
- `topic_specs.json` 不是 active 资源
- development corpus scripts 位于 `scripts/dev/`
- code starters 遵守 implementation language lock
