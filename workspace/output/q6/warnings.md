# q6 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q6-W01` | Medium | `PARTIAL` if overclaimed | 当前稳健性是预测稳健性，不是真实实验稳健性。 | 论文中必须保留“模型预测意义下”的限定。 | open-limitation |
| `Q6-W02` | Medium | `PARTIAL` if hidden | isolated peak 不能被包装成稳定开发配方。 | 在最终结果里显式区分 stable basin 与 isolated peak。 | open-limitation |
