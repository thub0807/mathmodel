"""
Shared result writer for mathmodel-copilot code starters.

The helper writes:
- results/result.json aligned with the Stage 3 Result JSON Contract
- results/run.log aligned with the Stage 3 run log contract
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
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
    main_result: dict[str, Any],
    metrics: dict[str, Any],
    outputs: dict[str, Any] | None = None,
    figures: list[str] | None = None,
    tables: list[str] | None = None,
    source_command: str | None = None,
    source_files: list[str] | None = None,
    validation_hooks: list[str] | None = None,
    warnings: list[str] | None = None,
    limitations: list[str] | None = None,
    paper_claims: list[str] | None = None,
    trace: dict[str, Any] | None = None,
    log_context: dict[str, Any] | None = None,
    results_dir: str | Path = "results",
) -> dict[str, Path]:
    if status not in {"pass", "partial", "fail"}:
        raise ValueError("status must be one of: pass, partial, fail")

    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    result = {
        "question_id": question_id,
        "status": status,
        "model_name": model_name,
        "implementation_language": "python",
        "inputs": _to_jsonable(inputs),
        "outputs": _to_jsonable(outputs or {}),
        "main_result": _to_jsonable(main_result),
        "metrics": _to_jsonable(metrics),
        "figures": figures or [],
        "tables": tables or [],
        "source_command": source_command or "python <starter>.py",
        "source_files": source_files or [],
        "validation_hooks": validation_hooks or [],
        "warnings": warnings or [],
        "limitations": limitations or [],
        "paper_claims": paper_claims or [],
        "trace": _to_jsonable(trace or {}),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    result_file = results_path / "result.json"
    result_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    context = _to_jsonable(log_context or {})
    run_log = [
        "# Run Log",
        "",
        "| Item | Content |",
        "|---|---|",
        f"| question_id | {question_id} |",
        f"| model_name | {model_name} |",
        f"| command | `{result['source_command']}` |",
        "| implementation_language | python |",
        f"| result.json status | {status} |",
        f"| input files | {json.dumps(result['inputs'], ensure_ascii=False)} |",
        f"| output files | {json.dumps(result['outputs'] or {'result_json': str(result_file)}, ensure_ascii=False)} |",
        f"| source files | {json.dumps(result['source_files'], ensure_ascii=False)} |",
        f"| validation hooks | {json.dumps(result['validation_hooks'], ensure_ascii=False)} |",
        f"| figures | {json.dumps(result['figures'], ensure_ascii=False)} |",
        f"| tables | {json.dumps(result['tables'], ensure_ascii=False)} |",
        f"| warnings | {json.dumps(result['warnings'], ensure_ascii=False)} |",
        f"| limitations | {json.dumps(result['limitations'], ensure_ascii=False)} |",
        f"| paper claims | {json.dumps(result['paper_claims'], ensure_ascii=False)} |",
        f"| metrics | {json.dumps(result['metrics'], ensure_ascii=False)} |",
        f"| main_result | {json.dumps(result['main_result'], ensure_ascii=False)} |",
        f"| trace | {json.dumps(result['trace'], ensure_ascii=False)} |",
        f"| context | {json.dumps(context, ensure_ascii=False)} |",
        "",
    ]
    log_file = results_path / "run.log"
    log_file.write_text("\n".join(run_log), encoding="utf-8")

    return {"result_json": result_file, "run_log": log_file}
