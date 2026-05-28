# Feedback Layer 1：局部质量检查

Layer 1 用于检查每个 `q*` 的局部产物质量。它保留“及时发现问题、及时修正”的思想，但不依赖旧状态机，不要求运行旧评分脚本。

## 检查对象

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/
workspace/output/q*/tables/
workspace/output/q*/q*_summary.md
```

## 输出位置

局部问题写入：

```text
workspace/output/q*/warnings.md
```

最终汇总写入：

```text
workspace/output/final/quality_report.md
```

必要时同步写入：

```text
workspace/output/final/review_report.md
```

## 检查维度

- 题意理解是否完整。
- 输入、输出和依赖是否清楚。
- 候选路线是否有取舍理由。
- 模型公式、目标、约束和算法流程是否自洽。
- 假设是否有依据。
- 符号是否有单位、类型和来源。
- 数据使用是否可追溯。
- `result.json.status` 是否为 `pass` / `partial` / `fail`。
- 验证与灵敏度是否支持结果状态。
- 图表是否有来源和用途。

## 建议记录格式

```markdown
## q1 局部质量检查

| 检查项 | 状态 | 证据文件 | 问题 | 修复建议 |
|---|---|---|---|---|
```

## 规则

- 不写入旧状态文件。
- 不把评分 JSON 作为流程门禁。
- 不要求运行 `scripts/score_artifact.py`。
- 如果检查发现硬数字缺少来源，必须标记为高风险。
- 如果检查发现结果只能 `partial`，必须要求在 `traceability.md` 与 `review_report.md` 中标注限制。
