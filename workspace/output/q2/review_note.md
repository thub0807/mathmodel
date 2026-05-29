# q2 Review Note

## Layer 1 Local Critic

Reviewed artifacts:

- `workspace/output/q2/review_packet.md`
- `workspace/output/q2/results/result.json`
- `workspace/output/q2/results/run.log`
- `workspace/output/q2/results/model_probe.csv`
- `workspace/output/q2/results/oof_predictions.csv`
- `workspace/output/q2/validation.md`
- `workspace/output/q2/sensitivity.md`
- `workspace/output/q2/warnings.md`

## 本轮 Build / Verification 记录

- 改进内容：已按 Manual 同意进入 Build，并把 `q2` 的主路线真正落到 `code/q2_build.py`。正式实现使用“预先固定的简单树融合 + 目标自适应选择”来满足反泄漏约束：`conductivity/pH/W_1/PI` 采用 `Blend_Tree3`，`R_W` 采用 `RandomForest`。
- 影响结论：主路线相比 `ElasticNet` 在五个目标上都降低了 OOF MAE，其中 `PI` 从 `0.0457` 降到 `0.0347`，`R_W` 从 `0.0192` 降到 `0.0156`；但 `conductivity` 的提升主要体现在 MAE 而非 `R^2`，因此其“全面优于线性基线”的表述需要收窄。
- 仍保留限制：`PI/W_1/R_W` 仍继承 `q1` 的短时 proxy 限制；低 `PI` 区域、稀有模式和 `R_W > 1` 切片误差显著偏高；`PI` 直接头与重构头虽然高度相关，但不能当作完全等价。
- 审查材料：`workspace/output/q2/review_packet.md`、`workspace/output/q2/results/result.json`、`workspace/output/q2/validation.md`、`workspace/output/q2/sensitivity.md`、`workspace/output/q2/warnings.md`、本文件。

Local verdict: PASS

| issue id | severity | artifact | finding | evidence | required patch | downstream impact | status |
|---|---|---|---|---|---|---|---|
| `Q2-C01` | Medium | `result.json`, `warnings.md` | `q2` 使用的稳定性与综合性能标签都继承自 `q1`，必须同步继承其 proxy 限制。 | `q1` warnings `Q1-W01` 已明确限定为短时稳定性 proxy。 | 在 `q2_summary.md` 和 final traceability 中保留“short-term proxy”表述。 | 若遗漏，会夸大 `q2` 预测任务的科学含义。 | open-limitation |
| `Q2-C02` | Medium | `result.json`, `model_probe.csv` | 返工后的树集成优化是有效的：`Blend_Tree3` 在 `conductivity`、`pH`、`PI` 三个关键目标上都优于最佳单树。 | `conductivity` MAE `7.8566 < 8.4225`，`pH` `0.1740 < 0.1822`，`PI` `0.0347 < 0.0361`。 | 保持简单树融合为主路线，并把其收益写入 `q2_summary.md`。 | 提升 `q3` 的解释入口质量与 `q5` 的候选预测质量。 | accepted |
| `Q2-C03` | Medium | `result.json`, `validation.md` | `PI` 直接头与重构头总体一致，但在高/低 `PI` 切片上并不完全重合。 | overall Spearman `0.9662`；高 `PI` 切片 direct/recon MAE 分别为 `0.0385/0.0205`；低 `PI` 切片为 `0.1042/0.0804`。 | 在摘要和后续 `q4` 中把 `PI` 直接头写成“精度更高、解释性略弱”，把 `PI_recon` 写成“解释性更强、整体精度略弱”。 | 影响 `PI` 作为下游统一目标量时的可解释性表述。 | open-limitation |
| `Q2-C04` | Medium | `slice_error_summary.csv`, `warnings.md` | 模型误差存在明显区域异质性，低 `PI` 区域和稀有模式区域更难预测。 | `PI` 在 `low_PI_bottom10` 切片上的 MAE 为整体的 `3.01` 倍；`pH` 在 `rare_pattern` 切片上的 MAE 为整体的 `1.85` 倍。 | 保留可信区/低可信区表述，供 `q4` 和 `q5` 继续使用。 | 影响下游候选配方的探索-开发平衡。 | accepted-with-limitation |
| `Q2-C05` | Low | `run.log`, `result.json` | toy demo 和全量 OOF 都成功跑通，且无未处理 NaN 或明显物理越界预测。 | toy demo `contains_nan = false` 且 `toy_success = true`；正式 OOF 中不存在负电导率、负 `W_1`、越界 `pH` 或超出 `[0,1]` 的 `PI` 预测。 | 无需返工。 | 说明 Stage 3 实现链路稳定。 | accepted |
| `Q2-C06` | Low | `model_probe.csv`, `result.json` | `R_W` 头仍是最脆弱的一头，不适合作为强结论中心。 | `R_W` 主路线 `R^2 = 0.7006`，且 `R_W > 1` 切片 MAE 为整体的 `2.98` 倍。 | 将 `R_W` 相关结论降级为 limited claim。 | 影响 `q3` 与 `q6` 中涉及稳定性保留率的叙述强度。 | accepted-with-limitation |

## 审查结论

- 当前 `q2` Build、Validation、Sensitivity 和图表底稿已形成完整闭环。
- 未发现必须回退到 `q1` 或重写 `q2` 路线的 High issue。
- `q2` 可以作为 `PASS` 进入下一问，但后续任何涉及稀有模式、低 `PI` 区域或 `R_W` 头的结论，都必须附带可见限制。

## review material paths

- `workspace/output/q2/review_packet.md`
- `workspace/output/q2/results/result.json`
- `workspace/output/q2/validation.md`
- `workspace/output/q2/sensitivity.md`
- `workspace/output/q2/warnings.md`
- `workspace/output/q2/review_note.md`
