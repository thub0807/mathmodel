# Quality Gate Contract

## Purpose

定义新版 workflow 的质量门禁。质量结果写入：

```text
workspace/output/final/quality_report.md
```

必要时同步写入：

```text
workspace/output/final/review_report.md
workspace/output/q*/warnings.md
```

## Gate Items

- stage completeness
- result status
- validation status
- sensitivity status
- figure/table citation
- paper traceability
- anonymity
- final verdict

## Final Verdict

最终结论只能为：

```text
PASS
PARTIAL
FAIL
```

## Failure Handling

任何缺失或失败都必须写入 `quality_report.md`。不可追溯硬数字必须从论文结论中移除或标记为不可用。
