# q5 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q5-W01` | Medium | `PARTIAL` if overclaimed | 推荐候选尚未经过真实实验验证。 | 论文中必须写成“下一轮实验建议”。 | open-limitation |
| `Q5-W02` | Medium | `PARTIAL` for exploration points | medium/low trust 候选用于探索，不代表更可靠。 | 在候选表中保留 trust_tier 与探索用途说明。 | open-limitation |
