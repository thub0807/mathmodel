# workspace 模板说明

`mathmodel-copilot` 使用固定单题工作区。

## 输入区

```text
workspace/
└── problem/
    ├── problem.md
    ├── reference.pdf
    ├── images/
    └── attachments/
```

要求：

- `problem.md` 必须存在，是主工作文本。
- `reference.pdf` 必须存在，是补充审计材料。
- `images/` 可不存在或为空。
- `attachments/` 可不存在或为空。

## 输出区

所有产物由 Agent 写入：

```text
workspace/output/
```

每问产物：

```text
workspace/output/q*/
```

最终产物：

```text
workspace/output/final/
```

`workspace/output/final/quality_report.md` 是新版质量记录。
