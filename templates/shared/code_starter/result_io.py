"""
Shared result writer for mathmodel-copilot code starters.

The helper writes:
- results/result.json aligned with templates/workspace/q/results/result.schema.json
- results/run.log aligned with templates/workspace/q/results/run_log.md
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
    figures: list[str] | None = None,
    tables: list[str] | None = None,
    warnings: list[str] | None = None,
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
        "inputs": _to_jsonable(inputs),
        "main_result": _to_jsonable(main_result),
        "metrics": _to_jsonable(metrics),
        "figures": figures or [],
        "tables": tables or [],
        "warnings": warnings or [],
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
        "| command | `python <starter>.py` |",
        "| implementation_language | python |",
        f"| result.json status | {status} |",
        f"| input files | {json.dumps(result['inputs'], ensure_ascii=False)} |",
        f"| output files | {json.dumps({'result_json': str(result_file)}, ensure_ascii=False)} |",
        f"| figures | {json.dumps(result['figures'], ensure_ascii=False)} |",
        f"| tables | {json.dumps(result['tables'], ensure_ascii=False)} |",
        f"| warnings | {json.dumps(result['warnings'], ensure_ascii=False)} |",
        f"| metrics | {json.dumps(result['metrics'], ensure_ascii=False)} |",
        f"| main_result | {json.dumps(result['main_result'], ensure_ascii=False)} |",
        f"| trace | {json.dumps(result['trace'], ensure_ascii=False)} |",
        f"| context | {json.dumps(context, ensure_ascii=False)} |",
        "",
    ]
    log_file = results_path / "run.log"
    log_file.write_text("\n".join(run_log), encoding="utf-8")

    return {"result_json": result_file, "run_log": log_file}
