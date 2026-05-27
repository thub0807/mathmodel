# Model Catalog

This catalog supports `per_question_plan.md` in `v1.2-alpha`. Use it during Stage 2 when writing `candidates.md`, `model.md`, and `solution_plan.md`.

## How To Use This Catalog

For each question:
- identify the task shape
- list a baseline model
- list a main model
- list an alternative model
- prefer candidates that differ structurally
- select a model that can be implemented and validated with the locked language

Do not treat this file as a scoring state machine or as a competition-startup guide.

## Quick Mapping

| Problem signal | Common model families |
|---|---|
| optimize, allocate, schedule, route | optimization |
| forecast, trend, time series | prediction |
| evaluate, rank, score | evaluation |
| classify, detect, identify | classification |
| simulate, what-if, uncertainty | simulation |
| network, path, flow | graph |
| distribution, significance, inference | statistics |
| dynamic process over time | dynamical systems |
| frequency, signal, spectrum | signal processing |
| strategic interaction, sequential decision | decision models |

## 1. Optimization

### Linear Programming
- Fit: linear objective and linear constraints
- Typical tools: `scipy.optimize`, `cvxpy`, `pulp`
- Good baseline when the structure is mostly linear

### Integer and Mixed-Integer Programming
- Fit: yes/no, count, route, assignment, selection
- Typical tools: `cvxpy`, `pulp`, `pyomo`, `ortools`
- Good when discrete choices matter and exact structure is still manageable

### Nonlinear Programming
- Fit: smooth nonlinear objective or constraints
- Typical tools: `scipy.optimize`, `pyomo`
- Good when realism requires nonlinear behavior

### Multi-Objective Optimization
- Fit: conflicting goals such as cost, quality, risk, or fairness
- Typical tools: weighted objective, epsilon-constraint, `pymoo`, `deap`
- Good main or alternative candidate when the paper needs trade-off analysis

### Dynamic Programming
- Fit: staged decisions with state transitions
- Typical tools: custom Python implementation
- Good when optimal substructure is clear

### Heuristics and Metaheuristics
- Examples: GA, PSO, SA, ACO, tabu search
- Fit: large combinatorial or nonconvex problems
- Typical tools: `deap`, `pygad`, `pyswarms`, custom implementations
- Good alternative when exact optimization is too slow

### Robust or Stochastic Optimization
- Fit: uncertainty enters parameters or scenarios
- Typical tools: `cvxpy`, `pyomo`, custom scenario models
- Good when sensitivity alone is not enough and uncertainty belongs inside the model

## 2. Prediction

### Regression
- Examples: linear, polynomial, ridge, lasso, elastic net
- Fit: interpretable predictive relationships
- Typical tools: `sklearn.linear_model`

### Classical Time Series
- Examples: ARIMA, SARIMA, exponential smoothing
- Fit: structured temporal signals
- Typical tools: `statsmodels`

### Grey Forecasting
- Examples: GM(1,1), GM(1,N)
- Fit: small-sample forecasting with limited information
- Good baseline or comparison model in many modeling papers

### Machine Learning Prediction
- Examples: random forest, XGBoost, LightGBM, LSTM
- Fit: nonlinear, feature-rich, or large-data prediction tasks
- Typical tools: `sklearn`, `xgboost`, `lightgbm`, `tensorflow`, `torch`

### Ensemble Forecasting
- Fit: when single models are unstable or biased in different ways
- Good main candidate when the paper needs a stronger predictive story plus comparison evidence

## 3. Evaluation and Ranking

### AHP
- Fit: structured subjective weighting
- Good when expert judgment matters

### Entropy Weighting
- Fit: objective weighting from data variability
- Good complement to AHP

### TOPSIS
- Fit: distance-to-ideal ranking
- Good for final ranking tables

### Fuzzy Comprehensive Evaluation
- Fit: vague or fuzzy criteria boundaries

### PCA and Factor Models
- Fit: dimensionality reduction, latent structure, composite scoring

### Clustering-Based Evaluation
- Fit: grouping entities before ranking or interpretation

## 4. Classification

### Logistic Regression
- Good interpretable baseline

### SVM
- Good for margin-based classification with smaller feature sets

### Tree Ensembles
- Examples: decision tree, random forest, GBDT
- Good main candidate for tabular classification

### Neural Networks
- Good when feature interactions or representation learning are central

### Naive Bayes and KNN
- Good sanity-check baselines

## 5. Simulation

### Monte Carlo
- Fit: uncertainty propagation, scenario evaluation, randomized estimation

### System Dynamics
- Fit: feedback loops, stocks and flows

### Cellular Automata
- Fit: local interaction and spatial rules

### Agent-Based Modeling
- Fit: heterogeneous actors with rule-based behavior

### Discrete Event Simulation
- Fit: queueing, process timing, operational flow

## 6. Graph Models

### Shortest Path
- Dijkstra, Floyd, A*

### Flow Models
- maximum flow, minimum-cost flow

### Spanning Trees
- MST for network construction or reduction

### Centrality and Community Detection
- Fit: influence, importance, structure in networks

### TSP and VRP
- Fit: route design and delivery planning

## 7. Statistics

### Descriptive Statistics
- always useful for first-pass understanding

### Hypothesis Testing
- t-test, chi-square, nonparametric tests

### ANOVA
- compare groups or treatments

### Correlation and Regression Diagnostics
- check relationships and fit assumptions

### Distribution Fitting
- useful before Monte Carlo or uncertainty modeling

## 8. Dynamical Systems

### ODE Models
- examples: SIR, growth, competition, resource dynamics

### PDE Models
- fit diffusion, transport, or field evolution problems

### Difference Equations
- fit discrete-time dynamics

## 9. Signal Processing

### FFT
- fit periodicity and spectrum inspection

### Wavelets
- fit multiscale or nonstationary signals

## 10. Decision Models

### Game Theory
- fit strategic interaction

### Decision Analysis Trees
- fit expected utility or scenario decisions

### MDP and Sequential Decision
- fit stateful policy optimization

## Hybrid Patterns

Common strong combinations:
- AHP + entropy weight + TOPSIS
- ARIMA + grey forecasting + ML ensemble
- optimization + simulation
- prediction + evaluation
- Monte Carlo + sensitivity analysis

## Candidate Checklist

For each candidate in `candidates.md`, record:
- model family
- fit to the question
- implementation path in the locked language
- expected validation route
- expected failure mode
- reason to keep or reject it
