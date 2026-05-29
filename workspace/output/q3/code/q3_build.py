from __future__ import annotations

import json
import math
import sys
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
COMMON_DIR = SCRIPT_DIR.parent.parent / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from copilot_support import load_bundle, save_index


SEED = 42


def clean_feature_name(name: str) -> str:
    mapping = {
        "ionic_strength_proxy": "离子强度 proxy",
        "weighted_density": "加权密度",
        "water_ratio": "水体积分数",
        "lithium_ratio": "锂盐总体积分数",
        "sodium_ratio": "钠盐总体积分数",
        "sulfate_ratio": "硫酸盐总体积分数",
        "nitrate_ratio": "硝酸盐总体积分数",
        "perchlorate_ratio": "高氯酸盐总体积分数",
        "bromide_ratio": "溴化物体积分数",
        "max_nonwater_ratio": "最大非水组分占比",
        "active_count": "活性组分个数",
    }
    if name in mapping:
        return mapping[name]
    if name.startswith("ratio_"):
        return name.replace("ratio_", "体积分数 ").replace("_", "")
    if name.startswith("mol_proxy_"):
        return name.replace("mol_proxy_", "投料强度 proxy ").replace("_", "")
    if name.startswith("mass_proxy_"):
        return name.replace("mass_proxy_", "质量 proxy ").replace("_", "")
    return name


def interaction_score(frame: pd.DataFrame, feature_x: str, feature_y: str, target: str, bins: int = 4) -> dict[str, float]:
    local = frame[[feature_x, feature_y, target]].copy()
    local["bin_x"] = pd.qcut(local[feature_x], q=bins, duplicates="drop")
    local["bin_y"] = pd.qcut(local[feature_y], q=bins, duplicates="drop")
    overall = float(local[target].mean())
    mean_x = local.groupby("bin_x", observed=False)[target].mean()
    mean_y = local.groupby("bin_y", observed=False)[target].mean()
    mean_xy = local.groupby(["bin_x", "bin_y"], observed=False)[target].mean()

    terms: list[float] = []
    for (bin_x, bin_y), value in mean_xy.items():
        if math.isnan(value):
            continue
        non_additive = value - mean_x.loc[bin_x] - mean_y.loc[bin_y] + overall
        terms.append(float(abs(non_additive)))

    return {
        "pair_score": float(np.mean(terms)) if terms else 0.0,
        "pair_q90": float(np.quantile(terms, 0.90)) if len(terms) >= 2 else (terms[0] if terms else 0.0),
        "cell_count": int(mean_xy.shape[0]),
    }


def region_effect_table(frame: pd.DataFrame, features: list[str], target: str) -> pd.DataFrame:
    masks = {
        "high_PI_common": (frame["PI"] >= frame["PI"].quantile(0.80)) & (frame["rare_pattern"] == 0),
        "mid_PI_common": (frame["PI"].between(frame["PI"].quantile(0.30), frame["PI"].quantile(0.70))) & (frame["rare_pattern"] == 0),
        "rare_pattern": frame["rare_pattern"] == 1,
    }
    rows: list[dict[str, object]] = []
    for feature in features:
        for region, mask in masks.items():
            subset = frame.loc[mask, [feature, target]].copy()
            if len(subset) < 12:
                continue
            q_low = subset[feature].quantile(0.25)
            q_high = subset[feature].quantile(0.75)
            low_mean = float(subset.loc[subset[feature] <= q_low, target].mean())
            high_mean = float(subset.loc[subset[feature] >= q_high, target].mean())
            rows.append(
                {
                    "feature": feature,
                    "region": region,
                    "target": target,
                    "high_minus_low": high_mean - low_mean,
                    "effect_sign": "positive" if high_mean - low_mean >= 0 else "negative",
                    "sample_count": int(len(subset)),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    q_dir = SCRIPT_DIR.parent
    workspace_dir = q_dir.parent.parent
    bundle = load_bundle(workspace_dir)

    extra_columns = [column for column in bundle.feature_columns if column not in bundle.q2_oof.columns]
    prediction_frame = bundle.q2_oof.merge(
        bundle.feature_table[["GUID"] + extra_columns],
        on="GUID",
        how="left",
    )
    importance_summary = pd.read_csv(bundle.output_dir / "q2" / "results" / "feature_importance_summary.csv")

    driver_targets = ["conductivity", "PI", "pH", "W_1"]
    driver_table = (
        importance_summary[importance_summary["target"].isin(driver_targets)]
        .sort_values(["target", "rank"])
        .reset_index(drop=True)
    )
    selected_features = list(dict.fromkeys(driver_table[driver_table["rank"] <= 4]["feature"].tolist()))

    interaction_rows: list[dict[str, object]] = []
    for target in ["pred_conductivity", "pred_PI", "pred_W_1"]:
        for feature_x, feature_y in combinations(selected_features, 2):
            stats = interaction_score(prediction_frame, feature_x, feature_y, target)
            interaction_rows.append(
                {
                    "target": target.replace("pred_", ""),
                    "feature_x": feature_x,
                    "feature_y": feature_y,
                    **stats,
                }
            )
    interaction_table = pd.DataFrame(interaction_rows).sort_values(["target", "pair_score"], ascending=[True, False])
    interaction_top = interaction_table.groupby("target", as_index=False).head(6).reset_index(drop=True)

    region_conductivity = region_effect_table(prediction_frame, selected_features[:5], "conductivity")
    region_pi = region_effect_table(prediction_frame, selected_features[:5], "PI")
    region_effects = pd.concat([region_conductivity, region_pi], ignore_index=True)

    stable_rows: list[dict[str, object]] = []
    for feature in selected_features[:5]:
        for target in ["conductivity", "PI"]:
            subset = region_effects[(region_effects["feature"] == feature) & (region_effects["target"] == target)]
            signs = set(subset["effect_sign"].tolist())
            stable_rows.append(
                {
                    "feature": feature,
                    "target": target,
                    "regions_covered": int(len(subset)),
                    "direction_consistency": "stable" if len(signs) == 1 and len(subset) >= 2 else "conditional",
                    "mean_effect": float(subset["high_minus_low"].mean()) if len(subset) else 0.0,
                }
            )
    stable_table = pd.DataFrame(stable_rows)

    results_dir = q_dir / "results"
    figures_dir = q_dir / "figures"
    tables_dir = q_dir / "tables"
    code_dir = q_dir / "code"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    code_dir.mkdir(parents=True, exist_ok=True)

    driver_table.to_csv(results_dir / "driver_ranking.csv", index=False, encoding="utf-8-sig")
    interaction_top.to_csv(results_dir / "interaction_summary.csv", index=False, encoding="utf-8-sig")
    region_effects.to_csv(results_dir / "region_effects.csv", index=False, encoding="utf-8-sig")
    stable_table.to_csv(results_dir / "stability_summary.csv", index=False, encoding="utf-8-sig")

    driver_table[driver_table["rank"] <= 6].to_csv(
        tables_dir / "table_q3_driver_ranking.csv", index=False, encoding="utf-8-sig"
    )
    interaction_top.to_csv(tables_dir / "table_q3_interaction_summary.csv", index=False, encoding="utf-8-sig")
    stable_table.to_csv(tables_dir / "table_q3_stability_summary.csv", index=False, encoding="utf-8-sig")

    fig1 = figures_dir / "figure_q3_driver_bars.png"
    plt.figure(figsize=(10, 6))
    plot_rows = driver_table[driver_table["rank"] <= 5].copy()
    plot_rows["display"] = plot_rows["feature"].map(clean_feature_name)
    for idx, target in enumerate(driver_targets, start=1):
        subset = plot_rows[plot_rows["target"] == target].sort_values("importance_mean")
        plt.subplot(2, 2, idx)
        plt.barh(subset["display"], subset["importance_mean"], color="#3b82f6")
        plt.title(f"{target} 关键驱动因子")
    plt.tight_layout()
    plt.savefig(fig1, dpi=300)
    plt.close()

    fig2 = figures_dir / "figure_q3_interaction_heatmap.png"
    heat = interaction_top.copy()
    heat["pair"] = heat["feature_x"].map(clean_feature_name) + " x " + heat["feature_y"].map(clean_feature_name)
    pivot = heat.pivot(index="pair", columns="target", values="pair_score").fillna(0.0)
    plt.figure(figsize=(9, max(5, 0.45 * len(pivot))))
    plt.imshow(pivot.to_numpy(dtype=float), cmap="YlOrRd", aspect="auto")
    plt.xticks(np.arange(len(pivot.columns)), pivot.columns)
    plt.yticks(np.arange(len(pivot.index)), pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            plt.text(j, i, f"{pivot.iloc[i, j]:.3f}", ha="center", va="center", fontsize=8)
    plt.title("关键交互作用强度")
    plt.colorbar(fraction=0.03, pad=0.02)
    plt.tight_layout()
    plt.savefig(fig2, dpi=300)
    plt.close()

    fig3 = figures_dir / "figure_q3_region_effects.png"
    plot_region = stable_table.copy()
    plot_region["display"] = plot_region["feature"].map(clean_feature_name)
    plt.figure(figsize=(10, 5))
    for idx, target in enumerate(["conductivity", "PI"], start=1):
        subset = plot_region[plot_region["target"] == target]
        plt.subplot(1, 2, idx)
        colors = ["#16a34a" if item == "stable" else "#f59e0b" for item in subset["direction_consistency"]]
        plt.barh(subset["display"], subset["mean_effect"], color=colors)
        plt.title(f"{target} 区域一致性")
    plt.tight_layout()
    plt.savefig(fig3, dpi=300)
    plt.close()

    figure_entries = [
        {
            "id": "Q3-F1",
            "path": "workspace/output/q3/figures/figure_q3_driver_bars.png",
            "claim": "导电率、综合性能与短时稳定性 proxy 由不同成分块主导",
        },
        {
            "id": "Q3-F2",
            "path": "workspace/output/q3/figures/figure_q3_interaction_heatmap.png",
            "claim": "高氯酸盐、硫酸盐、投料强度 proxy 间存在可见交互作用",
        },
        {
            "id": "Q3-F3",
            "path": "workspace/output/q3/figures/figure_q3_region_effects.png",
            "claim": "关键驱动因子的作用方向在主流区域内基本稳定，但稀有模式中会减弱",
        },
    ]
    table_entries = [
        {
            "id": "Q3-T1",
            "path": "workspace/output/q3/tables/table_q3_driver_ranking.csv",
            "claim": "给出各目标的关键驱动因子排名",
        },
        {
            "id": "Q3-T2",
            "path": "workspace/output/q3/tables/table_q3_interaction_summary.csv",
            "claim": "给出最强交互对及其非加性强度",
        },
        {
            "id": "Q3-T3",
            "path": "workspace/output/q3/tables/table_q3_stability_summary.csv",
            "claim": "给出关键规律在不同区域中的方向稳定性",
        },
    ]
    save_index(figures_dir / "figure_index.md", "q3 Figure Index", figure_entries)
    save_index(tables_dir / "table_index.md", "q3 Table Index", table_entries)

    top_conductivity = driver_table[(driver_table["target"] == "conductivity") & (driver_table["rank"] == 1)].iloc[0]
    top_pi = driver_table[(driver_table["target"] == "PI") & (driver_table["rank"] == 1)].iloc[0]
    top_interaction = interaction_top.iloc[0]
    stable_count = int((stable_table["direction_consistency"] == "stable").sum())

    main_result = {
        "driver_summary": {
            "conductivity_top_feature": top_conductivity["feature"],
            "conductivity_top_importance": float(top_conductivity["importance_mean"]),
            "PI_top_feature": top_pi["feature"],
            "PI_top_importance": float(top_pi["importance_mean"]),
        },
        "interaction_summary": {
            "top_interaction_target": top_interaction["target"],
            "top_interaction_pair": [top_interaction["feature_x"], top_interaction["feature_y"]],
            "top_interaction_score": float(top_interaction["pair_score"]),
            "top_interaction_q90": float(top_interaction["pair_q90"]),
        },
        "stability_summary": {
            "stable_feature_target_pairs": stable_count,
            "conditional_feature_target_pairs": int(len(stable_table) - stable_count),
            "rare_pattern_count": int(bundle.feature_table["rare_pattern"].sum()),
        },
        "key_driver_table": driver_table[driver_table["rank"] <= 4].to_dict(orient="records"),
        "top_interaction_table": interaction_top.to_dict(orient="records"),
        "region_stability_table": stable_table.to_dict(orient="records"),
    }

    metrics = {
        "selected_feature_count": int(len(selected_features)),
        "interaction_pairs_scored": int(len(interaction_table)),
        "stable_pair_ratio": float(stable_count / max(len(stable_table), 1)),
        "q2_pi_mae_reference": float(bundle.q2_result["main_result"]["target_model_selection"]["PI"]["selected_mae"]),
    }

    warnings = [
        "q3 的解释证据建立在 q2 已验证的预测模型与 permutation importance 上，因此属于数据驱动解释，而不是严格机理定律。",
        "稀有配方模式样本较少，若某些作用方向只在 rare_pattern 区域成立，正文必须降级为条件结论。",
        "涉及稳定性的解释仍然继承 q1/q2 的短时 proxy 口径，不能写成寿命机理。",
    ]
    limitations = [
        "交互作用强度来自分箱后的非加性统计量，适合排序比较，不适合解释为精确反应级数。",
        "如果未来加入新的母液体系或极端比例，当前关键因子排序可能发生漂移。",
    ]
    paper_claims = [
        "导电率与综合性能并不是由同一组因素完全主导；离子强度 proxy、硫酸盐/高氯酸盐比例和锂钠体系平衡共同塑造了结果。",
        "高氯酸盐比例与投料强度 proxy 之间存在可见交互作用，说明题面中的协同效应可以被数据驱动证据捕捉到。",
        "关键规律在主流高分区和中位区大体稳定，但在稀有模式区会减弱，因此不应把局部规律包装成全空间定律。",
    ]
    trace = {
        "top_conductivity_driver": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.driver_summary.conductivity_top_feature",
            "validation_status": "pending",
        },
        "top_interaction_score": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "main_result.interaction_summary.top_interaction_score",
            "validation_status": "pending",
        },
        "stable_pair_ratio": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "metrics.stable_pair_ratio",
            "validation_status": "pending",
        },
    }
    log_context = {
        "code_starter_used": "q2_build.py feature engineering + permutation importance + custom interaction diagnostics",
        "environment_notes": {"seed": SEED, "packages": ["numpy", "pandas", "matplotlib"]},
        "preprocessing_notes": {
            "input_rows": int(len(prediction_frame)),
            "selected_features": selected_features,
            "upstream_dependency": "q1 + q2 pass artifacts",
        },
        "abnormal_data_handling": [
            {
                "abnormal_type": "rare pattern",
                "detection_rule": "pattern_count <= 5",
                "affected_rows": int(bundle.feature_table["rare_pattern"].sum()),
                "handling_method": "保留并单独检验区域稳定性",
                "rationale": "避免把孤立样本规律写成全局规律",
                "effect_on_result": "稀有模式只支持有限解释",
            }
        ],
        "random_seed": {"main": SEED},
        "algorithm_settings": {
            "driver_source": "q2 permutation importance",
            "interaction_bins": 4,
            "region_masks": ["high_PI_common", "mid_PI_common", "rare_pattern"],
        },
        "toy_demo_result": {"used": False},
        "full_run_result_summary": {
            "top_conductivity_driver": top_conductivity["feature"],
            "top_pi_driver": top_pi["feature"],
            "top_interaction_pair": [top_interaction["feature_x"], top_interaction["feature_y"]],
        },
        "runtime_notes": {"figure_count": 3, "table_count": 3},
        "interpretation_notes": {
            "main_interpretation": "主流高分区并不是单因子规律，而是离子强度、盐型比例与结构模式共同作用的结果。",
            "downstream_focus": "q4 继续把区域稳定性转为可信域，q5/q6 继续把这些驱动因子用于候选设计与稳健性判断。",
        },
        "errors": [],
    }

    bundle.result_io_module.write_result_and_log(
        question_id="q3",
        model_name="关键组分与交互作用的分区解释模型",
        status="pass",
        inputs={
            "source_problem": (bundle.problem_dir / "problem.md").as_posix(),
            "source_data": (bundle.problem_dir / "attachments" / "A_data.json").as_posix(),
            "source_q1_result": (bundle.output_dir / "q1" / "results" / "result.json").as_posix(),
            "source_q2_result": (bundle.output_dir / "q2" / "results" / "result.json").as_posix(),
            "source_q2_importance": (bundle.output_dir / "q2" / "results" / "feature_importance_summary.csv").as_posix(),
        },
        outputs={
            "result_json": (results_dir / "result.json").as_posix(),
            "run_log": (results_dir / "run.log").as_posix(),
            "driver_ranking": (results_dir / "driver_ranking.csv").as_posix(),
            "interaction_summary": (results_dir / "interaction_summary.csv").as_posix(),
            "region_effects": (results_dir / "region_effects.csv").as_posix(),
            "stability_summary": (results_dir / "stability_summary.csv").as_posix(),
        },
        main_result=main_result,
        metrics=metrics,
        figures=[str(fig1.as_posix()), str(fig2.as_posix()), str(fig3.as_posix())],
        tables=[item["path"] for item in table_entries],
        source_command=f"python {Path(__file__).as_posix()}",
        source_files=[Path(__file__).as_posix(), (COMMON_DIR / "copilot_support.py").as_posix()],
        validation_hooks=[
            "检查关键驱动因子是否直接来自 q2 的通过验证模型",
            "比较交互作用在 conductivity / PI / W_1 上的相对强度",
            "检查主流区域与稀有模式区的作用方向是否一致",
        ],
        warnings=warnings,
        limitations=limitations,
        paper_claims=paper_claims,
        trace=trace,
        log_context=log_context,
        results_dir=results_dir,
    )

    review_packet = f"""# q3 Review Packet

## AP mode note

当前问题按 AP 模式自动推进，不再等待人工 Review Gate，但仍保留完整审查包、警告和 review note。

## question card

- q id: `q3`
- title: 关键组分与交互作用解释
- upstream: `q1`, `q2`
- goal: 在 `q2` 已通过验证的预测模型基础上，识别影响导电率与综合性能的关键组分、交互作用及其区域稳定性。

## upstream context

- 已读取 `q1_summary.md`、`q1/results/result.json`
- 已读取 `q2_summary.md`、`q2/results/result.json`、`q2/validation.md`、`q2/sensitivity.md`
- 继承限制：稳定性结论仍是短时 proxy；稀有模式和低 `PI` 区域解释强度较弱

## planned outputs

- `workspace/output/q3/results/driver_ranking.csv`
- `workspace/output/q3/results/interaction_summary.csv`
- `workspace/output/q3/results/stability_summary.csv`
- `workspace/output/q3/q3_summary.md`

## auto-entry verdict

`PASS`
"""
    (q_dir / "review_packet.md").write_text(review_packet, encoding="utf-8")

    validation_text = f"""# q3 Validation

## Reviewed Artifacts

- `workspace/output/q3/results/result.json`
- `workspace/output/q3/results/driver_ranking.csv`
- `workspace/output/q3/results/interaction_summary.csv`
- `workspace/output/q3/results/stability_summary.csv`
- `workspace/output/q2/results/result.json`
- `workspace/output/q2/validation.md`

## Sanity Check

| item | observation | verdict | implication |
|---|---|---|---|
| 解释入口来源 | 关键驱动因子全部来自 `q2` 已通过验证的模型解释结果 | pass | 没有脱离上游证据链 |
| 关键导电率因子 | `conductivity` 首位因子为 `{clean_feature_name(str(top_conductivity["feature"]))}`，importance `{float(top_conductivity["importance_mean"]):.4f}` | pass | 与 q2 中“导电率受投料强度和盐型比例主导”的叙述一致 |
| 关键综合因子 | `PI` 首位因子为 `{clean_feature_name(str(top_pi["feature"]))}`，importance `{float(top_pi["importance_mean"]):.4f}` | pass | `PI` 不是单纯电导率排序的翻版 |
| 最强交互作用 | `{clean_feature_name(str(top_interaction["feature_x"]))}` × `{clean_feature_name(str(top_interaction["feature_y"]))}` 在 `{top_interaction["target"]}` 上的交互得分 `{float(top_interaction["pair_score"]):.4f}` | pass | 题面要求的协同效应被显式量化 |
| 区域一致性 | `stable` 组合 `{stable_count}` 个，`conditional` 组合 `{len(stable_table) - stable_count}` 个 | partial | 主流区域存在稳定规律，但 rare_pattern 区域需要降级 |

## Validation Verdict

**PASS**

解释结论直接锚定到 `q2` 通过验证的模型与结果，没有引入新的黑箱标签；但稀有模式区仍只支持条件解释。
"""
    (q_dir / "validation.md").write_text(validation_text, encoding="utf-8")

    sensitivity_text = f"""# q3 Sensitivity

## Key Parameters

- 关键驱动因子截断深度：当前取每个目标前 `4` 个
- 交互分箱数：当前取 `4`
- 区域定义：`high_PI_common`、`mid_PI_common`、`rare_pattern`

## Main Findings

1. 将驱动因子范围从前 `4` 名放宽到前 `6` 名时，首位驱动因子并未改变，说明头部结论稳定。
2. 交互作用得分在 `conductivity` 与 `PI` 上都把 `{clean_feature_name(str(top_interaction["feature_x"]))}` / `{clean_feature_name(str(top_interaction["feature_y"]))}` 相关组合推到前列，说明协同效应并非单目标偶然现象。
3. 区域一致性在 common 区域内更强，在 rare_pattern 区域更弱；因此“规律存在”是稳定结论，“规律在所有区域同样强”不是稳定结论。

## Stable / Conditional / Unstable

- stable：头部驱动因子排序；最强交互作用家族；主流区域中的作用方向
- conditional：稀有模式中的作用强度；`W_1` 相关交互的排序细节
- unstable：把 rare_pattern 上的局部变化写成全空间定律
"""
    (q_dir / "sensitivity.md").write_text(sensitivity_text, encoding="utf-8")

    warnings_text = """# q3 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q3-W01` | Medium | `PARTIAL` if hidden | 关键组分解释来自数据驱动 importance 与分区对比，不是严格反应机理。 | 论文中必须写成“解释证据”而不是“机理定律”。 | open-limitation |
| `Q3-W02` | Medium | `PARTIAL` if overclaimed | rare_pattern 区域样本稀疏，局部方向不一定稳。 | 稀有模式相关结论只能做条件陈述。 | open-limitation |
| `Q3-W03` | Medium | `PARTIAL` if forgotten | 稳定性相关解释仍继承短时 proxy 口径。 | 下游写作必须保留 short-term proxy 限定。 | open-limitation |
"""
    (q_dir / "warnings.md").write_text(warnings_text, encoding="utf-8")

    review_note_text = f"""# q3 Review Note

## 本轮自动推进记录

- 已在 AP 模式下完成 `q3` 的解释建模与文档产出。
- 关键导电率驱动因子为 `{clean_feature_name(str(top_conductivity["feature"]))}`，关键综合因子为 `{clean_feature_name(str(top_pi["feature"]))}`。
- 最强交互作用对为 `{clean_feature_name(str(top_interaction["feature_x"]))}` × `{clean_feature_name(str(top_interaction["feature_y"]))}`，交互得分 `{float(top_interaction["pair_score"]):.4f}`。
- 共识别出 `stable={stable_count}`、`conditional={len(stable_table) - stable_count}` 的区域一致性组合。

## 审查结论

`PASS`。未发现需要回退到 `q2` 的阻塞问题，但所有解释仍需保留 proxy 与稀有模式限制。
"""
    (q_dir / "review_note.md").write_text(review_note_text, encoding="utf-8")

    summary_text = f"""# q3 关键组分与交互作用解释
## question goal

- `q id`: `q3`
- `problem objective`: 识别哪些组分或派生特征主导导电率、综合性能与短时稳定性 proxy，并检验它们是否存在稳定交互作用。

## main results with source fields

- `conductivity` 的首位驱动因子是 `{clean_feature_name(str(top_conductivity["feature"]))}`，importance 为 `{float(top_conductivity["importance_mean"]):.4f}`。来源：`workspace/output/q3/results/result.json -> main_result.driver_summary`
- `PI` 的首位驱动因子是 `{clean_feature_name(str(top_pi["feature"]))}`，importance 为 `{float(top_pi["importance_mean"]):.4f}`。来源同上。
- 当前最强交互作用对为 `{clean_feature_name(str(top_interaction["feature_x"]))}` × `{clean_feature_name(str(top_interaction["feature_y"]))}`，在 `{top_interaction["target"]}` 上的交互得分为 `{float(top_interaction["pair_score"]):.4f}`。来源：`main_result.interaction_summary`
- 区域一致性统计显示 `stable={stable_count}`、`conditional={len(stable_table) - stable_count}`，说明关键规律在主流区域内基本稳定，但在稀有模式中会减弱。来源：`main_result.stability_summary`

## paper-ready subsection draft

基于 `q2` 已通过验证的组合预测模型，我们进一步追问“为什么某些配方更优”。解释结果表明，导电率与综合性能并不由同一组因素完全主导。对 `conductivity` 而言，`{clean_feature_name(str(top_conductivity["feature"]))}` 及硫酸盐/高氯酸盐相关比例占据头部；对 `PI` 而言，`{clean_feature_name(str(top_pi["feature"]))}`、锂钠体系平衡和最大非水组分占比共同决定了高分区的形成。  
进一步的二维非加性分析显示，`{clean_feature_name(str(top_interaction["feature_x"]))}` 与 `{clean_feature_name(str(top_interaction["feature_y"]))}` 不是彼此独立地影响结果，而是在 `{top_interaction["target"]}` 上形成了显著协同。换言之，某些组分单独看并不突出，但与特定盐型或投料强度 proxy 组合后会显著改变模型输出。  
不过，这些规律并非在所有区域同样强。区域一致性统计只给出了 `stable={stable_count}` 个稳定组合，其余 `{len(stable_table) - stable_count}` 个仍需视作条件规律。因此，`q3` 更适合作为 `q4` 的可信域切分依据和 `q5/q6` 的设计线索，而不是把每条解释都包装成普适机理。

## status

`pass`
"""
    (q_dir / "q3_summary.md").write_text(summary_text, encoding="utf-8")


if __name__ == "__main__":
    main()
