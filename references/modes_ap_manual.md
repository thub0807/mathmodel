# Manual 与 AP 模式协议

## Manual 模式

Manual 是默认模式。

每个 `q*` 完成 Stage 2 Per-Question Plan 后，进入 Build 前必须暂停。暂停时只列出生成的 Plan 文件路径，不复述方案内容。

示例：

```text
q1 的 Plan 材料已生成，请审查：

workspace/output/q1/analysis.md
workspace/output/q1/candidates.md
workspace/output/q1/model.md
workspace/output/q1/assumptions.md
workspace/output/q1/notation.md
workspace/output/q1/data_recon.md
workspace/output/q1/warnings.md   # 如有

确认后进入 q1 Build。
```

用户确认后，才能进入该问题 Build 阶段。

本流程不要求额外生成统一的 `solution_plan.md`。每个问题的 Plan 由 `analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 和必要的 `warnings.md` / `review_note.md` 共同组成。

## AP 模式

AP 模式只有在用户明确要求时启用，例如：

- “AP 模式”
- “自动推进”
- “不逐问确认”

AP 模式下：

- 不逐问等待用户确认。
- 每个问题仍必须生成完整 Plan 文件。
- 如存在强假设、材料缺口或路线风险，写入 `workspace/output/q*/warnings.md`。
- 写入 `workspace/output/q*/review_note.md`，说明为什么自动采用当前方案。

## 两种模式的共同规则

- 所有关键产物都必须落盘到 `workspace/output/`。
- 硬数字必须通过 `result.json`、`validation.md` 或 `sensitivity.md` 进入最终论文。
- `partial` 与 `fail` 必须在追溯报告和终审报告中标明限制。
