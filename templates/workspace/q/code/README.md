# Code Directory 模板

## 文件用途

说明 `workspace/output/q*/code/` 中代码文件的职责、输入、输出和运行方式。

## 对应 stage

Stage 3 Per-Question Build

## 必填字段

| 字段 | 填写规则 |
|---|---|
| 代码文件 | 列出每个脚本或 notebook 的相对路径 |
| 运行入口 | 指明主入口文件和命令 |
| 输入文件 | 指向 `workspace/problem/` 或前序 `workspace/output/` 文件 |
| 输出文件 | 指向 `workspace/output/q*/results/`、`figures/` 或 `tables/` |
| 依赖 | 说明语言、包、版本或环境约束 |

## 来源字段

`model.md`、`data_recon.md`、输入数据、前序结果。

## 可追溯要求

每个输出必须能回到具体代码文件、输入文件和 `run.log` 记录。

## 禁止空泛表达

不要只写“运行代码”。必须说明入口、输入、输出和依赖。

## 模板正文

| 代码文件 | 作用 | 运行入口 | 输入 | 输出 | 依赖 |
|---|---|---|---|---|---|
| `<path>` | `<purpose>` | `<command or entry>` | `<input paths>` | `<output paths>` | `<dependencies>` |
