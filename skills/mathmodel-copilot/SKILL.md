---
name: mathmodel-copilot
description: Plugin shim for mathmodel-copilot. Use when Codex invokes the Markdown-first single-problem mathematical modeling copilot for workspace/problem/problem.md workflows.
---

# mathmodel-copilot 插件 shim

这个文件用于让 Codex plugin 布局发现 `mathmodel-copilot`。

实际工作流定义在仓库根目录的 `SKILL.md`。开始任何工作前，先读取 `../../SKILL.md`，并把它作为主控入口。

路径解析规则：

- `references/` 相对 `../..` 解析。
- `competitions/` 相对 `../..` 解析。
- `templates/` 相对 `../..` 解析。
- `scripts/` 相对 `../..` 解析。
- `config/` 相对 `../..` 解析。

不要在此复制工作流规则；根目录 `SKILL.md` 是唯一主控入口。
