# Workspace Protocol

## Purpose

定义固定输入、固定输出和模板契约。Agent 执行任何阶段前都必须遵守本协议。

## Fixed Input

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/
    └── attachments/
```

Required:

```text
workspace/problem/problem.md
```

Optional:

```text
workspace/problem/reference.pdf
workspace/problem/images/
workspace/problem/attachments/
```

## Fixed Output

```text
workspace/output/
```

## Source Priority

`problem.md` 是主工作文本。`reference.pdf` 是补充审计材料，仅在以下情况读取：

- `problem.md` 表述不完整或存在歧义。
- 图片说明不足。
- 附件来源不清。
- 单位、符号、编号、表格含义疑似缺失。
- 用户明确要求核对 PDF。
- 最终 review 发现题意依据不足。

## Templates Are Contracts

`templates/workspace/` 是输出文件契约库。生成 `workspace/output/` 文件时，应按对应模板的字段、表格和追溯要求填写。

模板不是可选示例。若某阶段无法满足模板必填字段，必须在该阶段输出中说明失败原因或限制。

## Material Indexing

`images/` 与 `attachments/` 按 `problem.md` 中的相对路径读取。

如果 `problem.md` 引用了不存在的图片、附件或数据文件，记录到：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## Failure Handling

- 缺失 `problem.md` 时，不能进入完整 workflow。
- 缺失 `reference.pdf` 时，记录为 audit-only 材料缺失；不得因此阻止 Agent 直接阅读和理解 `problem.md`。
- 缺失可选材料时，记录到 `problem_audit.md` 与 `material_index.md`。
- 材料无法解释时，进入 Manual checkpoint 请求用户补充或确认。
