# q3 Validation

## Reviewed Artifacts

- `workspace/output/q3/results/result.json`
- `workspace/output/q3/results/driver_ranking.csv`
- `workspace/output/q3/results/interaction_summary.csv`
- `workspace/output/q3/results/stability_summary.csv`
- `workspace/output/q2/results/result.json`
- `workspace/output/q2/validation.md`

## Sanity Check

| item | observation | verdict | implication |
|---|---|---|---|
| 解释入口来源 | 关键驱动因子全部来自 `q2` 已通过验证的模型解释结果 | pass | 没有脱离上游证据链 |
| 关键导电率因子 | `conductivity` 首位因子为 `离子强度 proxy`，importance `7.0973` | pass | 与 q2 中“导电率受投料强度和盐型比例主导”的叙述一致 |
| 关键综合因子 | `PI` 首位因子为 `离子强度 proxy`，importance `0.0260` | pass | `PI` 不是单纯电导率排序的翻版 |
| 最强交互作用 | `离子强度 proxy` × `加权密度` 在 `PI` 上的交互得分 `0.0563` | pass | 题面要求的协同效应被显式量化 |
| 区域一致性 | `stable` 组合 `6` 个，`conditional` 组合 `4` 个 | partial | 主流区域存在稳定规律，但 rare_pattern 区域需要降级 |

## Validation Verdict

**PASS**

解释结论直接锚定到 `q2` 通过验证的模型与结果，没有引入新的黑箱标签；但稀有模式区仍只支持条件解释。
