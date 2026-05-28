# Anonymity Report 模板

## 文件用途

检查最终论文和源文件是否包含身份、单位、队伍、路径或元数据风险。

## 对应 stage

Stage 9 Final Review

## 必填字段

| 字段 | 填写规则 |
|---|---|
| checked artifact | 写被检查文件或目录 |
| risk type | 写个人、学校、团队、路径、元数据或其他 |
| location | 写行号、页码、字段或文件属性 |
| action | 写已处理、需人工处理或保留原因 |
| status | 写 `pass`、`partial`、`fail` |

## 来源字段

`workspace/output/final/paper.md`、`paper.tex`、`paper.pdf`、`source/`、图表文件和附件元数据。

## 可追溯要求

每个匿名风险必须指向文件路径、位置和处理动作。

## 禁止空泛表达

不要只写“未发现明显问题”。必须列出检查范围和结果。

## Checked Artifacts

| checked artifact | checked | status | note |
|---|---|---|---|
| `<path>` | `<yes/no>` | `<pass/partial/fail>` | `<note>` |

## Anonymity Risks

| risk type | file | location | action | status |
|---|---|---|---|---|
| `<personal/school/team/path/metadata/other>` | `<path>` | `<line/page/field>` | `<action>` | `<pass/partial/fail>` |
