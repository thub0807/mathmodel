---
stage: 0
name: workspace_reading_problem_understanding
inputs: [workspace/problem/problem.md, workspace/problem/reference.pdf, workspace/problem/images, workspace/problem/attachments]
outputs: [workspace/output/problem_audit.md, workspace/output/material_index.md]
loads_reference: [references/workspace_protocol.md]
next: stage_01_problem_selection
---

# Stage 0：Workspace Reading & Problem Understanding

## 目标

确认固定工作区材料可用，直接阅读并理解 `workspace/problem/problem.md`，建立材料索引和题意审计记录。

## 输入

```text
workspace/problem/problem.md
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

## 输出

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## 执行步骤

1. 检查 `problem.md` 是否存在。
2. 检查 `reference.pdf` 是否存在。
3. 若任一必需文件缺失，提示用户补充并停止完整流程。
4. 直接读取 `problem.md`，形成题意理解。
5. 根据 `problem.md` 中的相对路径索引图片、附件和数据文件。
6. 记录缺失文件、路径错误、材料疑点和题意不确定处。
7. 仅在必要时读取 `reference.pdf`，并记录读取原因。

## `problem_audit.md` 建议结构

```markdown
# Problem Audit

## 必需文件

- problem.md：
- reference.pdf：

## 题意理解

## 材料疑点

## 缺失或路径错误

## reference.pdf 使用记录

## 是否可进入 Stage 1
```

## `material_index.md` 建议结构

```markdown
# Material Index

| 材料 | problem.md 引用路径 | 实际路径 | 状态 | 对应子问题 | 说明 |
|---|---|---|---|---|---|
```

## 禁止事项

- 不询问年份、题号、队员、分工或截止时间。
- 不初始化集中式状态文件。
- 不把 `reference.pdf` 当作默认全文审计对象。
- 不要求用户先运行脚本。
- 不使用 Python 语义解析 `problem.md`。

## 退出条件

- `problem.md` 和 `reference.pdf` 均存在。
- 已读取并理解 `problem.md`。
- 已生成 `problem_audit.md`。
- 已生成 `material_index.md`。
- 缺失材料和疑点已记录。
