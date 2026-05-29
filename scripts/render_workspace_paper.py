#!/usr/bin/env python3
"""Render workspace final outputs into Markdown, CUMCM LaTeX, and optionally PDF."""

from __future__ import annotations

import argparse
import json
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
    return sorted([p for p in output_dir.glob("q*") if p.is_dir()])


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

    for q_dir in q_dirs:
        qid = q_dir.name
        required_paths.extend(
            [
                q_dir / "review_packet.md",
                q_dir / f"{qid}_summary.md",
                q_dir / "results" / "result.json",
                q_dir / "validation.md",
                q_dir / "sensitivity.md",
            ]
        )

    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        return {}, missing

    q_payloads = []
    for q_dir in q_dirs:
        qid = q_dir.name
        result_path = q_dir / "results" / "result.json"
        try:
            result = json.loads(read_text(result_path))
        except json.JSONDecodeError as exc:
            missing.append(f"{result_path}: invalid JSON ({exc})")
            result = {}
        q_payloads.append(
            {
                "id": qid,
                "review_packet": read_text(q_dir / "review_packet.md"),
                "summary": read_text(q_dir / f"{qid}_summary.md"),
                "result": result,
                "validation": read_text(q_dir / "validation.md"),
                "sensitivity": read_text(q_dir / "sensitivity.md"),
            }
        )

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


def compact_section(text: str, max_lines: int = 80) -> str:
    lines = [line.rstrip() for line in text.strip().splitlines()]
    if len(lines) <= max_lines:
        return "\n".join(lines).strip()
    kept = lines[:max_lines]
    kept.append("")
    kept.append("（后续内容已省略；完整材料见对应源文件。）")
    return "\n".join(kept).strip()


def result_brief(result: dict) -> str:
    qid = result.get("question_id", "unknown")
    status = result.get("status", "unknown")
    model_name = result.get("model_name", "未记录模型名")
    metrics = result.get("metrics", {})
    warnings = result.get("warnings", [])
    lines = [
        f"- 问题：`{qid}`",
        f"- 模型：{model_name}",
        f"- 结果状态：`{status}`",
    ]
    if isinstance(metrics, dict) and metrics:
        preview = []
        for key, value in list(metrics.items())[:6]:
            if isinstance(value, (str, int, float, bool)):
                preview.append(f"{key}={value}")
            elif isinstance(value, (list, dict)):
                preview.append(f"{key}=见 result.json")
        if preview:
            lines.append(f"- 关键指标：{'; '.join(preview)}")
    if isinstance(warnings, list) and warnings:
        lines.append(f"- 限制：{'; '.join(str(item) for item in warnings[:3])}")
    return "\n".join(lines)


def build_paper_md(payload: dict) -> str:
    lines: list[str] = [
        "# 数学建模论文草稿",
        "",
        "## 摘要",
        "",
        "本文围绕题面要求建立递进式数学模型。摘要结论必须以 `traceability.md` 中允许进入摘要的 claim 为准；未通过追溯的结果不写入摘要。",
        "",
        "## 关键词",
        "",
        "数学建模；CUMCM；可追溯结果",
        "",
        "## 1 问题重述",
        "",
        "本文以 `workspace/problem/problem.md` 为主工作文本，围绕题面中的递进问题建立模型、求解并验证结果。",
        "",
        "## 2 问题分析",
        "",
        "各子问题按 `question_index.md` 中的依赖顺序处理；后续问题必须继承前序问题的结果、限制和验证状态。",
        "",
        "## 3 模型假设与符号说明",
        "",
        "本节假设和符号来自各问题的 `review_packet.md`、`q*_summary.md` 以及 Stage 7 统一符号整理。",
        "",
        "## 4 数据处理",
        "",
        "数据处理描述来自各问题审查包、运行日志、验证记录、灵敏度记录或最终追溯材料。",
        "",
        "## 5 模型建立与求解",
        "",
    ]

    for q in payload["q_payloads"]:
        lines.extend(
            [
                f"### {q['id']}",
                "",
                "#### 审查包摘要",
                "",
                compact_section(q.get("review_packet", ""), 45) or "本问题缺少 `review_packet.md`，需回到 Stage 2 补齐审查包。",
                "",
                "#### 论文小节草稿",
                "",
                compact_section(q["summary"], 120) or "本问题缺少论文小节草稿。",
                "",
                "#### 结果摘要",
                "",
                result_brief(q["result"]),
                "",
                "#### 验证",
                "",
                compact_section(q["validation"], 45) or "本问题缺少验证正文。",
                "",
                "#### 灵敏度",
                "",
                compact_section(q["sensitivity"], 45) or "本问题缺少灵敏度正文。",
                "",
            ]
        )

    lines.extend(
        [
            "## 6 结果分析与可追溯性",
            "",
            "### final_results.md",
            "",
            payload["final_results"].strip(),
            "",
            "### traceability.md",
            "",
            payload["traceability"].strip(),
            "",
            "## 7 图表索引",
            "",
            "### final_figures_index.md",
            "",
            payload["final_figures_index"].strip(),
            "",
            "### final_tables_index.md",
            "",
            payload["final_tables_index"].strip(),
            "",
            "## 8 模型评价与改进",
            "",
            "优点、局限与改进方向应具体对应模型结构、数据条件、验证结果和灵敏度边界。",
            "",
            "## 参考文献",
            "",
            "（参考文献和资料来源由 Agent 根据实际使用材料补全；不得伪造文献。）",
            "",
            "## 附录",
            "",
            "代码、数据和 source 说明见 `workspace/output/final/source/` 与各 `q*/code/`。",
            "",
        ]
    )
    return "\n".join(lines)


def scan_paper_md_quality(paper_md: str) -> list[str]:
    warnings: list[str] = []
    forbidden_markers = [
        "论文标题占位",
        "待 Agent 补全",
        "AP 测试产物",
        "快速测试",
        "仅用于端到端测试",
        "```json",
    ]
    for marker in forbidden_markers:
        if marker in paper_md:
            warnings.append(f"paper.md contains non-paper marker: {marker}")
    return warnings


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


def escape_latex_preserving_math(line: str) -> str:
    if line.strip().startswith("$$") or line.strip().endswith("$$"):
        return line
    parts = line.split("$")
    if len(parts) == 1:
        return escape_latex_text(line)
    escaped: list[str] = []
    for index, part in enumerate(parts):
        escaped.append(escape_latex_text(part) if index % 2 == 0 else "$" + part + "$")
    return "".join(escaped)


def markdown_to_latex(markdown: str) -> str:
    latex: list[str] = []
    in_code = False
    in_itemize = False
    in_display_math = False

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_itemize:
                latex.append(r"\end{itemize}")
                in_itemize = False
            latex.append(r"\end{verbatim}" if in_code else r"\begin{verbatim}")
            in_code = not in_code
            continue

        if in_code:
            latex.append(line)
            continue

        if stripped == "$$":
            latex.append(r"\]" if in_display_math else r"\[")
            in_display_math = not in_display_math
            continue

        if in_display_math:
            latex.append(line)
            continue

        if stripped.startswith("#"):
            if in_itemize:
                latex.append(r"\end{itemize}")
                in_itemize = False
            level = len(stripped) - len(stripped.lstrip("#"))
            heading = escape_latex_text(stripped[level:].strip())
            if level == 1:
                latex.append(r"\section*{" + heading + "}")
            elif level == 2:
                latex.append(r"\section{" + heading + "}")
            elif level == 3:
                latex.append(r"\subsection{" + heading + "}")
            else:
                latex.append(r"\subsubsection{" + heading + "}")
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_itemize:
                latex.append(r"\begin{itemize}")
                in_itemize = True
            latex.append(r"\item " + escape_latex_preserving_math(stripped[2:].strip()))
            continue

        if in_itemize:
            latex.append(r"\end{itemize}")
            in_itemize = False

        latex.append("" if not stripped else escape_latex_preserving_math(line) + r"\par")

    if in_itemize:
        latex.append(r"\end{itemize}")
    if in_code:
        latex.append(r"\end{verbatim}")
    if in_display_math:
        latex.append(r"\]")
    return "\n".join(latex)


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
    entry = template_dir / "MathModel.tex"
    body = "\n".join(
        [
            r"\maketitle",
            r"\begin{abstract}",
            "本摘要为自动生成占位。请依据 traceability.md 中 allowed in abstract = yes 的结论补全，并删除不可追溯数字。",
            "",
            r"\keywords{数学建模\quad CUMCM\quad 可追溯结果}",
            r"\end{abstract}",
            "",
            r"\tableofcontents",
            "",
            markdown_to_latex(paper_md),
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
                    lines.append(r"\title{论文标题占位}")
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

    return "\n".join(
        [
            r"\documentclass[UTF8]{ctexart}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{graphicx}",
            r"\usepackage{booktabs}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, margin=2.5cm}",
            r"\title{论文标题占位}",
            r"\author{匿名占位}",
            r"\date{}",
            r"\begin{document}",
            body,
            r"\end{document}",
            "",
        ]
    ), reason


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

    paper_md = build_paper_md(payload)
    warnings.extend(scan_paper_md_quality(paper_md))
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
