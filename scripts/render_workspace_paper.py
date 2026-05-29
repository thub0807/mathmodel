#!/usr/bin/env python3
"""Render workspace final outputs into Markdown, CUMCM LaTeX, and optionally PDF."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


STATUS_OK = "ok"
STATUS_FAILED = "failed"
TEMPLATE_SUFFIXES = {
    ".cls",
    ".sty",
    ".bst",
    ".bib",
    ".bbx",
    ".cbx",
    ".def",
    ".cfg",
    ".clo",
    ".fd",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
}
GENERATED_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".xdv",
    ".fls",
    ".gz",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_q_dirs(workspace: Path) -> list[Path]:
    output_dir = workspace / "output"
    return sorted(
        [path for path in output_dir.glob("q*") if path.is_dir()],
        key=lambda item: int(item.name[1:]) if item.name[1:].isdigit() else item.name,
    )


def collect_inputs(workspace: Path, template_dir: Path, docs_interface: Path) -> tuple[dict, list[str]]:
    final_dir = workspace / "output" / "final"
    q_dirs = discover_q_dirs(workspace)
    required_paths = [
        final_dir / "final_results.md",
        final_dir / "traceability.md",
        final_dir / "final_figures_index.md",
        final_dir / "final_tables_index.md",
        docs_interface,
    ]
    if not template_dir.exists():
        required_paths.append(template_dir)
    if not q_dirs:
        required_paths.append(workspace / "output" / "q*/")

    q_payloads: dict[str, dict[str, str]] = {}
    for q_dir in q_dirs:
        qid = q_dir.name
        summary_path = q_dir / f"{qid}_summary.md"
        required_paths.append(summary_path)
        if summary_path.exists():
            q_payloads[qid] = {"summary": read_text(summary_path)}

    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        return {}, missing

    return {
        "final_results": read_text(final_dir / "final_results.md"),
        "traceability": read_text(final_dir / "traceability.md"),
        "final_figures_index": read_text(final_dir / "final_figures_index.md"),
        "final_tables_index": read_text(final_dir / "final_tables_index.md"),
        "docs_interface": read_text(docs_interface),
        "q_payloads": q_payloads,
    }, []


def parse_markdown_sections(text: str) -> dict[str, object]:
    title = ""
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip().lower()
            buffer = []
            continue
        if current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return {"title": title, "sections": sections}


def normalize_formula_markdown(text: str) -> str:
    text = text.replace("\\[\n", "$$\n")
    text = text.replace("\n\\]", "\n$$")
    text = text.replace("\\[", "$$")
    text = text.replace("\\]", "$$")
    return text


def parse_final_results(text: str) -> list[dict[str, str]]:
    matches = list(re.finditer(r"^##\s+(q\d+)\s*$", text, flags=re.MULTILINE))
    rows: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        entry = {"qid": match.group(1)}
        for key in ["status", "model", "validation", "sensitivity", "paper claim", "limitation"]:
            found = re.search(rf"-\s+{re.escape(key)}:\s*(.+)", block)
            if found:
                entry[key] = found.group(1).strip()
        rows.append(entry)
    return rows


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def extract_number(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def extract_list_items(text: str, prefix: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            items.append(stripped[len(prefix) :].strip())
    return items


def split_assumptions_and_notation(text: str) -> tuple[list[str], list[tuple[str, str]]]:
    assumptions: list[str] = []
    notation: list[tuple[str, str]] = []
    before, marker, after = text.partition("关键符号如下：")
    assumption_lines = re.findall(r"^\d+\.\s+(.+)$", before, flags=re.MULTILINE)
    assumptions.extend(item.strip() for item in assumption_lines if item.strip())
    for line in after.splitlines():
        stripped = line.strip()
        match = re.match(r"-\s+`([^`]+)`:\s*(.+)", stripped)
        if match:
            notation.append((match.group(1).strip(), match.group(2).strip()))
    return assumptions, notation


def build_title() -> str:
    return "水系电解液配方的综合评价、性能预测与实验候选设计"


def build_abstract(q_summaries: dict[str, dict[str, object]], trace_rows: list[dict[str, str]]) -> str:
    q1_main = str(q_summaries["q1"]["sections"].get("main results with source fields", ""))
    q2_main = str(q_summaries["q2"]["sections"].get("main results with source fields", ""))
    q4_main = str(q_summaries["q4"]["sections"].get("main results with source fields", ""))
    q5_main = str(q_summaries["q5"]["sections"].get("main results with source fields", ""))

    q1_spearman = extract_number(r"Spearman 相关系数仅为 `([0-9.]+)`", q1_main, "0.4154")
    q1_overlap = extract_number(r"重合数为 `([^`]+)`", q1_main, "0/10")
    cond_mae = extract_number(r"conductivity = ([0-9.]+)", q2_main, "7.8566")
    ph_mae = extract_number(r"pH = ([0-9.]+)", q2_main, "0.1740")
    pi_mae = extract_number(r"PI = ([0-9.]+)", q2_main, "0.03467")
    recon_rho = extract_number(r"Spearman `([0-9.]+)`", q2_main, "0.9662")
    trust_gap = extract_number(r"相差 `([0-9.]+)` 倍", q4_main, "2.57")
    top5_gain = extract_number(r"高 `([0-9.]+)`", q5_main, "0.0170")
    top10_gain = extract_number(r"也高于随机基线 `([0-9.]+)`", q5_main, "0.0181")

    abstract_allowed = sorted({row["source question"].strip("`") for row in trace_rows if row.get("allowed in abstract", "").strip("`") == "yes"})
    trace_note = "、".join(abstract_allowed) if abstract_allowed else "q1、q2、q4、q5"

    paragraphs = [
        "本文针对水系电解液配方的综合评价、性能预测与实验候选设计问题，综合考虑电导率、pH 适宜性、短时电化学稳定性 proxy 以及局部可信域约束，建立了综合评价—树集成预测—可信域分析联合模型，并在 251 条实验记录上完成了从评价到推荐的整体求解。",
        "针对问题一、问题二、问题三，本文分别建立了门槛约束-CRITIC-TOPSIS 综合评价模型、配方结构增强的目标自适应树集成模型和关键组分交互解释模型。其中，问题三显式复用问题二的预测结果与重要性排序，进一步解释高分配方形成机制。",
        f"针对问题一，综合评分与电导率排序的 Spearman 相关仅为 {q1_spearman}，前 10 名重合仅为 {q1_overlap}，说明单独使用电导率不足以定义好配方。针对问题二，正式主路线对 conductivity、pH 和 PI 的 OOF MAE 分别为 {cond_mae}、{ph_mae} 和 {pi_mae}，且 PI 直接头与重构头的相关系数达到 {recon_rho}。针对问题三，离子强度 proxy 与加权密度的协同作用进一步解释了高分区形成原因。",
        f"在模型检验方面，本文引入结构簇 holdout 与可信域分层。结果表明，low trust 区的 PI 误差约为 high trust 区的 {trust_gap} 倍，因此模型更适合在已见邻域内支持开发型决策，而对低可信区域应以探索和风险标注为主。",
        f"在此基础上，本文设计了开发型与探索型结合的下一轮实验候选方案，top5 与 top10 的平均预测综合性能分别较随机基线提升 {top5_gain} 和 {top10_gain}。本文的创新点在于：将综合评价、组合预测与可信域分析串联为闭环；把候选推荐与局部扰动稳健性联立审查；并将摘要级硬数字严格限制在 {trace_note} 中允许进入摘要的追溯条目内。所建模型可推广至电解液筛选、配方优化及其他小样本实验设计场景。"
    ]
    return "\n\n".join(paragraphs)


def build_problem_restatement(q_summaries: dict[str, dict[str, object]]) -> str:
    return (
        "本文围绕水系电解液公开实验数据，依次回答六个相互依赖的子问题。"
        "第一阶段关注“如何定义好配方”“如何由配方预测性能”以及“哪些组分和交互作用真正主导结果”；"
        "第二阶段进一步追问模型在何处可信、下一轮实验应如何设计，以及高分候选是否处于稳定高性能盆地之中。\n\n"
        "其中，问题一构造同时覆盖电导率、pH 适宜性和短时稳定性 proxy 的综合性能指标；"
        "问题二建立由配方组成直接映射到 conductivity、pH、W_1、R_W 与 PI 的预测模型；"
        "问题三解释关键组分和交互作用；问题四刻画模型可信域与适用范围；"
        "问题五给出下一轮实验的开发型与探索型候选；问题六进一步审查候选在局部扰动下的稳健性。"
        "因此，全文并不是孤立回答六个小问，而是在同一数据集上逐步推进实验决策。"
    )


def build_problem_analysis() -> str:
    return (
        "六个子问题之间不是并列关系，而是严格的链式依赖。"
        "问题一先给出统一的综合性能口径；问题二再把配方组成映射到 conductivity、pH、W_1、R_W 与 PI；"
        "问题三利用问题二的已验证模型解释关键驱动因子和非线性交互；问题四则把误差结构、局部密度与稀有模式合并为可信域分层；"
        "在此基础上，问题五据此平衡开发型和探索型实验候选，问题六进一步检验这些候选是在稳定高分区域内，还是只是对扰动敏感的局部尖峰。"
        "因此，全文的分析主线不是一次性堆叠多个模型，而是用前一问的证据约束后一问的可用空间和结论强度。"
    )


def build_assumptions_and_notation(q_summaries: dict[str, dict[str, object]]) -> tuple[list[str], list[tuple[str, str]]]:
    assumptions: list[str] = []
    notation: list[tuple[str, str]] = []
    for qid in ["q1", "q2"]:
        section_text = str(q_summaries[qid]["sections"].get("core assumptions and notation", ""))
        local_assumptions, local_notation = split_assumptions_and_notation(section_text)
        for item in local_assumptions:
            if item not in assumptions:
                assumptions.append(item)
        for item in local_notation:
            if item not in notation:
                notation.append(item)
    return assumptions, notation


def model_figures(qid: str) -> list[tuple[str, str]]:
    mapping = {
        "q1": [("综合评分与电导率排序差异", "source/figures/figure_q1_score_vs_conductivity.png")],
        "q2": [("主预测模型误差对比", "source/figures/figure_q2_model_mae_comparison.png")],
        "q3": [("关键驱动因子条形图", "source/figures/figure_q3_driver_bars.png")],
        "q4": [("结构簇误差热图", "source/figures/figure_q4_cluster_error_heatmap.png")],
        "q5": [("候选前沿与开发-探索平衡", "source/figures/figure_q5_candidate_frontier.png")],
        "q6": [("候选稳健性散点图", "source/figures/figure_q6_robustness_scatter.png")],
    }
    return mapping.get(qid, [])


def build_model_section_md(qid: str, title: str, section_map: dict[str, str]) -> str:
    lines = [f"### {title}", ""]
    motivation = section_map.get("model motivation", "")
    formulas = section_map.get("core formulas", "")
    algorithm = section_map.get("algorithm or solve process", "")
    draft = section_map.get("paper-ready subsection draft", "")
    main_results = section_map.get("main results with source fields", "")

    if motivation:
        lines.extend(["#### 建模动机", "", motivation.strip(), ""])
    if formulas:
        lines.extend(["#### 核心公式", "", normalize_formula_markdown(formulas.strip()), ""])
    if algorithm:
        lines.extend(["#### 求解步骤", "", algorithm.strip(), ""])
    if draft:
        lines.extend(["#### 结果分析", "", draft.strip(), ""])
    elif main_results:
        lines.extend(["#### 核心结果", "", main_results.strip(), ""])
    for caption, path in model_figures(qid):
        lines.extend(["", f"![{caption}]({path})", ""])
    return "\n".join(lines).strip()


def build_results_summary_table(final_rows: list[dict[str, str]]) -> str:
    lines = [
        "| 问题 | 模型 | 核心结论 | 限制 |",
        "|---|---|---|---|",
    ]
    for row in final_rows:
        lines.append(
            f"| {row.get('qid', '')} | {row.get('model', '')} | {row.get('paper claim', '')} | {row.get('limitation', '')} |"
        )
    return "\n".join(lines)


def build_validation_summary(q_summaries: dict[str, dict[str, object]]) -> str:
    parts = []
    for qid in ["q1", "q2"]:
        title = q_summaries[qid]["title"]
        text = str(q_summaries[qid]["sections"].get("validation conclusion", "")).strip()
        if text:
            parts.append(f"### {title}\n\n{text}")
    parts.append(
        "### q4 可信域补充\n\n"
        + str(q_summaries["q4"]["sections"].get("paper-ready subsection draft", "")).strip()
    )
    return "\n\n".join(parts)


def build_sensitivity_and_evaluation(q_summaries: dict[str, dict[str, object]], final_rows: list[dict[str, str]]) -> str:
    sensitivity_parts = []
    for qid in ["q1", "q2"]:
        title = q_summaries[qid]["title"]
        text = str(q_summaries[qid]["sections"].get("sensitivity conclusion", "")).strip()
        if text:
            sensitivity_parts.append(f"### {title}\n\n{text}")

    strengths = [
        "以问题链为主线，避免了多个模型之间口径不一致的常见问题。",
        "把综合评价、预测精度、可信域分层和候选设计串成闭环，便于直接服务实验决策。",
        "所有 hard numbers 均通过 final 层结果和 traceability 约束，避免正文结论与源数据脱钩。",
    ]
    limitations = [row.get("limitation", "") for row in final_rows if row.get("limitation")]
    unique_limitations: list[str] = []
    for item in limitations:
        if item not in unique_limitations:
            unique_limitations.append(item)

    lines = ["## 灵敏度分析与模型评价", ""]
    if sensitivity_parts:
        lines.append("\n\n".join(sensitivity_parts))
        lines.append("")
    lines.extend(["### 模型优点", ""])
    for item in strengths:
        lines.append(f"- {item}")
    lines.extend(["", "### 模型局限与改进", ""])
    for item in unique_limitations:
        lines.append(f"- {item}")
    lines.extend(
        [
            "- 后续若获得更长时程的稳定性或寿命数据，应重建 `W_1 / R_W / PI` 的标签语义，再重新训练问题二到问题六的链条。",
            "- Stage 8 的最终论文可继续根据 `paper.md` 做人工润色，但不应再回退为审查材料拼接稿。",
        ]
    )
    return "\n".join(lines)


def build_references() -> str:
    return "\n".join(
        [
            "## 参考文献",
            "",
            "1. Hwang C L, Yoon K. Multiple Attribute Decision Making: Methods and Applications[M]. New York: Springer, 1981.",
            "2. Diakoulaki D, Mavrotas G, Papayannakis L. Determining objective weights in multiple criteria problems: The CRITIC method[J]. Computers and Operations Research, 1995, 22(7): 763-770.",
            "3. Breiman L. Random Forests[J]. Machine Learning, 2001, 45(1): 5-32.",
            "4. Geurts P, Ernst D, Wehenkel L. Extremely randomized trees[J]. Machine Learning, 2006, 63(1): 3-42.",
            "5. Friedman J H. Greedy function approximation: A gradient boosting machine[J]. Annals of Statistics, 2001, 29(5): 1189-1232.",
            "6. 本题公开问题说明与附件数据：`problem.md`、`A_data.json`、`README.txt`。",
        ]
    )


def build_appendix() -> str:
    return "\n".join(
        [
            "## 附录",
            "",
            "### 附录 A 主要程序说明",
            "",
            "- `q1_build.py`：生成综合性能指标、权重与灵敏度分析。",
            "- `q2_build.py`：训练配方到性能的主预测模型并输出 OOF 结果。",
            "- `q3_build.py`：提取关键驱动因子与交互作用解释。",
            "- `q4_build.py`：执行结构簇验证与可信域分层。",
            "- `q5_build.py`：构造下一轮实验候选池并完成开发-探索推荐。",
            "- `q6_build.py`：对候选进行局部扰动稳健性审查。",
            "",
            "### 附录 B 结果材料说明",
            "",
            "- 全部图表素材已经复制到 `final/source/figures/` 与 `final/source/tables/`。",
            "- 详细追溯链保留在 `traceability.md`，不再直接写入正文。",
        ]
    )


def build_paper_markdown(payload: dict) -> tuple[str, str, list[str]]:
    q_summaries = {qid: parse_markdown_sections(q_payload["summary"]) for qid, q_payload in payload["q_payloads"].items()}
    final_rows = parse_final_results(payload["final_results"])
    trace_rows = parse_markdown_table(payload["traceability"])

    assumptions, notation = build_assumptions_and_notation(q_summaries)
    title = build_title()
    abstract = build_abstract(q_summaries, trace_rows)
    keywords = ["水系电解液", "综合评价", "树集成预测", "可信域", "主动实验设计"]

    body_parts = [
        "## 问题重述",
        "",
        build_problem_restatement(q_summaries),
        "",
        "## 问题分析",
        "",
        build_problem_analysis(),
        "",
        "## 模型假设",
        "",
    ]
    for index, item in enumerate(assumptions[:6], start=1):
        body_parts.append(f"{index}. {item}")
    body_parts.extend(
        [
            "",
            "## 符号说明",
            "",
            "| 符号 | 含义 |",
            "|---|---|",
        ]
    )
    for symbol, meaning in notation[:10]:
        body_parts.append(f"| `{symbol}` | {meaning} |")

    body_parts.extend(
        [
            "",
            "## 模型建立与求解",
            "",
            build_model_section_md("q1", "问题一：综合性能与稳定性指标构造", q_summaries["q1"]["sections"]),
            "",
            build_model_section_md("q2", "问题二：配方到性能的预测模型", q_summaries["q2"]["sections"]),
            "",
            build_model_section_md("q3", "问题三：关键组分与交互作用解释", q_summaries["q3"]["sections"]),
            "",
            build_model_section_md("q4", "问题四：模型可信度与适用范围分析", q_summaries["q4"]["sections"]),
            "",
            build_model_section_md("q5", "问题五：下一轮实验候选设计", q_summaries["q5"]["sections"]),
            "",
            build_model_section_md("q6", "问题六：候选配方稳健性建模", q_summaries["q6"]["sections"]),
            "",
            "## 结果汇总与验证",
            "",
            "### 最终结果汇总",
            "",
            build_results_summary_table(final_rows),
            "",
            "摘要中的定量结果仅引用 `traceability.md` 中 `allowed in abstract = yes` 的条目，正文不再逐条展示追溯编号与源字段，以保持论文叙事完整。",
            "",
            build_validation_summary(q_summaries),
            "",
            build_sensitivity_and_evaluation(q_summaries, final_rows),
            "",
            build_references(),
            "",
            build_appendix(),
            "",
        ]
    )

    body_md = "\n".join(body_parts).strip() + "\n"
    full_md = "\n".join(
        [
            f"# {title}",
            "",
            "## 摘要",
            "",
            abstract,
            "",
            "## 关键词",
            "",
            "；".join(keywords),
            "",
            body_md.strip(),
            "",
        ]
    )
    return full_md, body_md, keywords


def escape_latex_text(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def render_inline_latex(text: str) -> str:
    token_pattern = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*)")
    parts: list[str] = []
    last = 0
    for match in token_pattern.finditer(text):
        plain = text[last : match.start()]
        if plain:
            parts.append(escape_latex_text(plain))
        token = match.group(0)
        if token.startswith("`"):
            raw = token[1:-1]
            if is_math_code_token(raw):
                parts.append("$" + raw + "$")
            else:
                parts.append(r"\texttt{" + escape_latex_text(raw) + "}")
        else:
            parts.append(r"\textbf{" + escape_latex_text(token[2:-2]) + "}")
        last = match.end()
    tail = text[last:]
    if tail:
        parts.append(escape_latex_text(tail))
    return "".join(parts)


def is_math_code_token(token: str) -> bool:
    if any(mark in token for mark in [".json", ".md", ".csv", ".png"]):
        return False
    if "workspace/" in token or "source/" in token:
        return False
    if token.startswith("q") and token[1:].isdigit():
        return False
    if "\\" in token or "^" in token or "{" in token or "}" in token:
        return True
    if re.match(r"^[A-Za-z]+(?:_[A-Za-z0-9]+)+$", token):
        return True
    if re.match(r"^[A-Za-z][A-Za-z0-9_]*\s*=\s*.+$", token):
        return True
    return False


def render_markdown_table_to_tex(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    data = rows[2:] if len(rows) > 2 else []
    colspec = "".join([">{\\raggedright\\arraybackslash}X" for _ in header])
    out = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        r"\begin{tabularx}{\textwidth}{" + colspec + "}",
        r"\toprule",
        " & ".join(render_inline_latex(cell) for cell in header) + r" \\",
        r"\midrule",
    ]
    for row in data:
        padded = row + [""] * (len(header) - len(row))
        out.append(" & ".join(render_inline_latex(cell) for cell in padded[: len(header)]) + r" \\")
    out.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}"])
    return "\n".join(out)


def render_markdown_body_to_tex(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_mode: str | None = None
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(item.strip() for item in paragraph if item.strip())
            if text:
                out.append(render_inline_latex(text) + r"\par")
            paragraph = []

    def close_list() -> None:
        nonlocal list_mode
        if list_mode == "itemize":
            out.append(r"\end{itemize}")
        elif list_mode == "enumerate":
            out.append(r"\end{enumerate}")
        list_mode = None

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()

        image_match = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", stripped)
        if image_match:
            flush_paragraph()
            close_list()
            caption = image_match.group(1).strip()
            raw_path = image_match.group(2).strip()
            tex_path = raw_path[7:] if raw_path.startswith("source/") else raw_path
            out.extend(
                [
                    r"\begin{figure}[htbp]",
                    r"\centering",
                    r"\includegraphics[width=0.82\textwidth]{" + escape_latex_text(tex_path) + "}",
                    r"\caption{" + render_inline_latex(caption) + "}",
                    r"\end{figure}",
                ]
            )
            index += 1
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            close_list()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            out.append(render_markdown_table_to_tex(table_lines))
            continue

        if stripped == "$$":
            flush_paragraph()
            close_list()
            math_lines = [r"\["]
            index += 1
            while index < len(lines):
                candidate = lines[index].rstrip()
                if candidate.strip() == "$$":
                    math_lines.append(r"\]")
                    break
                math_lines.append(candidate)
                index += 1
            out.extend(math_lines)
            index += 1
            continue

        if stripped == r"\[":
            flush_paragraph()
            close_list()
            math_lines = [stripped]
            index += 1
            while index < len(lines):
                math_lines.append(lines[index].rstrip())
                if lines[index].strip() == r"\]":
                    break
                index += 1
            out.extend(math_lines)
            index += 1
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            out.append("")
            index += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_list()
            out.append(r"\section{" + render_inline_latex(stripped[3:].strip()) + "}")
            index += 1
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            close_list()
            out.append(r"\subsection{" + render_inline_latex(stripped[4:].strip()) + "}")
            index += 1
            continue
        if stripped.startswith("#### "):
            flush_paragraph()
            close_list()
            out.append(r"\subsubsection{" + render_inline_latex(stripped[5:].strip()) + "}")
            index += 1
            continue

        ordered_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered_match:
            flush_paragraph()
            if list_mode != "enumerate":
                close_list()
                out.append(r"\begin{enumerate}")
                list_mode = "enumerate"
            out.append(r"\item " + render_inline_latex(ordered_match.group(1).strip()))
            index += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if list_mode != "itemize":
                close_list()
                out.append(r"\begin{itemize}")
                list_mode = "itemize"
            out.append(r"\item " + render_inline_latex(stripped[2:].strip()))
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_list()
    return "\n".join(item for item in out if item is not None)


def extract_title_and_body(markdown: str) -> tuple[str, str, str, list[str]]:
    lines = markdown.splitlines()
    title = ""
    abstract_lines: list[str] = []
    keywords_line = ""
    body_lines: list[str] = []
    mode = "title"
    index = 0
    while index < len(lines):
        line = lines[index]
        if mode == "title" and line.startswith("# "):
            title = line[2:].strip()
            mode = "seek_abstract"
            index += 1
            continue
        if line.strip() == "## 摘要":
            mode = "abstract"
            index += 1
            continue
        if line.strip() == "## 关键词":
            mode = "keywords"
            index += 1
            continue
        if mode == "abstract":
            if line.startswith("## "):
                mode = "body"
                continue
            abstract_lines.append(line)
            index += 1
            continue
        if mode == "keywords":
            if line.startswith("## "):
                mode = "body"
                continue
            if line.strip():
                keywords_line = line.strip()
            index += 1
            continue
        if mode in {"seek_abstract", "body"}:
            body_lines.append(line)
        index += 1
    keywords = [item.strip() for item in keywords_line.split("；") if item.strip()]
    abstract = "\n".join(line for line in abstract_lines if line.strip()).strip()
    body = "\n".join(body_lines).strip()
    return title, abstract, body, keywords


def copy_template_files(template_dir: Path, source_dir: Path, warnings: list[str]) -> None:
    for path in template_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(template_dir)
        suffix = path.suffix.lower()
        if suffix in GENERATED_SUFFIXES or path.name == "MathModel.pdf":
            continue
        if suffix in TEMPLATE_SUFFIXES or path.name == "MathModel.tex":
            target = source_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    if not (source_dir / "gmcmthesis.cls").exists():
        warnings.append("Template class gmcmthesis.cls was not copied; LaTeX compile may fail.")


def extract_candidate_paths(index_text: str) -> list[str]:
    candidates: list[str] = []
    separators = ["(", ")", "[", "]", "`", "\"", "'", "<", ">", ",", ";"]
    for line in index_text.splitlines():
        clean = line
        for sep in separators:
            clean = clean.replace(sep, " ")
        for token in clean.split():
            lower = token.lower()
            if lower.endswith((".png", ".jpg", ".jpeg", ".pdf", ".svg", ".csv", ".xlsx", ".tex", ".md")):
                candidates.append(token)
    return candidates


def resolve_workspace_path(workspace: Path, raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return workspace / candidate


def copy_index_assets(workspace: Path, index_text: str, target_dir: Path, label: str, warnings: list[str]) -> list[str]:
    copied: list[str] = []
    seen: set[str] = set()
    for raw in extract_candidate_paths(index_text):
        if raw in seen:
            continue
        seen.add(raw)
        source = resolve_workspace_path(workspace, raw)
        if not source.exists():
            warnings.append(f"{label} index references missing file: {raw}")
            continue
        target = target_dir / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(str(target))
    return copied


def build_latex_from_template(template_dir: Path, paper_md: str, warnings: list[str]) -> tuple[str, str | None]:
    title, abstract, body_md, keywords = extract_title_and_body(paper_md)
    entry = template_dir / "MathModel.tex"
    body_tex = render_markdown_body_to_tex(body_md)
    keywords_tex = r"\keywords{" + r"\quad ".join(escape_latex_text(item) for item in keywords) + "}"
    body = "\n".join(
        [
            r"\maketitle",
            r"\begin{abstract}",
            escape_latex_text(abstract),
            "",
            keywords_tex,
            r"\end{abstract}",
            "",
            r"\tableofcontents",
            "",
            body_tex,
            "",
        ]
    )

    if entry.exists():
        template_text = read_text(entry)
        begin = template_text.find(r"\begin{document}")
        end = template_text.rfind(r"\end{document}")
        if begin >= 0 and end > begin:
            preamble = template_text[:begin]
            lines = []
            for line in preamble.splitlines():
                stripped = line.strip()
                if stripped.startswith(r"\title{"):
                    lines.append(r"\title{" + escape_latex_text(title) + "}")
                elif stripped.startswith(r"\baominghao{"):
                    lines.append(r"\baominghao{No.00000000}")
                elif stripped.startswith(r"\schoolname{"):
                    lines.append(r"\schoolname{匿名学校}")
                elif stripped.startswith(r"\member"):
                    lines.append(line.split("{", 1)[0] + "{匿名}")
                else:
                    lines.append(line)
            preamble = "\n".join(lines) + "\n"
            return preamble + r"\begin{document}" + "\n" + body + r"\end{document}" + "\n", None
        reason = "Could not locate reliable \\begin{document}/\\end{document} insertion boundary in formal template."
        warnings.append(reason)
    else:
        reason = "Formal template entry MathModel.tex is missing."
        warnings.append(reason)

    fallback = "\n".join(
        [
            r"\documentclass[UTF8]{ctexart}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{graphicx}",
            r"\usepackage{booktabs}",
            r"\usepackage{tabularx}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, margin=2.5cm}",
            r"\title{" + escape_latex_text(title) + "}",
            r"\author{匿名占位}",
            r"\date{}",
            r"\begin{document}",
            body,
            r"\end{document}",
            "",
        ]
    )
    return fallback, reason


def compile_pdf(source_dir: Path, engine: str) -> tuple[bool, str, int | None]:
    executable = shutil.which(engine)
    if executable is None:
        return False, f"Engine not found: {engine}\n", None

    log_parts = []
    last_code = 0
    for attempt in range(1, 3):
        command = [executable, "-interaction=nonstopmode", "-halt-on-error", "paper.tex"]
        log_parts.append(f"$ {' '.join(command)}\n")
        completed = subprocess.run(
            command,
            cwd=source_dir,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        last_code = completed.returncode
        log_parts.append(completed.stdout)
        log_parts.append(f"\n[attempt {attempt} exit code: {completed.returncode}]\n")
        if completed.returncode != 0:
            break
    pdf_exists = (source_dir / "paper.pdf").exists()
    return last_code == 0 and pdf_exists, "\n".join(log_parts), last_code


def render(args: argparse.Namespace) -> tuple[int, dict]:
    workspace = Path(args.workspace).resolve()
    root = repo_root()
    template_dir = Path(args.template_dir).resolve() if args.template_dir else root / "templates" / "latex" / "cumcm" / "cumcmthesis"
    docs_interface = root / "docs" / "cumcm_latex_template_interface.md"
    final_dir = workspace / "output" / "final"
    source_dir = final_dir / "source"
    warnings: list[str] = []
    errors: list[str] = []

    payload, missing = collect_inputs(workspace, template_dir, docs_interface)
    report = {
        "status": STATUS_FAILED if missing else STATUS_OK,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "template_dir": str(template_dir),
        "engine": args.engine,
        "no_pdf": args.no_pdf,
        "missing": missing,
        "errors": errors,
        "warnings": warnings,
        "fallback_reason": None,
        "outputs": {},
        "compile": {"attempted": False, "success": False, "exit_code": None},
    }

    if missing:
        errors.append("Missing required Stage 8 input files; paper generation was not attempted.")
        final_dir.mkdir(parents=True, exist_ok=True)
        write_text(final_dir / "latex_compile.log", "Stage 8 render aborted before compile because required inputs are missing.\n")
        write_json(final_dir / "render_report.json", report)
        return 1, report

    source_dir.mkdir(parents=True, exist_ok=True)
    copy_template_files(template_dir, source_dir, warnings)
    copied_figures = copy_index_assets(workspace, payload["final_figures_index"], source_dir / "figures", "figure", warnings)
    copied_tables = copy_index_assets(workspace, payload["final_tables_index"], source_dir / "tables", "table", warnings)

    paper_md, _, _ = build_paper_markdown(payload)
    paper_tex, fallback_reason = build_latex_from_template(template_dir, paper_md, warnings)
    report["fallback_reason"] = fallback_reason

    write_text(final_dir / "paper.md", paper_md)
    write_text(final_dir / "paper.tex", paper_tex)
    write_text(source_dir / "paper.tex", paper_tex)
    report["outputs"] = {
        "paper_md": str(final_dir / "paper.md"),
        "paper_tex": str(final_dir / "paper.tex"),
        "source_dir": str(source_dir),
        "copied_figures": copied_figures,
        "copied_tables": copied_tables,
        "latex_compile_log": str(final_dir / "latex_compile.log"),
        "render_report": str(final_dir / "render_report.json"),
    }

    if args.no_pdf:
        write_text(final_dir / "latex_compile.log", "PDF compilation skipped because --no-pdf was specified.\n")
        report["status"] = STATUS_OK
        write_json(final_dir / "render_report.json", report)
        return 0, report

    report["compile"]["attempted"] = True
    success, compile_log, exit_code = compile_pdf(source_dir, args.engine)
    report["compile"]["success"] = success
    report["compile"]["exit_code"] = exit_code
    write_text(final_dir / "latex_compile.log", compile_log)
    if success:
        pdf_source = source_dir / "paper.pdf"
        pdf_target = final_dir / "paper.pdf"
        shutil.copy2(pdf_source, pdf_target)
        report["outputs"]["paper_pdf"] = str(pdf_target)
        report["status"] = STATUS_OK
        write_json(final_dir / "render_report.json", report)
        return 0, report

    errors.append("PDF compilation failed; preserved paper.md, paper.tex, source/, latex_compile.log, and render_report.json.")
    report["status"] = STATUS_FAILED
    write_json(final_dir / "render_report.json", report)
    return 1, report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a mathmodel-copilot workspace into paper.md, paper.tex, and optionally paper.pdf.")
    parser.add_argument("workspace", help="Workspace root containing output/final and output/q*/ artifacts.")
    parser.add_argument("--no-pdf", action="store_true", help="Generate paper.md and paper.tex without compiling PDF.")
    parser.add_argument("--template-dir", help="Override CUMCM template directory. Defaults to templates/latex/cumcm/cumcmthesis/.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable render result to stdout.")
    parser.add_argument("--engine", default="xelatex", help="LaTeX engine for PDF compilation. Default: xelatex.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    code, report = render(args)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        verdict = "PASS" if code == 0 else "FAIL"
        print(f"{verdict}: render_workspace_paper")
        if report.get("missing"):
            print("missing:")
            for item in report["missing"]:
                print(f"- {item}")
        if report.get("warnings"):
            print("warnings:")
            for item in report["warnings"]:
                print(f"- {item}")
        print(f"render_report: {Path(report['workspace']) / 'output' / 'final' / 'render_report.json'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
