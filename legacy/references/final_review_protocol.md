# 终审协议

Stage 9 输出：

```text
workspace/output/final/review_report.md
workspace/output/final/anonymity_report.md
workspace/output/final/quality_report.md
```

## `review_report.md`

检查：

- 是否回答所有子问题。
- 是否存在材料缺口。
- 是否存在未解决的 `problem.md` / `reference.pdf` 疑问。
- 每问是否有 Plan、Build、Verification、Figures/Tables、Summary。
- 每问是否有 `result.json`。
- `partial` / `fail` 是否标记。
- 图表是否被正文引用。
- 论文是否引入未验证结果。
- `paper.pdf` 是否生成成功。

## `anonymity_report.md`

检查：

- 队伍、学校、姓名、联系方式。
- 路径用户名。
- PDF 元数据。
- 其他匿名风险。

## `quality_report.md`

记录：

- 每个 `q*` 的完整性检查。
- 每个 `q*` 的 `result.json.status`。
- 每个 `q*` 的 validation / sensitivity 状态。
- 全局符号一致性。
- 全局单位一致性。
- 图表引用完整性。
- 论文模板合规性。
- 反模式检查。
- 匿名检查摘要。
- 最终质量结论。

`quality_report.md` 是新版质量记录。
