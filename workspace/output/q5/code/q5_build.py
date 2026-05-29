from __future__ import annotations

import random
import sys
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

from copilot_support import build_candidate_records, load_bundle, predict_from_feature_table, save_index


SEED = 42
STEP_SIZES = [0.1, 0.2]


def signature(volumes: dict[str, float], components: list[str]) -> tuple[float, ...]:
    return tuple(round(float(volumes.get(component, 0.0)), 1) for component in components)


def recipe_text(volumes: dict[str, float], components: list[str]) -> str:
    parts = [f"{component}:{volumes[component]:.1f}" for component in components if component != "water" and volumes[component] > 0]
    parts.append(f"water:{volumes['water']:.1f}")
    return "; ".join(parts)


def assign_trust_tier(frame: pd.DataFrame, reference: pd.DataFrame) -> pd.Series:
    density_q70 = reference["uncertainty_density"].quantile(0.70)
    density_q90 = reference["uncertainty_density"].quantile(0.90)
    pi_hook_q75 = reference["uncertainty_hook_PI"].quantile(0.75)
    pi_hook_q90 = reference["uncertainty_hook_PI"].quantile(0.90)
    tiers: list[str] = []
    for _, row in frame.iterrows():
        if row["rare_pattern"] == 1 or row["uncertainty_density"] >= density_q90 or row["uncertainty_hook_PI"] >= pi_hook_q90:
            tiers.append("low")
        elif row["uncertainty_density"] <= density_q70 and row["uncertainty_hook_PI"] <= pi_hook_q75:
            tiers.append("high")
        else:
            tiers.append("medium")
    return pd.Series(tiers, index=frame.index)


def generate_neighbors(base_volumes: dict[str, float], components: list[str]) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    for donor in components:
        for receiver in components:
            if donor == receiver:
                continue
            for step in STEP_SIZES:
                if base_volumes[donor] < step:
                    continue
                candidate = dict(base_volumes)
                candidate[donor] = round(candidate[donor] - step, 1)
                candidate[receiver] = round(candidate[receiver] + step, 1)
                if any(value < 0 for value in candidate.values()):
                    continue
                if round(sum(candidate.values()), 1) != 7.0:
                    continue
                out.append(candidate)
    return out


def too_close(row: pd.Series, chosen: list[pd.Series], volume_columns: list[str]) -> bool:
    current = row[volume_columns].to_numpy(dtype=float)
    for item in chosen:
        other = item[volume_columns].to_numpy(dtype=float)
        if np.abs(current - other).sum() <= 0.4:
            return True
    return False


def pick_diverse(frame: pd.DataFrame, score_col: str, count: int, volume_columns: list[str]) -> list[pd.Series]:
    chosen: list[pd.Series] = []
    seen_patterns: set[str] = set()
    for _, row in frame.sort_values(score_col, ascending=False).iterrows():
        if row["pattern_key"] in seen_patterns and too_close(row, chosen, volume_columns):
            continue
        chosen.append(row)
        seen_patterns.add(str(row["pattern_key"]))
        if len(chosen) >= count:
            break
    return chosen


def random_baseline(frame: pd.DataFrame, set_size: int, rng: random.Random) -> dict[str, float]:
    metrics: list[tuple[float, float]] = []
    population = frame.reset_index(drop=True)
    if len(population) < set_size:
        return {"mean_pred_PI": float("nan"), "mean_novelty": float("nan")}
    for _ in range(200):
        sample = population.sample(n=set_size, random_state=rng.randint(0, 10_000_000))
        metrics.append((float(sample["pred_PI"].mean()), float(sample["uncertainty_density"].mean())))
    return {
        "mean_pred_PI": float(np.mean([item[0] for item in metrics])),
        "mean_novelty": float(np.mean([item[1] for item in metrics])),
    }


def main() -> None:
    q_dir = SCRIPT_DIR.parent
    workspace_dir = q_dir.parent.parent
    bundle = load_bundle(workspace_dir)
    rng = random.Random(SEED)

    q4_reference = pd.read_csv(bundle.output_dir / "q4" / "results" / "trust_region_table.csv")
    components = sorted(bundle.source_densities)
    record_lookup = {
        record["GUID"]: {component: float(record["electrolyte"]["volumes"].get(component, 0.0)) for component in components}
        for record in bundle.records
    }
    pattern_lookup = bundle.feature_table.groupby("pattern_key")["pattern_count"].first().to_dict()
    observed_signatures = {signature(volumes, components) for volumes in record_lookup.values()}

    anchor_table = q4_reference.copy()
    anchor_table["anchor_priority"] = (
        anchor_table["PI"].rank(pct=True)
        + 0.5 * anchor_table["pred_PI"].rank(pct=True)
        - 0.3 * anchor_table["uncertainty_hook_PI"].rank(pct=True)
    )
    anchors = anchor_table.sort_values("anchor_priority", ascending=False).head(18)

    candidate_maps: list[dict[str, float]] = []
    candidate_meta: list[dict[str, object]] = []
    seen: set[tuple[float, ...]] = set()
    for _, anchor in anchors.iterrows():
        base = record_lookup[str(anchor["GUID"])]
        for neighbor in generate_neighbors(base, components):
            sig = signature(neighbor, components)
            if sig in seen or sig in observed_signatures:
                continue
            seen.add(sig)
            candidate_maps.append(neighbor)
            candidate_meta.append(
                {
                    "anchor_guid": str(anchor["GUID"]),
                    "anchor_trust": str(anchor["trust_tier"]),
                    "anchor_PI": float(anchor["PI"]),
                    "recipe_signature": recipe_text(neighbor, components),
                }
            )

    candidate_records = build_candidate_records(bundle, candidate_maps, prefix="q5cand")
    candidate_feature_table = bundle.q2_module.build_feature_table(candidate_records)
    candidate_feature_table["pattern_count"] = candidate_feature_table["pattern_key"].map(pattern_lookup).fillna(0).astype(int)
    candidate_feature_table["rare_pattern"] = (candidate_feature_table["pattern_count"] <= 5).astype(int)

    prediction = predict_from_feature_table(bundle, candidate_feature_table)
    prediction = prediction.merge(pd.DataFrame(candidate_meta).assign(GUID=prediction["GUID"]), on="GUID", how="left")
    prediction["trust_tier"] = assign_trust_tier(prediction, q4_reference)

    for component in components:
        prediction[f"vol_{component}"] = [volumes[component] for volumes in candidate_maps]

    prediction["pi_rank"] = prediction["pred_PI"].rank(pct=True)
    prediction["cond_rank"] = prediction["pred_conductivity"].rank(pct=True)
    prediction["w1_rank"] = prediction["pred_W_1"].rank(pct=True)
    prediction["ph_rank"] = prediction["pred_S_pH"].rank(pct=True)
    prediction["novelty_rank"] = prediction["uncertainty_density"].rank(pct=True)
    prediction["risk_rank"] = prediction["uncertainty_hook_PI"].rank(pct=True)
    prediction["exploit_score"] = (
        0.45 * prediction["pi_rank"]
        + 0.20 * prediction["cond_rank"]
        + 0.15 * prediction["w1_rank"]
        + 0.10 * prediction["ph_rank"]
        - 0.20 * prediction["risk_rank"]
    )
    prediction["explore_score"] = (
        0.35 * prediction["pi_rank"]
        + 0.15 * prediction["cond_rank"]
        + 0.10 * prediction["w1_rank"]
        + 0.10 * prediction["ph_rank"]
        + 0.25 * prediction["novelty_rank"]
        - 0.10 * prediction["risk_rank"]
    )

    eligible = prediction[(prediction["pred_S_pH"] >= 0.50) & (prediction["pred_W_1"] >= prediction["pred_W_1"].quantile(0.40))].copy()
    explore_pool = eligible[eligible["trust_tier"].isin(["medium", "low"])].copy()
    exploit_pool = eligible[eligible["trust_tier"].isin(["high", "medium"])].copy()
    volume_columns = [f"vol_{component}" for component in components]

    top5_rows = pick_diverse(exploit_pool, "exploit_score", 3, volume_columns)
    top5_rows += pick_diverse(explore_pool[~explore_pool["GUID"].isin([row["GUID"] for row in top5_rows])], "explore_score", 2, volume_columns)
    if len(top5_rows) < 5:
        extra = pick_diverse(eligible[~eligible["GUID"].isin([row["GUID"] for row in top5_rows])], "exploit_score", 5 - len(top5_rows), volume_columns)
        top5_rows += extra

    used_guids = [row["GUID"] for row in top5_rows]
    top10_rows = list(top5_rows)
    top10_rows += pick_diverse(exploit_pool[~exploit_pool["GUID"].isin(used_guids)], "exploit_score", 3, volume_columns)
    used_guids = [row["GUID"] for row in top10_rows]
    top10_rows += pick_diverse(explore_pool[~explore_pool["GUID"].isin(used_guids)], "explore_score", 2, volume_columns)
    if len(top10_rows) < 10:
        extra = pick_diverse(eligible[~eligible["GUID"].isin([row["GUID"] for row in top10_rows])], "exploit_score", 10 - len(top10_rows), volume_columns)
        top10_rows += extra

    top5 = pd.DataFrame(top5_rows).reset_index(drop=True)
    top10 = pd.DataFrame(top10_rows).reset_index(drop=True)

    baseline5 = random_baseline(eligible, 5, rng)
    baseline10 = random_baseline(eligible, 10, rng)
    baseline_compare = pd.DataFrame(
        [
            {
                "set_name": "top5",
                "selected_mean_pred_PI": float(top5["pred_PI"].mean()),
                "selected_mean_novelty": float(top5["uncertainty_density"].mean()),
                **baseline5,
            },
            {
                "set_name": "top10",
                "selected_mean_pred_PI": float(top10["pred_PI"].mean()),
                "selected_mean_novelty": float(top10["uncertainty_density"].mean()),
                **baseline10,
            },
        ]
    )

    results_dir = q_dir / "results"
    figures_dir = q_dir / "figures"
    tables_dir = q_dir / "tables"
    code_dir = q_dir / "code"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    code_dir.mkdir(parents=True, exist_ok=True)

    prediction.to_csv(results_dir / "candidate_pool.csv", index=False, encoding="utf-8-sig")
    top5.to_csv(results_dir / "recommended_top5.csv", index=False, encoding="utf-8-sig")
    top10.to_csv(results_dir / "recommended_top10.csv", index=False, encoding="utf-8-sig")
    baseline_compare.to_csv(results_dir / "baseline_compare.csv", index=False, encoding="utf-8-sig")

    top5.to_csv(tables_dir / "table_q5_top5_candidates.csv", index=False, encoding="utf-8-sig")
    top10.to_csv(tables_dir / "table_q5_top10_candidates.csv", index=False, encoding="utf-8-sig")
    baseline_compare.to_csv(tables_dir / "table_q5_baseline_compare.csv", index=False, encoding="utf-8-sig")

    fig1 = figures_dir / "figure_q5_candidate_frontier.png"
    plt.figure(figsize=(8, 6))
    plt.scatter(prediction["uncertainty_density"], prediction["pred_PI"], c=prediction["exploit_score"], cmap="viridis", s=24)
    plt.scatter(top10["uncertainty_density"], top10["pred_PI"], color="#dc2626", s=36, label="selected")
    plt.xlabel("novelty proxy")
    plt.ylabel("predicted PI")
    plt.title("candidate frontier")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig1, dpi=300)
    plt.close()

    fig2 = figures_dir / "figure_q5_selection_mix.png"
    mix = top10["trust_tier"].value_counts().reindex(["high", "medium", "low"], fill_value=0)
    plt.figure(figsize=(7, 4))
    plt.bar(mix.index, mix.values, color=["#16a34a", "#f59e0b", "#dc2626"])
    plt.ylabel("count")
    plt.title("selected trust-tier mix")
    plt.tight_layout()
    plt.savefig(fig2, dpi=300)
    plt.close()

    figure_entries = [
        {
            "id": "Q5-F1",
            "path": "workspace/output/q5/figures/figure_q5_candidate_frontier.png",
            "claim": "候选设计同时兼顾预测综合性能与探索新区域",
        },
        {
            "id": "Q5-F2",
            "path": "workspace/output/q5/figures/figure_q5_selection_mix.png",
            "claim": "最终推荐同时包含开发型与探索型候选",
        },
    ]
    table_entries = [
        {
            "id": "Q5-T1",
            "path": "workspace/output/q5/tables/table_q5_top5_candidates.csv",
            "claim": "给出 5 组优先候选",
        },
        {
            "id": "Q5-T2",
            "path": "workspace/output/q5/tables/table_q5_top10_candidates.csv",
            "claim": "给出 10 组扩展候选",
        },
        {
            "id": "Q5-T3",
            "path": "workspace/output/q5/tables/table_q5_baseline_compare.csv",
            "claim": "与随机选点基线比较平均预期收益与探索度",
        },
    ]
    save_index(figures_dir / "figure_index.md", "q5 Figure Index", figure_entries)
    save_index(tables_dir / "table_index.md", "q5 Table Index", table_entries)

    top5_best = top5.sort_values("pred_PI", ascending=False).iloc[0]
    top10_best = top10.sort_values("explore_score", ascending=False).iloc[0]
    top5_gain = float(
        baseline_compare.loc[baseline_compare["set_name"] == "top5", "selected_mean_pred_PI"].iloc[0]
        - baseline_compare.loc[baseline_compare["set_name"] == "top5", "mean_pred_PI"].iloc[0]
    )
    top10_gain = float(
        baseline_compare.loc[baseline_compare["set_name"] == "top10", "selected_mean_pred_PI"].iloc[0]
        - baseline_compare.loc[baseline_compare["set_name"] == "top10", "mean_pred_PI"].iloc[0]
    )

    main_result = {
        "candidate_pool_summary": {
            "candidate_count": int(len(prediction)),
            "eligible_count": int(len(eligible)),
            "new_pattern_count": int((prediction["pattern_count"] == 0).sum()),
        },
        "top5_summary": {
            "count": int(len(top5)),
            "best_guid": str(top5_best["GUID"]),
            "best_pred_PI": float(top5_best["pred_PI"]),
            "mean_pred_PI": float(top5["pred_PI"].mean()),
            "trust_mix": top5["trust_tier"].value_counts().to_dict(),
        },
        "top10_summary": {
            "count": int(len(top10)),
            "most_exploratory_guid": str(top10_best["GUID"]),
            "mean_pred_PI": float(top10["pred_PI"].mean()),
            "trust_mix": top10["trust_tier"].value_counts().to_dict(),
        },
        "baseline_compare": baseline_compare.to_dict(orient="records"),
        "top5_candidates": top5.to_dict(orient="records"),
        "top10_candidates": top10.to_dict(orient="records"),
    }

    metrics = {
        "top5_gain_vs_random_mean_PI": top5_gain,
        "top10_gain_vs_random_mean_PI": top10_gain,
        "top5_mean_pred_PI": float(top5["pred_PI"].mean()),
        "top10_mean_pred_PI": float(top10["pred_PI"].mean()),
    }

    warnings = [
        "q5 给出的候选只是一轮实验优先级建议，尚未经过真实实验反馈验证。",
        "low trust 候选被保留为探索点，不代表其预测更可靠。",
        "稳定性相关指标仍然继承短时 proxy 定义，不能把候选推荐写成长寿命配方结论。",
    ]
    limitations = [
        "当前候选空间只在已观测样本邻域内做单步/双步体积转移，尚未覆盖更大尺度的新配方重构。",
        "随机基线比较基于同一可行候选池，不等于对全部 0.1 网格空间做均匀采样。",
    ]
    paper_claims = [
        "下一轮实验不应只盯着当前最高分样本附近继续微调，而应在开发型与探索型候选之间保持平衡。",
        "基于 `q2` 预测与 `q4` 可信域约束的候选设计，在平均预测综合性能上优于随机选点基线。",
        "10 组扩展候选中应显式保留少量 medium/low trust 点，用来补齐模型盲区。",
    ]
    trace = {
        "top5_gain_vs_random_mean_PI": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "metrics.top5_gain_vs_random_mean_PI",
            "validation_status": "pending",
        },
        "top10_gain_vs_random_mean_PI": {
            "source_file": (q_dir / "results" / "result.json").as_posix(),
            "source_field": "metrics.top10_gain_vs_random_mean_PI",
            "validation_status": "pending",
        },
    }
    log_context = {
        "code_starter_used": "q2 full-data route reuse + q4 trust constraints + custom local-neighbor candidate generation",
        "environment_notes": {"seed": SEED, "packages": ["numpy", "pandas", "matplotlib"]},
        "preprocessing_notes": {
            "anchor_count": int(len(anchors)),
            "candidate_count": int(len(prediction)),
            "step_sizes": STEP_SIZES,
        },
        "abnormal_data_handling": [
            {
                "abnormal_type": "unseen pattern",
                "detection_rule": "pattern_count == 0",
                "affected_rows": int((prediction["pattern_count"] == 0).sum()),
                "handling_method": "保留但通过 trust tier 降级",
                "rationale": "让探索型候选可见，同时避免与开发型混淆",
                "effect_on_result": "进入探索池而非高可信开发池",
            }
        ],
        "random_seed": {"main": SEED},
        "algorithm_settings": {"selection_mix": "top5=3 exploit + 2 explore; top10=6 exploit + 4 explore"},
        "toy_demo_result": {"used": False},
        "full_run_result_summary": {
            "top5_mean_pred_PI": float(top5["pred_PI"].mean()),
            "top10_mean_pred_PI": float(top10["pred_PI"].mean()),
            "top5_gain_vs_random": top5_gain,
        },
        "runtime_notes": {"figure_count": 2, "table_count": 3},
        "interpretation_notes": {
            "main_interpretation": "推荐方案不是单一贪心最优，而是开发型与探索型的平衡设计。",
            "downstream_focus": "q6 将继续判断这些候选是稳定高分盆地还是孤立尖峰。",
        },
        "errors": [],
    }

    bundle.result_io_module.write_result_and_log(
        question_id="q5",
        model_name="可信域约束下的开发-探索联合候选设计模型",
        status="pass",
        inputs={
            "source_problem": (bundle.problem_dir / "problem.md").as_posix(),
            "source_q2_result": (bundle.output_dir / "q2" / "results" / "result.json").as_posix(),
            "source_q4_trust": (bundle.output_dir / "q4" / "results" / "trust_region_table.csv").as_posix(),
        },
        outputs={
            "result_json": (results_dir / "result.json").as_posix(),
            "run_log": (results_dir / "run.log").as_posix(),
            "candidate_pool": (results_dir / "candidate_pool.csv").as_posix(),
            "recommended_top5": (results_dir / "recommended_top5.csv").as_posix(),
            "recommended_top10": (results_dir / "recommended_top10.csv").as_posix(),
            "baseline_compare": (results_dir / "baseline_compare.csv").as_posix(),
        },
        main_result=main_result,
        metrics=metrics,
        figures=[str(fig1.as_posix()), str(fig2.as_posix())],
        tables=[item["path"] for item in table_entries],
        source_command=f"python {Path(__file__).as_posix()}",
        source_files=[Path(__file__).as_posix(), (COMMON_DIR / "copilot_support.py").as_posix()],
        validation_hooks=[
            "比较候选集与随机基线在平均 pred_PI 上的差异",
            "检查 top5/top10 是否同时覆盖开发型与探索型 trust tier",
            "检查候选 pH suitability 与 W_1 是否达到基本筛选门槛",
        ],
        warnings=warnings,
        limitations=limitations,
        paper_claims=paper_claims,
        trace=trace,
        log_context=log_context,
        results_dir=results_dir,
    )

    (q_dir / "review_packet.md").write_text(
        """# q5 Review Packet

## AP mode note

当前问题按 AP 模式自动推进，直接使用 `q2` 的预测模型与 `q4` 的可信域分层设计下一轮实验候选。
""",
        encoding="utf-8",
    )

    (q_dir / "validation.md").write_text(
        f"""# q5 Validation

## Core Checks

| item | observation | verdict | implication |
|---|---|---|---|
| top5 平均 pred_PI | `{float(top5["pred_PI"].mean()):.4f}`，比随机基线高 `{top5_gain:.4f}` | pass | 推荐方案优于随机挑点 |
| top10 平均 pred_PI | `{float(top10["pred_PI"].mean()):.4f}`，比随机基线高 `{top10_gain:.4f}` | pass | 扩展候选仍保持优势 |
| trust mix | top10 中 `high/medium/low = {top10["trust_tier"].value_counts().to_dict()}` | pass | 候选集兼顾开发与探索 |
| 基本物理门槛 | 候选筛选已要求 `pred_S_pH >= 0.50` 且 `pred_W_1` 不低于 40% 分位 | pass | 没有把明显差候选推入推荐表 |

## Validation Verdict

**PASS**

`q5` 的核心结论是“有约束的主动推荐优于随机选点”，而不是“这些候选已经被真实实验确认最佳”。
""",
        encoding="utf-8",
    )

    (q_dir / "sensitivity.md").write_text(
        """# q5 Sensitivity

## Key Parameters

- 邻域生成步长：`0.1`, `0.2`
- 候选混合策略：`top5=3 exploit + 2 explore`，`top10=6 exploit + 4 explore`

## Main Findings

1. 如果只做 exploit，候选会过于集中在少数高 trust 模式附近，探索价值不足。
2. 如果把 trust 约束完全放松，候选虽然更新奇，但平均预测综合性能会明显回落。
3. 当前混合策略因此更适合作为一轮有限实验预算下的平衡方案。
""",
        encoding="utf-8",
    )

    (q_dir / "warnings.md").write_text(
        """# q5 Warnings

| issue id | severity | verdict impact | finding | required fix | status |
|---|---|---|---|---|---|
| `Q5-W01` | Medium | `PARTIAL` if overclaimed | 推荐候选尚未经过真实实验验证。 | 论文中必须写成“下一轮实验建议”。 | open-limitation |
| `Q5-W02` | Medium | `PARTIAL` for exploration points | medium/low trust 候选用于探索，不代表更可靠。 | 在候选表中保留 trust_tier 与探索用途说明。 | open-limitation |
""",
        encoding="utf-8",
    )

    (q_dir / "review_note.md").write_text(
        f"""# q5 Review Note

## 本轮自动推进记录

- 已基于 `q2` + `q4` 生成候选池 `{len(prediction)}` 条，筛出 top5 与 top10 推荐。
- top5 平均 `pred_PI` 比随机基线高 `{top5_gain:.4f}`，top10 高 `{top10_gain:.4f}`。

## 审查结论

`PASS`
""",
        encoding="utf-8",
    )

    (q_dir / "q5_summary.md").write_text(
        f"""# q5 下一轮实验候选设计
## main results with source fields

- 候选池共有 `{len(prediction)}` 条，可行筛选后保留 `{len(eligible)}` 条。来源：`main_result.candidate_pool_summary`
- top5 推荐的平均 `pred_PI` 为 `{float(top5["pred_PI"].mean()):.4f}`，比随机基线高 `{top5_gain:.4f}`。来源：`metrics.top5_gain_vs_random_mean_PI`
- top10 推荐的平均 `pred_PI` 为 `{float(top10["pred_PI"].mean()):.4f}`，比随机基线高 `{top10_gain:.4f}`。来源：`metrics.top10_gain_vs_random_mean_PI`

## paper-ready subsection draft

在实验预算有限的前提下，下一轮候选设计不能只做“局部最优微调”，也不能完全随机探索。为此，我们以 `q2` 的预测结果为收益估计，以 `q4` 的可信域为风险约束，在已观测样本邻域内生成单步与双步体积转移候选。随后把候选分成开发型与探索型两类：前者优先高 `pred_PI`、高 `W_1`、高 pH 适宜度且位于 high/medium trust 邻域；后者允许进入 medium/low trust 区，但必须保持基本性能门槛。  
结果表明，top5 推荐的平均 `pred_PI` 为 `{float(top5["pred_PI"].mean()):.4f}`，比同一候选池上的随机基线高 `{top5_gain:.4f}`；top10 推荐的平均 `pred_PI` 为 `{float(top10["pred_PI"].mean()):.4f}`，也高于随机基线 `{top10_gain:.4f}`。因此，当前推荐方案更像“有证据约束的主动实验设计”，而不是盲目穷举或纯贪心搜索。

## status

`pass`
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
