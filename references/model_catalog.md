# Model Catalog

## Purpose

This file is the active modeling knowledge layer for Stage 2 Per-Question Plan. Use it to build `workspace/output/q*/candidates.md` and `workspace/output/q*/model.md`.

It is a knowledge reference, not an execution tool. It does not require any script or hidden state file.

## Active Inputs And Outputs

Read:

```text
workspace/output/question_index.md
workspace/output/q*/analysis.md
workspace/output/q*/data_recon.md
workspace/output/q*/assumptions.md
```

Write or update:

```text
workspace/output/q*/candidates.md
workspace/output/q*/model.md
workspace/output/q*/review_note.md      # AP mode or risky route
workspace/output/q*/warnings.md         # gaps, strong assumptions, infeasible routes
```

## Problem Type To Model Family Map

| Problem type | Good first families | Useful competitors | Typical evidence to check |
|---|---|---|---|
| Optimization / allocation / scheduling | linear programming, integer programming, nonlinear programming | dynamic programming, robust optimization, metaheuristics | feasibility, constraint satisfaction, objective sensitivity |
| Prediction / forecasting | regression, time series, grey prediction | machine learning predictors, ensemble prediction | train/test split, error metric, residual pattern |
| Evaluation / ranking | AHP, entropy weight, TOPSIS | fuzzy evaluation, PCA, factor analysis | indicator direction, weight stability, rank sensitivity |
| Classification / recognition | logistic regression, SVM, tree models | neural networks, kNN, naive Bayes | confusion matrix, class balance, threshold sensitivity |
| Clustering / segmentation | k-means, hierarchical clustering | DBSCAN, Gaussian mixture, spectral clustering | cluster validity, interpretability, robustness to scaling |
| Simulation / stochastic process | Monte Carlo, discrete-event simulation | system dynamics, agent-based model | random seed control, scenario design, convergence |
| Network / routing / graph | shortest path, max flow, min-cost flow | MST, TSP/VRP heuristics, centrality | graph construction, edge meaning, complexity |
| Statistical inference | descriptive statistics, hypothesis test, correlation/regression | ANOVA, distribution fitting, Bayesian update | assumptions, confidence intervals, sample size |
| Dynamics / diffusion / physical process | ODE, PDE, difference equations | compartment model, cellular automata | units, boundary conditions, stability |
| Signal / image / spatiotemporal data | FFT, wavelet, filtering | feature engineering, spatiotemporal regression | sampling rate, denoising effect, feature validity |
| Decision / policy / strategy | decision tree, game theory, MDP | multi-criteria decision, scenario policy | payoff definition, scenario coverage, risk tradeoff |

## Candidate Model Selection Method

For each `q*`, generate at least three structurally different candidates when the problem allows it:

| Candidate role | Purpose | Example |
|---|---|---|
| Baseline | Simple and auditable lower bound | manual formula, greedy rule, ordinary least squares, simple TOPSIS |
| Main model | Best balance of fit, interpretability, and implementability | mixed-integer model, ARIMA + regression, entropy-TOPSIS, random forest |
| Robust alternative | Tests whether conclusions depend on one modeling choice | robust optimization, bootstrap ranking, alternative classifier, scenario simulation |

Record rejected candidates in `candidates.md` with a concrete reason:

```text
candidate | kept/rejected | reason | data need | compute risk | paper interpretability
```

Reject a candidate when:

- required data are absent from `workspace/problem/` or cannot be reconstructed;
- assumptions are stronger than the problem supports;
- implementation would be too fragile for the available time;
- the model cannot produce traceable fields for `result.json`;
- the explanation would be weaker than a simpler model with similar performance.

## Model Families

### Optimization

- Linear programming: use when objective and constraints can be expressed linearly; strong for allocation and production planning.
- Integer or binary programming: use when decisions are discrete, selected, assigned, opened, routed, or scheduled.
- Nonlinear programming: use when objective or constraints include nonlinear response, saturation, risk, or physics.
- Multi-objective programming: use when tradeoffs are part of the question; report Pareto or weighted compromise clearly.
- Dynamic programming: use when decisions are sequential and have overlapping substructure.
- Robust or stochastic programming: use when parameters are uncertain and worst-case or distribution-aware decisions matter.
- Heuristics and metaheuristics: use for large combinatorial spaces; must include baseline comparison and reproducibility notes.

### Prediction

- Regression: interpretable baseline for numeric response.
- Time series: use trend, seasonality, autocorrelation, or temporal dependence.
- Grey prediction: acceptable for small-sample monotone systems, but validate carefully.
- Machine learning predictors: use when nonlinear features and enough samples exist.
- Ensemble prediction: use when multiple weak models offer complementary errors.

### Evaluation And Ranking

- AHP: useful for expert-structured criteria; document pairwise consistency.
- Entropy weight: useful when objective variation in indicators should drive weights.
- TOPSIS: useful for distance-to-ideal ranking; verify indicator normalization.
- Fuzzy evaluation: useful when criteria are qualitative or interval-like.
- PCA or factor analysis: useful when indicators are correlated and dimension reduction is justified.

### Classification

- Logistic regression: interpretable baseline for binary or multiclass with engineered features.
- SVM: useful for medium-size feature spaces and margin-based separation.
- Tree models: useful for nonlinear rules and feature importance.
- Neural networks: use only when data volume and validation are sufficient.
- kNN or naive Bayes: simple baselines for classification sanity checks.

### Simulation

- Monte Carlo: quantify uncertainty and scenario distributions.
- System dynamics: model feedback loops over time.
- Cellular automata: model local rules and spatial evolution.
- Agent-based model: model heterogeneous actors and interactions.
- Discrete-event simulation: model queues, service systems, and event timelines.

### Graph And Network

- Shortest path: route, transfer, or minimal-cost path.
- Max flow and min-cost flow: capacity-constrained transport or assignment.
- MST: minimal connection network.
- Centrality and community detection: influence, importance, or structure discovery.
- TSP/VRP: routing with visit constraints; usually needs heuristics for large instances.

### Statistics And Dynamics

- Hypothesis tests and confidence intervals: support claims and comparisons.
- Distribution fitting: describe uncertain variables or generate scenarios.
- ODE/PDE/difference equations: describe continuous or discrete physical evolution.
- FFT and wavelet methods: extract frequency or multiscale signal structure.
- Game theory and MDP: reason about strategic or sequential decisions.

## Hybrid Model Patterns

Good papers often combine a transparent baseline with a stronger model:

| Hybrid pattern | Use when | Example output |
|---|---|---|
| Prediction + optimization | future quantity drives allocation | predicted demand feeds integer program |
| Evaluation + clustering | alternatives need grouping and ranking | cluster first, rank within groups |
| Simulation + policy | policy must be stress-tested | scenario simulation compares rules |
| Graph + optimization | network structure constrains decisions | shortest path candidates enter allocation model |
| Statistical inference + mechanistic model | parameters need estimation | regression estimates coefficients for ODE |

## Plan Checklist

Before Stage 3 Build, `model.md` should answer:

- What is optimized, predicted, ranked, classified, simulated, or inferred?
- What are the variables, parameters, units, and domains?
- What assumptions are necessary and where are they recorded?
- What is the baseline or sanity-check method?
- What exact fields will appear in `result.json`?
- Which constraints or metrics will be checked in `validation.md`?
- Which parameters will be varied in `sensitivity.md`?
- What conclusion would make the model unusable?

## Manual And AP Behavior

Manual mode: after `candidates.md` and `model.md` are written, pause before Build and list file paths only.

AP mode: continue only when `review_note.md` records why the selected model is acceptable and `warnings.md` records unresolved risk.
