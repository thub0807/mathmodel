# 工作区协议

## 固定输入结构

`mathmodel-copilot` 只处理一个固定工作区：

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/
    └── attachments/
```

硬性要求：

- `workspace/problem/problem.md` 必须存在。
- `workspace/problem/reference.pdf` 必须存在。
- `images/` 可不存在或为空。
- `attachments/` 可不存在或为空。
- 如果 `problem.md` 或 `reference.pdf` 缺失，提示用户补充，不能进入完整建模流程。

## 材料优先级

`problem.md` 是主工作文本。Agent 必须直接阅读并理解 `problem.md`，不得依赖 Python 或正则脚本做语义拆题。

`reference.pdf` 是补充审计材料，不是默认全文审计对象。仅在以下场景读取：

- `problem.md` 表述不完整或存在歧义。
- 图片说明不足。
- 附件来源不清。
- 单位、符号、编号、表格含义疑似缺失。
- 用户明确要求核对 PDF。
- 最终 review 发现题意依据不足。

## 图片与附件

`images/` 与 `attachments/` 按 `problem.md` 中的相对路径读取。

如果 `problem.md` 引用了不存在的图片、附件或数据文件，记录到：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

不要静默忽略缺失材料，也不要伪造材料内容。

## Stage 0 输出

Stage 0 必须写入：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

`problem_audit.md` 记录：

- 必需文件是否存在。
- `problem.md` 阅读结论。
- 题意疑点。
- 材料缺口。
- 是否读取过 `reference.pdf` 以及读取原因。

`material_index.md` 记录：

- `problem.md` 中引用的图片、附件和数据文件。
- 实际存在的材料。
- 缺失或路径错误的材料。
- 每个材料的用途和对应子问题。

## 禁止事项

- 不要求先运行 `init_workspace.py`。
- 不要求先运行 `check_materials.py`。
- 不新增或要求 `detect_questions.py`。
- 不新增或要求 `create_question_dirs.py`。
- 不把 `question_manifest.json` 作为必需文件。
- 不初始化集中式状态文件。
