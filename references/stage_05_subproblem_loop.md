---
stage: 5
name: per_question_build
inputs: [workspace/output/q*/analysis.md, workspace/output/q*/model.md, workspace/output/q*/assumptions.md, workspace/output/q*/notation.md, workspace/output/q*/data_recon.md]
outputs: [workspace/output/q*/code, workspace/output/q*/results, workspace/output/q*/results/result.json, workspace/output/q*/results/run.log]
loads_reference: [references/per_question_build.md]
next: stage_06_robustness
---

# Stage 5：Per-Question Build

## 目标

对每个 `q*` 按已确认的 Plan 编写代码、运行求解或计算，并生成可追溯的结果文件。

## 输入

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # 如有
```

## 输出

```text
workspace/output/q*/code/
workspace/output/q*/results/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

## `result.json` 推荐结构

```json
{
  "question_id": "q1",
  "status": "pass",
  "model_name": "",
  "main_result": {},
  "metrics": {},
  "figures": [],
  "tables": [],
  "warnings": []
}
```

`status` 只允许：

```text
pass
partial
fail
```

## 结果门禁

- 没有 `result.json`，不得把该问题硬数字写入最终论文。
- `status = pass`：结果完整并通过验证，可进入论文正文与摘要。
- `status = partial`：结果部分完成或验证不足，可有限进入正文，但必须在 `traceability.md` 与 `review_report.md` 中标注限制，不得作为摘要强结论数字。
- `status = fail`：不得作为论文结论依据，必须在 `review_report.md` 中标记。

## 代码与日志规则

- 默认实现语言是 Python。
- Python 文本读写必须显式使用 `encoding="utf-8"`。
- JSON 写入必须使用 `ensure_ascii=False`。
- `run.log` 记录运行意图、输入、命令、输出、警告和失败原因。

## 禁止事项

- 不写入任何集中式状态文件。
- 不使用旧 per-Qi 分数作为流程门禁。
- 不调用旧评分脚本作为 Build 必需步骤。
- 不伪造运行结果或图表数据。

## 退出条件

- 每个已进入 Build 的 `q*` 均有 `result.json`。
- 每个已运行代码的 `q*` 均有 `run.log`。
- `result.json.status` 为 `pass`、`partial` 或 `fail`。
