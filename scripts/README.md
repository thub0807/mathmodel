# scripts 工具说明

本目录中的脚本都是可选工具，不是 `mathmodel-copilot` 新主流程的必需步骤。

主流程以 `workspace/problem/problem.md` 为入口，以 `workspace/output/` 下的 Markdown / JSON 文件为审查对象。Agent 不应要求用户先运行脚本，才能阅读题目或进入建模流程。

## 可选运行时工具

### `render_paper.py`

用途：在需要时辅助把论文中间文件转换为 LaTeX / PDF。

注意：

- 新主流程的论文输出位置是 `workspace/output/final/`。
- 如脚本内部仍保留旧参数或旧路径兼容逻辑，本轮不把它作为主流程依赖。
- 若 PDF 生成失败，应把失败原因写入 `workspace/output/final/review_report.md` 与 `workspace/output/final/quality_report.md`。

### `extract_diff.py`

用途：可选地辅助生成局部修改提示或差异内容。

注意：

- 不要求用户运行。
- 不作为阶段推进条件。

### `score_artifact.py`

用途：旧流程评分工具，当前保留为历史工具和维护参考。

注意：

- 新主流程不调用它。
- 新主流程不要求它写入任何集中式状态文件。
- 新质量记录统一是 `workspace/output/final/quality_report.md`。

## 离线维护工具

### `ingest_papers.py`

用于维护期蒸馏论文统计材料，不在用户建模运行时调用。

### `download_cumcm_papers.py`

用于维护期下载公开论文材料，不在用户建模运行时调用。

## 编码要求

Python 文件如涉及文本读写，应显式使用：

```python
encoding="utf-8"
```

JSON 写入应使用：

```python
ensure_ascii=False
```

不要引入 GBK、ANSI 或 Latin-1 编码假设。
