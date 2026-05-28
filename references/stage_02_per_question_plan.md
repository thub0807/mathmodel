# Stage 2: Per-Question Plan

## Purpose

在任何 build、solve 或 verification 前，为每个 `q*` 建立可审阅、可实现、可验证的 Plan 文件集。

本阶段把 Stage 1 的题意拆解转化为建模路线：question card、候选模型、最终模型选择、假设、符号、数据重构计划、toy demo 计划和 red-team 风险回应。不得跳过候选比较直接写求解代码。

## Required Inputs

```text
workspace/output/question_index.md
workspace/output/problem_audit.md
workspace/output/material_index.md
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
```

如当前 `q*` 依赖其他问题，应同时读取上游 `q*` 已存在的 relevant summary、result 或 limitation。

## Required Outputs

```text
workspace/output/q*/analysis.md
workspace/output/q*/solution_plan.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode or if needed
```

Manual mode 下 `solution_plan.md` 和 Plan 文件集完成后暂停，不进入 Stage 3。

## Templates

```text
templates/workspace/q/analysis.md
templates/workspace/q/solution_plan.md
templates/workspace/q/candidates.md
templates/workspace/q/model.md
templates/workspace/q/assumptions.md
templates/workspace/q/notation.md
templates/workspace/q/data_recon.md
templates/workspace/q/warnings.md
templates/workspace/q/review_note.md
```

模板字段不足时，可以增加 question card、candidate matrix、toy demo plan、red-team notes、model naming variants 等段落。

## Entry Conditions

- Stage 1 has produced `workspace/output/question_index.md`。
- 当前 `q*` 已定义 inputs、outputs、dependencies 和 materials。
- 题意歧义若会影响模型选择，已在 `problem_audit.md` 中解决或标记默认处理。
- 所需附件、图片或数据源已在 `material_index.md` 中定位，或缺失已记录。

## Procedure

1. 建立每个 `q*` 的 question card。

   写入 `analysis.md`：

   ```text
   q id
   source section from problem.md
   task type
   action verb
   object
   required input
   required output
   variables to define
   constraints
   objective or evaluation metric
   data requirements
   upstream dependencies
   downstream use
   paper-facing answer form
   ambiguity or risk
   ```

   要求：

   - 输入必须区分题面给定、附件提供、上游结果、Agent 需估计；
   - 输出必须说明是数值、表格、排序、分类、方案、图、解释还是政策建议；
   - 约束和目标必须来自题意，不要凭空添加。

2. 调用 `references/model_catalog.md`。

   依据 question card 中的 task type、action verb、object、constraints 和 data requirements：

   - 找到 2-4 个最可能的模型族；
   - 判断每个模型族的数据需求、输出形式、可解释性、失败模式；
   - 确认与 code starter 的潜在对应关系；
   - 把模型族选择理由写入 `analysis.md` 或 `candidates.md`。

3. 调用 `references/rubrics.md`。

   对当前 `q*` 明确质量要求：

   - 题意理解是否足够；
   - 模型选择是否需要 baseline；
   - 实现证据如何进入 `result.json`；
   - 验证和灵敏度至少检查什么；
   - CUMCM 论文表达需要什么模型名、图表或结果解释。

   把这些标准写入 `review_note.md` 或 `analysis.md` 的 quality expectations。

4. 生成至少 3 个候选模型。

   候选应尽量包括：

   - baseline：透明、可手算或快速实现；
   - main model：最符合任务、数据和论文表达的主路线；
   - robust alternative：用于检验结论是否依赖单一建模选择。

   如果不足 3 个，必须在 `candidates.md` 解释：

   ```text
   shortage reason
   why additional candidate would be artificial
   how baseline or toy demo will be strengthened
   risk carried forward
   ```

5. 写候选模型比较矩阵。

   `candidates.md` 必须包含下列维度：

   ```text
   candidate
   model family
   fit to q*
   data requirements
   interpretability
   implementation complexity
   validation feasibility
   CUMCM paper expressiveness
   risk
   expected result fields
   reason kept or rejected
   ```

   维度说明：

   - 题意适配性：是否直接回答 required output；
   - 数据需求：是否已有、需重构、需估计、缺失；
   - 可解释性：变量、参数、结果是否能进入论文解释；
   - 实现复杂度：Python 实现和求解风险；
   - 验证可行性：是否有 baseline、边界、残差、约束或交叉方法；
   - CUMCM 论文表达力：是否支持具体模型名、图表、假设、结果解释；
   - 风险：数学、数据、计算、论文审查风险。

6. 选择最终模型路线。

   在 `model.md` 中说明：

   ```text
   selected model name
   selected model family
   why it fits the task
   why it fits available data
   why it is implementable
   why it is verifiable
   why it is explainable in paper
   rejected candidates and reasons
   fallback if build fails
   ```

   如果没有强候选，写入 `warnings.md`，Manual mode 暂停；AP mode 只能在 limitation 明确时继续。

7. 生成模型命名变体。

   在 `model.md` 或 `candidates.md` 中给出 2-4 个 paper-facing name variants：

   ```text
   name variant
   what mechanism it emphasizes
   why accepted or rejected
   final name
   ```

   命名规则：

   - 描述真实机制、目标或数据关系；
   - 不使用空泛“改进”“智能”“综合”除非有实质依据；
   - hybrid 名称必须对应真实的数据流或模型组合。

8. 写模型完整 plan。

   `model.md` 应包含：

   - 变量、参数、单位、定义域；
   - 目标函数、评价指标或控制方程；
   - 约束条件；
   - 算法或求解步骤；
   - 预期 `result.json` 字段；
   - run 成功和失败的判据；
   - Stage 4 验证计划；
   - Stage 4 灵敏度参数初选；
   - fallback route。

9. 规划 toy demo / 最小可行性验证。

   在 `model.md` 写入：

   ```text
   toy demo input
   minimal data needed
   expected qualitative output
   success signal
   failure signal
   what failure blocks
   ```

   toy demo 可以是：

   - 极小规模优化实例；
   - 手工构造预测序列；
   - 3-5 个对象的评价矩阵；
   - 小型分类样本；
   - 简化仿真情景。

   toy demo 目的不是证明最终结果，而是验证模型可落地、变量方向正确、代码路径可运行。

10. 写 `assumptions.md`。

   每条假设包含：

   ```text
   assumption
   source or rationale
   used by which formula/code step
   risk if violated
   validation or sensitivity hook
   paper wording note
   ```

   禁止装饰性假设。未被模型、代码或论文解释使用的假设应删除。

11. 写 `notation.md`。

   每个符号包含：

   ```text
   symbol
   meaning
   unit
   domain
   q* scope or shared
   source
   code variable candidate
   ```

   注意早期跨问题符号冲突；必要时写入 `warnings.md`。

12. 写 `data_recon.md`。

   包含：

   - source files；
   - required fields；
   - preprocessing steps；
   - missing data handling；
   - abnormal value handling；
   - unit conversion；
   - derived variables；
   - row/shape tracking；
   - output intermediate files；
   - data limitations。

13. 执行 red-team 风险攻击与回应。

   在 `review_note.md` 或 `warnings.md` 中回答：

   - 该模型最可能在数学上哪里失败？
   - 数据缺口如何推翻路线？
   - 求解器或计算复杂度是否会阻塞 Stage 3？
   - 验证若失败，fallback 是什么？
   - 评委会质疑模型名、假设或结果解释的哪一点？
   - 哪些 claim 只能作为 limited claim？

   每个攻击必须有 response：

   ```text
   attack
   severity
   response
   affected files
   carried risk
   ```

14. 运行 Layer 1 Plan critic。

   使用 `references/feedback_layer1_critic.md` 检查：

   - question card 是否完整；
   - 候选模型是否足够且不同；
   - 最终模型是否可实现、可验证；
   - 假设、符号、数据计划是否一致；
   - high risk 是否进入 `warnings.md` 或 `review_note.md`。

15. 写 `solution_plan.md`。

   `solution_plan.md` 是 Manual review 和 AP audit 的统一入口，必须包含：

   ```text
   question_id
   plan file paths
   selected model
   baseline and fallback
   implementation_language: python
   expected result.json fields
   data sources
   validation and sensitivity plan
   warnings and limitations
   build entry checklist
   ```

   该文件不得替代详细 Plan 文件，也不得加入尚未在 Plan 文件中出现的新路线。

## Output Contract

每个 `q*` 的 Plan 文件集必须足以让 Stage 3 不重新发明路线：

```text
workspace/output/q*/analysis.md
workspace/output/q*/solution_plan.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if needed
workspace/output/q*/review_note.md     # AP mode or risky route
```

`analysis.md` 必须包含 question card。

`solution_plan.md` 必须列出 Plan 文件路径、所选路线、默认 Python implementation language、预期 `result.json` 字段、验证计划和 Build 进入条件。

`candidates.md` 必须包含：

- 至少 3 个候选模型，或明确不足 3 个的原因；
- 比较矩阵；
- kept/rejected 理由；
- baseline 和 fallback 信息。

`model.md` 必须包含：

- 最终模型选择理由；
- 模型命名变体和 final name；
- 变量、公式、约束、算法；
- 预期 `result.json` 字段；
- toy demo / 最小可行性验证计划；
- red-team 后保留的风险。

## Quality Gate

进入 Stage 3 前：

- question card 完整；
- 候选比较具体，不是泛泛列模型名；
- 候选模型至少 3 个，或 shortage reason 合理；
- 所选模型匹配题意、数据、约束和论文表达；
- 公式、变量、约束明确到可实现；
- 假设与来源、风险、验证 hook 相连；
- 数据计划说明预处理、缺失、异常、派生变量；
- toy demo 能检验最小可行性；
- red-team high risk 已回应；
- `solution_plan.md` 已生成；
- Manual mode 完成 Plan 后必须暂停，只列文件路径。

## Exit Conditions

- 每个 planned `q*` 都有完整 Plan 文件集。
- 每个 planned `q*` 都有 `solution_plan.md`。
- 模型选择、数据计划、假设、符号、toy demo、风险回应清楚到足以 Build。
- Manual mode 已在每个 `q*` Plan 后暂停并只展示文件路径。
- AP mode 已写入 `review_note.md` 说明继续的理由和风险。

## Failure Handling

- 如果无法选择模型路线，写出竞争选项和各自风险，Manual mode 暂停。
- 如果数据或材料不足，写 `warnings.md`，不得隐藏限制。
- 如果少于 3 个候选，写 shortage reason，并加强 baseline 或 toy demo。
- 如果 red-team 发现 blocking issue，不进入 Stage 3，除非路线被修正或以 visible limitation 接受。
- 如果模型命名只能靠夸张词汇支撑，回到候选比较，重写为机制性命名。
- 如果 `rubrics.md` 或 Layer 1 critic 显示该 Plan 无法支撑 CUMCM 表达，补充模型解释、验证计划或图表计划。

## Manual Mode Behavior

每个 `q*` Plan 完成后，Stage 3 前暂停，只列生成的 Plan 文件路径：

```text
workspace/output/q*/analysis.md
workspace/output/q*/solution_plan.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md
workspace/output/q*/review_note.md
```

不得在暂停前开始 build 或生成结果。

## AP Mode Behavior

不等待用户，但必须写 `review_note.md`：

- 为什么所选模型可接受；
- 哪些候选被拒绝；
- toy demo 预期检查什么；
- red-team 后仍保留哪些风险；
- 这些风险如何在 Stage 3-4 中验证或降级。

AP mode 同样必须写 `solution_plan.md`，用于后续 review、traceability 和质量报告审计。
