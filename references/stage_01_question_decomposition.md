# Stage 1: Question Decomposition

## Purpose

把单一题面 `workspace/problem/problem.md` 拆解为语义明确、可建模、可验证、可追踪的 `q1`、`q2`、`q3` 等子问题。

本阶段只做题意理解和子问题结构化，不做多题选择，不推荐题号，不恢复旧选题流程。Agent 必须直接阅读 `problem.md`，并把歧义、材料缺口和拆分依据写入可见 workspace 产物。

## Required Inputs

```text
workspace/problem/problem.md
workspace/problem/images/
workspace/problem/attachments/
workspace/output/problem_audit.md
workspace/output/material_index.md
references/rubrics.md
references/feedback_layer1_critic.md
```

`reference.pdf` 如存在，仅作为 audit-only 材料；不能替代 `problem.md` 的题意来源。

## Required Outputs

```text
workspace/output/question_index.md
workspace/output/q*/
workspace/output/problem_audit.md      # 如发现歧义或材料问题则更新
workspace/output/material_index.md     # 如材料映射变化则更新
```

每个 `workspace/output/q*/` 目录在本阶段只建立产物契约，不进行模型选择或求解。

## Templates

```text
templates/workspace/root/question_index.md
```

如果模板字段不足，应在不破坏模板主体的前提下增加 decomposition notes、dependency graph、material mapping 等段落。

## Entry Conditions

- Stage 0 outputs exist。
- `workspace/problem/problem.md` 存在并可直接阅读。
- `problem_audit.md` 不包含阻塞题意理解的 material gap。
- `material_index.md` 已记录现有 images 和 attachments，或其缺失已在 `problem_audit.md` 中说明。

## Procedure

1. 执行三遍精读。

   第一遍：表层任务读取。

   - 标记题面中的显式要求、编号问题、交付物、输出形式；
   - 记录“求、预测、评价、优化、分类、设计、比较、验证、说明”等动作；
   - 注意题面要求的表格、图、模型、结论、建议、灵敏度或论文表达。

   第二遍：结构读取。

   - 抽取动词：predict、optimize、evaluate、classify、simulate、compare、design、explain、verify 等对应中文语义；
   - 抽取对象：实体、时间段、区域、网络、产品、资源、指标、主体、方案；
   - 抽取约束：容量、预算、时间、物理规律、政策规则、数据可得性、精度、边界条件；
   - 抽取数据接口：表格、图片、附件、测量变量、派生变量、需要估计的参数；
   - 抽取评价指标：目标值、误差、排名、稳定性、可行性、成本、收益、风险、鲁棒性。

   第三遍：隐含工作读取。

   - 识别题面没有单独编号但必须完成的任务：数据重构、变量定义、参数估计、基线构造、模型验证、灵敏度分析、图表解释；
   - 判断这些任务应作为独立 `q*`，还是并入某个显式子问题；
   - 不为很小的支持任务创建独立 `q*`，除非它会产生被多个问题复用的结果。

2. 建立任务清单。

   每条任务至少记录：

   ```text
   source section
   action verb
   object
   required output
   constraints
   data interface
   evaluation metric
   explicit or implicit
   ```

3. 区分显式子问题与隐式子问题。

   - 显式子问题来自题面直接要求；
   - 隐式子问题来自求解所必需的支撑工作；
   - 隐式子问题若只服务于一个显式 `q*`，优先写入该 `q*` 的 analysis notes；
   - 隐式子问题若会被多个 `q*` 复用，或其失败会阻塞全局结论，可单独设为 `q*`。

4. 构造子问题依赖图。

   在 `question_index.md` 中记录：

   ```text
   from q*
   to q*
   dependency type: data | parameter | result | method | figure | writing
   dependency description
   blocking if missing: yes | no
   ```

   要求：

   - 依赖图应尽量无环；
   - 如果存在循环依赖，先尝试重写拆分；
   - 无法消除时，在 `problem_audit.md` 中记录 ambiguity，并说明后续需要用户确认或保守处理。

5. 映射数据附件到子问题。

   对 `material_index.md` 中每个 material，标记：

   ```text
   material path
   material type
   used by q*
   expected role: input data | parameter source | validation reference | figure source | audit-only | unused
   risk if missing
   ```

   若题面引用材料但实际缺失，更新 `problem_audit.md`。若材料存在但暂无使用，记录为 optional、audit-only 或 unexplained，不要假装已使用。

6. 早期识别关键变量和符号。

   在 `question_index.md` 的每个 `q*` 下记录 early variable hints：

   - 可能的决策变量、状态变量、指标变量、参数；
   - 变量的自然单位和范围；
   - 与附件列名、图片标注、题面术语的对应关系；
   - 跨 `q*` 可能共享的符号；
   - 可能导致冲突的术语。

   本阶段不需要完成正式 `notation.md`，但必须为 Stage 2 提供足够线索。

7. 处理题意歧义。

   歧义进入 `problem_audit.md`，格式建议：

   ```text
   ambiguity id
   source in problem.md
   competing interpretations
   affected q*
   modeling impact
   recommended default
   requires user confirmation: yes | no
   ```

   若歧义会改变模型路线、输出形式或最终结论，Manual mode 必须暂停。

8. 写入 `question_index.md`。

   每个 `q*` 使用稳定 ID：`q1`、`q2`、`q3`。不要因后续模型选择轻易重编号；若必须改动，记录原因和影响。

   每个 `q*` 至少写入：

   ```text
   q id
   title
   explicit or implicit
   source section from problem.md
   action verb
   object
   goal
   expected output
   evaluation metric
   input materials
   data interface
   constraints
   dependencies
   early variables and symbols
   known ambiguity or risk
   next-stage planning focus
   ```

9. 建立 `workspace/output/q*/` 目录契约。

   对每个 `q*`，声明 Stage 2 将生成：

   ```text
   workspace/output/q*/analysis.md
   workspace/output/q*/candidates.md
   workspace/output/q*/model.md
   workspace/output/q*/assumptions.md
   workspace/output/q*/notation.md
   workspace/output/q*/data_recon.md
   ```

   本阶段不预先填充模型内容。

10. 运行 Layer 1 局部检查。

   使用 `references/feedback_layer1_critic.md` 中 decomposition 相关问题检查：

   - 显式任务是否全部覆盖；
   - 隐式支撑任务是否合理；
   - 数据附件映射是否可追踪；
   - 依赖是否清楚；
   - 歧义是否可见。

## Output Contract

`workspace/output/question_index.md` 必须包含：

```text
q id
title
explicit or implicit
source section from problem.md
action verb
object
goal
expected output
evaluation metric
constraints
input materials
data attachments
data interface
dependencies
dependency graph
early variables and symbols
known ambiguity or risk
next-stage planning focus
```

必要时更新：

```text
workspace/output/problem_audit.md
workspace/output/material_index.md
```

更新必须说明：

- 发现了什么；
- 影响哪些 `q*`；
- 是否改变下游建模路线；
- 是否需要用户确认。

## Quality Gate

进入 Stage 2 前必须满足：

- `problem.md` 中每个显式要求至少映射到一个 `q*`；
- 每个 `q*` 有明确 expected output；
- 每个 `q*` 的动作、对象、约束、数据接口和评价指标至少有初步记录；
- 必需材料已映射到对应 `q*`，或缺失已记录；
- 子问题依赖图清楚，且无未解释循环；
- 关键变量和跨问题符号风险已早期标记；
- 题意歧义已写入 `problem_audit.md`；
- 没有恢复旧式候选题比较、题目推荐或旧选题逻辑。

## Exit Conditions

- `question_index.md` 定义了解答题目所需的全部 `q*`。
- 每个 `q*` 有清晰依赖、材料映射和预期 deliverable。
- 歧义已解决，或已在 `problem_audit.md` 中记录并标明处理策略。
- Stage 2 可直接为每个 `q*` 建立 question card 和模型候选。

## Failure Handling

- 如果拆分有多个合理解释，且会改变模型路线或最终答案，暂停并请求用户确认。
- 如果材料缺口阻止拆解，更新 `problem_audit.md` 并停止进入 Stage 2。
- 如果隐式子问题必要但不确定，把它写入 `question_index.md` 并附 risk note，不要隐藏。
- 如果发现某个附件无法读取或无法定位，更新 `material_index.md` 和 `problem_audit.md`。
- 如果依赖图出现循环，先重拆；无法重拆时标记 ambiguity 并给出保守默认路径。

## Manual Mode Behavior

通常不暂停。只有当拆分选择会显著改变建模路线、输出形式、所需材料或最终结论时暂停。

暂停时只返回：

```text
workspace/output/question_index.md
workspace/output/problem_audit.md
workspace/output/material_index.md
```

并说明需要用户确认的拆分点。

## AP Mode Behavior

选择最有证据支撑、最可验证、最利于 traceability 的拆分。所有不确定性写入 `question_index.md`、`problem_audit.md` 或 `material_index.md`，并在后续 Stage 2 中作为风险处理。
