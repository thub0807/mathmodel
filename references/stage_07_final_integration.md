# Stage 7: Final Integration

## Purpose

把所有 `q*` summary、结果、验证、灵敏度和图表索引整合为最终结果、最终图表索引和强绑定 traceability，为 Stage 8 论文生成提供唯一可信的最终材料层。

本阶段的核心不是简单合并文件，而是统一符号、单位、模型命名，处理跨 `q*` 依赖和结果冲突，并决定哪些结果可进入摘要。

## Required Inputs

```text
workspace/output/question_index.md
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/figures/figure_index.md
workspace/output/q*/tables/table_index.md
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
references/result_traceability.md
references/feedback_layer2_backtrack.md
references/rubrics.md
```

## Required Outputs

```text
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
workspace/output/final/review_report.md     # if integration issues require early review notes
```

## Output Contract

`final_results.md` 必须汇总每个 `q*` 的 result status、core result、validation verdict、sensitivity verdict、paper use 和 limitation。

`final_figures_index.md` / `final_tables_index.md` 必须只列可追踪图表，并标记 include in paper。

`traceability.md` 必须绑定 paper claim、source q、result field、validation status、sensitivity status、figure/table support、abstract eligibility 和 limitation。

## Entry Conditions

- 至少一个 `q*` 有完成的 `q*_summary.md`。
- 每个 included result 都有 `pass`、`partial` 或 `fail` 状态。
- Stage 5 图表索引已存在，或明确说明无图表进入论文。
- Stage 6 summary 中的 paper-ready claims 已标明来源。

## Procedure

1. 汇总所有 `q*` 状态。

   建立 integration table：

   ```text
   q*
   summary status
   result status
   validation verdict
   sensitivity verdict
   paper use: full | limited | not allowed
   blocking issues
   ```

   `fail` 结果不得作为论文 claim；`partial` 结果必须带 limitation。

2. 统一符号。

   从所有 `review_packet.md` 和 `q*_summary.md` 中建立 unified notation register：

   ```text
   symbol
   unified meaning
   unit
   used by q*
   original variants
   action: keep | rename | split
   paper notation
   ```

   处理原则：

   - 同一符号不同含义时必须改名或限定作用域；
   - 同一含义多个符号时统一；
   - 共享参数必须单位一致；
   - 论文中只保留必要符号，不堆砌内部变量。

3. 统一单位。

   建立 unit harmonization table：

   ```text
   quantity
   source q*
   original unit
   final unit
   conversion rule
   affected result fields
   paper wording
   ```

   所有 final hard numbers 必须使用统一单位；无法统一时必须说明原因和限制。

4. 统一模型命名。

   从各 `review_packet.md` 和 `q*_summary.md` 汇总模型名称：

   ```text
   q*
   final model name
   model family
   alternate names rejected
   paper section name
   naming risk
   ```

   模型名应：

   - 具体描述机制、目标或数据关系；
   - 与 Stage 2 naming variants 一致；
   - 不夸大 novelty；
   - 在 final_results、paper.md 和 paper.tex 中保持一致。

5. 处理跨 `q*` 依赖。

   建立 dependency map：

   ```text
   upstream q*
   downstream q*
   dependency type: data | parameter | result | method | figure | writing
   source field
   upstream status
   downstream impact
   action needed
   ```

   检查：

   - 下游是否使用了 obsolete upstream result；
   - upstream 为 `partial` 时，下游是否降级；
   - upstream 为 `fail` 时，下游是否移除或重建；
   - 共享假设变化是否影响多个 `q*`。

6. 处理结果冲突。

   常见冲突：

   - 两个 `q*` 给出相反结论；
   - summary 与 validation 不一致；
   - sensitivity 说 unstable，但 summary 写 stable；
   - 图表 claim 与结果字段不一致；
   - 单位转换后数值不一致；
   - final answer 与 source result 不一致。

   处理规则：

   - 优先采用验证状态更强、source field 更直接的结果；
   - 无法解决时，两者都标 limitation；
   - 影响中心 claim 时触发 `references/feedback_layer2_backtrack.md`；
   - 不通过论文措辞掩盖冲突。

7. 决定摘要资格。

   每个 final claim 标记：

   ```text
   abstract eligibility: yes | no
   reason
   validation status
   result status
   limitation note
   ```

   规则：

   - `fail` 不得进入摘要，也不得作为正文结论；
   - `partial` 通常不作为摘要强结论，除非中心任务必须呈现且限制可简短诚实表达；
   - 摘要数字必须能追溯到 source field，且 validation status 不能为 fail；
   - 图表性、装饰性或边缘结果不进入摘要。

8. 建立 `final_results.md`。

   每条 final result 包含：

   ```text
   final result id
   source q*
   claim
   hard numbers and units
   model name
   status
   validation status
   sensitivity status
   abstract eligibility
   limitation note
   source files
   source fields
   paper section
   ```

   `final_results.md` 是 Stage 8 论文结果段的主来源。

9. 合并最终图表索引。

   `final_figures_index.md` 和 `final_tables_index.md` 必须保留：

   ```text
   visual id
   source q*
   supported claim
   source file
   source field
   validation status
   result status
   intended paper section
   citation location
   include in paper
   limitation note
   ```

   不可追踪或 failed claim 图表不得进入 final paper figure/table。

10. 建立强绑定 `traceability.md`。

   按 `references/result_traceability.md`，每个 paper-facing claim 都必须映射：

   ```text
   paper claim
   source question
   source file
   source field
   validation status
   result status
   allowed in abstract
   limitation note
   paper location
   ```

   hard numeric claims 优先直接映射到：

   ```text
   workspace/output/q*/results/result.json
   ```

   validation/sensitivity claim 映射到对应 md 段落或表行。

11. 传播限制。

   任一来源中的 `partial` 或 `fail` 必须进入：

   ```text
   workspace/output/final/final_results.md
   workspace/output/final/traceability.md
   workspace/output/final/review_report.md    # if needed
   ```

   限制措辞要能直接被 Stage 8 论文使用。

12. 运行集成层 backtrack。

   使用 `references/feedback_layer2_backtrack.md` 检查：

   - downstream claim 是否使用了失效 upstream；
   - notation/unit/model naming 是否冲突；
   - final result 是否比 source evidence 更强；
   - traceability 是否断链。

## Output Contract

`final_results.md` 必须包含：

```text
final result id
source q*
claim
hard numbers and units
model name
status
validation status
sensitivity status
abstract eligibility
limitation note
source files
source fields
paper section
```

`traceability.md` 必须包含：

```text
paper claim
source question
source file
source field
validation status
result status
allowed in abstract
limitation note
claim type
paper location
```

`final_figures_index.md` 和 `final_tables_index.md` 必须保留 claim binding 和 citation location。

## Quality Gate

进入 Stage 8 前：

- 符号、单位、模型名称跨问题一致；
- 跨 `q*` 依赖已记录；
- 结果冲突已解决、降级或标记；
- `final_results.md` 与 `traceability.md` 强绑定；
- 每个 paper-facing hard claim 都有 traceability row；
- 摘要资格已明确；
- `partial` 和 `fail` 限制已传播；
- failed result 不作为论文结论；
- final visual indexes 中没有不可追踪图表。

## Exit Conditions

- `traceability.md` 能追踪最终结果中每个 hard number、figure claim、table claim、assumption 和 notation。
- `final_results.md` 不把 failed artifacts 写成结论。
- abstract-eligible claims 已明确标记。
- Stage 8 可只依赖 final layer 和 source artifacts 生成论文。

## Failure Handling

- Stage 8 前移除或标记不可追踪 claim。
- 符号、单位或跨问题冲突写入 `review_report.md` 或返回对应 `q*` 修复。
- 冲突使结果失效时，返回受影响 `q*` 产物，或标记该结果不可用于论文结论。
- 如果 traceability 无法覆盖中心 claim，final result 必须降级或删除。

## Manual Mode Behavior

Stage 7 完成后、进入 Stage 8 前必须暂停，供用户审查以下文件：

```text
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
```

只列文件路径和需要审查的要点，不提前生成论文。

## AP Mode Behavior

只有在 traceability limitations 已完整保留时才继续到 Stage 8。若存在 unresolved conflict，AP mode 必须降级 claim 或写入 `review_report.md`，不得静默推进。
