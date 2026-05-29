# docs 目录说明

本目录保存开发审计、历史迁移和设计复盘材料，不属于 `mathmodel-copilot` 的 active runtime contract。

active workflow 以以下文件为准：

```text
SKILL.md
references/workspace_protocol.md
references/workflow.md
references/modes_ap_manual.md
references/stage_00_workspace_audit.md
...
references/stage_09_final_review.md
```

历史审计文档中如果仍提到 `templates/workspace/`、旧的多文件 Plan 拆分或 fallback scaffold，应理解为 v1.2 之前的设计记录，不得作为当前运行时输入、模板来源或恢复依据。

当前 v1.2 规则：

- 不再使用 `templates/workspace/`；
- workspace 输出契约由 `references/stage_*.md` 直接定义；
- 每问 Plan 内容合并到 `workspace/output/q*/review_packet.md`；
- Manual 模式逐问停顿，进入 Build 前必须得到同意；
- AP 模式只跳过人工等待，不跳过完整 Plan/Build/Verify/Summary/Traceability。
