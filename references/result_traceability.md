# Result Traceability Contract

## Purpose

定义硬数字、图表、假设和符号如何进入最终论文。

## Traceable Sources

可作为论文结论来源的文件：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/traceability.md
```

## Required Trace Fields

每条论文 claim 至少记录：

- paper claim
- source question
- source file
- source field
- validation status
- allowed in abstract: yes / no
- limitation note

## Status Rule

- `pass`：可进入正文和摘要。
- `partial`：只能有限进入正文，必须写 limitation note。
- `fail`：不能作为论文结论依据。
