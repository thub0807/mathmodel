# Result Traceability Contract

## Purpose

定义论文 claim 如何追溯到 source question、source file、source field 和 validation status。

本契约用于：

```text
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

任何进入论文的 hard number、figure claim、table claim、模型结论、假设或符号，都必须能通过 traceability 找到来源。

## Traceable Sources

可作为论文 claim 来源的文件：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/q*_summary.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
```

Hard numeric claims 优先直接映射到：

```text
workspace/output/q*/results/result.json
```

验证、灵敏度、图表、论文表达类 claim 可映射到对应 md 文件的明确段落、表格行或 source field。

## Required Trace Fields

每条 paper claim 至少记录：

```text
paper claim
source question
source file
source field
validation status
result status
allowed in abstract: yes | no
limitation note
claim type
paper location
figure/table id if relevant
last checked in review stage
```

其中：

- `source question` 必须是 `q*` 或 `final`；
- `source file` 必须是 workspace/output 下的可见文件；
- `source field` 对 JSON 应为字段路径，对 Markdown 应为章节/表格行/claim id；
- `validation status` 使用 `PASS`、`PARTIAL`、`FAIL` 或 source 中等价状态；
- `result status` 使用 `pass`、`partial`、`fail`；
- `claim type` 可为 hard number、figure claim、table claim、assumption、notation、qualitative conclusion、validation conclusion、sensitivity conclusion。

## Mapping Rule

每个论文 claim 必须满足：

```text
paper claim -> source question -> source file -> source field -> validation status
```

映射规则：

- hard number：直接映射到 `result.json` 字段，或 final_results 中保留 source field 的行；
- validation conclusion：映射到 `validation.md` 的具体检查或 verdict；
- sensitivity conclusion：映射到 `sensitivity.md` 的参数扰动、失稳边界或稳定性 verdict；
- figure claim：映射到 `final_figures_index.md`，并继续映射到原 `q*/figures/figure_index.md` 和 source field；
- table claim：映射到 `final_tables_index.md`，并继续映射到原 `q*/tables/table_index.md` 和 source field；
- assumption：映射到 `assumptions.md` 或 final paper 中明确保留的 assumption source；
- notation：映射到 `notation.md` 或 Stage 7 unified notation register。

如果无法建立完整链条，该 claim 不得进入论文结论。

## Abstract Rule

允许进入摘要的 claim 必须全部满足：

- source traceable；
- validation status 不是 `FAIL`；
- result status 不是 `fail`；
- limitation note 为空，或可在摘要中简短诚实表达；
- claim 是中心答案，不是装饰性发现；
- hard number 有单位和语境；
- 不依赖 failed figure/table。

`partial` 结果通常不作为摘要强结论。若中心任务必须在摘要呈现 partial 结果，必须使用限制性表达。

## Status Rule

- `pass` / `PASS`：可进入正文；满足摘要规则时可进入摘要。
- `partial` / `PARTIAL`：可进入正文，但必须标 limitation；通常不能作为摘要强结论。
- `fail` / `FAIL`：不能作为论文 claim，不能作为摘要或正文结论；只能作为失败说明、风险说明或后续改进。

## Claim Eligibility

建议在 `traceability.md` 增加 eligibility 字段：

```text
claim eligibility: full | limited | not allowed
```

规则：

- `full`：source pass，validation pass，sensitivity 不推翻，适合正文；可能适合摘要；
- `limited`：source partial 或验证/灵敏度有范围限制，只能带条件使用；
- `not allowed`：source fail、validation fail、不可追踪、图表无 source 或 claim 被 backtrack 移除。

## Figure And Table Traceability

每个 final visual claim 必须记录：

```text
visual id
visual type
source q*
source visual index
source file
source field
supported claim
validation status
paper section
caption
limitation note
```

图表不能只追踪到图片路径；必须追踪到数据或结果字段。

## Review Rule

Stage 9 必须检查：

- paper 中每个 hard number 是否有 trace row；
- 摘要每个数字是否 allowed in abstract；
- partial claim 是否带限制；
- fail claim 是否已移除；
- figure/table claim 是否有 source field；
- paper location 是否准确；
- final_results 与 traceability 是否一致。

任何 traceability failure 都应进入：

```text
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```
