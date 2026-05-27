# Rubrics

These rubrics support `v1.2-alpha` review and self-check. They are not an active stage machine and they do not control startup, topic selection, or legacy scoring state.

Use them for:
- per-question planning self-check
- per-question verification self-check
- final integration self-check
- paper and final review self-check

## 1. Per-Question Plan

Review `solution_plan.md`, `analysis.md`, `candidates.md`, `model.md`, `assumptions.md`, `notation.md`, and `data_recon.md`.

| Dimension | What good looks like |
|---|---|
| problem fit | the question goal, constraints, and expected outputs are explicit |
| candidate quality | baseline, main, and alternative are all meaningful and structurally distinct enough |
| assumption quality | assumptions are explicit, scoped, and reviewable |
| notation quality | symbols and units are coherent with both the model and the data |
| build readiness | the plan can realistically be implemented and verified in the locked language |

## 2. Per-Question Verification

Review `result.json`, `validation.md`, and `sensitivity.md`.

| Dimension | What good looks like |
|---|---|
| correctness checks | constraints, boundary cases, and sanity checks are covered |
| comparison quality | there is a baseline or cross-method comparison where it matters |
| sensitivity quality | key parameters, ranges, and changes are reported clearly |
| failure honesty | failure cases and instability are described instead of hidden |
| evidence traceability | major numbers can be traced into machine-readable or documented evidence |

## 3. Per-Question Summary

Review `q_i_summary.md`.

| Dimension | What good looks like |
|---|---|
| result clarity | the question result is easy to state and understand |
| evidence boundary | claims stay inside what the question actually established |
| interpretation quality | numbers are translated into meaning |
| dependency clarity | reused upstream results are acknowledged explicitly |
| paper readiness | the summary can be lifted into the final paper without inventing new claims |

## 4. Final Integration

Review `final_results.md`, `final_figures_index.md`, `final_tables_index.md`, `traceability.md`, and `locked_numbers.md`.

| Dimension | What good looks like |
|---|---|
| cross-question coherence | question results do not contradict each other |
| figure and table readiness | each reusable visual has a clear source and role |
| traceability quality | major claims map back to question evidence cleanly |
| locked-number discipline | the quantitative paper boundary is explicit |
| integration quality | the project-level story is stronger than a pile of separate question notes |

## 5. Paper Review

Review `paper.md`, `paper.tex`, `paper.pdf`, `review_report.md`, `anonymity_report.md`, and `quality_report.md`.

| Dimension | What good looks like |
|---|---|
| structure and coverage | the paper covers the problem, method, results, verification, and discussion clearly |
| quantitative discipline | hard numbers come from locked evidence only |
| figure and table quality | visuals are readable, cited, and not misleading |
| notation and unit consistency | symbols, units, and names stay stable throughout |
| review readiness | obvious anonymity, citation, and PDF issues have been checked |

## Competition-Specific Use

- `competitions/*/winning_patterns.md` can inspire stronger structure or phrasing.
- `competitions/*/anti_patterns.md` can sharpen final review.
- `competitions/*/abstract_template.md` and `paper_skeleton.md` can guide paper assembly.

These assets inform judgment but do not replace evidence.
