# q1 Sensitivity

## Key Parameters

| parameter | baseline value | source | why important | plausible range | affected result field |
|---|---|---|---|---|---|
| pH 适宜区间 | `[6.5, 8.5]` | `review_packet.md` 默认设定 | 它决定酸性/碱性样本的惩罚强度，是当前最敏感的设定项 | `[6.0, 8.0]` 到 `[7.0, 9.0]` | `PI` 排名、Top10 roster、Top1 配方 |
| 权重混合系数 `alpha` | `1.0` | 主路线使用纯 CRITIC 权重 | 用于测试是否需要完全依赖 CRITIC 权重 | `0.6` 到 `1.0` | `PI` 排名、权重稳健性 |
| 稳定性特征集合 | `W_1 + R_W` | `review_packet.md` 的主路线定义 | 用于判断 `R_W` 是否改变排序结构 | `W_1 only` 与 `W_1 + R_W` | `PI` 排名、稳定性解释力度 |

## Perturbation Ranges

- pH 区间扰动：
  - low: `[6.0, 8.0]`
  - nominal: `[6.5, 8.5]`
  - high: `[7.0, 9.0]`
- 权重混合系数扰动：
  - low: `0.6`
  - nominal: `1.0`
  - mid: `0.8`
- 稳定性特征集合扰动：
  - nominal: `W_1 + R_W`
  - stress alternative: `W_1 only`

## Single-Parameter Perturbation

| parameter / scenario | low | nominal | high | output at low | output at nominal | output at high | conclusion impact |
|---|---|---|---|---|---|---|---|
| pH 区间 | `[6.0,8.0]` | `[6.5,8.5]` | `[7.0,9.0]` | Top10 重合 `6/10`，Spearman `0.6936`，Top1 改变 | Top10 重合 `10/10`，Spearman `1.0000` | Top10 重合 `9/10`，Spearman `0.8386`，Top1 不变 | pH 区间是最主要敏感源，尤其会影响精确 Top10 与榜首配方 |
| 权重混合系数 `alpha` | `0.6` | `1.0` | `0.8` | Top10 重合 `9/10`，Spearman `0.9945`，Top1 不变 | Top10 重合 `10/10` | Top10 重合 `9/10`，Spearman `0.9983`，Top1 不变 | 对权重方案不太敏感，说明 CRITIC 并未造成脆弱排序 |
| 稳定性特征集合 | `W_1 only` | `W_1 + R_W` | not applicable | Top10 重合 `7/10`，Spearman `0.9798`，Top1 不变 | Top10 重合 `10/10` | not applicable | 去掉 `R_W` 会影响中后位排序，但不会推翻高分配方的大体结构 |

## Joint Perturbation Scenarios

| scenario | varied parameters | rationale | result | conclusion impact |
|---|---|---|---|---|
| optimistic_mix | pH 区间改为 `[7.0, 9.0]`，`alpha = 0.8` | 假设研究者更关注近中性到弱碱区，并接受较弱的客观赋权强度 | Top10 重合 `9/10`，Spearman `0.8452`，Top1 保持 `{C728CD3D-8F64-3AC1-255C-2BDE9394431E}` | 主结论稳定，精确次序有中等波动 |
| stress_mix | pH 区间改为 `[6.0, 8.0]`，`alpha = 0.6` | 同时放宽酸性容忍度并削弱 CRITIC 权重的主导性，作为最不利情景 | Top10 重合 `7/10`，Spearman `0.6600`，Top1 改为 `{B6BBEE56-6A44-E2C5-A640-FE532DF4CF73}` | 精确榜首样本不再稳定，但“需要多指标评价”的结论仍成立 |
| window_reduced_mix | 仅保留 `W_1`，并设 `alpha = 0.8` | 检查 `R_W` 去除后，排序是否仍由实用窗口主导 | Top10 重合 `7/10`，Spearman `0.9781`，Top1 不变 | 高分配方结构仍稳定，但中位次序会重新排序 |

## Instability Boundary

### stable range

- 当 pH 区间保持在 `[6.5, 8.5]` 或向 `[7.0, 9.0]` 小幅移动时，Top1 配方保持不变。
- 当 `alpha` 在 `[0.6, 1.0]` 范围内变化时，Top10 至少保留 `9/10`，排序相关系数始终高于 `0.99`。

### conditionally stable range

- 若仍使用 `W_1 + R_W` 双稳定性指标，但把 pH 区间放宽到 `[6.0, 8.0]`，则 Top10 只保留 `6/10`，Top1 发生变化。
- 去掉 `R_W` 后，Top1 仍稳定，但 Top10 只保留 `7/10`，说明 `R_W` 主要影响中高位样本的细排序。

### failure range

- 当前没有出现“主结论完全翻转”为“电导率单指标足够”的失效区间。
- 真正失稳的是“具体名单级”结论，而不是“多指标评价有必要”这一方法级结论。

## Critical Parameters

| critical parameter | threshold value or trigger | effect |
|---|---|---|
| pH 适宜区间下界 | 由 `6.5` 放宽到 `6.0` | 会显著提升酸性高电导样本的综合排名，并改变榜首样本 |
| 是否保留 `R_W` | 从 `W_1 + R_W` 改为 `W_1 only` | Top1 不变，但中高位排序明显重排 |
| 权重混合系数 `alpha` | 在 `0.6` 到 `1.0` 之间变化 | 影响很小，不构成主要失稳源 |

## Stable Or Unstable Conclusions

- **stable**：
  - 仅靠电导率不足以定义“好配方”。
  - `W_1` 是当前四项指标中贡献最高的评价维度。
  - 排名前列样本总体上表现为“较高电导率 + 近中性 pH + 较大实用稳定窗口”。

- **conditionally stable**：
  - 具体 Top10 roster 和榜首配方受 pH 区间设定影响。
  - `R_W` 主要决定高分样本之间的细排序，而不是是否进入高分区域。

- **unstable / not supported as unconditional claim**：
  - “某一条具体配方是绝对最优解”。
  - “当前稳定性 proxy 足以代表长期寿命表现”。

## Paper Impact

- 可以把“多指标综合评价优于单电导率排序”作为 `full` claim 写入正文。
- 必须把“榜首配方 / Top10 名单”写成条件稳定结论，并在正文附近注明 pH 区间前提。
- 在 Stage 7 和 Stage 8 中，`q1` 产生的 `PI` 可作为后续预测目标，但应随同携带“短时稳定性 proxy”限制。
