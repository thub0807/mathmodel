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
- CUMCM abstract quality
- model naming and formula consistency
- anti-pattern review
- feedback layer findings
- final verdict

## Feedback Layers

Final review should run or simulate:

```text
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
references/feedback_layer3_panel.md
references/feedback_layer4_calibration.md
```

Findings must be summarized in:

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## Paper Quality Gate

Check:

- abstract uses traceable hard results and does not use validation-failed claims;
- key results have hard numbers, units, and source fields;
- figures and tables serve paper conclusions;
- model names, variables, formulas, and units are consistent;
- CUMCM anti-pattern hits are fixed or reported;
- a quick judge read can identify the contribution from abstract, final results, and main visuals.

## Final Verdict

最终结论只能为：

```text
PASS
PARTIAL
FAIL
```

## Failure Handling

任何缺失或失败都必须写入 `quality_report.md`。不可追溯硬数字必须从论文结论中移除或标记为不可用。
