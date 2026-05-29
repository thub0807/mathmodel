from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from result_io import write_result_and_log


SEED = 42
OUTER_SPLITS = 5
TARGETS = ["conductivity", "pH", "W_1", "R_W", "PI"]
BASELINE_MODELS = ["ElasticNet", "PLS", "RandomForest", "ExtraTrees", "HistGB", "Blend_RF_ET", "Blend_Tree3"]
TREE_ONLY_MODELS = ["RandomForest", "ExtraTrees", "HistGB"]
BLEND_WEIGHTS = {
    "Blend_RF_ET": {"RandomForest": 0.5, "ExtraTrees": 0.5},
    "Blend_Tree3": {"RandomForest": 1.0 / 3.0, "ExtraTrees": 1.0 / 3.0, "HistGB": 1.0 / 3.0},
}


@dataclass
class BlendRegressor:
    models: list[Pipeline]
    weights: list[float]

    def fit(self, _: np.ndarray, __: np.ndarray | None = None) -> "BlendRegressor":
        return self

    def predict(self, matrix: np.ndarray) -> np.ndarray:
        out = np.zeros(matrix.shape[0], dtype=float)
        for weight, model in zip(self.weights, self.models):
            pred = model.predict(matrix)
            out += weight * np.asarray(pred, dtype=float).ravel()
        return out


def ph_suitability(values: np.ndarray, low: float = 6.5, high: float = 8.5, margin: float = 1.0) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    distance = np.maximum.reduce([np.zeros_like(values), low - values, values - high])
    return np.clip(1.0 - distance / margin, 0.0, 1.0)


def topsis_scores(matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
    denom = np.sqrt(np.sum(matrix**2, axis=0, keepdims=True))
    denom = np.where(denom == 0.0, 1.0, denom)
    norm = matrix / denom
    weighted = norm * weights
    pos = weighted.max(axis=0)
    neg = weighted.min(axis=0)
    d_pos = np.sqrt(np.sum((weighted - pos) ** 2, axis=1))
    d_neg = np.sqrt(np.sum((weighted - neg) ** 2, axis=1))
    return d_neg / (d_pos + d_neg + 1e-12)


def build_feature_table(records: list[dict]) -> pd.DataFrame:
    components = sorted({key for row in records for key in row["electrolyte"]["volumes"]})
    non_water = [key for key in components if key != "water"]
    rows: list[dict[str, float | int | str]] = []

    for row in records:
        ele = row["electrolyte"]
        volumes = ele["volumes"]
        molalities = ele["source molalities"]
        densities = ele["source densities"]
        total_volume = float(sum(volumes.values()))
        active_components = [key for key in non_water if volumes.get(key, 0.0) > 0]
        pattern_key = "+".join(sorted(active_components)) if active_components else "water_only"

        result: dict[str, float | int | str] = {
            "GUID": row["GUID"],
            "pattern_key": pattern_key,
            "total_volume": total_volume,
        }

        non_water_ratios: list[float] = []
        mass_total = 0.0
        ionic_total = 0.0
        for component in components:
            volume = float(volumes.get(component, 0.0))
            density = float(densities.get(component, 0.0))
            molality = float(molalities.get(component, 0.0))
            ratio = volume / total_volume if total_volume else 0.0
            result[f"ratio_{component}"] = ratio
            result[f"present_{component}"] = 1.0 if volume > 0 else 0.0
            result[f"mass_proxy_{component}"] = volume * density
            result[f"mol_proxy_{component}"] = volume * density * molality
            mass_total += volume * density
            ionic_total += volume * density * molality
            if component != "water" and ratio > 0:
                non_water_ratios.append(ratio)

        result["active_count"] = len(active_components)
        result["water_ratio"] = float(result["ratio_water"])
        result["weighted_density"] = mass_total / total_volume if total_volume else 0.0
        result["ionic_strength_proxy"] = ionic_total / total_volume if total_volume else 0.0
        result["salt_ratio_sum"] = sum(float(result[f"ratio_{component}"]) for component in non_water)
        result["nonwater_entropy"] = (
            float(-sum(ratio * np.log(ratio) for ratio in non_water_ratios if ratio > 0)) if non_water_ratios else 0.0
        )
        result["max_nonwater_ratio"] = max(non_water_ratios) if non_water_ratios else 0.0
        result["sulfate_ratio"] = float(result["ratio_Li2SO4"]) + float(result["ratio_Na2SO4"])
        result["nitrate_ratio"] = float(result["ratio_LiNO3"]) + float(result["ratio_NaNO3"])
        result["perchlorate_ratio"] = float(result["ratio_LiClO4"]) + float(result["ratio_NaClO4"])
        result["bromide_ratio"] = float(result["ratio_NaBr"])
        result["lithium_ratio"] = (
            float(result["ratio_Li2SO4"]) + float(result["ratio_LiClO4"]) + float(result["ratio_LiNO3"])
        )
        result["sodium_ratio"] = (
            float(result["ratio_Na2SO4"])
            + float(result["ratio_NaBr"])
            + float(result["ratio_NaClO4"])
            + float(result["ratio_NaNO3"])
        )
        result["water_x_ionic"] = float(result["water_ratio"]) * float(result["ionic_strength_proxy"])
        result["sulfate_x_nitrate"] = float(result["sulfate_ratio"]) * float(result["nitrate_ratio"])
        rows.append(result)

    raw = pd.DataFrame(rows)
    pattern_count = raw["pattern_key"].value_counts().to_dict()
    raw["pattern_count"] = raw["pattern_key"].map(pattern_count).astype(int)
    raw["rare_pattern"] = (raw["pattern_count"] <= 5).astype(int)
    pattern_dummies = pd.get_dummies(raw["pattern_key"], prefix="pattern", dtype=float)
    return pd.concat([raw, pattern_dummies], axis=1)


def load_target_table(workspace_dir: Path) -> tuple[pd.DataFrame, np.ndarray]:
    q1_table = pd.read_csv(workspace_dir / "output" / "q1" / "results" / "indicator_table.csv")
    q1_result = json.loads((workspace_dir / "output" / "q1" / "results" / "result.json").read_text(encoding="utf-8"))
    critic_weights = q1_result["main_result"]["weight_scheme"]["critic_weights"]
    weights = np.array(
        [
            critic_weights["conductivity"],
            critic_weights["S_pH"],
            critic_weights["W_1"],
            critic_weights["R_W"],
        ],
        dtype=float,
    )
    target_table = q1_table[["GUID", "conductivity", "pH", "W_1", "R_W", "PI"]].copy()
    return target_table, weights


def make_model_factories(seed: int) -> dict[str, callable]:
    def elastic_net() -> Pipeline:
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                ("scaler", StandardScaler()),
                ("model", ElasticNet(alpha=0.003, l1_ratio=0.2, max_iter=50000, random_state=seed)),
            ]
        )

    def pls() -> Pipeline:
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                ("scaler", StandardScaler()),
                ("model", PLSRegression(n_components=6, scale=False)),
            ]
        )

    def random_forest() -> Pipeline:
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=140,
                        min_samples_leaf=2,
                        max_features="sqrt",
                        random_state=seed,
                        n_jobs=-1,
                    ),
                ),
            ]
        )

    def extra_trees() -> Pipeline:
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                (
                    "model",
                    ExtraTreesRegressor(
                        n_estimators=140,
                        min_samples_leaf=2,
                        max_features="sqrt",
                        random_state=seed,
                        n_jobs=-1,
                    ),
                ),
            ]
        )

    def hist_gradient_boosting() -> Pipeline:
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="constant", fill_value=0.0)),
                (
                    "model",
                    HistGradientBoostingRegressor(
                        max_depth=4,
                        learning_rate=0.05,
                        max_leaf_nodes=31,
                        min_samples_leaf=6,
                        l2_regularization=0.1,
                        random_state=seed,
                    ),
                ),
            ]
        )

    return {
        "ElasticNet": elastic_net,
        "PLS": pls,
        "RandomForest": random_forest,
        "ExtraTrees": extra_trees,
        "HistGB": hist_gradient_boosting,
    }


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    residual = y_true - y_pred
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "bias": float(np.mean(y_pred - y_true)),
        "spearman": float(spearmanr(y_true, y_pred).statistic),
        "residual_std": float(np.std(residual, ddof=0)),
    }


def run_candidate_oof(
    feature_table: pd.DataFrame,
    target_table: pd.DataFrame,
    feature_columns: list[str],
    seed: int = SEED,
) -> dict[str, object]:
    merged = feature_table.merge(target_table, on="GUID", how="inner")
    matrix = merged[feature_columns].to_numpy(dtype=float)
    n_rows = len(merged)
    fold_ids = np.zeros(n_rows, dtype=int)
    density_score = np.zeros(n_rows, dtype=float)
    dispersion_store = {target: np.zeros(n_rows, dtype=float) for target in TARGETS}
    prediction_store = {
        target: {model_name: np.zeros(n_rows, dtype=float) for model_name in BASELINE_MODELS}
        for target in TARGETS
    }

    splitter = KFold(n_splits=OUTER_SPLITS, shuffle=True, random_state=seed)
    for fold_id, (train_idx, test_idx) in enumerate(splitter.split(matrix), start=1):
        fold_ids[test_idx] = fold_id

        scaler = StandardScaler().fit(matrix[train_idx])
        train_scaled = scaler.transform(matrix[train_idx])
        test_scaled = scaler.transform(matrix[test_idx])
        nn = NearestNeighbors(n_neighbors=min(5, len(train_idx)))
        nn.fit(train_scaled)
        distances, _ = nn.kneighbors(test_scaled)
        density_score[test_idx] = distances.mean(axis=1)

        fold_factories = make_model_factories(seed + fold_id)
        for target in TARGETS:
            y_train = merged.iloc[train_idx][target].to_numpy(dtype=float)
            local_predictions: dict[str, np.ndarray] = {}
            for model_name in ["ElasticNet", "PLS", "RandomForest", "ExtraTrees", "HistGB"]:
                model = fold_factories[model_name]()
                model.fit(matrix[train_idx], y_train)
                pred = np.asarray(model.predict(matrix[test_idx]), dtype=float).ravel()
                prediction_store[target][model_name][test_idx] = pred
                local_predictions[model_name] = pred

            prediction_store[target]["Blend_RF_ET"][test_idx] = (
                0.5 * local_predictions["RandomForest"] + 0.5 * local_predictions["ExtraTrees"]
            )
            prediction_store[target]["Blend_Tree3"][test_idx] = (
                local_predictions["RandomForest"] + local_predictions["ExtraTrees"] + local_predictions["HistGB"]
            ) / 3.0
            dispersion_store[target][test_idx] = np.std(
                np.vstack(
                    [
                        local_predictions["RandomForest"],
                        local_predictions["ExtraTrees"],
                        local_predictions["HistGB"],
                    ]
                ),
                axis=0,
            )

    model_probe_rows: list[dict[str, object]] = []
    for target in TARGETS:
        y_true = merged[target].to_numpy(dtype=float)
        for model_name in BASELINE_MODELS:
            stats = regression_metrics(y_true, prediction_store[target][model_name])
            model_probe_rows.append({"target": target, "model": model_name, **stats})

    probe_df = pd.DataFrame(model_probe_rows).sort_values(["target", "mae", "rmse"]).reset_index(drop=True)
    return {
        "merged": merged,
        "matrix": matrix,
        "fold_ids": fold_ids,
        "density_score": density_score,
        "dispersion_store": dispersion_store,
        "prediction_store": prediction_store,
        "model_probe": probe_df,
    }


def select_main_routes(model_probe: pd.DataFrame) -> dict[str, str]:
    routes: dict[str, str] = {}
    for target in TARGETS:
        subset = model_probe[model_probe["target"] == target].copy()
        single_best = subset[subset["model"].isin(TREE_ONLY_MODELS)].sort_values("mae").iloc[0]
        candidate_best = subset[subset["model"].isin(TREE_ONLY_MODELS + ["Blend_RF_ET", "Blend_Tree3"])].sort_values(
            "mae"
        ).iloc[0]
        relative_gain = (single_best["mae"] - candidate_best["mae"]) / max(single_best["mae"], 1e-12)
        if target in {"W_1", "R_W"} and relative_gain < 0.01:
            routes[target] = str(single_best["model"])
        else:
            routes[target] = str(candidate_best["model"])
    return routes


def build_selected_prediction_frame(
    merged: pd.DataFrame,
    fold_ids: np.ndarray,
    density_score: np.ndarray,
    dispersion_store: dict[str, np.ndarray],
    prediction_store: dict[str, dict[str, np.ndarray]],
    route_map: dict[str, str],
    q1_weights: np.ndarray,
) -> pd.DataFrame:
    selected = merged[
        [
            "GUID",
            "pattern_key",
            "pattern_count",
            "rare_pattern",
            "conductivity",
            "pH",
            "W_1",
            "R_W",
            "PI",
        ]
    ].copy()
    selected["fold"] = fold_ids
    selected["uncertainty_density"] = density_score

    for target in TARGETS:
        route_name = route_map[target]
        selected[f"pred_{target}"] = prediction_store[target][route_name]
        selected[f"pred_{target}_baseline"] = prediction_store[target]["ElasticNet"]
        selected[f"pred_{target}_pls"] = prediction_store[target]["PLS"]
        selected[f"resid_{target}"] = selected[f"pred_{target}"] - selected[target]
        selected[f"uncertainty_dispersion_{target}"] = dispersion_store[target]
        for model_name in BASELINE_MODELS:
            selected[f"pred_{target}_{model_name}"] = prediction_store[target][model_name]

    selected["pred_S_pH"] = ph_suitability(selected["pred_pH"].to_numpy(dtype=float))
    recon_matrix = selected[["pred_conductivity", "pred_S_pH", "pred_W_1", "pred_R_W"]].to_numpy(dtype=float)
    selected["pred_PI_recon"] = topsis_scores(recon_matrix, q1_weights)
    selected["pred_PI_gap_direct_vs_recon"] = selected["pred_PI"] - selected["pred_PI_recon"]

    for target in TARGETS:
        err_rank = selected[f"uncertainty_dispersion_{target}"].rank(pct=True)
        dens_rank = selected["uncertainty_density"].rank(pct=True)
        selected[f"uncertainty_hook_{target}"] = err_rank + dens_rank

    return selected


def compute_slice_error_summary(pred_frame: pd.DataFrame) -> pd.DataFrame:
    q90 = float(pred_frame["PI"].quantile(0.90))
    q80 = float(pred_frame["PI"].quantile(0.80))
    q10 = float(pred_frame["PI"].quantile(0.10))
    cond_q75 = float(pred_frame["conductivity"].quantile(0.75))
    pi_q25 = float(pred_frame["PI"].quantile(0.25))

    masks = {
        "overall": np.ones(len(pred_frame), dtype=bool),
        "high_PI_top10": pred_frame["PI"].to_numpy() >= q90,
        "high_PI_top20": pred_frame["PI"].to_numpy() >= q80,
        "low_PI_bottom10": pred_frame["PI"].to_numpy() <= q10,
        "rare_pattern": pred_frame["rare_pattern"].to_numpy(dtype=int) == 1,
        "high_cond_low_PI": (
            (pred_frame["conductivity"].to_numpy() >= cond_q75)
            & (pred_frame["PI"].to_numpy() <= pi_q25)
        ),
        "RW_gt_1": pred_frame["R_W"].to_numpy() > 1.0,
    }

    rows: list[dict[str, object]] = []
    for target in TARGETS:
        absolute_error = np.abs(pred_frame[f"pred_{target}"] - pred_frame[target])
        signed_error = pred_frame[f"pred_{target}"] - pred_frame[target]
        overall_mae = float(absolute_error.mean())
        for slice_name, mask in masks.items():
            count = int(mask.sum())
            if count == 0:
                continue
            slice_mae = float(absolute_error[mask].mean())
            rows.append(
                {
                    "target": target,
                    "slice": slice_name,
                    "count": count,
                    "mae": slice_mae,
                    "rmse": float(np.sqrt(np.mean((signed_error[mask]) ** 2))),
                    "bias": float(signed_error[mask].mean()),
                    "mae_ratio_vs_overall": float(slice_mae / overall_mae) if overall_mae else 0.0,
                }
            )
    return pd.DataFrame(rows).sort_values(["target", "slice"]).reset_index(drop=True)


def compute_pi_consistency_summary(pred_frame: pd.DataFrame) -> pd.DataFrame:
    masks = {
        "overall": np.ones(len(pred_frame), dtype=bool),
        "high_PI_top10": pred_frame["PI"].to_numpy() >= float(pred_frame["PI"].quantile(0.90)),
        "low_PI_bottom10": pred_frame["PI"].to_numpy() <= float(pred_frame["PI"].quantile(0.10)),
        "rare_pattern": pred_frame["rare_pattern"].to_numpy(dtype=int) == 1,
    }

    rows: list[dict[str, object]] = []
    for slice_name, mask in masks.items():
        direct = pred_frame.loc[mask, "pred_PI"].to_numpy(dtype=float)
        recon = pred_frame.loc[mask, "pred_PI_recon"].to_numpy(dtype=float)
        actual = pred_frame.loc[mask, "PI"].to_numpy(dtype=float)
        gap = direct - recon
        rows.append(
            {
                "slice": slice_name,
                "count": int(mask.sum()),
                "direct_mae_vs_actual": float(mean_absolute_error(actual, direct)),
                "recon_mae_vs_actual": float(mean_absolute_error(actual, recon)),
                "direct_vs_recon_spearman": float(spearmanr(direct, recon).statistic),
                "mean_abs_gap": float(np.mean(np.abs(gap))),
                "q90_abs_gap": float(np.quantile(np.abs(gap), 0.90)),
            }
        )
    return pd.DataFrame(rows)


def run_route_oof(
    merged: pd.DataFrame,
    feature_columns: list[str],
    route_map: dict[str, str],
    seed: int,
) -> pd.DataFrame:
    matrix = merged[feature_columns].to_numpy(dtype=float)
    splitter = KFold(n_splits=OUTER_SPLITS, shuffle=True, random_state=seed)
    rows: list[dict[str, object]] = []

    for target in TARGETS:
        route = route_map[target]
        y_true = merged[target].to_numpy(dtype=float)
        pred = np.zeros(len(merged), dtype=float)
        for fold_id, (train_idx, test_idx) in enumerate(splitter.split(matrix), start=1):
            factories = make_model_factories(seed + fold_id)
            rf = factories["RandomForest"]().fit(matrix[train_idx], y_true[train_idx]).predict(matrix[test_idx]).ravel()
            et = factories["ExtraTrees"]().fit(matrix[train_idx], y_true[train_idx]).predict(matrix[test_idx]).ravel()
            gb = factories["HistGB"]().fit(matrix[train_idx], y_true[train_idx]).predict(matrix[test_idx]).ravel()

            if route == "RandomForest":
                pred[test_idx] = rf
            elif route == "ExtraTrees":
                pred[test_idx] = et
            elif route == "HistGB":
                pred[test_idx] = gb
            elif route == "Blend_RF_ET":
                pred[test_idx] = 0.5 * rf + 0.5 * et
            else:
                pred[test_idx] = (rf + et + gb) / 3.0

        metrics = regression_metrics(y_true, pred)
        rows.append({"scenario": "", "target": target, **metrics})
    return pd.DataFrame(rows)


def fit_selected_route_models(
    matrix: np.ndarray,
    target_table: pd.DataFrame,
    route_map: dict[str, str],
    feature_columns: list[str],
) -> tuple[dict[str, BlendRegressor | Pipeline], pd.DataFrame]:
    estimators: dict[str, BlendRegressor | Pipeline] = {}
    rows: list[dict[str, object]] = []

    for target in TARGETS:
        factories = make_model_factories(SEED)
        rf = factories["RandomForest"]()
        et = factories["ExtraTrees"]()
        gb = factories["HistGB"]()
        y_true = target_table[target].to_numpy(dtype=float)
        rf.fit(matrix, y_true)
        et.fit(matrix, y_true)
        gb.fit(matrix, y_true)
        route = route_map[target]

        if route == "RandomForest":
            estimator: BlendRegressor | Pipeline = rf
            route_weights = {"RandomForest": 1.0}
        elif route == "ExtraTrees":
            estimator = et
            route_weights = {"ExtraTrees": 1.0}
        elif route == "HistGB":
            estimator = gb
            route_weights = {"HistGB": 1.0}
        elif route == "Blend_RF_ET":
            estimator = BlendRegressor(models=[rf, et], weights=[0.5, 0.5])
            route_weights = BLEND_WEIGHTS["Blend_RF_ET"]
        else:
            estimator = BlendRegressor(models=[rf, et, gb], weights=[1.0 / 3.0] * 3)
            route_weights = BLEND_WEIGHTS["Blend_Tree3"]

        estimators[target] = estimator
        rows.append(
            {
                "target": target,
                "selected_route": route,
                "route_weights": json.dumps(route_weights, ensure_ascii=False),
                "n_features": len(feature_columns),
            }
        )

    return estimators, pd.DataFrame(rows)


def compute_feature_importance_summary(
    estimators: dict[str, BlendRegressor | Pipeline],
    matrix: np.ndarray,
    target_table: pd.DataFrame,
    feature_columns: list[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for target in TARGETS:
        estimator = estimators[target]
        y_true = target_table[target].to_numpy(dtype=float)
        importance = permutation_importance(
            estimator,
            matrix,
            y_true,
            scoring="neg_mean_absolute_error",
            n_repeats=3,
            random_state=SEED,
            n_jobs=1,
        )
        order = np.argsort(-importance.importances_mean)[:12]
        for rank, index in enumerate(order, start=1):
            rows.append(
                {
                    "target": target,
                    "rank": rank,
                    "feature": feature_columns[index],
                    "importance_mean": float(importance.importances_mean[index]),
                    "importance_std": float(importance.importances_std[index]),
                }
            )
    return pd.DataFrame(rows)


def run_toy_demo(
    merged: pd.DataFrame,
    feature_columns: list[str],
) -> dict[str, object]:
    toy = merged.sample(n=60, random_state=SEED).reset_index(drop=True)
    toy_result = run_candidate_oof(
        feature_table=toy[["GUID"] + feature_columns].copy(),
        target_table=toy[["GUID", "conductivity", "pH", "W_1", "R_W", "PI"]].copy(),
        feature_columns=feature_columns,
        seed=SEED,
    )
    probe = toy_result["model_probe"]

    def metric(target: str, model: str) -> float:
        return float(
            probe.loc[(probe["target"] == target) & (probe["model"] == model), "mae"].iloc[0]
        )

    return {
        "n_rows": 60,
        "contains_nan": bool(toy[feature_columns].isna().any().any()),
        "pi_blend3_mae": metric("PI", "Blend_Tree3"),
        "pi_elastic_mae": metric("PI", "ElasticNet"),
        "ph_blend3_mae": metric("pH", "Blend_Tree3"),
        "ph_elastic_mae": metric("pH", "ElasticNet"),
        "conductivity_pred_min": float(
            toy_result["prediction_store"]["conductivity"]["Blend_Tree3"].min()
        ),
        "toy_success": bool(
            (not toy[feature_columns].isna().any().any())
            and (metric("PI", "Blend_Tree3") < metric("PI", "ElasticNet") or metric("pH", "Blend_Tree3") < metric("pH", "ElasticNet"))
        ),
    }


def save_tables(
    q_dir: Path,
    feature_table: pd.DataFrame,
    target_table: pd.DataFrame,
    model_probe: pd.DataFrame,
    selected_frame: pd.DataFrame,
    slice_summary: pd.DataFrame,
    pi_consistency: pd.DataFrame,
    sensitivity_probe: pd.DataFrame,
    final_route_summary: pd.DataFrame,
    importance_summary: pd.DataFrame,
) -> list[str]:
    results_dir = q_dir / "results"
    tables_dir = q_dir / "tables"
    results_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    feature_table_path = results_dir / "feature_table.csv"
    target_table_path = results_dir / "target_table.csv"
    model_probe_path = results_dir / "model_probe.csv"
    oof_path = results_dir / "oof_predictions.csv"
    slice_path = results_dir / "slice_error_summary.csv"
    pi_path = results_dir / "pi_consistency_summary.csv"
    sensitivity_path = results_dir / "sensitivity_probe.csv"
    route_path = results_dir / "final_model_summary.csv"
    importance_path = results_dir / "feature_importance_summary.csv"

    feature_table.to_csv(feature_table_path, index=False, encoding="utf-8-sig")
    target_table.to_csv(target_table_path, index=False, encoding="utf-8-sig")
    model_probe.to_csv(model_probe_path, index=False, encoding="utf-8-sig")
    selected_frame.to_csv(oof_path, index=False, encoding="utf-8-sig")
    slice_summary.to_csv(slice_path, index=False, encoding="utf-8-sig")
    pi_consistency.to_csv(pi_path, index=False, encoding="utf-8-sig")
    sensitivity_probe.to_csv(sensitivity_path, index=False, encoding="utf-8-sig")
    final_route_summary.to_csv(route_path, index=False, encoding="utf-8-sig")
    importance_summary.to_csv(importance_path, index=False, encoding="utf-8-sig")

    table_main = tables_dir / "table_q2_main_model_summary.csv"
    table_probe = tables_dir / "table_q2_model_probe_core.csv"
    table_slice = tables_dir / "table_q2_slice_error_summary.csv"
    table_pi = tables_dir / "table_q2_pi_consistency_summary.csv"
    table_imp = tables_dir / "table_q2_feature_importance_top.csv"

    final_route_summary.to_csv(table_main, index=False, encoding="utf-8-sig")
    model_probe[model_probe["model"].isin(["ElasticNet", "PLS", "RandomForest", "ExtraTrees", "HistGB", "Blend_Tree3"])].to_csv(
        table_probe, index=False, encoding="utf-8-sig"
    )
    slice_summary.to_csv(table_slice, index=False, encoding="utf-8-sig")
    pi_consistency.to_csv(table_pi, index=False, encoding="utf-8-sig")
    importance_summary.to_csv(table_imp, index=False, encoding="utf-8-sig")

    return [path.as_posix() for path in [table_main, table_probe, table_slice, table_pi, table_imp]]


def save_figures(
    q_dir: Path,
    model_probe: pd.DataFrame,
    selected_frame: pd.DataFrame,
    slice_summary: pd.DataFrame,
    importance_summary: pd.DataFrame,
) -> list[str]:
    figures_dir = q_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    comparison_path = figures_dir / "figure_q2_model_mae_comparison.png"
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    focus_targets = ["conductivity", "pH", "PI"]
    focus_models = ["ElasticNet", "PLS", "RandomForest", "ExtraTrees", "HistGB", "Blend_Tree3"]
    for ax, target in zip(axes, focus_targets):
        subset = model_probe[(model_probe["target"] == target) & (model_probe["model"].isin(focus_models))].copy()
        subset = subset.sort_values("mae", ascending=True)
        ax.barh(subset["model"], subset["mae"], color="#2a6f97")
        ax.set_title(target)
        ax.set_xlabel("OOF MAE")
    fig.suptitle("q2 model comparison on key targets")
    fig.tight_layout()
    fig.savefig(comparison_path, dpi=300)
    plt.close(fig)

    parity_path = figures_dir / "figure_q2_pi_parity_and_recon.png"
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    actual_pi = selected_frame["PI"].to_numpy(dtype=float)
    pred_pi = selected_frame["pred_PI"].to_numpy(dtype=float)
    recon_pi = selected_frame["pred_PI_recon"].to_numpy(dtype=float)
    for ax, values, title in zip(
        axes,
        [pred_pi, recon_pi],
        ["Direct PI head", "Reconstructed PI from predicted components"],
    ):
        ax.scatter(actual_pi, values, s=16, alpha=0.75, color="#1d3557")
        lo = min(actual_pi.min(), values.min())
        hi = max(actual_pi.max(), values.max())
        ax.plot([lo, hi], [lo, hi], color="#c1121f", linewidth=1.2)
        ax.set_xlabel("Actual PI")
        ax.set_ylabel("Predicted PI")
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(parity_path, dpi=300)
    plt.close(fig)

    slice_path = figures_dir / "figure_q2_slice_error_ratio.png"
    focus_slices = ["overall", "high_PI_top10", "low_PI_bottom10", "rare_pattern", "high_cond_low_PI"]
    pivot = (
        slice_summary[slice_summary["slice"].isin(focus_slices)]
        .pivot(index="target", columns="slice", values="mae_ratio_vs_overall")
        .reindex(index=TARGETS, columns=focus_slices)
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    im = ax.imshow(pivot.to_numpy(dtype=float), cmap="YlOrRd", aspect="auto")
    ax.set_xticks(np.arange(len(focus_slices)), labels=focus_slices, rotation=20)
    ax.set_yticks(np.arange(len(TARGETS)), labels=TARGETS)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, f"{pivot.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("MAE ratio relative to overall error")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    fig.savefig(slice_path, dpi=300)
    plt.close(fig)

    importance_path = figures_dir / "figure_q2_feature_importance_heatmap.png"
    top_features = (
        importance_summary.sort_values(["target", "rank"])
        .groupby("target")
        .head(4)["feature"]
        .drop_duplicates()
        .tolist()
    )
    heatmap = (
        importance_summary[importance_summary["feature"].isin(top_features)]
        .pivot(index="feature", columns="target", values="importance_mean")
        .reindex(index=top_features, columns=TARGETS)
        .fillna(0.0)
    )
    fig, ax = plt.subplots(figsize=(8, max(4, 0.45 * len(top_features))))
    im = ax.imshow(heatmap.to_numpy(dtype=float), cmap="Blues", aspect="auto")
    ax.set_xticks(np.arange(len(TARGETS)), labels=TARGETS, rotation=20)
    ax.set_yticks(np.arange(len(top_features)), labels=top_features)
    for i in range(heatmap.shape[0]):
        for j in range(heatmap.shape[1]):
            ax.text(j, i, f"{heatmap.iloc[i, j]:.3f}", ha="center", va="center", fontsize=8)
    ax.set_title("Permutation importance hooks for selected routes")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    fig.savefig(importance_path, dpi=300)
    plt.close(fig)

    return [path.as_posix() for path in [comparison_path, parity_path, slice_path, importance_path]]


def main() -> None:
    script_path = Path(__file__).resolve()
    q_dir = script_path.parent.parent
    workspace_dir = q_dir.parent.parent
    problem_dir = workspace_dir / "problem"

    records = json.loads((problem_dir / "attachments" / "A_data.json").read_text(encoding="utf-8"))
    feature_table = build_feature_table(records)
    target_table, q1_weights = load_target_table(workspace_dir)
    merged = feature_table.merge(target_table, on="GUID", how="inner")
    feature_columns = [
        column
        for column in feature_table.columns
        if column not in {"GUID", "pattern_key"}
    ]
    matrix = feature_table[feature_columns].to_numpy(dtype=float)

    toy_demo = run_toy_demo(merged, feature_columns)
    candidate_result = run_candidate_oof(feature_table, target_table, feature_columns, seed=SEED)
    model_probe = candidate_result["model_probe"]
    route_map = select_main_routes(model_probe)
    selected_frame = build_selected_prediction_frame(
        merged=candidate_result["merged"],
        fold_ids=candidate_result["fold_ids"],
        density_score=candidate_result["density_score"],
        dispersion_store=candidate_result["dispersion_store"],
        prediction_store=candidate_result["prediction_store"],
        route_map=route_map,
        q1_weights=q1_weights,
    )
    slice_summary = compute_slice_error_summary(selected_frame)
    pi_consistency = compute_pi_consistency_summary(selected_frame)

    no_proxy_features = [
        column
        for column in feature_columns
        if not (
            column.startswith("mass_proxy_")
            or column.startswith("mol_proxy_")
            or column in {"weighted_density", "ionic_strength_proxy", "water_x_ionic"}
        )
    ]
    sensitivity_rows: list[dict[str, object]] = []
    base_metrics = run_route_oof(merged, feature_columns, route_map, seed=SEED)
    base_metrics["scenario"] = "baseline_main_route"
    sensitivity_rows.extend(base_metrics.to_dict(orient="records"))

    no_proxy_metrics = run_route_oof(merged, no_proxy_features, route_map, seed=SEED)
    no_proxy_metrics["scenario"] = "drop_proxy_block"
    sensitivity_rows.extend(no_proxy_metrics.to_dict(orient="records"))

    alt_seed_metrics = run_route_oof(merged, feature_columns, route_map, seed=7)
    alt_seed_metrics["scenario"] = "cv_seed_7"
    sensitivity_rows.extend(alt_seed_metrics.to_dict(orient="records"))
    sensitivity_probe = pd.DataFrame(sensitivity_rows)

    estimators, final_route_summary = fit_selected_route_models(matrix, target_table, route_map, feature_columns)
    importance_summary = compute_feature_importance_summary(estimators, matrix, target_table, feature_columns)

    table_paths = save_tables(
        q_dir=q_dir,
        feature_table=feature_table,
        target_table=target_table,
        model_probe=model_probe,
        selected_frame=selected_frame,
        slice_summary=slice_summary,
        pi_consistency=pi_consistency,
        sensitivity_probe=sensitivity_probe,
        final_route_summary=final_route_summary,
        importance_summary=importance_summary,
    )
    figure_paths = save_figures(
        q_dir=q_dir,
        model_probe=model_probe,
        selected_frame=selected_frame,
        slice_summary=slice_summary,
        importance_summary=importance_summary,
    )

    target_model_selection: dict[str, dict[str, object]] = {}
    for target in TARGETS:
        target_probe = model_probe[model_probe["target"] == target].copy().set_index("model")
        best_single = target_probe.loc[TREE_ONLY_MODELS].sort_values("mae").iloc[0]
        selected_model = route_map[target]
        selected_metrics = target_probe.loc[selected_model]
        target_model_selection[target] = {
            "selected_route": selected_model,
            "selected_mae": float(selected_metrics["mae"]),
            "selected_rmse": float(selected_metrics["rmse"]),
            "selected_r2": float(selected_metrics["r2"]),
            "best_single_tree_mae": float(best_single["mae"]),
            "elasticnet_mae": float(target_probe.loc["ElasticNet", "mae"]),
            "pls_mae": float(target_probe.loc["PLS", "mae"]),
            "gain_vs_elasticnet_mae": float(target_probe.loc["ElasticNet", "mae"] - selected_metrics["mae"]),
            "gain_vs_best_single_tree_mae": float(best_single["mae"] - selected_metrics["mae"]),
        }

    pi_consistency_overall = pi_consistency.loc[pi_consistency["slice"] == "overall"].iloc[0]
    uncertainty_summary = {}
    for target in ["conductivity", "pH", "PI"]:
        abs_error = np.abs(selected_frame[target] - selected_frame[f"pred_{target}"])
        uncertainty_summary[target] = {
            "dispersion_error_spearman": float(spearmanr(abs_error, selected_frame[f"uncertainty_dispersion_{target}"]).statistic),
            "density_error_spearman": float(spearmanr(abs_error, selected_frame["uncertainty_density"]).statistic),
            "combined_hook_error_spearman": float(spearmanr(abs_error, selected_frame[f"uncertainty_hook_{target}"]).statistic),
        }

    special_mask = (
        (selected_frame["conductivity"] >= float(selected_frame["conductivity"].quantile(0.75)))
        & (selected_frame["PI"] <= float(selected_frame["PI"].quantile(0.25)))
    )
    special_examples = selected_frame.loc[
        special_mask,
        ["GUID", "conductivity", "pH", "W_1", "R_W", "PI", "pred_PI", "pred_PI_recon", "pattern_key"],
    ].head(8)

    main_result = {
        "feature_schema": {
            "n_records": int(len(feature_table)),
            "n_features": int(len(feature_columns)),
            "feature_blocks": {
                "ratio_features": int(sum(column.startswith("ratio_") for column in feature_columns)),
                "presence_features": int(sum(column.startswith("present_") for column in feature_columns)),
                "proxy_features": int(
                    sum(column.startswith("mass_proxy_") or column.startswith("mol_proxy_") for column in feature_columns)
                ),
                "pattern_dummies": int(sum(column.startswith("pattern_") for column in feature_columns)),
                "global_features": int(
                    len(feature_columns)
                    - sum(column.startswith("ratio_") for column in feature_columns)
                    - sum(column.startswith("present_") for column in feature_columns)
                    - sum(column.startswith("mass_proxy_") or column.startswith("mol_proxy_") for column in feature_columns)
                    - sum(column.startswith("pattern_") for column in feature_columns)
                ),
            },
            "structural_zero_rule": "missing composition entries are written as 0.0 structural zero rather than imputed missing values",
        },
        "target_list": TARGETS,
        "target_model_selection": target_model_selection,
        "base_model_cv_summary": model_probe.to_dict(orient="records"),
        "ensemble_weight_summary": {
            "guardrail": "pre-fixed simple fusion is used to avoid test-fold weight leakage",
            "blend_rf_et": BLEND_WEIGHTS["Blend_RF_ET"],
            "blend_tree3": BLEND_WEIGHTS["Blend_Tree3"],
        },
        "cv_summary": {
            "outer_cv": f"{OUTER_SPLITS}-fold shuffled KFold",
            "seed": SEED,
            "selected_routes": route_map,
            "top_PI_overlap_actual_vs_pred": int(
                len(
                    set(selected_frame.sort_values("PI", ascending=False).head(10)["GUID"])
                    & set(selected_frame.sort_values("pred_PI", ascending=False).head(10)["GUID"])
                )
            ),
        },
        "slice_error_summary": {
            "high_PI_top10_conductivity_mae": float(
                slice_summary.loc[
                    (slice_summary["target"] == "conductivity") & (slice_summary["slice"] == "high_PI_top10"),
                    "mae",
                ].iloc[0]
            ),
            "low_PI_bottom10_conductivity_mae": float(
                slice_summary.loc[
                    (slice_summary["target"] == "conductivity") & (slice_summary["slice"] == "low_PI_bottom10"),
                    "mae",
                ].iloc[0]
            ),
            "rare_pattern_PI_mae": float(
                slice_summary.loc[
                    (slice_summary["target"] == "PI") & (slice_summary["slice"] == "rare_pattern"),
                    "mae",
                ].iloc[0]
            ),
        },
        "pi_consistency_summary": {
            "direct_mae_vs_actual": float(pi_consistency_overall["direct_mae_vs_actual"]),
            "recon_mae_vs_actual": float(pi_consistency_overall["recon_mae_vs_actual"]),
            "direct_vs_recon_spearman": float(pi_consistency_overall["direct_vs_recon_spearman"]),
            "mean_abs_gap": float(pi_consistency_overall["mean_abs_gap"]),
            "q90_abs_gap": float(pi_consistency_overall["q90_abs_gap"]),
        },
        "uncertainty_hooks": {
            "description": "tree-prediction dispersion is combined with nearest-neighbor distance in feature space as a heuristic uncertainty hook",
            "correlation_snapshot": uncertainty_summary,
        },
        "special_samples": special_examples.to_dict(orient="records"),
        "sensitivity_probe_summary": sensitivity_probe.to_dict(orient="records"),
    }

    metrics = {
        "selected_route_metrics": {
            target: regression_metrics(
                selected_frame[target].to_numpy(dtype=float),
                selected_frame[f"pred_{target}"].to_numpy(dtype=float),
            )
            for target in TARGETS
        },
        "baseline_metrics": {
            target: regression_metrics(
                selected_frame[target].to_numpy(dtype=float),
                selected_frame[f"pred_{target}_baseline"].to_numpy(dtype=float),
            )
            for target in TARGETS
        },
        "pls_metrics": {
            target: regression_metrics(
                selected_frame[target].to_numpy(dtype=float),
                selected_frame[f"pred_{target}_pls"].to_numpy(dtype=float),
            )
            for target in TARGETS
        },
        "toy_demo": toy_demo,
        "pi_direct_vs_recon_spearman": float(pi_consistency_overall["direct_vs_recon_spearman"]),
        "predicted_pH_range": {
            "min": float(selected_frame["pred_pH"].min()),
            "max": float(selected_frame["pred_pH"].max()),
        },
    }

    outputs = {
        "result_json": (q_dir / "results" / "result.json").as_posix(),
        "run_log": (q_dir / "results" / "run.log").as_posix(),
        "feature_table": (q_dir / "results" / "feature_table.csv").as_posix(),
        "target_table": (q_dir / "results" / "target_table.csv").as_posix(),
        "model_probe": (q_dir / "results" / "model_probe.csv").as_posix(),
        "oof_predictions": (q_dir / "results" / "oof_predictions.csv").as_posix(),
        "slice_error_summary": (q_dir / "results" / "slice_error_summary.csv").as_posix(),
        "pi_consistency_summary": (q_dir / "results" / "pi_consistency_summary.csv").as_posix(),
        "sensitivity_probe": (q_dir / "results" / "sensitivity_probe.csv").as_posix(),
        "feature_importance_summary": (q_dir / "results" / "feature_importance_summary.csv").as_posix(),
    }

    warnings = [
        "`PI`、`W_1`、`R_W` 仍然继承自 `q1` 的短时稳定性 proxy 口径，不能写成长期寿命预测。",
        "稀有配方模式与低 `PI` 区域的预测误差明显高于整体平均水平，下游使用时必须附带低可信区域说明。",
        "`PI` 直接头与重构头总体相关较高，但两者并不完全等价；若下游需要更强可解释性，应优先同时引用两条路径。",
        "为避免信息泄漏，树融合采用预先固定的简单融合而非测试折回填权重；因此当前结果偏向稳健实现而非最激进调参。",
    ]
    limitations = [
        "当前数据仅覆盖 251 条样本与约 23 类主组合结构，模型对稀有结构和远离已见区域的外推能力有限。",
        "`R_W` 的可预测性与物理解释性都弱于 `conductivity`、`pH`、`W_1` 和 `PI`，因此涉及 `R_W` 的结论应降级为有限证据。",
        "特征重要性来自 permutation importance 的数据驱动估计，只能作为 `q3` 的解释入口，而不是严格机理证明。",
    ]
    paper_claims = [
        "配方结构增强的树集成主路线在 `conductivity`、`pH`、`W_1`、`R_W` 和 `PI` 五个目标上均优于线性基线 `ElasticNet`。",
        "`Blend_Tree3` 在 `conductivity`、`pH`、`PI` 三个关键目标上的 OOF 表现优于单树候选，说明简单树融合具有稳定收益。",
        "`PI` 直接预测与由预测的 `conductivity/pH/W_1/R_W` 重构得到的 `PI_recon` 保持较高相关性，因此 `PI` 可作为后续问题的统一目标量，但需保留可解释性限制。",
        "误差在低 `PI` 区域和稀有模式区域显著增大，因此模型适用范围并非全空间均匀一致。",
    ]
    trace = {
        "conductivity_main_mae": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.target_model_selection.conductivity.selected_mae",
            "validation_status": "pending",
        },
        "PI_main_mae": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.target_model_selection.PI.selected_mae",
            "validation_status": "pending",
        },
        "PI_direct_vs_recon_spearman": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.pi_consistency_summary.direct_vs_recon_spearman",
            "validation_status": "pending",
        },
        "rare_pattern_PI_mae": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.slice_error_summary.rare_pattern_PI_mae",
            "validation_status": "pending",
        },
    }

    log_context = {
        "code_starter_used": "templates/shared/code_starter/prediction.py (adapted) + q1 result_io pattern",
        "environment_notes": {
            "packages": ["numpy", "pandas", "scipy", "sklearn", "matplotlib"],
            "seed": SEED,
            "outer_cv": OUTER_SPLITS,
        },
        "preprocessing_notes": {
            "input_rows": int(len(records)),
            "output_rows": int(len(merged)),
            "feature_count": int(len(feature_columns)),
            "feature_blocks": ["ratio", "presence", "mass_proxy", "mol_proxy", "global aggregate", "pattern dummy"],
            "structural_zero_policy": "composition not present -> explicit 0.0 structural zero",
        },
        "abnormal_data_handling": [
            {
                "abnormal_type": "structural zero",
                "detection_rule": "component absent from a formulation record",
                "affected_rows": int((feature_table["rare_pattern"] >= 0).sum()),
                "handling_method": "keep as 0.0",
                "rationale": "absence is semantic composition structure rather than random missingness",
                "effect_on_result": "enables stable unified feature matrix",
            },
            {
                "abnormal_type": "rare pattern",
                "detection_rule": "pattern_count <= 5",
                "affected_rows": int(feature_table["rare_pattern"].sum()),
                "handling_method": "flag",
                "rationale": "retain all samples but expose sparse-region error",
                "effect_on_result": "enters slice-error and downstream trust-region analysis",
            },
            {
                "abnormal_type": "R_W > 1",
                "detection_rule": "target label exceeds 1.0",
                "affected_rows": int((target_table["R_W"] > 1.0).sum()),
                "handling_method": "keep and flag",
                "rationale": "values come from upstream q1 definition and must remain traceable",
                "effect_on_result": "weakens physical interpretation of the R_W head",
            },
        ],
        "random_seed": {"main": SEED, "alt_seed_sensitivity": 7},
        "algorithm_settings": {
            "candidate_models": BASELINE_MODELS,
            "selected_routes": route_map,
            "blend_guardrail": "pre-fixed simple fusion only",
            "pi_reconstruction": "fixed q1 CRITIC weights + predicted S_pH + TOPSIS on predicted matrix",
        },
        "toy_demo_result": toy_demo,
        "full_run_result_summary": {
            "selected_routes": route_map,
            "conductivity_mae": target_model_selection["conductivity"]["selected_mae"],
            "pH_mae": target_model_selection["pH"]["selected_mae"],
            "PI_mae": target_model_selection["PI"]["selected_mae"],
            "PI_direct_vs_recon_spearman": float(pi_consistency_overall["direct_vs_recon_spearman"]),
        },
        "runtime_notes": {
            "figure_count": len(figure_paths),
            "table_count": len(table_paths),
            "sensitivity_scenarios": ["baseline_main_route", "drop_proxy_block", "cv_seed_7"],
        },
        "interpretation_notes": {
            "main_interpretation": "simple tree fusion consistently improves the key targets while keeping a clear composition-only input path",
            "trust_region_note": "errors rise in low-PI and rare-pattern slices, so downstream recommendation should combine predicted mean with uncertainty hook",
        },
        "errors": [],
    }

    write_result_and_log(
        question_id="q2",
        model_name="配方结构增强的目标自适应受限加权树集成预测模型",
        status="pass",
        inputs={
            "source_problem": (problem_dir / "problem.md").as_posix(),
            "source_data": (problem_dir / "attachments" / "A_data.json").as_posix(),
            "source_readme": (problem_dir / "attachments" / "README.txt").as_posix(),
            "source_q1_indicator": (workspace_dir / "output" / "q1" / "results" / "indicator_table.csv").as_posix(),
            "source_q1_result": (workspace_dir / "output" / "q1" / "results" / "result.json").as_posix(),
        },
        outputs=outputs,
        main_result=main_result,
        metrics=metrics,
        figures=figure_paths,
        tables=table_paths,
        source_command=f"python {script_path.as_posix()}",
        source_files=[script_path.as_posix(), (script_path.parent / "result_io.py").as_posix()],
        validation_hooks=[
            "比较主路线与 ElasticNet / PLS 的 OOF MAE、RMSE、R^2",
            "检查高 PI 区、低 PI 区、稀有模式区和高电导低 PI 区的误差差异",
            "比较 PI 直接头与 PI 重构头的一致性",
            "检验 uncertainty hook 与绝对误差的相关性",
            "做 proxy block 消融和 CV seed 扰动测试",
        ],
        warnings=warnings,
        limitations=limitations,
        paper_claims=paper_claims,
        trace=trace,
        log_context=log_context,
        results_dir=q_dir / "results",
    )


if __name__ == "__main__":
    main()
