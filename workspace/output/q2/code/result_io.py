"""
q2 shared result writer aligned with the mathmodel-copilot Stage 3 contract.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value.as_posix())
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    return value


def write_result_and_log(
    *,
    question_id: str,
    model_name: str,
    status: str,
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    main_result: dict[str, Any],
    metrics: dict[str, Any],
    figures: list[str],
    tables: list[str],
    source_command: str,
    source_files: list[str],
    validation_hooks: list[str],
    warnings: list[str],
    limitations: list[str],
    paper_claims: list[str],
    trace: dict[str, Any],
    log_context: dict[str, Any],
    results_dir: str | Path,
) -> dict[str, Path]:
    if status not in {"pass", "partial", "fail"}:
        raise ValueError("status must be one of pass, partial, fail")

    result = {
        "question_id": question_id,
        "status": status,
        "model_name": model_name,
        "implementation_language": "python",
        "inputs": _to_jsonable(inputs),
        "outputs": _to_jsonable(outputs),
        "main_result": _to_jsonable(main_result),
        "metrics": _to_jsonable(metrics),
        "figures": _to_jsonable(figures),
        "tables": _to_jsonable(tables),
        "source_command": source_command,
        "source_files": _to_jsonable(source_files),
        "validation_hooks": _to_jsonable(validation_hooks),
        "warnings": _to_jsonable(warnings),
        "limitations": _to_jsonable(limitations),
        "paper_claims": _to_jsonable(paper_claims),
        "trace": _to_jsonable(trace),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)
    result_path = results_path / "result.json"
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    run_log_lines = [
        "# Run Log",
        "",
        "| Item | Content |",
        "|---|---|",
        f"| question_id | {question_id} |",
        f"| model_name | {model_name} |",
        f"| command | `{source_command}` |",
        "| implementation_language | python |",
        f"| input files | {json.dumps(_to_jsonable(inputs), ensure_ascii=False)} |",
        f"| output files | {json.dumps(_to_jsonable(outputs), ensure_ascii=False)} |",
        f"| code files | {json.dumps(_to_jsonable(source_files), ensure_ascii=False)} |",
        f"| code starter used | {json.dumps(log_context.get('code_starter_used'), ensure_ascii=False)} |",
        f"| environment notes | {json.dumps(log_context.get('environment_notes'), ensure_ascii=False)} |",
        f"| preprocessing notes | {json.dumps(log_context.get('preprocessing_notes'), ensure_ascii=False)} |",
        f"| abnormal data handling | {json.dumps(log_context.get('abnormal_data_handling'), ensure_ascii=False)} |",
        f"| random seed | {json.dumps(log_context.get('random_seed'), ensure_ascii=False)} |",
        f"| solver or algorithm settings | {json.dumps(log_context.get('algorithm_settings'), ensure_ascii=False)} |",
        f"| toy demo result | {json.dumps(log_context.get('toy_demo_result'), ensure_ascii=False)} |",
        f"| full run result summary | {json.dumps(log_context.get('full_run_result_summary'), ensure_ascii=False)} |",
        f"| warnings | {json.dumps(warnings, ensure_ascii=False)} |",
        f"| errors | {json.dumps(log_context.get('errors', []), ensure_ascii=False)} |",
        f"| runtime or solver notes | {json.dumps(log_context.get('runtime_notes'), ensure_ascii=False)} |",
        f"| interpretation notes | {json.dumps(log_context.get('interpretation_notes'), ensure_ascii=False)} |",
        "",
        "## Main Result Snapshot",
        "",
        "```json",
        json.dumps(_to_jsonable(main_result), ensure_ascii=False, indent=2),
        "```",
    ]

    run_log_path = results_path / "run.log"
    run_log_path.write_text("\n".join(run_log_lines), encoding="utf-8")
    return {"result_json": result_path, "run_log": run_log_path}
