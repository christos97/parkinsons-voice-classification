# Chapter 5: Experimental Design

## 5.1 Overview

This chapter details the experimental design, including the 2×2 factorial structure, cross-validation protocols, and evaluation procedures. The design prioritizes methodological rigor over performance optimization.

## 5.2 Research Questions

The experiments address the following research questions:

1. **RQ1:** How do classical ML models perform on PD voice classification?
2. **RQ2:** Does feature set extension (47 → 78) improve classification performance?
3. **RQ3:** Does class weighting improve performance on imbalanced datasets?
4. **RQ4:** How do results compare between Dataset A (grouped CV) and Dataset B (standard CV)?

## 5.3 Experimental Matrix

### 5.3.1 2×2 Factorial Design

| Condition | Features | Weighting | Output Directory |
|-----------|----------|-----------|-----------------|
| **C1** | Baseline (47) | None | `baseline/baseline/` |
| **C2** | Extended (78) | None | `baseline/extended/` |
| **C3** | Baseline (47) | Balanced | `weighted/baseline/` |
| **C4** | Extended (78) | Balanced | `weighted/extended/` |

### 5.3.2 Models Under Evaluation

Each condition evaluates three models:

| Model | Abbreviation | Parameters |
|-------|--------------|------------|
| Logistic Regression | LR | C=1.0, max_iter=1000 |
| Support Vector Machine (RBF) | SVM | C=1.0, gamma='scale' |
| Random Forest | RF | n_estimators=100, max_depth=10 |

### 5.3.3 Datasets

| Dataset | Task(s) | CV Strategy |
|---------|---------|-------------|
| Dataset A (MDVR-KCL) | ReadText, SpontaneousDialogue | Grouped Stratified 5-Fold |
| Dataset B (PD_SPEECH) | N/A | Stratified 5-Fold |

## 5.4 Cross-Validation Protocols

### 5.4.1 Dataset A: Grouped Stratified K-Fold

```
Subject Pool (37 subjects)
├── Fold 1: Train on 30 subjects, Test on 7 subjects
├── Fold 2: Train on 30 subjects, Test on 7 subjects
├── Fold 3: Train on 30 subjects, Test on 7 subjects
├── Fold 4: Train on 30 subjects, Test on 7 subjects
└── Fold 5: Train on 29 subjects, Test on 8 subjects

Key constraint: All recordings from a subject appear in ONE fold only
```

This prevents **subject identity leakage**, which would occur if recordings from the same subject appeared in both training and test sets.

### 5.4.2 Dataset B: Stratified K-Fold

```
Sample Pool (756 samples)
├── Fold 1: Train on ~605 samples, Test on ~151 samples
├── Fold 2: Train on ~605 samples, Test on ~151 samples
...
└── Fold 5: Train on ~605 samples, Test on ~151 samples

Key constraint: Class proportions maintained across folds
```

**Caveat:** Without subject identifiers, potential subject overlap cannot be controlled.

## 5.5 Evaluation Metrics

### 5.5.1 Primary Metric

**ROC-AUC** is the primary metric because:
- Threshold-independent evaluation
- Robust to class imbalance
- Standard in clinical ML literature

### 5.5.2 Secondary Metrics

| Metric | Purpose |
|--------|---------|
| Accuracy | Overall performance (reference only) |
| Precision | False positive analysis |
| Recall | False negative analysis (critical for screening) |
| F1 Score | Balance between precision and recall |

### 5.5.3 Statistical Reporting

All metrics reported as: **mean ± std** across 5 folds

## 5.6 Experimental Procedure

### 5.6.1 Step-by-Step Protocol

```
1. Feature Extraction (Dataset A only)
   └── pvc-extract --task all
   
2. For each condition (C1-C4):
   └── For each model (LR, SVM, RF):
       └── For each dataset/task:
           └── 5-fold cross-validation
               ├── Fit scaler on train
               ├── Transform train and test
               ├── Fit model on train
               ├── Predict on test
               └── Compute metrics
               
3. Aggregate results
   └── Mean ± std across folds
```

### 5.6.2 Feature Extraction Settings

Extracted features stored in:
- `outputs/features/baseline/` (47 features)
- `outputs/features/extended/` (78 features)

### 5.6.3 Random Seed

All experiments use `random_state=42` for reproducibility.

## 5.7 Implementation

### 5.7.1 CLI Commands

```bash
# Feature extraction (both baseline and extended)
pvc-extract --task all

# Run experiments (all conditions)
pvc-experiment
```

### 5.7.2 Output Structure

```
outputs/
├── features/
│   ├── baseline/
│   │   ├── features_readtext.csv
│   │   └── features_spontaneousdialogue.csv
│   └── extended/
│       ├── features_readtext.csv
│       └── features_spontaneousdialogue.csv
│
└── results/
    ├── baseline/          # Unweighted
    │   ├── baseline/      # 47 features
    │   └── extended/      # 78 features
    └── weighted/          # Class-weighted
        ├── baseline/      # 47 features
        └── extended/      # 78 features
```

## 5.8 Expected Outcomes

### 5.8.1 Hypotheses

| Hypothesis | Rationale |
|------------|-----------|
| H1: Extended features improve ROC-AUC | Additional MFCC statistics capture speech variability |
| H2: Class weighting improves recall | Balances penalty for misclassifying minority class |
| H3: Dataset B shows higher performance | Larger sample size and potential subject leakage |
| H4: RF outperforms LR and SVM | Handles non-linear relationships and feature interactions |

### 5.8.2 Analysis Plan

1. **Within-condition comparison:** Compare models within each condition
2. **Feature ablation:** Compare Condition 1 vs 2 and Condition 3 vs 4
3. **Weighting effect:** Compare Condition 1 vs 3 and Condition 2 vs 4
4. **Cross-dataset comparison:** Compare Dataset A vs Dataset B (with caveats)

## 5.9 Limitations of Design

### 5.9.1 Acknowledged Constraints

1. **Small sample size (Dataset A):** High variance in fold-level metrics
2. **No subject IDs (Dataset B):** Cannot guarantee subject separation
3. **No hyperparameter tuning:** Fixed parameters to avoid overfitting
4. **No external validation:** Results may not generalize

### 5.9.2 Mitigation Strategies

- Report confidence intervals via standard deviation
- Clearly document assumptions and caveats
- Prioritize relative comparisons over absolute performance claims

## 5.10 Summary

The experimental design implements:

- **2×2 factorial structure** (features × weighting)
- **Grouped CV for Dataset A** (prevents leakage)
- **5 metrics** reported as mean ± std
- **Reproducible pipeline** via CLI commands
