# Feedback Layer 4：反包装与校准检查

Layer 4 用于防止论文过度包装、证据不足或图表伪数据。它服务于最终质量报告，不依赖旧评分状态。

## 检查对象

```text
workspace/output/final/paper.md
workspace/output/final/traceability.md
workspace/output/final/final_results.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/
workspace/output/q*/tables/
```

## 输出位置

```text
workspace/output/final/quality_report.md
workspace/output/final/review_report.md
workspace/output/q*/warnings.md
```

## 检查重点

- 论文是否出现未验证硬数字。
- 摘要是否把 `partial` 结果写成强结论。
- 是否存在数据图来源不明或疑似伪造。
- 概念图是否标记为 `conceptual`。
- 模型优缺点是否空泛。
- 改进方向是否不可执行。
- 反模式检查是否覆盖 CUMCM 默认模板要求。
- 文字包装是否超过证据支持。

## 建议记录格式

```markdown
## 反包装与校准检查

| 检查项 | 状态 | 证据 | 风险级别 | 修复建议 |
|---|---|---|---|---|
```

## 规则

- 不读取旧状态文件。
- 不写入旧状态文件。
- 不要求运行旧评分脚本。
- 所有校准结论必须指向 `workspace/output/` 下的证据文件。
