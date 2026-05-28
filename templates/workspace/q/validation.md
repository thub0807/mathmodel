# Validation 模板

## 文件用途

记录结果验证过程和 PASS / PARTIAL / FAIL 结论。

## 对应 stage

Stage 4 Verification and Sensitivity

## 必填字段

约束满足、边界条件、数值稳定性、baseline、ablation 或 cross-method comparison、失败情形、结论。

## 来源字段

`result.json`、`run.log`、`model.md`、代码输出。

## 可追溯要求

每个验证结论必须指向结果字段或运行输出。

## 禁止空泛表达

不要写“验证通过”。必须写验证项和证据。

## 模板正文

| 检查项 | 结论 | 证据 | 影响 |
|---|---|---|---|
| 约束满足 | `<结论>` | `<证据>` | `<影响>` |
| 边界条件 | `<结论>` | `<证据>` | `<影响>` |
| 数值稳定性 | `<结论>` | `<证据>` | `<影响>` |
| Baseline 对比 | `<结论>` | `<证据>` | `<影响>` |
| Ablation / Cross-method | `<结论>` | `<证据>` | `<影响>` |
| 失败情形 | `<结论>` | `<证据>` | `<影响>` |

### 总结论

`PASS / PARTIAL / FAIL`：`<理由>`
