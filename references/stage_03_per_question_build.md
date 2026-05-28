# Stage 3: Per-Question Build

## Purpose

按 Stage 2 已确认的 Plan，为每个 `q*` 实现求解、运行计算，并生成结果关口。

本阶段不是重新选模型，而是把 `model.md`、`assumptions.md`、`notation.md`、`data_recon.md` 落地为可审计代码、`run.log` 和符合 schema 语义的 `result.json`。所有 solve、verify-prep、figure-prep、data-processing code 必须使用锁定实现语言。

## Required Inputs

```text
workspace/output/q*/analysis.md
workspace/output/q*/solution_plan.md
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/assumptions.md
workspace/output/q*/notation.md
workspace/output/q*/data_recon.md
workspace/output/q*/warnings.md        # if exists
workspace/output/q*/review_note.md     # if exists
templates/workspace/q/results/result.schema.json
references/model_catalog.md
references/rubrics.md
references/feedback_layer1_critic.md
```

如当前 `q*` 依赖上游问题结果，同时读取相应：

```text
workspace/output/q*/results/result.json
workspace/output/q*/q*_summary.md
```

## Required Outputs

```text
workspace/output/q*/code/
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/warnings.md        # if new warnings appear
workspace/output/q*/review_note.md     # if L1 critic finds issues
```

## Templates

```text
templates/workspace/q/code/README.md
templates/workspace/q/results/result.schema.json
templates/workspace/q/results/result.example.json
templates/workspace/q/results/run_log.md
templates/shared/code_starter/result_io.py
templates/shared/code_starter/optimization.py
templates/shared/code_starter/prediction.py
templates/shared/code_starter/evaluation.py
templates/shared/code_starter/classification.py
templates/shared/code_starter/simulation.py
```

根据 `model.md` 的任务类型选择 code starter：

| 任务类型 | 优先 code starter |
|---|---|
| 优化、路径、资源分配、调度 | `templates/shared/code_starter/optimization.py` |
| 预测、回归、时间序列、参数估计 | `templates/shared/code_starter/prediction.py` |
| 综合评价、排序、指标赋权、聚类评价 | `templates/shared/code_starter/evaluation.py` |
| 分类、识别、风险等级 | `templates/shared/code_starter/classification.py` |
| 仿真、Monte Carlo、系统动力学、机理演化 | `templates/shared/code_starter/simulation.py` |

如果没有完全匹配的 starter，选择最接近的模板并在 `run.log` 中说明适配原因。

复制任一 starter 时，同时复制或等价实现 `templates/shared/code_starter/result_io.py`，以统一写入 `result.json` 和 `run.log`。

## Entry Conditions

- Stage 2 Plan exists for the current `q*`。
- `solution_plan.md` 存在并锁定 `implementation_language: python`。
- Manual mode 已收到用户确认，或 AP mode 已写入 `review_note.md`。
- `data_recon.md` 已记录必要数据路径和预处理决策。
- `model.md` 已定义预期 `result.json` 字段和 toy demo / 最小可行性检查。
- 阻塞级 `warnings.md` 不存在，或已被用户接受为 limited route。

## Procedure

1. 执行子问题求解循环。

   对每个 `q*` 采用以下循环：

   ```text
   model completion
   data preprocessing
   implementation
   toy/minimal run
   full run
   result interpretation
   L1 self-review
   output handoff
   ```

   若任一环节失败，先定位失败类型，再决定 patch、fallback、partial 或 fail。

2. 模型完整化。

   编码前检查 `model.md`：

   - 变量是否都有单位、域、shape；
   - 参数是否有来源或估计方式；
   - 目标函数、评价指标、控制方程、约束是否可计算；
   - 输入输出是否与 `analysis.md` 一致；
   - 预期 `result.json` 字段是否足以支撑后续 summary 和 traceability；
   - toy demo 是否能触发核心逻辑。
   - `solution_plan.md` 是否与详细 Plan 文件一致，并确认 implementation language 为 Python。

   如发现模型不完整，先 patch `model.md`、`notation.md` 或 `assumptions.md`；不得在代码中引入隐藏假设。

3. 公式到代码的落地规则。

   - 每个公式中的变量必须能对应到 `notation.md` 和代码变量；
   - 目标函数或评价指标应封装成清楚函数；
   - 约束检查应保留为可重复调用的函数或输出表；
   - 单位转换集中处理，不散落在多个计算段；
   - 随机过程必须设置并记录 seed；
   - 启发式算法必须记录迭代次数、停止条件和最佳值；
   - 机器学习类模型必须记录 split、特征、target 和 metric；
   - 评价类模型必须记录指标方向、归一化、权重和排名；
   - 仿真类模型必须记录情景、重复次数和输出统计。

4. 选择并接入 code starter。

   - 从 `templates/shared/code_starter/` 复制或参考最接近的 starter；
   - 将其放入 `workspace/output/q*/code/` 下，并按当前 `q*` 改名；
   - 保留 starter 中有价值的输入、运行、输出结构；
   - 保留或等价实现 starter 的 `write_result_and_log` 输出约定；
   - 删除与当前任务无关的占位逻辑；
   - 在文件顶部或 `README.md` 中说明该代码对应的 `q*`、模型名、输入、输出。

5. 实现数据预处理。

   只读取 `data_recon.md` 和 `material_index.md` 中记录的材料：

   - 文件读取路径必须可复核；
   - 记录 cleaning、filtering、unit conversion、normalization；
   - 记录 missing value handling；
   - 记录 abnormal value handling；
   - 记录 derived variables；
   - 记录输入输出 shape；
   - 必要的中间结果保存在 `workspace/output/q*/code/` 或 `workspace/output/q*/results/` 可审计位置。

   不得静默删除行、改列名、补值或重标单位。

6. 异常数据处理。

   对异常数据采用显式策略：

   ```text
   abnormal type
   detection rule
   affected rows/items
   handling method: keep | remove | cap | impute | flag | scenario
   rationale
   effect on result
   ```

   如果异常值可能影响中心结论，必须在 `warnings.md` 或 `review_note.md` 中记录，并进入 Stage 4 sensitivity。

7. 运行 toy demo / 最小可行性检查。

   先用 Stage 2 设计的最小输入验证：

   - 代码能运行；
   - 变量方向正确；
   - 约束或指标能计算；
   - 输出字段能写入 `result.json` 结构；
   - 结果量级有基本解释。

   toy demo 失败时，先修代码或模型 plan；若失败说明路线不可行，转 fallback 或标记 blocked。

8. 执行完整求解实现。

   根据任务类型生成：

   - 优化：决策变量、目标值、约束残差、可行性、solver status；
   - 预测：预测值、误差、残差、区间或 horizon；
   - 评价：权重、得分、排名、排序稳定信息；
   - 分类：类别、概率、混淆矩阵或关键 metric；
   - 仿真：情景、重复次数、均值/区间、风险概率；
   - 机理模型：参数、轨迹、稳定性或关键时刻；
   - 图网络：路径、流量、瓶颈、总成本或中心性。

9. 解释结果。

   在 `result.json` 可容纳字段中写入解释；否则写入 `run.log` 的 interpretation notes。

   解释必须说明：

   - 数字代表什么；
   - 单位是什么；
   - 与题目目标如何对应；
   - 是否满足约束；
   - 能否进入论文 claim；
   - 有哪些 immediate limitations。

10. 处理执行异常。

   必须显式记录：

   - solver infeasibility；
   - missing data；
   - convergence failure；
   - unstable estimate；
   - empty output；
   - timeout；
   - schema mismatch；
   - external library failure。

   不得用猜测值替代失败结果。

11. 写 `workspace/output/q*/results/run.log`。

   `run.log` 必须包含：

   ```text
   q id
   model name
   command
   implementation language
   code files
   input files
   output files
   code starter used
   environment notes
   preprocessing notes
   abnormal data handling
   random seed if relevant
   solver or algorithm settings
   toy demo result
   full run result summary
   warnings
   errors
   runtime or solver notes
   interpretation notes
   ```

12. 写 `workspace/output/q*/results/result.json`。

   `result.json` 必须与以下 schema 在语义上对齐：

   ```text
   templates/workspace/q/results/result.schema.json
   ```

   要求：

   - `status` 必须是 `pass`、`partial` 或 `fail`；
   - hard numbers 进入结构化字段；
   - 单位、来源命令、输入文件、输出文件可追踪；
   - `warnings` 和 `limitations` 反映 partial/fail 风险；
   - 字段名与 `model.md` 的 expected result fields 对齐；
   - 论文可能使用的数字必须先出现在 `result.json`。

13. 执行 L1 自评。

   使用 `references/feedback_layer1_critic.md` 的 Build Critic 检查：

   - `run.log` 是否足够复现；
   - `result.json` 是否包含所有硬数字；
   - 结果状态是否与证据匹配；
   - 代码公式是否匹配 `model.md`；
   - 单位是否匹配 `notation.md`；
   - 隐含假设是否已回写；
   - failure 是否可见。

   如果发现 high issue，先修 `run.log`、`result.json`、`warnings.md` 或回到 Stage 2，而不是进入 Stage 4。

14. 输出移交。

   Stage 3 完成后，向 Stage 4 移交：

   ```text
   workspace/output/q*/code/
   workspace/output/q*/results/result.json
   workspace/output/q*/results/run.log
   workspace/output/q*/warnings.md
   workspace/output/q*/review_note.md
   ```

   同时明确哪些结果可验证、哪些只是 partial、哪些不能用于论文。

## Output Contract

`workspace/output/q*/code/` 必须包含实现文件，或包含 README 解释为什么无法产生可执行代码。

`workspace/output/q*/results/run.log` 必须记录：

```text
q id
model name
command
inputs
outputs
implementation language
code starter used
environment notes
preprocessing notes
abnormal data handling
warnings
errors
runtime or solver notes
toy demo result
interpretation notes
```

`workspace/output/q*/results/result.json` 必须在概念上符合：

```text
templates/workspace/q/results/result.schema.json
```

论文使用的 hard numbers 必须先进入 `result.json`，之后才能进入 summary、traceability 或 final paper。

## Quality Gate

进入 Stage 4 前：

- code path 存在且可审计；
- 已根据任务类型接入或说明 code starter；
- implementation language 为 Python，且 solve、verify-prep、figure-prep、data-processing code 未混用其他语言；
- preprocessing 遵循 `data_recon.md`；
- 异常数据处理可见；
- 代码公式匹配 `model.md`；
- 单位匹配 `notation.md`；
- 实现所需假设已记录；
- toy demo 或最小可行性检查已运行或说明不可行；
- `run.log` 说明成功或失败；
- `result.json.status` 存在且有依据；
- unverified results 未写成最终结论；
- L1 自评没有 unresolved high issue。

## Exit Conditions

- `result.json` 存在，并在语义上符合 `templates/workspace/q/results/result.schema.json`。
- `result.json.status` 是 `pass`、`partial` 或 `fail`。
- `run.log` 说明结果如何产生，或为何失败。
- 如果结果是 `partial` 或 `fail`，限制已写入 `warnings.md` 或 `review_note.md`。

## Failure Handling

- 如果执行失败，写 `run.log`，设置 `result.json.status` 为 `fail` 或 `partial`，保留诊断信息。
- 如果 toy demo 失败，先修模型/代码；无法修复时启用 fallback 或阻塞。
- 如果完整运行失败但基线可运行，可把主模型标为 `fail`，基线结果作为 limited result，但必须在 `result.json` 中明确。
- 如果数据预处理改变建模路线，回到 Stage 2 修 Plan，或在 `review_note.md` 写 visible limitation。
- 如果 code starter 不适配，记录不适配原因和替代实现方式。
- 如果 hard number 不在 `result.json`，不得提升到论文侧产物。
- 如果出现 schema mismatch，优先修 `result.json` 结构；不能修复时标记 `partial` 或 `fail`。

## Manual Mode Behavior

通常继续到 Stage 4。若 `status` 为 `partial` 或 `fail`，或需要 fallback/rebuild，暂停并只列出受影响文件：

```text
workspace/output/q*/results/result.json
workspace/output/q*/results/run.log
workspace/output/q*/warnings.md
workspace/output/q*/review_note.md
```

说明限制，但不隐藏失败。

## AP Mode Behavior

继续到 Stage 4，但必须把所有 warnings、partial/fail 状态、异常数据处理和 fallback 信息带入 validation、sensitivity 和后续 traceability。
