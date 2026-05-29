# q4 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q4-W01` | Medium | `PARTIAL` if hidden | 可信域只覆盖当前组分体系内的相对邻域。 | 后续推荐新配方时必须保留“同体系邻域内有效”的措辞。 | open-limitation |
| `Q4-W02` | Medium | `PARTIAL` for `R_W` | `R_W` 在低可信区最脆弱。 | q5/q6 中涉及 `R_W` 的排序或稳健性都要降级。 | open-limitation |
