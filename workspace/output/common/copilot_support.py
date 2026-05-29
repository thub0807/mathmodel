from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


@dataclass
class Bundle:
    workspace_dir: Path
    output_dir: Path
    problem_dir: Path
    records: list[dict[str, Any]]
    feature_table: pd.DataFrame
    target_table: pd.DataFrame
    merged: pd.DataFrame
    feature_columns: list[str]
    matrix: np.ndarray
    q1_weights: np.ndarray
    q2_oof: pd.DataFrame
    q2_result: dict[str, Any]
    route_map: dict[str, str]
    q2_module: ModuleType
    result_io_module: ModuleType
    selected_estimators: dict[str, Any]
    base_estimators: dict[str, dict[str, Any]]
    scaler: StandardScaler
    nn_model: NearestNeighbors
    source_molalities: dict[str, float]
    source_densities: dict[str, float]


def _load_module(module_name: str, path: Path) -> ModuleType:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_bundle(workspace_dir: Path) -> Bundle:
    workspace_dir = workspace_dir.resolve()
    output_dir = workspace_dir / "output"
    problem_dir = workspace_dir / "problem"
    q2_code_dir = output_dir / "q2" / "code"
    if str(q2_code_dir) not in sys.path:
        sys.path.insert(0, str(q2_code_dir))

    q2_module = _load_module("mathmodel_q2_build", q2_code_dir / "q2_build.py")
    result_io_module = _load_module("mathmodel_result_io", q2_code_dir / "result_io.py")

    records = json.loads((problem_dir / "attachments" / "A_data.json").read_text(encoding="utf-8"))
    feature_table = q2_module.build_feature_table(records)
    target_table, q1_weights = q2_module.load_target_table(workspace_dir)
    merged = feature_table.merge(target_table, on="GUID", how="inner")
    feature_columns = [column for column in feature_table.columns if column not in {"GUID", "pattern_key"}]
    matrix = feature_table[feature_columns].to_numpy(dtype=float)

    q2_oof = pd.read_csv(output_dir / "q2" / "results" / "oof_predictions.csv")
    q2_result = json.loads((output_dir / "q2" / "results" / "result.json").read_text(encoding="utf-8"))
    route_map = q2_result["main_result"]["cv_summary"]["selected_routes"]

    selected_estimators, _ = q2_module.fit_selected_route_models(matrix, target_table, route_map, feature_columns)

    base_estimators: dict[str, dict[str, Any]] = {}
    for target in q2_module.TARGETS:
        factories = q2_module.make_model_factories(q2_module.SEED)
        y_true = target_table[target].to_numpy(dtype=float)
        rf = factories["RandomForest"]()
        et = factories["ExtraTrees"]()
        gb = factories["HistGB"]()
        rf.fit(matrix, y_true)
        et.fit(matrix, y_true)
        gb.fit(matrix, y_true)
        base_estimators[target] = {"RandomForest": rf, "ExtraTrees": et, "HistGB": gb}

    scaler = StandardScaler().fit(matrix)
    nn_model = NearestNeighbors(n_neighbors=min(5, len(matrix)))
    nn_model.fit(scaler.transform(matrix))

    source_molalities: dict[str, float] = {}
    source_densities: dict[str, float] = {}
    for record in records:
        for key, value in record["electrolyte"]["source molalities"].items():
            source_molalities.setdefault(key, float(value))
        for key, value in record["electrolyte"]["source densities"].items():
            source_densities.setdefault(key, float(value))

    return Bundle(
        workspace_dir=workspace_dir,
        output_dir=output_dir,
        problem_dir=problem_dir,
        records=records,
        feature_table=feature_table,
        target_table=target_table,
        merged=merged,
        feature_columns=feature_columns,
        matrix=matrix,
        q1_weights=q1_weights,
        q2_oof=q2_oof,
        q2_result=q2_result,
        route_map=route_map,
        q2_module=q2_module,
        result_io_module=result_io_module,
        selected_estimators=selected_estimators,
        base_estimators=base_estimators,
        scaler=scaler,
        nn_model=nn_model,
        source_molalities=source_molalities,
        source_densities=source_densities,
    )


def predict_from_feature_table(bundle: Bundle, feature_table: pd.DataFrame) -> pd.DataFrame:
    working = feature_table.copy()
    for column in bundle.feature_columns:
        if column not in working.columns:
            working[column] = 0.0
    matrix = working[bundle.feature_columns].to_numpy(dtype=float)
    prediction = working[["GUID", "pattern_key", "pattern_count", "rare_pattern"]].copy()
    density = bundle.nn_model.kneighbors(bundle.scaler.transform(matrix))[0].mean(axis=1)
    prediction["uncertainty_density"] = density

    for target in bundle.q2_module.TARGETS:
        preds = {
            name: estimator.predict(matrix).ravel()
            for name, estimator in bundle.base_estimators[target].items()
        }
        route = bundle.route_map[target]
        if route == "RandomForest":
            selected = preds["RandomForest"]
        elif route == "ExtraTrees":
            selected = preds["ExtraTrees"]
        elif route == "HistGB":
            selected = preds["HistGB"]
        elif route == "Blend_RF_ET":
            selected = 0.5 * preds["RandomForest"] + 0.5 * preds["ExtraTrees"]
        else:
            selected = (preds["RandomForest"] + preds["ExtraTrees"] + preds["HistGB"]) / 3.0

        dispersion = np.std(
            np.vstack([preds["RandomForest"], preds["ExtraTrees"], preds["HistGB"]]),
            axis=0,
        )
        prediction[f"pred_{target}"] = selected
        prediction[f"uncertainty_dispersion_{target}"] = dispersion

    prediction["pred_S_pH"] = bundle.q2_module.ph_suitability(prediction["pred_pH"].to_numpy(dtype=float))
    recon_matrix = prediction[["pred_conductivity", "pred_S_pH", "pred_W_1", "pred_R_W"]].to_numpy(dtype=float)
    prediction["pred_PI_recon"] = bundle.q2_module.topsis_scores(recon_matrix, bundle.q1_weights)
    prediction["pred_PI_gap_direct_vs_recon"] = prediction["pred_PI"] - prediction["pred_PI_recon"]

    density_rank = prediction["uncertainty_density"].rank(pct=True)
    for target in bundle.q2_module.TARGETS:
        prediction[f"uncertainty_hook_{target}"] = (
            pd.Series(prediction[f"uncertainty_dispersion_{target}"]).rank(pct=True) + density_rank
        )
    return prediction


def build_candidate_records(
    bundle: Bundle,
    volume_maps: list[dict[str, float]],
    prefix: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, volumes in enumerate(volume_maps, start=1):
        normalized = {key: float(volumes.get(key, 0.0)) for key in bundle.source_densities}
        records.append(
            {
                "GUID": f"{prefix}_{index:04d}",
                "electrolyte": {
                    "volumes": normalized,
                    "source molalities": bundle.source_molalities,
                    "source densities": bundle.source_densities,
                },
            }
        )
    return records


def save_index(
    path: Path,
    title: str,
    entries: list[dict[str, str]],
) -> None:
    lines = [f"# {title}", ""]
    for item in entries:
        lines.append(f"- `{item['id']}` {item['path']}")
        lines.append(f"  - claim: {item['claim']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
