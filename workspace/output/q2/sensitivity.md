# q2 Sensitivity

## Key Parameters

| parameter | baseline value | source | why important | plausible range | affected result field |
|---|---|---|---|---|---|
| 浓度 / 质量 proxy 特征块 | 保留 | `review_packet.md` 与 `feature_schema` | 它们承载了“配方强度”信息，可能决定树模型是否真正学到非线性浓度效应 | 保留 vs 删除 | 五个目标的 MAE / `R^2`，尤其是 `conductivity` 与 `PI` |
| 树模型家族 / 融合方式 | `Blend_Tree3` 或 `RandomForest` | `result.json -> main_result.target_model_selection` | 用于判断树融合是否真的带来稳定收益 | 单树 `RF/ET/HistGB`、`Blend_RF_ET`、`Blend_Tree3` | `conductivity/pH/W_1/PI` 的 OOF 精度 |
| 交叉验证随机种子 | `42` | Build 设置 | 若模型对折叠变化过敏，则结论难以防御 | `42` vs `7` | OOF MAE、`R^2`、下游可复用性 |
| 高性能区阈值 | 前 `10%` | `review_packet.md` | 题目要求比较高性能区/低性能区，阈值会影响区域误差解读 | 前 `10%` vs 前 `20%` | 切片误差与“高性能区是否更可信”的判断 |
| `PI` 表达路径 | direct head | `result.json` | 统一目标量既追求精度，也追求可解释性 | direct vs recon | `PI` 的可解释性与下游可用性 |

## Perturbation Ranges

- proxy block：
  - nominal: 保留 `mass_proxy_*`、`mol_proxy_*`、`weighted_density`、`ionic_strength_proxy`
  - low-information alternative: 删除上述 proxy block
- model family：
  - single tree: `RandomForest` / `ExtraTrees` / `HistGB`
  - simple fusion: `Blend_RF_ET`
  - main route: `Blend_Tree3`
- CV seed：
  - nominal: `42`
  - alternative: `7`
- high-performance threshold：
  - nominal: `Top10%`
  - relaxed: `Top20%`
- `PI` pathway：
  - direct head: `pred_PI`
  - reconstructed head: `pred_PI_recon`

## Single-Parameter Perturbation

| parameter / scenario | low | nominal | high | output at low | output at nominal | output at high | conclusion impact |
|---|---|---|---|---|---|---|---|
| proxy block | 删除 proxy | 保留 proxy | not applicable | `conductivity` MAE `9.5179`，`PI` MAE `0.03765` | `conductivity` MAE `7.8566`，`PI` MAE `0.03467` | not applicable | 删除 proxy 后，`conductivity` MAE 上升约 `21.2%`，`PI` 上升约 `8.6%`，说明 proxy block 是关键特征组 |
| model family | 最佳单树 | `Blend_Tree3` | `Blend_RF_ET` | 例如 `conductivity` 最佳单树 MAE `8.4225`，`PI` 最佳单树 `0.0361` | `conductivity` `7.8566`，`PI` `0.0347` | `conductivity` `8.4181`，`PI` `0.0359` | `Blend_Tree3` 在关键目标上稳定优于单树或二树融合；`R_W` 例外，单树 `RandomForest` 最佳 |
| CV seed | `7` | `42` | not applicable | `conductivity` MAE `7.6885`，`PI` `0.03575` | `conductivity` MAE `7.8566`，`PI` `0.03467` | not applicable | 改变折叠随机种子只带来小幅波动，没有推翻主路线 |
| 高性能区阈值 | `Top10%` | not applicable | `Top20%` | `conductivity` 在高性能区 MAE `6.7864`；`PI` 为 `0.0385` | not applicable | `conductivity` 在高性能区 MAE `5.3367`；`PI` 为 `0.0299` | 把高性能区放宽到前 `20%` 后，区域误差反而更平稳，但主结论不变 |
| `PI` 路径 | recon | direct | not applicable | overall MAE `0.03911`；高 `PI` 切片 MAE `0.0205` | overall MAE `0.03467`；高 `PI` 切片 MAE `0.0385` | not applicable | direct 头整体更准，但 recon 在高/低 `PI` 极端区更稳，更适合解释性用途 |

## Joint Perturbation Scenarios

| scenario | varied parameters | rationale | result | conclusion impact |
|---|---|---|---|---|
| optimistic_region | 高性能区阈值从 `Top10%` 放宽到 `Top20%` | 假设后续实验筛选更关注一片高分区域，而不是只盯住最尖端前 10% | 五个目标在 `Top20%` 区域的 MAE 都低于或不高于 `Top10%`，如 `PI` 从 `0.0385` 降到 `0.0299` | “高分区更易预测”的结论保持成立 |
| pessimistic_simplify | 删除 proxy block | 检查若只保留比例与结构特征，主路线是否仍能工作 | `conductivity` MAE 从 `7.8566` 升到 `9.5179`，`W_1` 从 `0.0443` 升到 `0.0474`，`PI` 从 `0.03467` 升到 `0.03765` | 说明 proxy block 不能被轻易删去，否则主路线会明显退化 |
| mixed_stress | 低 `PI` 区域与 `rare_pattern` 同时触发 | 这是最接近“模型陌生且性能差”的极端场景 | 仅 `8` 条样本，但 `conductivity` MAE 达 `10.96`、`pH` 达 `0.4004`、`PI` 达 `0.0936` | 下游若探索该区域，应优先把它当作高不确定性探索区，而非开发区 |

## Instability Boundary

### stable range

- 当 CV 随机种子从 `42` 换到 `7` 时，五个目标的 MAE 变化都较小，没有出现主路线失效。
- `Blend_Tree3` 在 `conductivity`、`pH`、`PI` 上都保持对最佳单树的优势，因此“简单树融合优于单树”的方向是稳定的。

### conditionally stable range

- 把高性能区从前 `10%` 改为前 `20%` 时，高性能区误差会变化，但“低 `PI` 区域更难预测”的结论并未翻转。
- `PI` direct/recon 两条路径在 overall 上高度一致，但在高/低 `PI` 切片上的优劣会互换，因此二者更适合被视为互补而不是互相替代。

### failure range

- 当删除 proxy block 时，`conductivity` 和 `PI` 的精度明显下降，说明主路线对浓度强度特征具有真实依赖。
- 在 `low_PI_bottom10`、`rare_pattern` 和 `R_W > 1` 等切片中，误差会显著放大；此时若仍把模型当作全空间均匀可信工具，就会产生过度 claim。

## Critical Parameters

| critical parameter | threshold value or trigger | effect |
|---|---|---|
| proxy block 是否保留 | 删除 `mass_proxy_*` / `mol_proxy_*` / `weighted_density` / `ionic_strength_proxy` | `conductivity` 精度损失最大，主路线收益明显收缩 |
| 是否进入低 `PI` 区域 | `PI` 落入底部 `10%` | 五个目标的误差都显著升高，`PI` 本身 MAE 约为整体 `3.01` 倍 |
| `R_W` 是否处于异常区间 | `R_W > 1.0` | `R_W` 头误差接近整体 `3` 倍，强解释结论失效 |
| 高性能区阈值 | 前 `10%` vs 前 `20%` | 改变局部误差水平，但不改变“高分区相对更可预测”的总体方向 |

## Stable Or Unstable Conclusions

- **stable**
  - 树路线在五个目标上的 MAE 都优于 `ElasticNet`。
  - `Blend_Tree3` 对 `conductivity`、`pH`、`PI` 的收益是真实存在的。
  - uncertainty hook 与误差呈中等正相关，可继续用于 `q4/q5`。

- **conditionally stable**
  - `PI` direct head 与 `PI_recon` 的使用场景不同：overall 上 direct 更准，极端高/低 `PI` 区域 recon 更稳。
  - 高性能区的局部误差会随阈值变化，但不会推翻区域异质性的主结论。

- **unstable / not supported as unconditional claim**
  - 模型在稀有模式、低 `PI` 区域和 `R_W > 1` 切片上与整体一样可靠。
  - `R_W` 头足以支撑强稳定性结论。
  - 只用比例与结构特征就能保持当前主路线精度。

## Paper Impact

- 可以把“树集成优于线性基线”和“proxy block 对 `conductivity`/`PI` 至关重要”写成 `full` claim。
- 必须把“模型适用范围”写成条件结论：高分区与已见邻域更可信，低 `PI` / 稀有模式 / `R_W > 1` 区域更应谨慎。
- `PI` 相关论述最好同时提到 direct 与 recon 两条路径：前者偏精度，后者偏解释。
