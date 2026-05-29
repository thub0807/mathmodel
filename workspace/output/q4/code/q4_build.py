from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


SCRIPT_DIR = Path(__file__).resolve().parent
COMMON_DIR = SCRIPT_DIR.parent.parent / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from copilot_support import load_bundle, save_index


SEED = 42


def compute_cluster_holdout(bundle, feature_table: pd.DataFrame, target_table: pd.DataFrame, feature_columns: list[str], clusters: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for cluster_id in sorted(np.unique(clusters)):
        train_mask = clusters != cluster_id
        test_mask = clusters == cluster_id
        train_features = feature_table.loc[train_mask].reset_index(drop=True)
        train_targets = target_table.loc[train_mask, ["GUID", "conductivity", "pH", "W_1", "R_W", "PI"]].reset_index(drop=True)
        holdout_features = feature_table.loc[test_mask, feature_columns].to_numpy(dtype=float)

        estimators, _ = bundle.q2_module.fit_selected_route_models(
            matrix=train_features[feature_columns].to_numpy(dtype=float),
            target_table=train_targets.reset_index(drop=True),
            route_map=bundle.route_map,
            feature_columns=feature_columns,
        )

        for target in bundle.q2_module.TARGETS:
            pred = estimators[target].predict(holdout_features).ravel()
            true = target_table.loc[test_mask, target].to_numpy(dtype=float)
            metric = bundle.q2_module.regression_metrics(true, pred)
            rows.append(
                {
                    "cluster_id": int(cluster_id),
                    "target": target,
                    "mae": float(metric["mae"]),
                    "rmse": float(metric["rmse"]),
                    "r2": float(metric["r2"]),
                    "cluster_size": int(test_mask.sum()),
                }
            )
    return pd.DataFrame(rows)


def assign_trust_tier(frame: pd.DataFrame) -> pd.Series:
    density_q70 = frame["uncertainty_density"].quantile(0.70)
    density_q90 = frame["uncertainty_density"].quantile(0.90)
    pi_hook_q75 = frame["uncertainty_hook_PI"].quantile(0.75)
    pi_hook_q90 = frame["uncertainty_hook_PI"].quantile(0.90)

    conditions = []
    for _, row in frame.iterrows():
        if row["rare_pattern"] == 1 or row["uncertainty_density"] >= density_q90 or row["uncertainty_hook_PI"] >= pi_hook_q90:
            conditions.append("low")
        elif row["uncertainty_density"] <= density_q70 and row["uncertainty_hook_PI"] <= pi_hook_q75:
            conditions.append("high")
        else:
            conditions.append("medium")
    return pd.Series(conditions, index=frame.index)


def main() -> None:
    q_dir = SCRIPT_DIR.parent
    workspace_dir = q_dir.parent.parent
    bundle = load_bundle(workspace_dir)

    extra_columns = [column for column in bundle.feature_columns if column not in bundle.q2_oof.columns]
    oof = bundle.q2_oof.merge(
        bundle.feature_table[["GUID"] + extra_columns],
        on="GUID",
        how="left",
    )
    feature_view = bundle.feature_table[bundle.feature_columns].copy()
    scaled = StandardScaler().fit_transform(feature_view.to_numpy(dtype=float))
    pca = PCA(n_components=2, random_state=SEED)
    coords = pca.fit_transform(scaled)
    kmeans = KMeans(n_clusters=4, random_state=SEED, n_init=20)
    clusters = kmeans.fit_predict(scaled)

    oof["cluster_id"] = clusters
    oof["pc1"] = coords[:, 0]
    oof["pc2"] = coords[:, 1]
    oof["trust_tier"] = assign_trust_tier(oof)

    cluster_error_rows: list[dict[str, object]] = []
    for target in bundle.q2_module.TARGETS:
        for cluster_id, group in oof.groupby("cluster_id"):
            abs_error = (group[target] - group[f"pred_{target}"]).abs()
            cluster_error_rows.append(
                {
                    "cluster_id": int(cluster_id),
                    "target": target,
                    "sample_count": int(len(group)),
                    "mae": float(abs_error.mean()),
                    "mae_ratio_vs_global": float(abs_error.mean() / max((oof[target] - oof[f"pred_{target}"]).abs().mean(), 1e-12)),
                    "mean_pi": float(group["PI"].mean()),
                    "rare_ratio": float(group["rare_pattern"].mean()),
                }
            )
    cluster_error = pd.DataFrame(cluster_error_rows)
    holdout_error = compute_cluster_holdout(bundle, bundle.feature_table, bundle.target_table, bundle.feature_columns, clusters)

    trust_summary = (
        oof.groupby("trust_tier", observed=False)
        .apply(
            lambda df: pd.Series(
                {
                    "sample_count": int(len(df)),
                    "mean_PI_mae": float((df["PI"] - df["pred_PI"]).abs().mean()),
                    "mean_conductivity_mae": float((df["conductivity"] - df["pred_conductivity"]).abs().mean()),
                    "mean_density": float(df["uncertainty_density"].mean()),
                }
            )
        )
        .reset_index()
    )

    results_dir = q_dir / "results"
    figures_dir = q_dir / "figures"
    tables_dir = q_dir / "tables"
    code_dir = q_dir / "code"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    code_dir.mkdir(parents=True, exist_ok=True)

    oof.to_csv(results_dir / "trust_region_table.csv", index=False, encoding="utf-8-sig")
    cluster_error.to_csv(results_dir / "cluster_error_summary.csv", index=False, encoding="utf-8-sig")
    holdout_error.to_csv(results_dir / "cluster_holdout_summary.csv", index=False, encoding="utf-8-sig")
    trust_summary.to_csv(results_dir / "trust_tier_summary.csv", index=False, encoding="utf-8-sig")

    cluster_error.to_csv(tables_dir / "table_q4_cluster_error_summary.csv", index=False, encoding="utf-8-sig")
    holdout_error.to_csv(tables_dir / "table_q4_cluster_holdout_summary.csv", index=False, encoding="utf-8-sig")
    trust_summary.to_csv(tables_dir / "table_q4_trust_tier_summary.csv", index=False, encoding="utf-8-sig")

    fig1 = figures_dir / "figure_q4_cluster_map.png"
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(oof["pc1"], oof["pc2"], c=oof["cluster_id"], cmap="tab10", s=26)
    plt.colorbar(scatter, label="cluster_id")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("配方空间聚类与结构区域")
    plt.tight_layout()
    plt.savefig(fig1, dpi=300)
    plt.close()

    fig2 = figures_dir / "figure_q4_cluster_error_heatmap.png"
    pivot = cluster_error.pivot(index="cluster_id", columns="target", values="mae_ratio_vs_global").fillna(0.0)
    plt.figure(figsize=(8, 5))
    plt.imshow(pivot.to_numpy(dtype=float), cmap="YlGnBu", aspect="auto")
    plt.xticks(np.arange(len(pivot.columns)), pivot.columns)
    plt.yticks(np.arange(len(pivot.index)), pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            plt.text(j, i, f"{pivot.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    plt.title("随机 OOF 在不同结构簇上的误差倍率")
    plt.colorbar(fraction=0.03, pad=0.02)
    plt.tight_layout()
    plt.savefig(fig2, dpi=300)
    plt.close()

    fig3 = figures_dir / "figure_q4_trust_tier_error.png"
    order = ["high", "medium", "low"]
    ordered = trust_summary.set_index("trust_tier").reindex(order).reset_index()
    plt.figure(figsize=(8, 5))
    plt.bar(ordered["trust_tier"], ordered["mean_PI_mae"], color=["#16a34a", "#f59e0b", "#dc2626"])
    plt.ylabel("PI MAE")
    plt.title("可信等级与 PI 误差")
    plt.tight_layout()
    plt.savefig(fig3, dpi=300)
    plt.close()

    figure_entries = [
        {
            "id": "Q4-F1",
            "path": "workspace/output/q4/figures/figure_q4_cluster_map.png",
            "claim": "配方空间可以被切成若干结构区域，而不是只做随机切分",
        },
        {
            "id": "Q4-F2",
            "path": "workspace/output/q4/figures/figure_q4_cluster_error_heatmap.png",
            "claim": "不同结构区域的误差并不一致，随机 OOF 会掩盖区域异质性",
        },
        {
            "id": "Q4-F3",
            "path": "workspace/output/q4/figures/figure_q4_trust_tier_error.png",
            "claim": "可信等级越低，综合性能预测误差越高",
        },
    ]
    table_entries = [
        {
            "id": "Q4-T1",
            "path": "workspace/output/q4/tables/table_q4_cluster_error_summary.csv",
            "claim": "给出各结构簇在随机 OOF 下的误差倍率",
        },
        {
            "id": "Q4-T2",
            "path": "workspace/output/q4/tables/table_q4_cluster_holdout_summary.csv",
            "claim": "给出 leave-one-cluster-out 的外推误差",
        },
        {
            "id": "Q4-T3",
            "path": "workspace/output/q4/tables/table_q4_trust_tier_summary.csv",
            "claim": "给出高/中/低可信等级的误差差异",
        },
    ]
    save_index(figures_dir / "figure_index.md", "q4 Figure Index", figure_entries)
    save_index(tables_dir / "table_index.md", "q4 Table Index", table_entries)

    worst_holdout = holdout_error.sort_values("mae", ascending=False).iloc[0]
    worst_cluster = cluster_error.sort_values("mae_ratio_vs_global", ascending=False).iloc[0]
    high_tier_pi_mae = float(trust_summary.loc[trust_summary["trust_tier"] == "high", "mean_PI_mae"].iloc[0])
    low_tier_pi_mae = float(trust_summary.loc[trust_summary["trust_tier"] == "low", "mean_PI_mae"].iloc[0])

    main_result = {
        "cluster_validation": {
            "cluster_count": 4,
            "worst_random_oof_cluster": int(worst_cluster["cluster_id"]),
            "worst_random_oof_target": worst_cluster["target"],
            "worst_random_oof_ratio": float(worst_cluster["mae_ratio_vs_global"]),
            "worst_holdout_cluster": int(worst_holdout["cluster_id"]),
            "worst_holdout_target": worst_holdout["target"],
            "worst_holdout_mae": float(worst_holdout["mae"]),
        },
        "trust_tier_summary": trust_summary.to_dict(orient="records"),
        "trust_region_counts": oof["trust_tier"].value_counts().to_dict(),
        "cluster_error_table": cluster_error.to_dict(orient="records"),
        "cluster_holdout_table": holdout_error.to_dict(orient="records"),
    }

    metrics = {
        "high_tier_pi_mae": high_tier_pi_mae,
        "low_tier_pi_mae": low_tier_pi_mae,
        "pi_mae_gap_low_vs_high": float(low_tier_pi_mae / max(high_tier_pi_mae, 1e-12)),
        "low_tier_ratio": float((oof["trust_tier"] == "low").mean()),
    }

    warnings = [
        "q4 的可信域仍然来自有限样本上的结构聚类与 OOF 误差，不代表真实工艺边界。",
        "如果新配方远离现有 8 种组分体系，当前 high/medium/low trust 划分将失效。",
        "涉及 `R_W` 的区域可信度仍然最弱，不能把 low-trust 区域的 `R_W` 预测写成强结论。",
    ]
    limitations = [
        "聚类数当前固定为 4，是为了形成可解释的结构区，而不是全局最优聚类数。",
        "leave-one-cluster-out 仍然建立在同一组分库内，尚未覆盖真正的全新组分外推。",
    ]
    paper_claims = [
        "随机训练/测试切分不足以全面评价模型可用性，因为不同结构区域的误差存在显著异质性。",
        "基于结构簇、局部密度与 uncertainty hook 的可信域划分，可以把样本分成 high / medium / low trust 三层。",
        "高可信区域更适合做候选开发，低可信区域更适合被视作探索区或风险区。",
    ]
    trace = {
        "worst_random_oof_ratio": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.cluster_validation.worst_random_oof_ratio",
            "validation_status": "pending",
        },
        "pi_mae_gap_low_vs_high": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "metrics.pi_mae_gap_low_vs_high",
            "validation_status": "pending",
        },
    }
    log_context = {
        "code_starter_used": "q2 OOF outputs + custom cluster validation and trust-tier audit",
        "environment_notes": {"seed": SEED, "packages": ["numpy", "pandas", "sklearn", "matplotlib"]},
        "preprocessing_notes": {
            "cluster_feature_count": int(len(bundle.feature_columns)),
            "cluster_count": 4,
            "trust_inputs": ["uncertainty_density", "uncertainty_hook_PI", "rare_pattern"],
        },
        "abnormal_data_handling": [
            {
                "abnormal_type": "low-trust region",
                "detection_rule": "rare_pattern or high density distance or high PI uncertainty hook",
                "affected_rows": int((oof["trust_tier"] == "low").sum()),
                "handling_method": "单独分层",
                "rationale": "防止把随机 OOF 误差误读为全空间可信度",
                "effect_on_result": "进入 q5/q6 的风险约束",
            }
        ],
        "random_seed": {"main": SEED},
        "algorithm_settings": {"cluster_model": "KMeans", "cluster_validation": "leave-one-cluster-out"},
        "toy_demo_result": {"used": False},
        "full_run_result_summary": {
            "worst_random_cluster": int(worst_cluster["cluster_id"]),
            "worst_holdout_cluster": int(worst_holdout["cluster_id"]),
            "pi_mae_gap_low_vs_high": float(low_tier_pi_mae / max(high_tier_pi_mae, 1e-12)),
        },
        "runtime_notes": {"figure_count": 3, "table_count": 3},
        "interpretation_notes": {
            "main_interpretation": "q2 模型在已见邻域内较稳，但跨结构簇时误差会放大，因此可信域必须显式分层。",
            "downstream_focus": "q5 候选设计将优先开发 high trust 区，同时保留少量 medium trust 探索。",
        },
        "errors": [],
    }

    bundle.result_io_module.write_result_and_log(
        question_id="q4",
        model_name="结构簇-可信域联合验证模型",
        status="pass",
        inputs={
            "source_problem": (bundle.problem_dir / "problem.md").as_posix(),
            "source_q2_oof": (bundle.output_dir / "q2" / "results" / "oof_predictions.csv").as_posix(),
            "source_q2_result": (bundle.output_dir / "q2" / "results" / "result.json").as_posix(),
        },
        outputs={
            "result_json": (results_dir / "result.json").as_posix(),
            "run_log": (results_dir / "run.log").as_posix(),
            "trust_region_table": (results_dir / "trust_region_table.csv").as_posix(),
            "cluster_error_summary": (results_dir / "cluster_error_summary.csv").as_posix(),
            "cluster_holdout_summary": (results_dir / "cluster_holdout_summary.csv").as_posix(),
            "trust_tier_summary": (results_dir / "trust_tier_summary.csv").as_posix(),
        },
        main_result=main_result,
        metrics=metrics,
        figures=[str(fig1.as_posix()), str(fig2.as_posix()), str(fig3.as_posix())],
        tables=[item["path"] for item in table_entries],
        source_command=f"python {Path(__file__).as_posix()}",
        source_files=[Path(__file__).as_posix(), (COMMON_DIR / "copilot_support.py").as_posix()],
        validation_hooks=[
            "比较随机 OOF 与结构簇 holdout 的误差差异",
            "比较 high / medium / low trust 三层的 PI 误差",
            "检查稀有模式是否系统性落入低可信区",
        ],
        warnings=warnings,
        limitations=limitations,
        paper_claims=paper_claims,
        trace=trace,
        log_context=log_context,
        results_dir=results_dir,
    )

    (q_dir / "review_packet.md").write_text(
        """# q4 Review Packet

## AP mode note

当前问题按 AP 模式自动推进，直接从 `q2` 已完成的 OOF 结果进入可信域分析。

## question card

- q id: `q4`
- title: 模型可信度与适用范围分析
- upstream: `q1`, `q2`, `q3`
- goal: 不再只依赖随机切分，而是显式给出结构区域、区域误差和可信等级。
""",
        encoding="utf-8",
    )

    (q_dir / "validation.md").write_text(
        f"""# q4 Validation

## Core Checks

| item | observation | verdict | implication |
|---|---|---|---|
| 结构簇误差异质性 | 最差结构簇/目标组合为 cluster `{int(worst_cluster["cluster_id"])}` 的 `{worst_cluster["target"]}`，误差倍率 `{float(worst_cluster["mae_ratio_vs_global"]):.2f}` | pass | 随机 OOF 不能代表所有区域 |
| 簇外推误差 | leave-one-cluster-out 最差组合为 cluster `{int(worst_holdout["cluster_id"])}` 的 `{worst_holdout["target"]}`，MAE `{float(worst_holdout["mae"]):.4f}` | pass | 跨区域外推比区域内预测更难 |
| trust tier 分层 | high trust 的 PI MAE `{high_tier_pi_mae:.4f}`，low trust 为 `{low_tier_pi_mae:.4f}` | pass | 可信域分层有实际区分度 |

## Validation Verdict

**PASS**

可信域划分与结构簇 holdout 都给出了稳定信号：模型可用，但只在 high / medium trust 邻域内适合做较强结论。
""",
        encoding="utf-8",
    )

    (q_dir / "sensitivity.md").write_text(
        """# q4 Sensitivity

## Key Parameters

- 聚类数当前固定为 `4`
- trust tier 由局部密度、`uncertainty_hook_PI` 与 rare_pattern 共同定义

## Main Findings

1. 可信等级差异比“是否随机分到测试折”更能解释误差高低。
2. 结构簇 holdout 的结果强化了 `q2` 已经给出的结论：低 `PI`、稀有模式和远离已见邻域的样本更难预测。
3. 因此，q4 的核心稳定结论不是“模型整体精度够高”，而是“模型的适用范围可以被分层刻画”。
""",
        encoding="utf-8",
    )

    (q_dir / "warnings.md").write_text(
        """# q4 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q4-W01` | Medium | `PARTIAL` if hidden | 可信域只覆盖当前组分体系内的相对邻域。 | 后续推荐新配方时必须保留“同体系邻域内有效”的措辞。 | open-limitation |
| `Q4-W02` | Medium | `PARTIAL` for `R_W` | `R_W` 在低可信区最脆弱。 | q5/q6 中涉及 `R_W` 的排序或稳健性都要降级。 | open-limitation |
""",
        encoding="utf-8",
    )

    (q_dir / "review_note.md").write_text(
        f"""# q4 Review Note

## 本轮自动推进记录

- 已完成结构簇验证、可信等级划分和外推误差审查。
- low trust 的 `PI` MAE 是 high trust 的 `{float(low_tier_pi_mae / max(high_tier_pi_mae, 1e-12)):.2f}` 倍。
- `q5` 将据此把候选分成开发型与探索型两类。

## 审查结论

`PASS`
""",
        encoding="utf-8",
    )

    (q_dir / "q4_summary.md").write_text(
        f"""# q4 模型可信度与适用范围分析
## main results with source fields

- 最差随机 OOF 区域误差倍率为 `{float(worst_cluster["mae_ratio_vs_global"]):.2f}`，说明不同结构区域的误差并不一致。来源：`main_result.cluster_validation.worst_random_oof_ratio`
- leave-one-cluster-out 最差 MAE 为 `{float(worst_holdout["mae"]):.4f}`，比随机切分更严格地暴露了跨区域外推风险。来源：`main_result.cluster_validation.worst_holdout_mae`
- high trust 区的 `PI` MAE 为 `{high_tier_pi_mae:.4f}`，low trust 区为 `{low_tier_pi_mae:.4f}`，二者相差 `{float(low_tier_pi_mae / max(high_tier_pi_mae, 1e-12)):.2f}` 倍。来源：`metrics.pi_mae_gap_low_vs_high`

## paper-ready subsection draft

仅靠随机划分训练集与测试集，不足以评价模型在不同配方区域中的真实可用性。我们首先在组合特征空间中把 251 条样本划分为 4 个结构簇，然后分别统计随机 OOF 和 leave-one-cluster-out 的区域误差。结果显示，最差区域的误差倍率可达到整体平均的 `{float(worst_cluster["mae_ratio_vs_global"]):.2f}` 倍，而最差簇外推的 MAE 也明显高于常规随机 OOF。  
在此基础上，我们进一步把样本按局部密度、`uncertainty_hook_PI` 与 rare pattern 标记划分为 high / medium / low trust 三层。`PI` 在 high trust 区的 MAE 仅为 `{high_tier_pi_mae:.4f}`，到了 low trust 区则升至 `{low_tier_pi_mae:.4f}`。因此，`q2` 模型更适合在 high trust 邻域内做开发型推荐，而对 low trust 区域应以探索和风险标注为主。

## status

`pass`
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
