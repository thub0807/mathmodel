# 每问 Plan 协议

每个 `q*` 必须生成：

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # 如有
workspace/output/q*/review_note.md     # AP 模式或必要时
```

## 文件含义

- `analysis.md`：题意理解、输入输出、依赖关系、评价目标。
- `candidates.md`：候选模型路线及取舍理由。
- `model.md`：确定采用的模型、公式、目标函数 / 评价指标、约束或算法流程。
- `assumptions.md`：建模假设及依据。
- `notation.md`：符号表、单位、变量类型。
- `data_recon.md`：数据来源、附件使用方式、预处理计划、缺失 / 异常处理。
- `warnings.md`：强假设、材料缺口、风险项。
- `review_note.md`：AP 模式下说明为什么自动采用当前方案；Manual 模式仅在必要时写。

## 计划规则

- 根据 `problem.md` 语义理解问题。
- 不使用 Python 正则脚本拆题。
- 明确每问输入、输出和依赖。
- 如果某问依赖前一问结果，写清依赖的 `q*` 和预期文件。
- 如果材料路径缺失，引用 Stage 0 审计记录，不要假设材料存在。
- Manual 模式下，Plan 完成后暂停，只列路径。
