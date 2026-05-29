# q2 Validation

## Reviewed Artifacts

- `workspace/output/q2/review_packet.md`
- `workspace/output/q2/results/result.json`
- `workspace/output/q2/results/run.log`
- `workspace/output/q2/results/model_probe.csv`
- `workspace/output/q2/results/oof_predictions.csv`
- `workspace/output/q2/results/slice_error_summary.csv`
- `workspace/output/q2/results/pi_consistency_summary.csv`
- `workspace/output/q2/tables/table_q2_main_model_summary.csv`

## Sanity Check

| check item | expected behavior | observed value | pass/partial/fail | implication |
|---|---|---|---|---|
| 样本与特征完整性 | 输入记录数与输出记录数一致，特征矩阵无未处理缺失 | `251 -> 251`，特征数 `73`，toy demo `contains_nan = false` | pass | 可以直接进入 OOF 比较与切片分析 |
| 预测范围合理性 | 预测值应落在可解释范围内，不出现明显物理越界 | `conductivity` 预测范围 `[59.93, 182.41]`，`pH` `[5.71, 8.95]`，`W_1 > 0`，`R_W` 预测最大 `1.033`，`PI` 位于 `[0.362, 0.829]` | pass | 主路线没有出现数值爆炸或方向错误 |
| `PI` 双路径一致性 | `PI` 直接头与重构头应保持较高相关 | overall Spearman `0.9662`，direct/recon 平均绝对差 `0.0343` | pass | `PI` 可以继续作为统一目标量，但需保留 direct vs recon 限制 |
| 不确定性 hook 可用性 | heuristic uncertainty 应与绝对误差呈正相关 | combined hook 与误差的 Spearman：`conductivity 0.5974`、`pH 0.4981`、`PI 0.5180` | pass | `uncertainty_hook_*` 可以交给 `q4/q5` 继续使用 |
| 排名保持性 | 预测 `PI` 应至少保留高分区的大体结构 | actual/pred `PI` Top10 重合 `7/10`，但 Top1 样本已改变 | partial | 可以支持高分区筛选，但不应宣称精确 Top1 已被稳定重建 |

## Baseline Comparison

### baseline 方法

- baseline: `ElasticNet`
- robust alternative: `PLSRegression`
- main route: 目标自适应树路线，其中 `conductivity/pH/W_1/PI` 为 `Blend_Tree3`，`R_W` 为 `RandomForest`

### 对比结果

| target | main route result | baseline result | PLS result | judgment | implication |
|---|---|---|---|---|---|
| `conductivity` | MAE `7.8566`, RMSE `17.6784`, `R^2 = 0.7264` | MAE `8.0303`, RMSE `17.3050`, `R^2 = 0.7379` | MAE `8.9585`, `R^2 = 0.7143` | better on MAE, mixed on RMSE/`R^2` | 树融合在平均绝对误差上更优，但并未在所有二次误差指标上全面压倒线性基线 |
| `pH` | MAE `0.1740`, `R^2 = 0.9190` | MAE `0.1952`, `R^2 = 0.9132` | MAE `0.2307`, `R^2 = 0.8947` | better | 主路线稳定优于两类对照 |
| `W_1` | MAE `0.0443`, `R^2 = 0.9595` | MAE `0.0513`, `R^2 = 0.9542` | MAE `0.0563`, `R^2 = 0.9443` | better | 短时窗口主指标的可预测性很强 |
| `R_W` | MAE `0.0156`, `R^2 = 0.7006` | MAE `0.0192`, `R^2 = 0.5720` | MAE `0.0215`, `R^2 = 0.4951` | better | `R_W` 仍能被学习，但可靠性弱于其他目标 |
| `PI` | MAE `0.0347`, `R^2 = 0.7730` | MAE `0.0457`, `R^2 = 0.6980` | MAE `0.0480`, `R^2 = 0.6670` | better | 综合目标量适合用树集成直接预测 |

## Constraint Satisfaction

| item | audit result | pass/partial/fail | note |
|---|---|---|---|
| 输入边界 | 预测输入只来自配方组成及其派生特征 | pass | 未引入 `reference.pdf` 或其他非题面真值字段 |
| 结构零处理 | 缺失组分统一按 `0.0 structural zero` 处理 | pass | `run.log` 已显式记录，不属于普通缺失补值 |
| 反泄漏约束 | 融合权重不得依赖测试折表现 | pass | 正式 Build 使用预先固定的 `Blend_RF_ET` / `Blend_Tree3` |
| 上游标签一致性 | `PI`、`W_1`、`R_W` 必须沿用 `q1` 口径 | pass | 与 `q1` 的 `indicator_table.csv` 和 `result.json` 一致 |
| 结果契约 | `result.json` 含有 Stage 3 约定字段且 hard numbers 可追踪 | pass | `target_model_selection`、`pi_consistency_summary`、`slice_error_summary` 等字段均存在 |

## Boundary Conditions

| boundary case | expected behavior | observed value | pass/partial/fail | implication |
|---|---|---|---|---|
| 60 样本 toy demo | 最小可行集应跑通，且树路线至少在 `PI` 或 `pH` 上优于线性基线 | `PI` MAE `0.0520 < 0.0605`，`pH` MAE `0.2527 < 0.3790` | pass | 主路线在最小闭环下可运行 |
| 低 `PI` 区域 | 若该区域更难学习，应在验证中显式暴露 | `PI` 在 `low_PI_bottom10` 切片 MAE 为 `0.1042`，约为整体 `3.01` 倍 | partial | 下游不得把模型当作“全空间均匀可信”工具 |
| `R_W > 1` 切片 | 异常切片不应被隐藏 | `R_W` 头在该切片上的 MAE 为 `0.0465`，约为整体 `2.98` 倍 | partial | 涉及 `R_W` 的解释要降级 |

## Consistency With Assumptions And Notation

- 与 `review_packet.md` 一致，仅使用配方组成和派生特征建模，不重新定义 `PI/W_1/R_W`。
- Build 阶段根据 `Q2-W05` 的 guardrail，把“受限加权融合”具体实现为预先固定的简单融合，这是可见且可审计的实现收缩，而非隐藏换模。
- 没有在代码中加入需要 `reference.pdf` 才能解释的额外变量或标签。

## Failure Cases

- `conductivity` 头虽然在总体 MAE 上优于 `ElasticNet`，但在高 `PI` Top10 切片上的 MAE 为 `6.7864`，高于基线的 `4.1390`；在 `rare_pattern` 切片上也高于基线的 `7.1953`。因此不能把 `conductivity` 头写成“对所有局部区域都更好”。
- `PI` 低分区和稀有模式区的误差显著增大，说明模型更适合排序和筛选已知邻域内的候选，而不适合对离群低分样本做强结论。
- `R_W` 头在 `R_W > 1` 切片上明显不稳，只能作为有限证据使用。

## Validation Verdict

**PASS**

理由：

1. 主路线在五个目标上都优于 `ElasticNet` 的 OOF MAE，且 `pH/W_1/R_W/PI` 也同步优于 `PLS`。
2. 所有预测输出都保持在合理范围内，没有出现 NaN、负窗口或越界 `PI`。
3. `PI` 直接头与重构头保持高相关，且 uncertainty hook 与误差呈中等正相关，说明结果既可用也可继续审查。

## Affected Claims

| claim | status | paper claim eligibility | note |
|---|---|---|---|
| 树集成主路线在五个目标上都优于线性基线 `ElasticNet` 的 MAE | PASS | full | 可直接进入正文 |
| `Blend_Tree3` 对 `conductivity/pH/PI` 的 OOF MAE 优于最佳单树 | PASS | full | 可直接进入正文 |
| `conductivity` 头在所有区域都优于线性基线 | PARTIAL | not allowed | 高 `PI` 切片和稀有模式切片不成立 |
| `PI` 可以作为统一目标量继续传递给 `q3`-`q6` | PASS | limited | 需保留 direct vs recon 与短时 proxy 限制 |
| `R_W` 头足以支撑强稳定性结论 | PARTIAL | limited | 需保留异常切片误差说明 |

## Required Downgrade Or Backtrack

- 不需要回退到 Stage 2 或 Stage 3。
- 需要在 `q2_summary.md`、`q4` 和后续 final traceability 中保留三类限制：
  1. `conductivity` 头不是所有切片都优于线性基线；
  2. 低 `PI` 区域与稀有模式区域误差更高；
  3. `R_W` 头与 `PI` 直接头都只能做有限解释。
