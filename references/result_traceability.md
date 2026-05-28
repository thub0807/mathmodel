# Result Traceability Contract

## Purpose

定义硬数字、图表、假设和符号如何进入最终论文。

## Traceable Sources

可作为论文结论来源的文件：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```

## Required Trace Fields

每条论文 claim 至少记录：

- paper claim
- source question
- source file
- source field
- validation status
- allowed in abstract: yes / no
- limitation note
- result status: pass / partial / fail
- claim type: hard number / figure claim / table claim / assumption / notation / qualitative conclusion
- paper location

## Mapping Rule

Hard numeric claims should map as directly as possible to a field in:

```text
workspace/output/q*/results/result.json
```

If the claim is a validation or sensitivity conclusion, map it to the exact section or row in:

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

Figure and table claims must also point to:

```text
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
```

## Abstract Rule

Claims allowed in the abstract must satisfy all of the following:

- source is traceable;
- validation status is not `fail`;
- result status is not `fail`;
- limitation note is empty or short enough to state honestly in the abstract;
- claim is central to the answer, not decorative.

## Status Rule

- `pass`：可进入正文和摘要。
- `partial`：只能有限进入正文，必须写 limitation note。
- `fail`：不能作为论文结论依据。
