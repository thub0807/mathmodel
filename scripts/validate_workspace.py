#!/usr/bin/env python3
"""Validate mathmodel-copilot workspace structure and final report consistency."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PDF_MISSING_MARKERS = ["paper.pdf missing", "PDF missing", "not generated", "未生成", "缺失"]
PDF_GENERATED_MARKERS = ["paper.pdf generated", "PDF generated", "generated successfully", "已生成", "生成成功"]
REPORT_PASS_MARKERS = ["paper generation pass", "paper generation: pass", "generation pass", "生成通过"]
SUMMARY_MARKERS = ["conclusion", "结论", "result", "结果", "摘要", "final"]
TRACE_SOURCE_MARKERS = ["source file", "source_file", "source:", "来源文件"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        return json.loads(read_text(path)), None
    except json.JSONDecodeError as exc:
        return None, str(exc)


def add_checked(state: dict, path: Path) -> None:
    state["checked"].append(str(path))


def require_file(state: dict, path: Path, label: str | None = None) -> bool:
    add_checked(state, path)
    if path.is_file():
        return True
    state["missing"].append(str(path if label is None else label))
    return False


def require_dir(state: dict, path: Path, label: str | None = None) -> bool:
    add_checked(state, path)
    if path.is_dir():
        return True
    state["missing"].append(str(path if label is None else label))
    return False


def warn(state: dict, message: str) -> None:
    state["warnings"].append(message)


def error(state: dict, message: str) -> None:
    state["errors"].append(message)


def contradiction(state: dict, message: str) -> None:
    state["contradictions"].append(message)


def q_dirs(workspace: Path) -> list[Path]:
    output = workspace / "output"
    dirs = [p for p in output.glob("q*") if p.is_dir()]
    return sorted(dirs, key=lambda path: (q_number(path) is None, q_number(path) or 0, path.name))


def q_number(path: Path) -> int | None:
    name = path.name.lower()
    if not name.startswith("q"):
        return None
    suffix = name[1:]
    return int(suffix) if suffix.isdigit() else None


def check_question_order(state: dict, workspace: Path) -> None:
    dirs = q_dirs(workspace)
    numbers = [q_number(path) for path in dirs]
    if any(number is None for number in numbers):
        warn(state, "q directories should use stable numeric ids such as q1, q2, q3")
        return
    expected = list(range(1, len(numbers) + 1))
    actual = [number for number in numbers if number is not None]
    if actual != expected:
        warn(state, f"q directories are not contiguous in question-major order: {actual}, expected {expected}")


def check_stage0(state: dict, workspace: Path) -> None:
    require_file(state, workspace / "problem" / "problem.md")
    require_file(state, workspace / "problem" / "reference.pdf")
    require_file(state, workspace / "output" / "problem_audit.md")
    require_file(state, workspace / "output" / "material_index.md")


def check_stage1(state: dict, workspace: Path) -> None:
    require_file(state, workspace / "output" / "question_index.md")
    dirs = q_dirs(workspace)
    add_checked(state, workspace / "output" / "q*/")
    if not dirs:
        state["missing"].append(str(workspace / "output" / "q*/"))
    check_question_order(state, workspace)


def check_stage2(state: dict, workspace: Path) -> None:
    for q_dir in q_dirs(workspace):
        require_file(state, q_dir / "review_packet.md")
        for name in ["warnings.md", "review_note.md"]:
            add_checked(state, q_dir / name)
        legacy_plan_files = ["analysis.md", "candidates.md", "model.md", "assumptions.md", "notation.md", "data_recon.md", "solution_plan.md"]
        legacy_existing = [name for name in legacy_plan_files if (q_dir / name).is_file()]
        if legacy_existing:
            warn(state, f"{q_dir}: legacy split Plan files are present but not v1.2 review entry: {', '.join(legacy_existing)}")


def validate_result_json_minimal(state: dict, path: Path, qid: str) -> dict | None:
    data, json_error = load_json(path)
    if json_error:
        error(state, f"{path}: invalid JSON: {json_error}")
        return None
    assert data is not None

    required = [
        "question_id",
        "status",
        "model_name",
        "implementation_language",
        "inputs",
        "outputs",
        "main_result",
        "metrics",
        "figures",
        "tables",
        "source_command",
        "source_files",
        "validation_hooks",
        "warnings",
        "limitations",
        "paper_claims",
        "trace",
        "created_at",
    ]
    for key in required:
        if key not in data:
            error(state, f"{path}: missing required key `{key}`")

    if data.get("status") not in {"pass", "partial", "fail"}:
        error(state, f"{path}: status must be pass, partial, or fail")

    question_id = str(data.get("question_id", ""))
    if question_id and question_id.lower() != qid.lower():
        warn(state, f"{path}: question_id `{question_id}` differs from directory `{qid}`")

    for key in ["figures", "tables", "source_files", "validation_hooks", "warnings", "limitations", "paper_claims"]:
        if key in data and not isinstance(data[key], list):
            error(state, f"{path}: `{key}` must be a list")
    for key in ["inputs", "outputs", "main_result", "metrics", "trace"]:
        if key in data and not isinstance(data[key], dict):
            error(state, f"{path}: `{key}` must be an object")
    return data


def check_stage3(state: dict, workspace: Path) -> dict[str, dict]:
    results: dict[str, dict] = {}
    for q_dir in q_dirs(workspace):
        qid = q_dir.name
        require_dir(state, q_dir / "code")
        result_path = q_dir / "results" / "result.json"
        if require_file(state, result_path):
            result = validate_result_json_minimal(state, result_path, qid)
            if result is not None:
                results[qid] = result
                check_result_references(state, workspace, q_dir, result_path, result)
        require_file(state, q_dir / "results" / "run.log")
    return results


def check_stage4(state: dict, workspace: Path) -> None:
    for q_dir in q_dirs(workspace):
        require_file(state, q_dir / "validation.md")
        require_file(state, q_dir / "sensitivity.md")


def extract_candidate_paths(text: str) -> list[str]:
    candidates: list[str] = []
    separators = ["(", ")", "[", "]", "`", "\"", "'", "<", ">", ",", ";", "|"]
    for line in text.splitlines():
        clean = line
        for sep in separators:
            clean = clean.replace(sep, " ")
        for token in clean.split():
            lower = token.lower()
            if lower.endswith((".png", ".jpg", ".jpeg", ".pdf", ".svg", ".csv", ".xlsx", ".tex", ".md", ".json")):
                candidates.append(token)
    return candidates


def resolve_path(workspace: Path, q_dir: Path | None, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    if raw.startswith("workspace/"):
        return workspace.parent / raw
    q_candidate = q_dir / raw if q_dir is not None else None
    if q_candidate is not None and q_candidate.exists():
        return q_candidate
    return workspace / raw


def check_index_paths(state: dict, workspace: Path, index_path: Path, q_dir: Path | None) -> None:
    if not index_path.is_file():
        return
    try:
        text = read_text(index_path)
    except OSError as exc:
        warn(state, f"{index_path}: could not read index: {exc}")
        return
    for raw in extract_candidate_paths(text):
        if raw == index_path.name:
            continue
        candidate = resolve_path(workspace, q_dir, raw)
        if not candidate.exists():
            warn(state, f"{index_path}: referenced path does not exist: {raw}")


def check_result_references(state: dict, workspace: Path, q_dir: Path, result_path: Path, result: dict) -> None:
    for key in ["figures", "tables"]:
        values = result.get(key, [])
        if not isinstance(values, list):
            continue
        for raw in values:
            if not isinstance(raw, str) or not raw.strip():
                continue
            candidate = resolve_path(workspace, q_dir, raw)
            if not candidate.exists():
                warn(state, f"{result_path}: `{key}` references missing path: {raw}")


def check_stage5(state: dict, workspace: Path) -> None:
    for q_dir in q_dirs(workspace):
        figure_index = q_dir / "figures" / "figure_index.md"
        table_index = q_dir / "tables" / "table_index.md"
        if require_file(state, figure_index):
            check_index_paths(state, workspace, figure_index, q_dir)
        if require_file(state, table_index):
            check_index_paths(state, workspace, table_index, q_dir)


def check_stage6(state: dict, workspace: Path) -> None:
    for q_dir in q_dirs(workspace):
        require_file(state, q_dir / f"{q_dir.name}_summary.md")


def check_question_major_dependencies(state: dict, workspace: Path) -> None:
    dirs = q_dirs(workspace)
    for index, q_dir in enumerate(dirs):
        if index == 0:
            continue
        qid = q_dir.name
        text_parts = []
        for name in ["review_packet.md", f"{qid}_summary.md", "review_note.md", "warnings.md"]:
            path = q_dir / name
            if path.is_file():
                text_parts.append(read_text(path))
        combined = "\n".join(text_parts).lower()
        previous = [path.name.lower() for path in dirs[:index]]
        missing_refs = [qid_prev for qid_prev in previous if qid_prev not in combined]
        if missing_refs:
            warn(state, f"{q_dir}: downstream question does not visibly reference upstream context: {', '.join(missing_refs)}")


def check_stage7(state: dict, workspace: Path) -> None:
    final = workspace / "output" / "final"
    for name in ["final_results.md", "final_figures_index.md", "final_tables_index.md", "traceability.md"]:
        path = final / name
        if require_file(state, path) and name.endswith("_index.md"):
            check_index_paths(state, workspace, path, None)


def check_stage8(state: dict, workspace: Path, strict: bool) -> None:
    final = workspace / "output" / "final"
    for name in ["paper.md", "paper.tex", "render_report.json", "latex_compile.log"]:
        require_file(state, final / name)
    require_dir(state, final / "source")
    if strict:
        require_file(state, final / "paper.pdf")


def check_stage9(state: dict, workspace: Path) -> None:
    final = workspace / "output" / "final"
    for name in ["review_report.md", "anonymity_report.md", "quality_report.md"]:
        require_file(state, final / name)


def final_report_texts(workspace: Path) -> dict[str, str]:
    final = workspace / "output" / "final"
    texts: dict[str, str] = {}
    for name in ["review_report.md", "anonymity_report.md", "quality_report.md"]:
        path = final / name
        if path.is_file():
            texts[name] = read_text(path)
    return texts


def contains_any(text: str, markers: list[str]) -> bool:
    lower = text.lower()
    return any(marker.lower() in lower for marker in markers)


def check_pdf_contradictions(state: dict, workspace: Path) -> None:
    final = workspace / "output" / "final"
    pdf_exists = (final / "paper.pdf").exists()
    texts = final_report_texts(workspace)
    for name, text in texts.items():
        if pdf_exists and contains_any(text, PDF_MISSING_MARKERS):
            contradiction(state, f"{name}: says PDF is missing/not generated, but paper.pdf exists")
        if not pdf_exists and contains_any(text, PDF_GENERATED_MARKERS):
            contradiction(state, f"{name}: claims PDF was generated, but paper.pdf is missing")

    render_report = final / "render_report.json"
    quality_report = texts.get("quality_report.md", "")
    if render_report.is_file():
        data, json_error = load_json(render_report)
        if json_error:
            error(state, f"{render_report}: invalid JSON: {json_error}")
        elif data:
            status = str(data.get("status", "")).lower()
            compile_success = bool(data.get("compile", {}).get("success"))
            if (status in {"failed", "fail", "error"} or data.get("errors") or (data.get("compile", {}).get("attempted") and not compile_success)) and contains_any(quality_report, REPORT_PASS_MARKERS):
                contradiction(state, "render_report.json shows render failed, but quality_report.md claims paper generation pass")


def q_status_map(workspace: Path) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for q_dir in q_dirs(workspace):
        result_path = q_dir / "results" / "result.json"
        if result_path.is_file():
            data, _ = load_json(result_path)
            if isinstance(data, dict):
                statuses[q_dir.name] = str(data.get("status", "")).lower()
    return statuses


def check_status_claim_consistency(state: dict, workspace: Path) -> None:
    final = workspace / "output" / "final"
    final_results = read_text(final / "final_results.md") if (final / "final_results.md").is_file() else ""
    traceability = read_text(final / "traceability.md") if (final / "traceability.md").is_file() else ""
    combined = final_results + "\n" + traceability
    for qid, status in q_status_map(workspace).items():
        q_pattern = re.compile(rf"\b{re.escape(qid)}\b", re.IGNORECASE)
        if status == "fail" and q_pattern.search(combined) and contains_any(combined, SUMMARY_MARKERS):
            warn(state, f"{qid}: result.json status is fail, but final_results.md/traceability.md appears to include a summary claim")
        if status == "partial" and q_pattern.search(traceability):
            pattern = re.compile(rf"{re.escape(qid)}.*allowed in abstract.*yes", re.IGNORECASE)
            if pattern.search(traceability.replace("\n", " ")):
                warn(state, f"{qid}: partial result appears marked allowed in abstract = yes")


def check_traceability_sources(state: dict, workspace: Path) -> None:
    trace = workspace / "output" / "final" / "traceability.md"
    if not trace.is_file():
        return
    text = read_text(trace)
    for raw in extract_candidate_paths(text):
        candidate = resolve_path(workspace, None, raw)
        if not candidate.exists():
            message = f"{trace}: referenced source file does not exist: {raw}"
            if contains_any(raw, [".json", ".md"]):
                warn(state, message)
            else:
                warn(state, message)
    for line in text.splitlines():
        lower = line.lower()
        if any(marker in lower for marker in TRACE_SOURCE_MARKERS):
            for raw in extract_candidate_paths(line):
                candidate = resolve_path(workspace, None, raw)
                if not candidate.exists():
                    warn(state, f"{trace}: source file reference missing: {raw}")


def compute_verdict(state: dict, strict: bool) -> str:
    if state["errors"] or state["contradictions"] or state["missing"]:
        return "fail"
    if strict and state["warnings"]:
        return "fail"
    if state["warnings"]:
        return "partial"
    return "pass"


def validate(workspace: Path, max_stage: int, strict: bool) -> dict:
    state = {
        "verdict": "fail",
        "errors": [],
        "warnings": [],
        "missing": [],
        "contradictions": [],
        "checked": [],
    }
    checks = [
        check_stage0,
        check_stage1,
        check_stage2,
        check_stage3,
        check_stage4,
        check_stage5,
        check_stage6,
        check_stage7,
        check_stage8,
        check_stage9,
    ]
    for stage_number, check in enumerate(checks):
        if stage_number > max_stage:
            break
        if check is check_stage3:
            check(state, workspace)
        elif check is check_stage8:
            check(state, workspace, strict)
        else:
            check(state, workspace)

    if max_stage >= 6:
        check_question_major_dependencies(state, workspace)
    check_pdf_contradictions(state, workspace)
    check_status_claim_consistency(state, workspace)
    check_traceability_sources(state, workspace)
    state["checked"] = sorted(dict.fromkeys(state["checked"]))
    state["missing"] = sorted(dict.fromkeys(state["missing"]))
    state["warnings"] = sorted(dict.fromkeys(state["warnings"]))
    state["errors"] = sorted(dict.fromkeys(state["errors"]))
    state["contradictions"] = sorted(dict.fromkeys(state["contradictions"]))
    state["verdict"] = compute_verdict(state, strict)
    return state


def print_human(state: dict) -> None:
    print(state["verdict"].upper())
    for key in ["errors", "warnings", "missing", "contradictions", "checked"]:
        print(f"\n{key}:")
        items = state[key]
        if not items:
            print("- none")
        else:
            for item in items:
                print(f"- {item}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate mathmodel-copilot workspace contract, schemas, and final report consistency.")
    parser.add_argument("workspace", help="Workspace root to validate.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation result.")
    parser.add_argument("--stage", type=int, default=9, choices=range(0, 10), metavar="N", help="Validate through stage N, 0-9. Default: 9.")
    parser.add_argument("--strict", action="store_true", help="Require strict final artifacts and fail on warnings.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    state = validate(Path(args.workspace).resolve(), args.stage, args.strict)
    if args.json:
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print_human(state)
    if state["errors"] or state["contradictions"]:
        return 1
    if args.strict and (state["missing"] or state["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
