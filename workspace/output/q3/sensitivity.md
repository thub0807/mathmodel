# q3 Sensitivity

## Key Parameters

- 关键驱动因子截断深度：当前取每个目标前 `4` 个
- 交互分箱数：当前取 `4`
- 区域定义：`high_PI_common`、`mid_PI_common`、`rare_pattern`

## Main Findings

1. 将驱动因子范围从前 `4` 名放宽到前 `6` 名时，首位驱动因子并未改变，说明头部结论稳定。
2. 交互作用得分在 `conductivity` 与 `PI` 上都把 `离子强度 proxy` / `加权密度` 相关组合推到前列，说明协同效应并非单目标偶然现象。
3. 区域一致性在 common 区域内更强，在 rare_pattern 区域更弱；因此“规律存在”是稳定结论，“规律在所有区域同样强”不是稳定结论。

## Stable / Conditional / Unstable

- stable：头部驱动因子排序；最强交互作用家族；主流区域中的作用方向
- conditional：稀有模式中的作用强度；`W_1` 相关交互的排序细节
- unstable：把 rare_pattern 上的局部变化写成全空间定律
