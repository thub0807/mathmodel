# Solution Plan 模板

## 文件用途

作为当前 `q*` 进入 Build 前的统一审阅入口，汇总 Plan 文件路径、所选路线、风险、默认实现语言和 Build 进入条件。

## 对应 stage

Stage 2 Per-Question Plan

## 必填字段

| 字段 | 填写规则 |
|---|---|
| question_id | 当前 `q*` |
| Plan 文件 | 列出 `analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 和可选风险文件 |
| 所选模型 | 写最终模型名和模型族 |
| baseline 与 fallback | 写基线模型和失败回退路线 |
| implementation_language | 默认且锁定为 `python`，除非用户显式更新 |
| 预期 result.json 字段 | 列出 Stage 3 必须写入的结构化结果字段 |
| 数据来源 | 列出题面、附件、上游结果或重构数据 |
| 验证与灵敏度计划 | 概括 Stage 4 必须完成的检查 |
| 风险与限制 | 汇总 `warnings.md` 或 `review_note.md` 中会影响 Build 的风险 |
| Build 进入条件 | 列出进入 Stage 3 前必须满足的检查项 |

## 来源字段

`analysis.md`、`candidates.md`、`model.md`、`assumptions.md`、`notation.md`、`data_recon.md`、`warnings.md`、`review_note.md`

## 可追溯要求

本文件只能汇总已写入详细 Plan 文件的信息，不引入新的模型路线、假设或数据处理策略。

## 模板正文

| 项目 | 内容 |
|---|---|
| question_id | `<q*>` |
| 所选模型 | `<模型名和模型族>` |
| baseline | `<baseline>` |
| fallback | `<fallback>` |
| implementation_language | `python` |

### Plan 文件

```text
workspace/output/q*/analysis.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode or if needed
```

### 预期 result.json 字段

| 字段 | 计划内容 | 来源 Plan 文件 |
|---|---|---|
| `<field>` | `<planned value or structure>` | `<path>` |

### 数据来源

| 数据 | 路径 | 用途 | 风险 |
|---|---|---|---|
| `<data>` | `<path>` | `<use>` | `<risk>` |

### 验证与灵敏度计划

| 检查 | 目标 | 来源 |
|---|---|---|
| `<check>` | `<expected evidence>` | `<plan file>` |

### 风险与限制

| 风险 | 影响 | 处理方式 | 文件 |
|---|---|---|---|
| `<risk>` | `<impact>` | `<response>` | `<path>` |

### Build 进入条件

| 条件 | 状态 | 说明 |
|---|---|---|
| Plan 文件完整 | `<pass/partial/fail>` | `<说明>` |
| 数据来源可定位 | `<pass/partial/fail>` | `<说明>` |
| Python 实现路线明确 | `<pass/partial/fail>` | `<说明>` |
| 预期 result.json 字段明确 | `<pass/partial/fail>` | `<说明>` |
| 验证计划明确 | `<pass/partial/fail>` | `<说明>` |
