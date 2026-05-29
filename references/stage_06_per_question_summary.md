# Stage 6: Per-Question Summary

## Purpose

把每个 `q*` 的完整产物集转换成论文小节草稿，而不是普通文件摘要。

`q*_summary.md` 应能直接进入 Stage 8 的论文主体：它必须包含问题目标、建模动机、模型公式、求解算法、核心结果、验证结论、灵敏度结论、图表引用、局限性，以及可直接复用的中文论文段落。

## Required Inputs

```text
workspace/output/q*/review_packet.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
references/rubrics.md
references/feedback_layer1_critic.md
```

## Required Outputs

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/review_note.md     # if summary critic finds issues
```

## Output Contract

`q*_summary.md` 必须是可进入论文正文的中文小节草稿，包含 question objective、model motivation、assumptions and notation、model equations、algorithm, results、validation、sensitivity、figures/tables、limitations、traceable claims 和 downgraded claims。

## Entry Conditions

- 当前 `q*` 已完成 Build 和 Verification。
- `result.json`、`validation.md`、`sensitivity.md` 至少说明了 `pass`、`partial` 或 `fail` 状态。
- Figure/table indexes 存在，或明确说明该 `q*` 不使用 visual artifact。
- 所有计划写入 summary 的 hard numbers 都能追溯。

## Procedure

1. 把 `q*_summary.md` 当作论文小节草稿。

   不写“本文件总结了……”。应直接使用论文语气，形成后续可复制到 `paper.md` 的段落。

2. 写问题目标。

   包含：

   ```text
   q id
   problem objective
   required output
   evaluation metric
   relation to other q*
   paper section role
   ```

   目标必须来自 `review_packet.md` 的 question card 和 `question_index.md`，不得新增题目要求。

3. 写建模动机。

   说明：

   - 为什么该任务需要这个模型；
   - 题意、数据、约束如何指向模型族；
   - baseline 或 rejected route 为什么不足；
   - 所选模型如何支持 CUMCM 论文表达。

   该段可直接进入论文“问题分析”或“模型建立”前导段。

4. 写核心假设与符号。

   从 `review_packet.md` 的 assumptions and notation 选择论文必要内容：

   - 只保留模型使用的假设；
   - 保留关键变量、参数、单位和定义域；
   - 避免把全部内部符号原样堆入 summary；
   - 若假设较弱，必须写 limitation。

5. 写模型公式。

   包含：

   - 决策变量或状态变量；
   - 目标函数、评价指标或控制方程；
   - 关键约束；
   - 参数含义；
   - 输出量定义。

   公式必须与 `review_packet.md` 一致，不得为了论文好看新增未实现公式。

6. 写求解算法。

   说明：

   - 数据如何进入模型；
   - 算法步骤；
   - 求解器或主要库；
   - 迭代、训练、仿真或评价流程；
   - 输出如何写入 `result.json`。

   算法叙述应能让读者理解“从输入到结果”的过程。

7. 写核心结果。

   只允许使用可追溯结果，来源限于：

   ```text
   workspace/output/q*/results/result.json
   workspace/output/q*/validation.md
   workspace/output/q*/sensitivity.md
   ```

   每个重要 hard number 应在 summary 中附 source note 或在 claims table 中列出：

   ```text
   claim
   source file
   source field
   status
   allowed paper use
   ```

8. 写验证结论。

   从 `validation.md` 提炼：

   - sanity check；
   - baseline comparison；
   - constraint satisfaction；
   - boundary cases；
   - final validation verdict；
   - affected claims。

   如果 validation 为 `PARTIAL` 或 `FAIL`，不能写成稳定结论。

9. 写灵敏度结论。

   从 `sensitivity.md` 提炼：

   - key parameters；
   - single-parameter perturbation；
   - joint perturbation；
   - instability boundary；
   - stable / conditionally stable / unstable conclusion；
   - paper impact。

   若结论条件稳定，必须写稳定范围或触发条件。

10. 引用图表。

   仅使用 `figure_index.md` 和 `table_index.md` 中 `include in paper: yes` 的图表。

   每个图表引用必须说明：

   - 图表编号或 intended id；
   - 支撑 claim；
   - 来源；
   - validation status；
   - 在正文中读者应关注什么。

11. 写局限性和改进。

   局限必须来自：

   - `warnings.md`；
   - `review_note.md`；
   - `validation.md`；
   - `sensitivity.md`；
   - `result.json` status。

   改进建议要具体：增加数据、换模型、扩大情景、增强验证、收窄假设等。

12. 写可直接进入论文的段落。

   `q*_summary.md` 应包含一个或多个 paper-ready paragraphs：

   ```text
   可进入论文的问题分析段
   可进入论文的模型建立段
   可进入论文的求解与结果段
   可进入论文的验证/灵敏度段
   可进入论文的局限性段
   ```

   段落中硬数字仍必须可追溯。

13. 降级 partial/fail 表达。

   - `pass`：可作为正常正文结论；
   - `partial`：必须使用“在……条件下”“结果表明……但……”“可作为有限依据”等限制表达；
   - `fail`：不得作为论文 claim，只能写失败原因、不可用原因或需要重建。

   `fail` 结果不能写入 paper-ready conclusion。

14. 运行 Layer 1 Summary critic。

   使用 `references/feedback_layer1_critic.md` 检查：

   - 是否新增不可追踪数字；
   - 是否隐藏 partial/fail；
   - 公式是否与模型一致；
   - 图表是否支撑 claim；
   - paper-ready 段落是否过度 claim。

## Output Contract

`q*_summary.md` 必须包含：

```text
question goal
model motivation
core assumptions and notation
core formulas
algorithm or solve process
main results with source fields
validation conclusion
sensitivity conclusion
figures and tables for paper use
paper-ready subsection draft
limitations and improvements
status: pass / partial / fail
```

Hard numbers 只能来自：

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
```

必须包含 traceable claims table：

```text
claim
source file
source field
status
paper use: full | limited | not allowed
limitation note
```

## Quality Gate

进入 Stage 7 前：

- summary 可直接改写为论文小节；
- 每个 hard number 有 source file 和 source field；
- 模型公式与 `review_packet.md` 一致；
- 求解算法与 `run.log` 和代码输出一致；
- validation 和 sensitivity 结论可见；
- partial/fail 限制靠近受影响 claim；
- 图表引用支撑具体 claim；
- 没有在 prose 中发明新结果；
- `fail` 结果没有作为论文结论。

## Exit Conditions

- `q*_summary.md` 包含目标、路线、公式、算法、主结果、验证、灵敏度、图表、论文段落、限制和改进。
- 每个 paper-ready claim 都可追踪。
- `partial` 或 `fail` 结果被显式标记并降级表达。

## Failure Handling

- 如果验证缺失，summary 标为 `partial` 或 `fail`，并限制论文使用。
- 如果 summary 与 validation 冲突，暂停并先协调后再进入 Stage 7。
- 如果 paper-ready 段落需要不可追踪数字，删除该数字或返回 Stage 3/4。
- 如果图表 claim 与 figure/table index 不一致，返回 Stage 5 修图表索引。
- 如果 `fail` 结果对应必答任务，写明阻塞风险，供 Stage 7 final verdict 判断。

## Manual Mode Behavior

通常继续。若 summary 改变、弱化或推翻用户已审阅结论，则暂停并列出：

```text
workspace/output/q*/q*_summary.md
workspace/output/q*/review_note.md
```

## AP Mode Behavior

继续执行，但必须保留 explicit limitation notes。AP mode 不得把 partial/fail 结果润色成无条件结论。
