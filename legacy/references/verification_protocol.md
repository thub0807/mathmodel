# 验证协议

每个 `q*` 必须生成：

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

## `validation.md`

至少覆盖：

- 约束满足检查。
- 边界条件检查。
- 数值稳定性检查。
- baseline 对比。
- ablation 或 cross-method comparison。
- 失败情形。
- PASS / PARTIAL / FAIL 结论。

`validation.md` 的结论应与 `result.json.status` 一致。若不一致，必须解释原因，并在最终 review 中标注限制。

## `sensitivity.md`

至少覆盖：

- 敏感参数。
- 扰动范围。
- 结果变化。
- 结论稳定性。
- 对论文结论的影响。

灵敏度分析中的硬数字必须可追溯，只有通过证据门禁后才能写入最终论文。
