# Active Runtime Scripts

当前 active workflow 没有必需 runtime scripts。

`mathmodel-copilot` 的主流程由以下文件和目录驱动：

```text
SKILL.md
references/
competitions/cumcm/
templates/workspace/
templates/latex/cumcm/
```

Agent 直接读取：

```text
workspace/problem/problem.md
```

并把全部产物写入：

```text
workspace/output/
```

旧评分、旧 patch、旧渲染或历史维护脚本均不属于 active workflow。历史脚本已移动到 `legacy/scripts/`，离线资料维护脚本位于 `maintenance/`。

如未来新增 active helper，本 README 必须说明：

- helper 是否为可选；
- 关联 stage；
- 输入输出路径；
- 是否会影响 quality gate；
- UTF-8 文本读写和 JSON `ensure_ascii=False` 要求。
