---
stage: 1
name: question_decomposition
inputs: [workspace/output/problem_audit.md, workspace/output/material_index.md, workspace/problem/problem.md]
outputs: [workspace/output/question_index.md, workspace/output/q1, workspace/output/q2]
loads_reference: [references/workflow.md]
next: per_question_plan
---

# Stage 1：Question Decomposition

## 目标

根据 `problem.md` 的语义把单个建模题拆分为可独立推进的 `q1`、`q2`、`q3` 等子问题，并建立每问输出目录。

## 输入

```text
workspace/problem/problem.md
workspace/output/problem_audit.md
workspace/output/material_index.md
```

## 输出

```text
workspace/output/question_index.md
workspace/output/q1/
workspace/output/q2/
...
```

## 拆分原则

- 以 `problem.md` 的语义为准。
- 支持“问题一 / 问题1 / Q1 / 第一问 / 任务一 / 隐含问题”等表达。
- 对隐含问题要说明推断依据。
- 每个子问题必须写清输入、输出、依赖和对应附件。
- 不把 `question_manifest.json` 作为必需文件。
- 不做多题选择。
- 不做多题评分。
- 不用 Python 或正则脚本拆题。

## `question_index.md` 推荐格式

```markdown
# Question Index

## q1

原题标记：
标题：
输入：
输出：
依赖：
对应附件：
核心任务类型：优化 / 预测 / 评价 / 仿真 / 机理 / 分类 / 综合评价

## q2

原题标记：
标题：
输入：
输出：
依赖：
对应附件：
核心任务类型：
```

## 目录规则

为每个问题建立：

```text
workspace/output/q*/
```

此阶段只建立问题索引和目录，不进入建模求解。

## 退出条件

- `question_index.md` 已写入。
- 每个问题有明确编号。
- 每个问题有输入、输出和依赖说明。
- 已标记对应附件和材料缺口。
- 已建立每问输出目录。
