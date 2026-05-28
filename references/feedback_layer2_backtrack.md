# Feedback Layer 2：跨问题一致性检查

Layer 2 用于检查跨问题、跨阶段的一致性。它不回滚旧状态机，而是通过 `traceability.md`、`review_report.md` 和 `quality_report.md` 记录问题与修复建议。

## 检查对象

```text
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/final/traceability.md
```

## 输出位置

```text
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
workspace/output/q*/warnings.md
```

## 检查重点

- 同一符号在不同 `q*` 中的含义、单位和类型是否一致。
- 同一假设是否被不同问题矛盾使用。
- 后续问题是否正确引用前序问题结果。
- 硬数字是否能追溯到 `result.json`、`validation.md` 或 `sensitivity.md`。
- 图表是否来自对应问题的 `figures/` 与 `tables/`。
- `partial` / `fail` 是否影响最终结论。

## 建议记录格式

```markdown
## 跨问题一致性检查

| 类型 | 涉及问题 | 证据文件 | 风险 | 处理建议 |
|---|---|---|---|---|
```

## 规则

- 不读取旧状态文件。
- 不写入旧状态文件。
- 不以隐式 conversation memory 作为证据来源。
- 所有跨问题证据必须落到 `workspace/output/` 文件。
