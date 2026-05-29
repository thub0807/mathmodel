# Stage 8: Paper Generation

## Purpose

仅从已验证、可追踪、已完成 final integration 的产物生成 CUMCM 风格论文。

本阶段的目标是把 `q*_summary.md` 和 final layer 转化为完整论文，而不是重新发明结果。论文硬数字、图表 claim、模型结论都必须来自可追溯来源。

## Required Inputs

```text
workspace/problem/problem.md
workspace/output/q*/review_packet.md
workspace/output/q*/q*_summary.md
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/final/traceability.md
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/phrase_bank.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_structures.md
competitions/cumcm/distilled_formats.md
templates/latex/cumcm/cumcmthesis/
references/rubrics.md
references/feedback_layer1_critic.md
```

默认只按 CUMCM 材料生成论文结构和表达。

## Required Outputs

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf       # if generated
workspace/output/final/source/
workspace/output/final/review_report.md    # if generation warnings need early recording
```

## Output Contract And Rendering Assets

```text
templates/latex/cumcm/cumcmthesis/
```

`paper.md` 是 Markdown 中间稿，必须先形成完整可读论文草稿。CUMCM 正式排版优先使用 `templates/latex/cumcm/cumcmthesis/`。若正式 LaTeX 资产不可用，helper 可生成内部临时 LaTeX 草稿并在 `render_report.json` 与 Stage 9 final review 中记录原因；不得把临时草稿当作正式 CUMCM 模板。

## Entry Conditions

- Stage 7 outputs exist。
- `traceability.md` 明确哪些 claims 可进入正文和摘要。
- `final_results.md` 不包含 unresolved source conflict。
- `final_figures_index.md` 和 `final_tables_index.md` 已标记 include in paper。
- 没有论文必须使用但不可追踪的 hard number。
- Manual mode 下 Stage 7 checkpoint 已由用户审查或接受继续。

## Procedure

1. 加载 CUMCM 写作知识。

   使用：

   ```text
   competitions/cumcm/paper_skeleton.md
   competitions/cumcm/abstract_template.md
   competitions/cumcm/winning_patterns.md
   competitions/cumcm/phrase_bank.md
   competitions/cumcm/anti_patterns.md
   competitions/cumcm/distilled_structures.md
   competitions/cumcm/distilled_formats.md
   ```

   用途：

   - `paper_skeleton.md`：确定默认章节；
   - `abstract_template.md`：指导摘要结构；
   - `winning_patterns.md`：作为质量 anchor；
   - `phrase_bank.md`：提供中文学术表达，不能替代证据；
   - `anti_patterns.md`：检查常见失败；
   - `distilled_structures.md`：组织问题分析、模型建立、结果讨论；
   - `distilled_formats.md`：统一公式、图表、caption、引用格式。

2. 使用 CUMCM 默认写作结构。

   `paper.md` 建议结构：

   ```text
   标题
   摘要
   关键词
   1 问题重述
   2 问题分析
   3 模型假设
   4 符号说明
   5 模型建立与求解
   6 结果分析与验证
   7 灵敏度分析
   8 模型评价与推广
   参考文献
   附录
   ```

   具体章节可根据题目调整，但不得省略结果、验证、灵敏度和局限性表达。

3. 先写 Markdown 中间稿 `paper.md`。

   `paper.md` 是主契约：

   - 完整表达论文逻辑；
   - 可被人工审阅；
   - 包含所有正文 claim；
   - 图表位置和来源清楚；
   - hard numbers 都可追踪；
   - partial/fail 限制可见。

   不要直接只生成 LaTeX 而跳过 Markdown 中间稿。

4. 严格限制硬数字来源。

   论文中的硬数字只能来自：

   ```text
   workspace/output/q*/results/result.json
   workspace/output/q*/validation.md
   workspace/output/q*/sensitivity.md
   workspace/output/final/final_results.md
   workspace/output/final/traceability.md
   ```

   不能从记忆、临时计算、未记录草稿、图中目测值或无 source field 的文字中引入硬数字。

5. 写问题重述。

   - 依据 `problem.md` 重述背景和任务；
   - 不新增题目没有要求的目标；
   - 保持简洁，突出建模对象、输入、输出和约束；
   - 避免复制题面大段文字。

6. 写问题分析。

   使用 Stage 1 和各 `q*_summary.md`：

   - 说明各子问题如何衔接；
   - 解释为什么需要分步建模；
   - 点出数据接口、变量关系和评价指标；
   - 为模型选择埋下逻辑，而不是直接列模型名。

7. 写模型假设和符号说明。

   - 只写对模型和结果必要的假设；
   - 假设要说明作用和合理性；
   - 符号表统一使用 Stage 7 后的 notation；
   - 单位保持一致；
   - 不把内部临时变量全部堆入符号表。

8. 写模型建立章节。

   对每个主要 `q*`：

   - 先写建模动机；
   - 写模型变量、参数、目标/指标、约束或控制方程；
   - 写模型名称和模型族；
   - 说明模型为什么适合题意和数据；
   - 使用 `distilled_structures.md` 提供的结构模式；
   - 避免公式装饰化，公式必须与实现和结果相连。

9. 写求解章节。

   从 `q*_summary.md` 和 `run.log` 提炼：

   - 数据预处理；
   - 算法步骤；
   - 求解器或库；
   - 参数设定；
   - 输出字段；
   - 失败或 fallback 情况。

   文字应说明从输入到结果的过程，而不是只写“用 Python 求解”。

10. 写结果分析章节。

   使用 `final_results.md` 和 `traceability.md`：

   - 按 `q*` 或主题组织答案；
   - 每个结论给出 hard number、单位和含义；
   - partial 结果必须写限制；
   - fail 结果不得作为结论；
   - 结果表应直接回答题目。

11. 嵌入图表论证。

   只使用 `final_figures_index.md` 和 `final_tables_index.md` 中 include in paper 的图表。

   每张图表必须：

   - 在正文中被引用；
   - 说明支撑哪个 claim；
   - caption 符合 `distilled_formats.md`；
   - partial/fail 限制可见；
   - 不能仅作装饰。

12. 写验证、灵敏度、优缺点章节。

   验证章节应包含：

   - sanity check；
   - baseline comparison；
   - constraint satisfaction；
   - boundary cases；
   - validation verdict。

   灵敏度章节应包含：

   - key parameters；
   - single-parameter perturbation；
   - joint perturbation；
   - instability boundary；
   - stable / conditionally stable / unstable conclusion。

   优缺点章节应：

   - 具体说明模型优势；
   - 具体说明局限和影响；
   - 提出可行改进；
   - 不写空泛“有一定误差，未来可改进”。

13. 使用 phrase bank。

   `competitions/cumcm/phrase_bank.md` 用于改进中文表达：

   - 连接建模逻辑；
   - 表达验证和灵敏度；
   - 写 limitation；
   - 写摘要方法句和结果句。

   禁止用 phrase bank 生成无证据 claim。表达只能润色已有证据。

14. 写摘要，且最后写。

   使用 `abstract_template.md`：

   - 第一段交代问题与建模路线；
   - 后续按核心问题写方法和结果；
   - 尽量包含可追踪 hard numbers；
   - 说明关键验证或稳定性；
   - 避免背景铺陈过长；
   - 避免 unsupported superlatives。

   摘要规则：

   - 摘要数字必须在 `traceability.md` 中允许；
   - validation status 不能为 fail；
   - partial 结果通常不作为摘要强结论，除非限制可简短呈现；
   - fail 结果不得进入摘要。

15. 反模式检查。

   使用 `competitions/cumcm/anti_patterns.md` 检查：

   - 摘要空泛；
   - 模型名夸大；
   - 假设装饰化；
   - 公式与求解脱节；
   - 结果无硬数字；
   - 图表无解释；
   - 验证/灵敏度装饰化；
   - limitation 被隐藏。

   发现问题应在 `paper.md` 中修正，或写入 `review_report.md` 供 Stage 9。

16. 生成 CUMCM LaTeX。

   优先使用：

   ```text
   templates/latex/cumcm/cumcmthesis/
   ```

   要求：

   - 正式排版使用 cumcmthesis 结构；
   - 图表、公式、参考文献、附录格式尽量按模板；
   - 未由用户提供的正式字段使用安全占位，不伪造身份或队伍信息；
   - 若使用内部临时 LaTeX 草稿，必须记录正式模板不可用原因。

17. 生成 `paper.pdf`。

   如果环境支持 LaTeX 编译，生成 PDF 并记录命令。若失败：

   - 保留 `paper.md` 和 `paper.tex`；
   - 记录错误；
   - 在 Stage 9 review 中报告；
   - 不隐藏失败。

18. 存放 source assets。

   将论文所需图、表、LaTeX source、参考资源或生成说明放入：

   ```text
   workspace/output/final/source/
   ```

## Output Contract

`paper.md` 必须是完整 Markdown 中间稿，包含摘要、关键词、问题重述、问题分析、模型假设与符号、数据处理、模型建立与求解、结果分析、验证、灵敏度、优缺点、参考文献和附录。

`paper.tex` 应优先使用 CUMCM formal template：

```text
templates/latex/cumcm/cumcmthesis/
```

若使用内部临时 LaTeX 草稿，必须记录原因。

`source/` 必须包含或引用审计 paper generation 所需资产。

论文中每个 hard number、figure claim、table claim 都必须能通过 `traceability.md` 找到 source。

## Quality Gate

进入 Stage 9 前：

- `paper.md` 完整且可读；
- 论文每个 hard number 出现在 `traceability.md`；
- 摘要数字可追踪且 validation status 不是 fail；
- CUMCM 结构、摘要、caption、公式、表格符合知识文件；
- partial limitation 在正文保留；
- fail result 未作为论文 claim；
- 图表被嵌入论证而非装饰；
- phrase bank 只用于润色已有证据；
- anti-pattern hits 已修复或写入 final review；
- 当 `cumcmthesis` 可用时，内部临时 LaTeX 草稿不被当作正式模板。

## Exit Conditions

- `paper.md` 和 `paper.tex` 不引入 unsupported claims。
- 如生成 `paper.pdf`，它对应当前 `paper.tex`。
- PDF generation failure 被记录，供 Stage 9 review，而不是隐藏。
- Stage 9 可直接审查论文、traceability、图表和质量报告。

## Failure Handling

- claim 不可追踪时，移除或改写为 clearly limited statement。
- 摘要数字无法追踪时，从摘要删除。
- PDF generation fails 时，记录命令、错误和受影响 output。
- CUMCM formal template 不可用时，记录原因，并只把内部临时 LaTeX 草稿作为临时输出。
- 若发现 final layer 缺少必要结果，返回 Stage 7 或对应 `q*`，不要在论文中补造。

## Manual Mode Behavior

生成后列出：

```text
workspace/output/final/paper.md
workspace/output/final/paper.tex
workspace/output/final/paper.pdf       # if exists
workspace/output/final/source/
workspace/output/final/review_report.md    # if generation warnings exist
```

若 PDF 或 formal template 失败，列出 failure record path。

## AP Mode Behavior

继续到 Stage 9，但必须保留所有 generation warnings、内部临时 LaTeX 草稿使用原因、PDF failure 和 claim limitation。AP mode 不得绕过 traceability 写强结论。

## Active Runtime Helper

Stage 8 should prefer the active render bridge:

```bash
python scripts/render_workspace_paper.py <workspace>
```

For review-only Markdown and TeX generation:

```bash
python scripts/render_workspace_paper.py <workspace> --no-pdf
```

Formal template priority:

```text
templates/latex/cumcm/cumcmthesis/  highest priority
internal temporary LaTeX draft only when formal assets are unavailable
```

Before generation, Stage 8 must read:

```text
docs/cumcm_latex_template_interface.md
competitions/cumcm/paper_skeleton.md
competitions/cumcm/abstract_template.md
competitions/cumcm/winning_patterns.md
competitions/cumcm/phrase_bank.md
competitions/cumcm/anti_patterns.md
competitions/cumcm/distilled_structures.md
competitions/cumcm/distilled_formats.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
workspace/output/final/final_figures_index.md
workspace/output/final/final_tables_index.md
workspace/output/q*/q*_summary.md
```

If the render helper fails:

- inspect `workspace/output/final/latex_compile.log`;
- inspect `workspace/output/final/render_report.json`;
- do not claim `paper.pdf` was generated;
- record the failure in `review_report.md` and `quality_report.md`;
- keep `paper.md` and `paper.tex` as partial outputs when they exist.

Paper hard numbers may only come from:

```text
workspace/output/q*/results/result.json
workspace/output/q*/validation.md
workspace/output/q*/sensitivity.md
workspace/output/final/final_results.md
workspace/output/final/traceability.md
```
