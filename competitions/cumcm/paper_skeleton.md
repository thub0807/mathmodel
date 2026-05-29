# 国赛论文骨架 (paper_skeleton — 纯占位符)

> CUMCM 论文写作骨架。Stage 8 应从 `workspace/output/q*/q*_summary.md`、`workspace/output/final/final_results.md`、`workspace/output/final/traceability.md`、最终图表索引中抽取可追溯内容填入 `<填...>` 占位符。
> 本文件提供竞赛经验与写作结构，不是 workspace 输出契约。

---

## 章节字数 / 页数监控

| 章节 | 目标页数 | 目标字数 (中文) |
|------|---------|---------|
| 摘要 | 1 | 600-900 |
| §1 重述 | 1-2 | 600-1200 |
| §2 分析 | 2-3 | 1500-2500 |
| §3 假设 | 0.5-1 | 300-800 |
| §4 符号 | 0.5-1 | 200-500 (主要表格) |
| §5 主体 | 12-16 | 8000-12000 |
| §6 灵敏度 | 2-3 | 1000-2000 |
| §7 评价 | 1-2 | 800-1500 |
| §8 引用 | 0.5-1 | (列表) |
| 附录 | 不计 | 自由 |
| **正文合计** | **22-25** | **18000-22000** |

实测分布参见本目录的 `empirical.json` 和 `empirical_notes.md`。

---

## 骨架 (`paper.md` 中间稿 → cumcmthesis LaTeX)

```
[标题页 — cumcmthesis 自动生成, 通过 \title \tihao 等命令]

[摘要 — 5 段式见 abstract_template.md]
关键词: <填 4-6 个>

# 1. 问题重述

## 1.1 问题背景
<填: 领域背景 + 本题场景, 600-1200 字>

## 1.2 问题描述
<填: 自己语言重述三个子问题, 不抄题>

# 2. 问题分析

## 2.1 问题一分析  <填: 类型+约束+决策变量+目标+难点+策略>
[图 1: 问题一求解流程图]
## 2.2 问题二分析  <同>
## 2.3 问题三分析  <同, 引用 Q1/Q2 结果>

# 3. 模型假设
<填: 3-7 条, 每条带支撑 (文献/数据/物理意义); 来源为 workspace/output/q*/review_packet.md 的 assumptions and notation>

# 4. 符号说明
<填: ≥10 行表格, 全有单位; 来源为 workspace/output/q*/review_packet.md 的 assumptions and notation 与 Stage 7 unified notation register>

# 5. 模型的建立与求解 (主体, 12-16 页)

## 5.1 问题一: <模型族变体名>
### 5.1.1 模型建立  <填: 决策变量 + 目标函数 + 约束>
### 5.1.2 求解算法  <填: 步骤 + 流程图>
### 5.1.3 求解结果与分析  <填: 数值结果 + 图 + 物理意义>

## 5.2 问题二: <同>
## 5.3 问题三: <同, 显式引用 Q1/Q2>

# 6. 灵敏度分析与稳健性检验
<填: 多参数扰动 + 表 + 图; 来源为 workspace/output/q*/sensitivity.md>

# 7. 模型评价与推广
## 7.1 优点  <填: ≥3 条, 每条带数据证据>
## 7.2 缺点  <填: ≥3 条, 每条 (a)替代方法 (b)改进估算 (c)代价>
## 7.3 改进方向
## 7.4 推广

# 8. 参考文献
<填: ≥10 条, GB/T 7714 格式>

# 附录 A: 程序代码
<填: 各 Qi 求解代码 + 灵敏度代码, 中文注释, 首行 "对应论文 §X.Y">

# 附录 B: 计算结果详表
```

---

## 与其他模板的关系

| 章节 | 对应模板 |
|------|--------|
| 摘要 | `abstract_template.md` (5 段式) |
| §3 假设 | `workspace/output/q*/review_packet.md` |
| §4 符号 | `workspace/output/q*/review_packet.md` 与 Stage 7 unified notation register |
| §5 结果 | `workspace/output/q*/q*_summary.md` 与 `workspace/output/final/final_results.md` |
| §6 灵敏度 | `workspace/output/q*/sensitivity.md` |
| 全文证据链 | `workspace/output/final/traceability.md` |
| 一等奖共性 | `winning_patterns.md` |
| 句式 | `phrase_bank.md` |
| 反模式自检 | `anti_patterns.md` |
