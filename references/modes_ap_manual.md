# Manual / AP Mode Protocol

## 共同规则

- 默认模式是 Manual。
- 两种模式都按 question-major loop 执行：一个 `q*` 完成 Plan、Build、Verification/Sensitivity、Figures/Tables、Summary 后，才进入下一个 `q*`。
- 每个 `q*` 的主要审查入口是 `workspace/output/q*/review_packet.md`。
- AP 模式只跳过人工等待，不跳过思考、建模、验证、灵敏度、总结、警告、追溯或质量审查。
- 默认 `implementation_language` 为 `python`。所有 solve、verify、figure 和 data-processing code 必须使用锁定语言。
- 硬数字必须通过 `result.json`、`validation.md` 或 `sensitivity.md` 进入最终论文。
- `partial` 与 `fail` 必须在 `warnings.md`、`review_note.md`、`traceability.md` 和 final reports 中标明限制。

## Manual 模式

Manual 模式下，每个问题有两个硬停顿点。

### Build 前审查

完成当前 `q*` 的 Stage 2 Plan 后，必须生成：

```text
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md        # 如有
workspace/output/q*/review_note.md     # 如有返工或风险说明
```

随后停止，不进入 Stage 3 Build。回复用户时只列文件路径，不复述方案内容：

```text
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md
workspace/output/q*/review_note.md
```

用户明确同意后，才能进入该问题 Stage 3 Build。

### 下一问前审查

当前 `q*` 完成 Stage 6 Summary 后，必须暂停并只列：

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/warnings.md
workspace/output/q*/review_note.md
```

用户明确同意后，才能进入下一个 `q*` 的 Stage 2 Plan。

### 返工记录

每次返工后必须更新 `review_note.md`，包含：

```text
rework round
user concern or trigger
what changed
affected results or claims
files updated
review material paths
remaining limitations
```

如果返工会改变上游结果，下游问题必须重新读取上游产物并说明影响。

## AP 模式

AP 模式只有在用户明确要求时启用，例如：

- “AP 模式”
- “自动推进”
- “不逐问确认”

AP 模式下：

- 不等待用户逐问确认。
- 每个问题仍必须按顺序生成完整 `review_packet.md`。
- 每个问题仍必须执行 Build、Verification、Sensitivity、Figures/Tables 和 Summary。
- 每个问题必须写 `review_note.md`，说明为什么自动采用当前方案、候选为何被拒绝、风险如何验证或降级。
- 存在强假设、材料缺口、partial/fail、异常数据、fallback 或生成失败时，必须写入 `warnings.md`。
- 不得用“快速测试占位”“仅用于端到端测试”等内容替代正式建模产物，除非用户明确要求 smoke test；即使 smoke test，也必须在所有下游和 final reports 中标记为不可提交结论。
