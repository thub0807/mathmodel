# 每问 Build 协议

每个 `q*` 必须生成：

```text
workspace/output/q*/code/
workspace/output/q*/results/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
```

默认实现语言是 Python。所有求解、验证、绘图、制表和数据处理代码必须使用锁定实现语言。

Python 文本读写必须使用：

```python
encoding="utf-8"
```

JSON 写入必须使用：

```python
ensure_ascii=False
```

## `result.json`

推荐 schema：

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

`status` 允许：

```text
pass
partial
fail
```

规则：

- 没有 `result.json`，不得把该问题硬数字写入最终论文。
- `pass`：结果完整并通过验证，可进入论文正文与摘要。
- `partial`：结果部分完成或验证不足，可有限进入论文，但必须在 `traceability.md` 与 `review_report.md` 中标注限制，不得作为摘要强结论数字。
- `fail`：不得作为论文结论依据，必须在 `review_report.md` 中标记。

## `run.log`

`run.log` 记录运行意图、输入文件、生成文件、警告和未解决问题。它不需要冗长，但必须支持审查。
