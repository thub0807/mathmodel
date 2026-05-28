# Problem Audit 模板

## 文件用途

记录固定输入材料是否满足 Stage 0 进入条件。

## 对应 stage

Stage 0 Workspace Audit

## 必填字段

| 字段 | 填写规则 |
|---|---|
| 必需文件检查 | 必须列出 `problem.md` 与 `reference.pdf` 是否存在 |
| 题意理解 | 用自己的话概括，不复制原文 |
| 材料疑点 | 记录单位、符号、图片、附件和表格疑点 |
| 缺失或路径错误 | 记录 `problem.md` 引用但不存在的材料 |
| reference.pdf 使用记录 | 记录是否读取、读取原因、范围和结论 |

## 来源字段

`workspace/problem/problem.md`、`workspace/problem/reference.pdf`、`workspace/problem/images/`、`workspace/problem/attachments/`

## 可追溯要求

所有材料疑点必须指向原始路径或 `problem.md` 中的引用位置。

## 禁止空泛表达

不要写“材料基本完整”。必须逐项列出状态。

## 模板正文

| 文件 | 状态 | 说明 |
|---|---|---|
| `workspace/problem/problem.md` | `<存在/缺失>` | `<说明>` |
| `workspace/problem/reference.pdf` | `<存在/缺失>` | `<说明>` |

### 题意理解

`<概括题意。>`

### 材料疑点

| 疑点 | 来源 | 影响 | 是否需要核对 PDF |
|---|---|---|---|
| `<疑点>` | `<来源>` | `<影响>` | `<是/否>` |

### 缺失或路径错误

| 引用路径 | 状态 | 影响 |
|---|---|---|
| `<路径>` | `<缺失/错误/待确认>` | `<影响>` |

### reference.pdf 使用记录

| 是否读取 | 读取原因 | 读取范围 | 结论 |
|---|---|---|---|
| `<是/否>` | `<原因>` | `<页码或章节>` | `<结论>` |
