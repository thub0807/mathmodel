from __future__ import annotations

import json
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def normalize_artifact_path(workspace_dir: Path, raw: str) -> str:
    path = Path(raw)
    if path.is_absolute():
        return str(path)
    if raw.startswith("workspace/"):
        return str((workspace_dir.parent / raw).resolve())
    return str((workspace_dir / raw).resolve())


def main() -> None:
    workspace_dir = Path(__file__).resolve().parents[2]
    output_dir = workspace_dir / "output"
    final_dir = output_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    q_dirs = sorted([path for path in output_dir.glob("q*") if path.is_dir()], key=lambda item: int(item.name[1:]))
    result_rows = []
    trace_rows = []
    figure_rows = []
    table_rows = []

    for q_dir in q_dirs:
        qid = q_dir.name
        result = load_json(q_dir / "results" / "result.json")
        validation = read_text(q_dir / "validation.md")
        sensitivity = read_text(q_dir / "sensitivity.md")
        summary = read_text(q_dir / f"{qid}_summary.md")
        result_rows.append(
            {
                "qid": qid,
                "status": result["status"],
                "model_name": result["model_name"],
                "paper_claims": result["paper_claims"],
                "warnings": result["warnings"],
                "validation": "PASS" if "**PASS**" in validation or "`PASS`" in validation else "PARTIAL",
                "sensitivity": "stable" if "stable" in sensitivity.lower() else "conditional",
            }
        )
        for key, value in result.get("trace", {}).items():
            trace_rows.append(
                {
                    "claim_id": key,
                    "qid": qid,
                    "source_file": value.get("source_file", ""),
                    "source_field": value.get("source_field", ""),
                    "allowed_in_abstract": "yes" if qid in {"q1", "q2", "q4", "q5"} else "no",
                    "limitation": result["warnings"][0] if result["warnings"] else "",
                }
            )
        for index, figure in enumerate(result.get("figures", []), start=1):
            figure_rows.append(
                {
                    "visual_id": f"{qid.upper()}-F{index}",
                    "qid": qid,
                    "path": normalize_artifact_path(workspace_dir, figure),
                    "include": "yes",
                }
            )
        for index, table in enumerate(result.get("tables", []), start=1):
            table_rows.append(
                {
                    "visual_id": f"{qid.upper()}-T{index}",
                    "qid": qid,
                    "path": normalize_artifact_path(workspace_dir, table),
                    "include": "yes",
                }
            )

    final_results_lines = ["# Final Results", ""]
    for row in result_rows:
        final_results_lines.extend(
            [
                f"## {row['qid']}",
                "",
                f"- status: `{row['status']}`",
                f"- model: {row['model_name']}",
                f"- validation: `{row['validation']}`",
                f"- sensitivity: `{row['sensitivity']}`",
                f"- paper claim: {row['paper_claims'][0]}",
                f"- limitation: {row['warnings'][0] if row['warnings'] else '无'}",
                "",
            ]
        )
    (final_dir / "final_results.md").write_text("\n".join(final_results_lines), encoding="utf-8")

    trace_lines = [
        "# Traceability",
        "",
        "| claim id | source question | source file | source field | allowed in abstract | limitation note |",
        "|---|---|---|---|---|---|",
    ]
    for row in trace_rows:
        trace_lines.append(
            f"| `{row['claim_id']}` | `{row['qid']}` | `{row['source_file']}` | `{row['source_field']}` | `{row['allowed_in_abstract']}` | {row['limitation']} |"
        )
    (final_dir / "traceability.md").write_text("\n".join(trace_lines) + "\n", encoding="utf-8")

    figure_lines = [
        "# Final Figures Index",
        "",
        "| visual id | source q | source file | include in paper |",
        "|---|---|---|---|",
    ]
    for row in figure_rows:
        figure_lines.append(f"| `{row['visual_id']}` | `{row['qid']}` | `{row['path']}` | `{row['include']}` |")
    (final_dir / "final_figures_index.md").write_text("\n".join(figure_lines) + "\n", encoding="utf-8")

    table_lines = [
        "# Final Tables Index",
        "",
        "| visual id | source q | source file | include in paper |",
        "|---|---|---|---|",
    ]
    for row in table_rows:
        table_lines.append(f"| `{row['visual_id']}` | `{row['qid']}` | `{row['path']}` | `{row['include']}` |")
    (final_dir / "final_tables_index.md").write_text("\n".join(table_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
