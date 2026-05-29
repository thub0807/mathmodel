# q3 关键组分与交互作用解释
## question goal

- `q id`: `q3`
- `problem objective`: 识别哪些组分或派生特征主导导电率、综合性能与短时稳定性 proxy，并检验它们是否存在稳定交互作用。

## main results with source fields

- `conductivity` 的首位驱动因子是 `离子强度 proxy`，importance 为 `7.0973`。来源：`workspace/output/q3/results/result.json -> main_result.driver_summary`
- `PI` 的首位驱动因子是 `离子强度 proxy`，importance 为 `0.0260`。来源同上。
- 当前最强交互作用对为 `离子强度 proxy` × `加权密度`，在 `PI` 上的交互得分为 `0.0563`。来源：`main_result.interaction_summary`
- 区域一致性统计显示 `stable=6`、`conditional=4`，说明关键规律在主流区域内基本稳定，但在稀有模式中会减弱。来源：`main_result.stability_summary`

## paper-ready subsection draft

基于 `q2` 已通过验证的组合预测模型，我们进一步追问“为什么某些配方更优”。解释结果表明，导电率与综合性能并不由同一组因素完全主导。对 `conductivity` 而言，`离子强度 proxy` 及硫酸盐/高氯酸盐相关比例占据头部；对 `PI` 而言，`离子强度 proxy`、锂钠体系平衡和最大非水组分占比共同决定了高分区的形成。  
进一步的二维非加性分析显示，`离子强度 proxy` 与 `加权密度` 不是彼此独立地影响结果，而是在 `PI` 上形成了显著协同。换言之，某些组分单独看并不突出，但与特定盐型或投料强度 proxy 组合后会显著改变模型输出。  
不过，这些规律并非在所有区域同样强。区域一致性统计只给出了 `stable=6` 个稳定组合，其余 `4` 个仍需视作条件规律。因此，`q3` 更适合作为 `q4` 的可信域切分依据和 `q5/q6` 的设计线索，而不是把每条解释都包装成普适机理。

## status

`pass`
