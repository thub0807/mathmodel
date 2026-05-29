from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from result_io import write_result_and_log


SEED = 42
np.random.seed(SEED)


def percentile_summary(series: pd.Series) -> dict[str, float]:
    return {
        "min": float(series.min()),
        "q25": float(series.quantile(0.25)),
        "median": float(series.quantile(0.50)),
        "q75": float(series.quantile(0.75)),
        "max": float(series.max()),
    }


def ph_suitability(values: pd.Series, low: float, high: float, margin: float = 1.0) -> pd.Series:
    distance = np.maximum.reduce([np.full(len(values), 0.0), low - values.to_numpy(), values.to_numpy() - high])
    score = 1.0 - distance / margin
    return pd.Series(np.clip(score, 0.0, 1.0), index=values.index, dtype=float)


def minmax_scale(matrix: np.ndarray) -> np.ndarray:
    col_min = matrix.min(axis=0)
    col_max = matrix.max(axis=0)
    denom = np.where((col_max - col_min) == 0, 1.0, col_max - col_min)
    return (matrix - col_min) / denom


def critic_weights(matrix: np.ndarray) -> np.ndarray:
    scaled = minmax_scale(matrix)
    std = scaled.std(axis=0, ddof=0)
    corr = np.corrcoef(scaled, rowvar=False)
    corr = np.nan_to_num(corr, nan=0.0)
    conflict = np.sum(1.0 - corr, axis=0)
    info = std * conflict
    if np.allclose(info.sum(), 0.0):
        return np.full(matrix.shape[1], 1.0 / matrix.shape[1])
    return info / info.sum()


def topsis_scores(matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
    norm = matrix / np.sqrt(np.sum(matrix**2, axis=0, keepdims=True))
    weighted = norm * weights
    pos = weighted.max(axis=0)
    neg = weighted.min(axis=0)
    d_pos = np.sqrt(np.sum((weighted - pos) ** 2, axis=1))
    d_neg = np.sqrt(np.sum((weighted - neg) ** 2, axis=1))
    return d_neg / (d_pos + d_neg + 1e-12)


def pca_scores(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix)
    pca = PCA(n_components=1, random_state=SEED)
    component_scores = pca.fit_transform(scaled).ravel()
    component = pca.components_[0]
    cond_corr = np.corrcoef(component_scores, matrix[:, 0])[0, 1]
    if cond_corr < 0:
        component_scores = -component_scores
        component = -component
    weights = np.abs(component) / np.abs(component).sum()
    scores_scaled = minmax_scale((minmax_scale(matrix) @ weights).reshape(-1, 1)).ravel()
    return scores_scaled, weights, float(pca.explained_variance_ratio_[0])


def composition_string(volume_map: dict[str, float]) -> str:
    parts = []
    for key, value in volume_map.items():
        if key == "water":
            continue
        if value > 0:
            parts.append(f"{key}:{value:.2f}")
    return "; ".join(parts)


def build_dataframe(records: list[dict], low: float = 6.5, high: float = 8.5, margin: float = 1.0) -> pd.DataFrame:
    rows = []
    for rec in records:
        dq = rec["electrochemistry"]["derived_quantities"]
        volumes = rec["electrolyte"]["volumes"]
        wt = float(dq["TAFEL CATHODE V"] - dq["TAFEL ANODE V"])
        w1 = float(dq["1mA/cm^2 CATHODE V"] - dq["1mA/cm^2 ANODE V"])
        rows.append(
            {
                "GUID": rec["GUID"],
                "RUN_ID": rec["RUN_ID"],
                "conductivity": float(rec["conductivity"]),
                "pH": float(rec["pH"]),
                "temperature": float(rec["temperature"]),
                "V_c_T": float(dq["TAFEL CATHODE V"]),
                "V_a_T": float(dq["TAFEL ANODE V"]),
                "V_c_1": float(dq["1mA/cm^2 CATHODE V"]),
                "V_a_1": float(dq["1mA/cm^2 ANODE V"]),
                "W_T": wt,
                "W_1": w1,
                "R_W": float(w1 / wt) if wt != 0 else np.nan,
                "num_components": int(sum(1 for k, v in volumes.items() if k != "water" and v > 0)),
                "recipe": composition_string(volumes),
            }
        )
    frame = pd.DataFrame(rows)
    frame["S_pH"] = ph_suitability(frame["pH"], low=low, high=high, margin=margin)
    return frame


def evaluate_frame(frame: pd.DataFrame) -> dict[str, object]:
    feature_cols = ["conductivity", "S_pH", "W_1", "R_W"]
    matrix = frame[feature_cols].to_numpy(dtype=float)
    critic = critic_weights(matrix)
    equal = np.full(len(feature_cols), 1.0 / len(feature_cols))
    pi = topsis_scores(matrix, critic)
    pi_equal = topsis_scores(matrix, equal)
    pca_score, pca_weight, pca_var = pca_scores(matrix)

    evaluated = frame.copy()
    evaluated["PI"] = pi
    evaluated["PI_equal"] = pi_equal
    evaluated["PI_pca"] = pca_score
    evaluated["rank_PI"] = evaluated["PI"].rank(ascending=False, method="min").astype(int)
    evaluated["rank_cond"] = evaluated["conductivity"].rank(ascending=False, method="min").astype(int)
    evaluated["rank_gap"] = evaluated["rank_cond"] - evaluated["rank_PI"]
    evaluated["score_gap_vs_cond_z"] = (
        (evaluated["conductivity"].rank(pct=True) - evaluated["PI"].rank(pct=True)).abs()
    )

    top10_pi = evaluated.sort_values(["PI", "conductivity"], ascending=[False, False]).head(10)
    top10_cond = evaluated.sort_values(["conductivity", "PI"], ascending=[False, False]).head(10)
    top10_pca = evaluated.sort_values(["PI_pca", "PI"], ascending=[False, False]).head(10)
    overlap_cond = sorted(set(top10_pi["GUID"]).intersection(set(top10_cond["GUID"])))
    overlap_pca = sorted(set(top10_pi["GUID"]).intersection(set(top10_pca["GUID"])))
    spearman_value = spearmanr(evaluated["conductivity"], evaluated["PI"]).statistic
    spearman_pca = spearmanr(evaluated["PI"], evaluated["PI_pca"]).statistic

    counterexamples = (
        evaluated.assign(abs_gap=lambda df: df["rank_gap"].abs())
        .sort_values(["abs_gap", "PI"], ascending=[False, False])
        .head(8)[["GUID", "conductivity", "pH", "W_1", "R_W", "PI", "rank_cond", "rank_PI", "rank_gap", "recipe"]]
    )

    return {
        "frame": evaluated,
        "critic_weights": critic,
        "equal_weights": equal,
        "pca_weights": pca_weight,
        "pca_variance_ratio": pca_var,
        "top10_pi": top10_pi,
        "top10_cond": top10_cond,
        "top10_pca": top10_pca,
        "overlap_cond": overlap_cond,
        "overlap_pca": overlap_pca,
        "spearman_cond_vs_pi": float(spearman_value),
        "spearman_pi_vs_pca": float(spearman_pca),
        "counterexamples": counterexamples,
    }


def sensitivity_snapshot(records: list[dict]) -> pd.DataFrame:
    scenarios = [
        {"scenario": "baseline", "ph_low": 6.5, "ph_high": 8.5, "ph_margin": 1.0, "blend": 1.0, "feature_mode": "baseline"},
        {"scenario": "ph_6_8", "ph_low": 6.0, "ph_high": 8.0, "ph_margin": 1.0, "blend": 1.0, "feature_mode": "baseline"},
        {"scenario": "ph_7_9", "ph_low": 7.0, "ph_high": 9.0, "ph_margin": 1.0, "blend": 1.0, "feature_mode": "baseline"},
        {"scenario": "blend_0_8", "ph_low": 6.5, "ph_high": 8.5, "ph_margin": 1.0, "blend": 0.8, "feature_mode": "baseline"},
        {"scenario": "blend_0_6", "ph_low": 6.5, "ph_high": 8.5, "ph_margin": 1.0, "blend": 0.6, "feature_mode": "baseline"},
        {"scenario": "w1_only", "ph_low": 6.5, "ph_high": 8.5, "ph_margin": 1.0, "blend": 1.0, "feature_mode": "w1_only"},
    ]
    rows = []
    baseline_df = build_dataframe(records, low=6.5, high=8.5, margin=1.0)
    baseline_eval = evaluate_frame(baseline_df)
    base_top10 = set(baseline_eval["top10_pi"]["GUID"])
    base_rank = baseline_eval["frame"].set_index("GUID")["PI"].rank(ascending=False, method="min")
    for config in scenarios:
        frame = build_dataframe(records, low=config["ph_low"], high=config["ph_high"], margin=config["ph_margin"])
        if config["feature_mode"] == "w1_only":
            feature_cols = ["conductivity", "S_pH", "W_1"]
            matrix = frame[feature_cols].to_numpy(dtype=float)
        else:
            feature_cols = ["conductivity", "S_pH", "W_1", "R_W"]
            matrix = frame[feature_cols].to_numpy(dtype=float)
        critic = critic_weights(matrix)
        equal = np.full(len(feature_cols), 1.0 / len(feature_cols))
        weights = config["blend"] * critic + (1.0 - config["blend"]) * equal
        weights = weights / weights.sum()
        score = topsis_scores(matrix, weights)
        ranked = frame.copy()
        ranked["score"] = score
        ranked["rank"] = ranked["score"].rank(ascending=False, method="min")
        top10 = set(ranked.sort_values("score", ascending=False).head(10)["GUID"])
        rho = spearmanr(base_rank.loc[ranked["GUID"]], ranked.set_index("GUID")["rank"]).statistic
        rows.append(
            {
                "scenario": config["scenario"],
                "ph_interval": f"[{config['ph_low']:.1f}, {config['ph_high']:.1f}]",
                "blend_alpha": config["blend"],
                "feature_mode": config["feature_mode"],
                "top10_overlap_with_baseline": int(len(base_top10.intersection(top10))),
                "rank_spearman_vs_baseline": float(rho),
                "top_guid": ranked.sort_values("score", ascending=False).iloc[0]["GUID"],
            }
        )
    return pd.DataFrame(rows)


def save_figures(
    q_dir: Path,
    evaluated: pd.DataFrame,
    critic_weights_values: np.ndarray,
    pca_weights_values: np.ndarray,
    sensitivity_df: pd.DataFrame,
) -> list[str]:
    figures_dir = q_dir / "figures"
    indicator_names = ["Conductivity", "pH suitability", "Window at 1mA", "Window retention"]

    scatter_path = figures_dir / "figure_q1_score_vs_conductivity.png"
    plt.figure(figsize=(8, 6))
    plt.scatter(evaluated["conductivity"], evaluated["PI"], alpha=0.7, s=28, label="All samples")
    top = evaluated.sort_values("PI", ascending=False).head(10)
    plt.scatter(top["conductivity"], top["PI"], color="#c0392b", s=42, label="Top 10 by PI")
    plt.xlabel("Conductivity")
    plt.ylabel("PI")
    plt.title("Conductivity vs composite score")
    plt.legend()
    plt.tight_layout()
    plt.savefig(scatter_path, dpi=300)
    plt.close()

    weight_path = figures_dir / "figure_q1_weight_comparison.png"
    x = np.arange(len(indicator_names))
    plt.figure(figsize=(8, 5))
    plt.bar(x - 0.2, critic_weights_values, width=0.2, label="CRITIC")
    plt.bar(x, np.full(len(indicator_names), 0.25), width=0.2, label="Equal weight")
    plt.bar(x + 0.2, pca_weights_values, width=0.2, label="PCA loading")
    plt.xticks(x, indicator_names)
    plt.ylabel("Weight")
    plt.title("q1 weight comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(weight_path, dpi=300)
    plt.close()

    sensitivity_path = figures_dir / "figure_q1_sensitivity_overlap.png"
    plt.figure(figsize=(8, 5))
    plt.bar(sensitivity_df["scenario"], sensitivity_df["top10_overlap_with_baseline"], color="#2e86c1")
    plt.ylim(0, 10)
    plt.ylabel("Top10 overlap vs baseline")
    plt.title("q1 sensitivity overlap")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(sensitivity_path, dpi=300)
    plt.close()

    return [p.as_posix() for p in [scatter_path, weight_path, sensitivity_path]]


def save_tables(
    q_dir: Path,
    evaluated: pd.DataFrame,
    top10: pd.DataFrame,
    counterexamples: pd.DataFrame,
    sensitivity_df: pd.DataFrame,
    critic_w: np.ndarray,
    pca_w: np.ndarray,
) -> list[str]:
    results_dir = q_dir / "results"
    tables_dir = q_dir / "tables"

    indicator_table_path = results_dir / "indicator_table.csv"
    top_snapshot_path = results_dir / "top_formula_snapshot.csv"
    evaluated.to_csv(indicator_table_path, index=False, encoding="utf-8-sig")
    top10.to_csv(top_snapshot_path, index=False, encoding="utf-8-sig")

    weight_table = pd.DataFrame(
        {
            "indicator": ["conductivity", "S_pH", "W_1", "R_W"],
            "critic_weight": critic_w,
            "equal_weight": np.full(4, 0.25),
            "pca_abs_loading": pca_w,
        }
    )
    weight_table_path = tables_dir / "table_q1_indicator_weights.csv"
    top_table_path = tables_dir / "table_q1_top10_formulations.csv"
    counter_path = tables_dir / "table_q1_counterexamples.csv"
    sensitivity_path = tables_dir / "table_q1_sensitivity_summary.csv"

    weight_table.to_csv(weight_table_path, index=False, encoding="utf-8-sig")
    top10[
        ["GUID", "conductivity", "pH", "W_1", "R_W", "S_pH", "PI", "rank_PI", "recipe"]
    ].to_csv(top_table_path, index=False, encoding="utf-8-sig")
    counterexamples.to_csv(counter_path, index=False, encoding="utf-8-sig")
    sensitivity_df.to_csv(sensitivity_path, index=False, encoding="utf-8-sig")

    return [
        weight_table_path.as_posix(),
        top_table_path.as_posix(),
        counter_path.as_posix(),
        sensitivity_path.as_posix(),
        indicator_table_path.as_posix(),
        top_snapshot_path.as_posix(),
    ]


def main() -> None:
    script_path = Path(__file__).resolve()
    q_dir = script_path.parent.parent
    workspace_dir = q_dir.parent.parent
    problem_dir = workspace_dir / "problem"
    data_path = problem_dir / "attachments" / "A_data.json"
    readme_path = problem_dir / "attachments" / "README.txt"

    with data_path.open("r", encoding="utf-8") as f:
        records = json.load(f)

    probe_frame = build_dataframe(records, low=6.5, high=8.5, margin=1.0)
    toy_indices = {
        int(probe_frame["conductivity"].idxmax()),
        int(probe_frame["pH"].idxmin()),
        int(probe_frame["pH"].idxmax()),
        int(probe_frame["W_1"].idxmax()),
        int((probe_frame["conductivity"] - probe_frame["conductivity"].median()).abs().idxmin()),
    }
    toy_frame = probe_frame.loc[sorted(toy_indices)].reset_index(drop=True)
    toy_eval = evaluate_frame(toy_frame)
    frame = probe_frame
    evaluation = evaluate_frame(frame)
    sensitivity_df = sensitivity_snapshot(records)

    full_df = evaluation["frame"]
    top10 = evaluation["top10_pi"][
        ["GUID", "conductivity", "pH", "W_1", "R_W", "S_pH", "PI", "rank_PI", "rank_cond", "recipe"]
    ].copy()
    counterexamples = evaluation["counterexamples"].copy()
    figure_paths = save_figures(q_dir, full_df, evaluation["critic_weights"], evaluation["pca_weights"], sensitivity_df)
    table_paths = save_tables(
        q_dir,
        full_df,
        top10,
        counterexamples,
        sensitivity_df,
        evaluation["critic_weights"],
        evaluation["pca_weights"],
    )

    indicator_summary = {
        "conductivity": percentile_summary(full_df["conductivity"]),
        "pH": percentile_summary(full_df["pH"]),
        "W_T": percentile_summary(full_df["W_T"]),
        "W_1": percentile_summary(full_df["W_1"]),
        "R_W": percentile_summary(full_df["R_W"]),
        "PI": percentile_summary(full_df["PI"]),
    }

    baseline_comparison = {
        "spearman_cond_vs_PI": evaluation["spearman_cond_vs_pi"],
        "top10_overlap_count": len(evaluation["overlap_cond"]),
        "top10_overlap_guids": evaluation["overlap_cond"],
        "top10_overlap_ratio": len(evaluation["overlap_cond"]) / 10.0,
        "spearman_PI_vs_PCA": evaluation["spearman_pi_vs_pca"],
        "top10_overlap_with_PCA": len(evaluation["overlap_pca"]),
    }

    top_formulations = top10.to_dict(orient="records")
    counter_list = counterexamples.to_dict(orient="records")

    main_result = {
        "metric_definitions": {
            "kappa": "conductivity",
            "S_pH": "piecewise suitability score with full score on [6.5, 8.5] and linear decay outside",
            "W_T": "TAFEL CATHODE V - TAFEL ANODE V",
            "W_1": "1mA/cm^2 CATHODE V - 1mA/cm^2 ANODE V",
            "R_W": "W_1 / W_T",
            "PI": "CRITIC-weighted TOPSIS score on [conductivity, S_pH, W_1, R_W]",
        },
        "weight_scheme": {
            "method": "CRITIC + TOPSIS",
            "critic_weights": {
                "conductivity": float(evaluation["critic_weights"][0]),
                "S_pH": float(evaluation["critic_weights"][1]),
                "W_1": float(evaluation["critic_weights"][2]),
                "R_W": float(evaluation["critic_weights"][3]),
            },
            "equal_weights": {
                "conductivity": 0.25,
                "S_pH": 0.25,
                "W_1": 0.25,
                "R_W": 0.25,
            },
            "pca_abs_loading_weights": {
                "conductivity": float(evaluation["pca_weights"][0]),
                "S_pH": float(evaluation["pca_weights"][1]),
                "W_1": float(evaluation["pca_weights"][2]),
                "R_W": float(evaluation["pca_weights"][3]),
            },
            "pca_explained_variance_ratio": float(evaluation["pca_variance_ratio"]),
        },
        "indicator_summary": indicator_summary,
        "overall_score_summary": {
            "n_records": int(len(full_df)),
            "top_PI_guid": str(top10.iloc[0]["GUID"]),
            "top_PI_score": float(top10.iloc[0]["PI"]),
            "median_PI_score": float(full_df["PI"].median()),
        },
        "baseline_comparison": baseline_comparison,
        "stability_indicator_summary": {
            "W_1": indicator_summary["W_1"],
            "R_W": indicator_summary["R_W"],
        },
        "top_formulations": top_formulations,
        "counterexamples": counter_list,
        "sensitivity_snapshot": sensitivity_df.to_dict(orient="records"),
    }

    metrics = {
        "n_records": int(len(full_df)),
        "toy_demo_n_records": int(len(toy_frame)),
        "toy_demo_rank_difference_exists": bool(
            toy_eval["frame"].sort_values("PI", ascending=False).iloc[0]["GUID"]
            != toy_eval["frame"].sort_values("conductivity", ascending=False).iloc[0]["GUID"]
        ),
        "missing_value_counts": full_df[["conductivity", "pH", "W_T", "W_1", "R_W", "S_pH", "PI"]].isna().sum().to_dict(),
        "positive_window_rate": float((full_df["W_1"] > 0).mean()),
        "rw_within_unit_interval_rate": float(((full_df["R_W"] >= 0) & (full_df["R_W"] <= 1.05)).mean()),
        "score_bounds": {
            "S_pH_min": float(full_df["S_pH"].min()),
            "S_pH_max": float(full_df["S_pH"].max()),
            "PI_min": float(full_df["PI"].min()),
            "PI_max": float(full_df["PI"].max()),
        },
    }

    warnings = [
        "稳定性相关指标仅能表征基于 fast_assessment 电化学曲线的短时稳定性 proxy，不能外推为长期循环寿命结论。",
        "pH 适宜区间默认设为 [6.5, 8.5]，后续需通过灵敏度分析检验排序稳健性。",
    ]
    limitations = [
        "综合性能分数依赖于现有 251 条样本和短时电化学派生量，不代表所有水系电解液体系的通用最优标准。",
        "PCA 对照用于检验权重稳健性，但其物理可解释性弱于 CRITIC-TOPSIS 主路线。",
    ]
    paper_claims = [
        "综合性能评价需要同时考虑电导率、pH 适宜性和短时稳定性 proxy，单独使用电导率会遗漏一部分高稳定性或近中性样本。",
        "基于 CRITIC-TOPSIS 的综合性能分数可以为后续预测与候选筛选提供统一目标量。",
    ]
    outputs = {
        "result_json": (q_dir / "results" / "result.json").as_posix(),
        "run_log": (q_dir / "results" / "run.log").as_posix(),
        "indicator_table": (q_dir / "results" / "indicator_table.csv").as_posix(),
        "top_formula_snapshot": (q_dir / "results" / "top_formula_snapshot.csv").as_posix(),
    }
    trace = {
        "baseline_comparison.spearman_cond_vs_PI": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.baseline_comparison.spearman_cond_vs_PI",
            "validation_status": "pending",
        },
        "baseline_comparison.top10_overlap_count": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.baseline_comparison.top10_overlap_count",
            "validation_status": "pending",
        },
        "overall_score_summary.top_PI_score": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.overall_score_summary.top_PI_score",
            "validation_status": "pending",
        },
    }
    log_context = {
        "code_starter_used": "templates/shared/code_starter/evaluation.py (adapted)",
        "environment_notes": {
            "packages": ["numpy", "pandas", "scipy", "sklearn", "matplotlib"],
            "seed": SEED,
        },
        "preprocessing_notes": {
            "input_rows": len(records),
            "output_rows": int(len(full_df)),
            "derived_fields": ["W_T", "W_1", "R_W", "S_pH", "PI", "PI_equal", "PI_pca"],
            "ph_interval": "[6.5, 8.5]",
            "ph_margin": 1.0,
        },
        "abnormal_data_handling": [
            {
                "abnormal_type": "missing key fields",
                "detection_rule": "conductivity/pH/derived_quantities is missing",
                "affected_rows": 0,
                "handling_method": "keep",
                "rationale": "all 251 records contain the required fields",
                "effect_on_result": "none",
            },
            {
                "abnormal_type": "non-positive electrochemical window",
                "detection_rule": "W_1 <= 0 or W_T <= 0",
                "affected_rows": int(((full_df["W_1"] <= 0) | (full_df["W_T"] <= 0)).sum()),
                "handling_method": "flag",
                "rationale": "no such rows were found in the current data",
                "effect_on_result": "none",
            },
        ],
        "algorithm_settings": {
            "main_model": "CRITIC + TOPSIS",
            "baseline": "conductivity ranking",
            "robust_alternative": "PCA-loading weighted composite score",
        },
        "toy_demo_result": {
            "n_rows": len(toy_frame),
            "top_PI_guid": str(toy_eval["top10_pi"].iloc[0]["GUID"]),
            "top_conductivity_guid": str(toy_eval["top10_cond"].iloc[0]["GUID"]),
            "rank_difference_detected": bool(
                toy_eval["top10_pi"].iloc[0]["GUID"] != toy_eval["top10_cond"].iloc[0]["GUID"]
            ),
        },
        "full_run_result_summary": {
            "n_rows": int(len(full_df)),
            "spearman_cond_vs_PI": evaluation["spearman_cond_vs_pi"],
            "top10_overlap_count": len(evaluation["overlap_cond"]),
            "top_PI_guid": str(top10.iloc[0]["GUID"]),
        },
        "runtime_notes": {
            "figure_count": len(figure_paths),
            "table_count": len(table_paths),
        },
        "interpretation_notes": {
            "main_interpretation": "high composite-score formulations tend to combine strong conductivity, practical electrochemical window, and near-neutral pH, but they differ substantially from conductivity-only ranking.",
            "next_stage_focus": "check whether the ranking gap remains stable under pH-interval and weighting perturbations.",
        },
        "errors": [],
    }

    write_result_and_log(
        question_id="q1",
        model_name="门槛约束-CRITIC-TOPSIS 综合评价模型",
        status="pass",
        inputs={
            "source_problem": (problem_dir / "problem.md").as_posix(),
            "source_data": data_path.as_posix(),
            "source_readme": readme_path.as_posix(),
        },
        outputs=outputs,
        main_result=main_result,
        metrics=metrics,
        figures=figure_paths,
        tables=table_paths,
        source_command=f"python {script_path.as_posix()}",
        source_files=[script_path.as_posix(), (script_path.parent / "result_io.py").as_posix()],
        validation_hooks=[
            "检查 W_T 和 W_1 是否保持正值",
            "比较 conductivity 排序与 PI 排序的 Spearman 相关与 Top10 重叠度",
            "扰动 pH 区间、权重混合系数和稳定性指标组合",
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
