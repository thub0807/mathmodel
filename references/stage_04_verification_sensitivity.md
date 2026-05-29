# Stage 4: Verification and Sensitivity

## Purpose

验证每个 `q*` 的结果是否可信，并测试关键结论在合理扰动下是否稳定。

本阶段决定 Stage 3 的结果能否进入 summary、traceability 和最终论文。验证不是重复结果，而是主动寻找约束违背、基线落后、边界异常、参数失稳和过度 claim。

## Required Inputs

```text
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/review_packet.md
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
references/rubrics.md
references/feedback_layer1_critic.md
references/feedback_layer2_backtrack.md
```

如有上游依赖，同时读取相关上游 `q*` 的 `result.json`、`validation.md`、`sensitivity.md` 或 summary。

## Required Outputs

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/review_note.md     # if findings require local notes
workspace/output/q*/warnings.md        # if new risks appear
```

影响最终论文的风险必须写成可迁移到以下文件的措辞：

```text
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

## Output Contract

`validation.md` 必须包含 sanity check、baseline comparison、constraint audit、boundary cases、result status verdict、paper claim eligibility 和 unresolved risks。

`sensitivity.md` 必须包含 tested parameters、perturbation ranges、single-parameter perturbation、joint perturbation、instability boundary、paper impact 和 limitations。

## Entry Conditions

- Stage 3 has produced `workspace/output/q*/results/result.json`。
- `result.json.status` 存在，且为 `pass`、`partial` 或 `fail`。
- `run.log` 能说明结果如何产生或为何失败。
- `review_packet.md` 中存在验证计划和灵敏度参数初选，或其缺失已在 `review_note.md` 中记录。

## Procedure

1. 读取结果与风险背景。

   从 `result.json` 和 `run.log` 提取：

   - hard numbers；
   - units；
   - source command；
   - solver or algorithm status；
   - warnings；
   - limitations；
   - expected result fields；
   - paper-facing claims。

   若 `result.json.status` 已是 `fail`，仍需写 `validation.md` 说明失败原因、是否有可保留的 limited evidence，以及是否需要回到 Stage 2 或 Stage 3。

2. 执行 sanity check。

   检查：

   - 数值量级是否合理；
   - 正负号是否合理；
   - 单位是否匹配 `review_packet.md`；
   - 单调性是否符合常识；
   - 结果是否落在可能范围；
   - 输出字段是否与 `review_packet.md` 预期一致；
   - toy demo 或手算 case 是否能复现关键方向。

   写入 `validation.md`：

   ```text
   check item
   expected behavior
   observed value
   pass/partial/fail
   implication
   ```

3. 执行 baseline 对比。

   优先使用 `review_packet.md` 中的 baseline。若 baseline 不存在，必须说明原因，并选择可防御替代：

   - 手算近似；
   - 简化模型；
   - 贪心规则；
   - 历史/题面参考；
   - 消融；
   - 交叉方法；
   - 常识边界。

   记录主模型相对 baseline：

   ```text
   better | comparable | worse | inconclusive
   ```

   如果主模型不优于 baseline，必须触发 claim downgrade 或 Layer 2 backtrack。

4. 检查约束满足。

   根据任务类型检查：

   - 优化：容量、预算、上下界、整数性、流量守恒、solver status、constraint residual；
   - 预测：训练/测试划分、误差、残差、外推范围；
   - 评价：指标方向、归一化、权重和排名；
   - 分类：类别平衡、阈值、混淆矩阵或关键 metric；
   - 仿真：重复次数、随机种子、情景覆盖、收敛；
   - 微分/机理：单位、初值、边界条件、稳定性；
   - 图网络：连通性、边权含义、容量或路径合法性。

   任何硬约束违背都必须进入 `validation.md` 和 `review_note.md`。

5. 检查边界条件。

   选择有意义的边界：

   - zero / empty case；
   - minimum / maximum；
   - small toy case；
   - extreme capacity；
   - all-equal indicators；
   - single-node / disconnected graph；
   - no-demand / high-demand scenario；
   - known-simple classification or ranking case。

   如果边界测试不适用，写明原因，不要留空。

6. 识别关键参数。

   从 `review_packet.md`、`result.json` 和 domain reasoning 选择 3-5 个可能改变结论的参数。

   优先考虑：

   - 成本、容量、需求、价格；
   - 权重、阈值、误差率；
   - 初值、增长率、转移率；
   - 情景概率、资源上限；
   - 数据清洗或重构参数；
   - solver tolerance 或随机 seed（如果会影响结果）。

   在 `sensitivity.md` 记录：

   ```text
   parameter
   baseline value
   source
   why important
   plausible range
   affected result field
   ```

7. 执行单参数扰动。

   对每个关键参数设置 low / nominal / high。常见范围可从题面、数据分位、领域常识或合理百分比扰动获得，但必须写明来源。

   记录：

   ```text
   parameter
   low
   nominal
   high
   output at low
   output at nominal
   output at high
   absolute change
   relative change
   conclusion impact
   ```

   不得只说“变化不大”；必须报告影响方向和规模。

8. 执行多变量联合扰动。

   构造至少三类情景，除非明确不可行：

   - optimistic scenario；
   - pessimistic scenario；
   - mixed or stress scenario。

   对参数多的模型，选择 2-4 个最有影响的参数，并说明选择理由。

   记录 joint perturbation：

   ```text
   scenario
   varied parameters
   rationale
   result
   conclusion impact
   ```

9. 定位失稳边界和临界参数。

   查找主结论发生变化的阈值：

   - 可行变不可行；
   - 排名变化；
   - 分类翻转；
   - 推荐方案变化；
   - 预测误差超过可接受范围；
   - 风险概率跨过决策阈值；
   - 优化目标出现明显退化。

   在 `sensitivity.md` 中标记：

   ```text
   stable range
   conditionally stable range
   failure range
   critical parameter
   threshold value
   paper wording impact
   ```

10. 判断结果可信度。

   使用 `PASS`、`PARTIAL`、`FAIL`：

   - `PASS`：sanity、baseline、约束、边界、敏感性总体支持结果，没有 unresolved high issue；
   - `PARTIAL`：结果可用，但有明确范围、假设、数据或稳定性限制；
   - `FAIL`：结果被验证反驳、不可复现、约束违规、敏感性推翻，或不能支撑论文 claim。

   如果 `result.json.status` 与验证 verdict 不一致，论文侧采用更严格 verdict，并写明原因。

11. 写 `validation.md`。

   必须包含：

   ```text
   sanity check
   baseline or comparison method
   constraint satisfaction
   boundary conditions
   consistency with assumptions and notation
   failure cases
   validation verdict: PASS | PARTIAL | FAIL
   affected claims
   required downgrade or backtrack
   ```

12. 写 `sensitivity.md`。

   必须包含：

   ```text
   key parameters
   perturbation ranges
   single-parameter results
   joint perturbation scenarios
   instability boundary
   critical parameters
   stable or unstable conclusions
   paper impact
   ```

13. 写入风险传播说明。

   任何影响最终论文使用的风险必须用可迁移措辞写入：

   ```text
   workspace/output/q*/validation.md
   workspace/output/q*/sensitivity.md
   workspace/output/q*/review_note.md
   workspace/output/q*/warnings.md
   ```

   后续应进入：

   ```text
   workspace/output/final/traceability.md
   workspace/output/final/review_report.md
   workspace/output/final/quality_report.md
   ```

14. 运行 Layer 1 和 Layer 2。

   使用 `references/feedback_layer1_critic.md` 检查 validation/sensitivity 完整性。

   以下情况必须触发 `references/feedback_layer2_backtrack.md`：

   - 验证推翻 `review_packet.md` 的目标、约束或假设；
   - 灵敏度推翻 `q*` 的主要结论；
   - baseline 明显优于主模型；
   - 单位、符号或数据处理与 Stage 2/3 不一致；
   - `result.json.status` 与 validation verdict 不一致；
   - paper-facing claim 必须移除或降级；
   - 上游 `q*` 的结果变化影响当前问题；
   - 异常数据处理影响中心结论。

## Output Contract

`workspace/output/q*/validation.md` 必须包含：

```text
sanity check
baseline or comparison method
constraint satisfaction
boundary conditions
consistency with assumptions and notation
failure cases
PASS/PARTIAL/FAIL judgment
affected claims
backtrack trigger if any
```

`workspace/output/q*/sensitivity.md` 必须包含：

```text
key parameters
perturbation ranges
single-parameter results
joint perturbation scenarios
instability boundary
critical parameters
stable or unstable conclusions
paper impact
```

风险必须写成可进入以下文件的句子：

```text
workspace/output/final/traceability.md
workspace/output/final/review_report.md
workspace/output/final/quality_report.md
```

示例：

```text
该结论仅在需求参数位于 [low, high] 范围内稳定；超出该范围时推荐方案发生变化，因此 final paper 中只能作为条件稳定结论使用。
```

## Quality Gate

进入 Stage 5 前：

- `validation.md` 必须声明 `PASS`、`PARTIAL` 或 `FAIL`；
- sanity check 已完成；
- baseline 或 comparison 存在，或其缺失有充分理由；
- 约束满足检查已完成；
- 边界条件已测试或标记 not applicable；
- sensitivity 测试重要参数，而非装饰参数；
- 单参数扰动有输出变化；
- 多变量联合扰动已尝试，或说明不可行；
- 失稳边界或稳定范围已记录；
- 任何 `PARTIAL` 或 `FAIL` 风险已准备向 final reporting 传播；
- 触发条件存在时已执行或标记 Layer 2 backtrack。

## Exit Conditions

- `validation.md` 给出带证据的最终 `PASS`、`PARTIAL` 或 `FAIL` judgment。
- `sensitivity.md` 说明主结论 stable、conditionally stable 或 unstable。
- `result.json.status` 与 validation verdict 的不一致已解释。
- 需要降级、移除或回溯的 claim 已记录。

## Failure Handling

- 如果 validation fails，先更新或限定 downstream status，再进入 Stage 5。
- 如果 sensitivity undermines result，把受影响结论标为 limited 或 unusable。
- 如果 validation contradicts `result.json.status`，记录 mismatch，并采用更严格 judgment 作为 paper-facing verdict。
- 如果发现 instability boundary，下游 summary 必须先说明 stable range 才能使用结果。
- 如果 baseline 优于主模型，回到 Stage 2/3 或把主模型 claim 降级。
- 如果关键参数无法确定范围，把结论标为 `PARTIAL`，并在 `quality_report.md` 风险措辞中保留。
- 如果需要 final reporting，将风险写成可直接迁移到 `quality_report.md` 的句子。

## Manual Mode Behavior

当 verification 推翻所选 Plan、使 pass result 变为 unusable、要求 rebuild、移除中心 claim 或触发重要 L2 backtrack 时暂停。

暂停时只列相关文件：

```text
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/q*/review_note.md
workspace/output/q*/warnings.md
```

并说明需要用户确认的 downgrade、rebuild 或 claim removal。

## AP Mode Behavior

继续执行，但必须在 `validation.md` 和 `sensitivity.md` 中写明 limitation。若结论为 `PARTIAL` 或 `FAIL`，必须把风险带入后续 `traceability.md`、`review_report.md` 和 `quality_report.md`，不得以论文措辞掩盖。
