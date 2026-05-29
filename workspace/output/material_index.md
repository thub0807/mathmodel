# Material Index

## 固定路径盘点

| material path | material type | 题面引用情况 | 实际状态 | used by q* | expected role | risk if missing | 使用限制 |
|---|---|---|---|---|---|---|---|
| `workspace/problem/problem.md` | 主题面 Markdown | 固定输入，显式必需 | 存在 | `q1`-`q6` | 题意主来源 | High | 不得用派生文件替代其题意来源 |
| `workspace/problem/reference.pdf` | 审计支持 PDF | 固定输入，非主来源 | 存在 | `q1`-`q6` | audit-only | Low | 仅在题意核对、材料补证或终审时读取 |
| `workspace/problem/images/` | 图片目录 | 题面未显式引用 | 存在但为空 | 暂无 | optional | Low | 当前不作为建模证据 |
| `workspace/problem/attachments/` | 附件目录 | 题面隐含引用数据集 | 存在 | `q1`-`q6` | 数据容器 | Medium | 需结合具体附件文件使用 |
| `workspace/problem/attachments/A_data.json` | 实验数据集 | 对应题面“公开的水系电解液实验数据集” | 存在 | `q1`-`q6` | input data | High | 后续所有定量结论均需可追溯到该文件及其派生结果 |
| `workspace/problem/attachments/README.txt` | 数据字段说明 | 未在题面单独点名 | 存在 | `q1`-`q6` | parameter source / schema note | Medium | 仅作字段解释，不替代数据本体 |

## 附件内容摘要

### `A_data.json`

- 记录数：251
- 顶层字段：`GUID`、`RUN_ID`、`RUN_TYPE`、`conductivity`、`pH`、`temperature`、`timestamp`、`electrolyte`、`electrochemistry`
- `RUN_TYPE` 当前均为 `production`
- `electrolyte.volumes` 涉及 8 种组分：`water`、`NaNO3`、`NaClO4`、`LiNO3`、`Li2SO4`、`Na2SO4`、`NaBr`、`LiClO4`
- `electrochemistry.derived_quantities` 当前已见字段：
  - `TAFEL CATHODE V`
  - `TAFEL ANODE V`
  - `1mA/cm^2 CATHODE V`
  - `1mA/cm^2 ANODE V`

### `images/`

- 当前为空目录。
- 题面未给出必须读取的图片路径，故暂记为 unused。

## 缺失与风险记录

- 当前未发现题面显式引用但缺失的图片或附件。
- 当前没有阻止 Stage 1 的材料缺口。
- 与“稳定性”相关的证据目前仅来自单次 `fast_assessment` 电化学测试，需在 `q1` 以后持续标记为 proxy 级证据。
