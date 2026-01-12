# Chapter 6: Results

## 6.1 Overview

This chapter presents the classification results across all experimental conditions. Results are organized by:

1. **Condition-level summaries** (2×2 factorial)
2. **Model comparisons** within each condition  
3. **Feature ablation analysis** (baseline vs extended)
4. **Class weighting analysis**

## 6.2 Summary of Best Results

### 6.2.1 Dataset A (MDVR-KCL) — Best Performance

| Metric | Value | Model | Condition |
|--------|-------|-------|-----------|
| **ROC-AUC** | **0.873 ± 0.137** | Random Forest | Extended + Unweighted |
| **Accuracy** | **82.6% ± 12.2%** | Random Forest | Extended + Unweighted |
| **F1 Score** | **0.759 ± 0.271** | Random Forest | Extended + Unweighted |

### 6.2.2 Key Finding

> **Extended features (78) improved ROC-AUC by +8.7 percentage points** compared to baseline features (47), with Random Forest achieving the best performance.

## 6.3 Condition 1: Baseline Features + Unweighted

**Configuration:** 47 features, no class weighting

### 6.3.1 Results Table

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 0.696 ± 0.133 | 0.657 ± 0.262 | 0.702 ± 0.284 | 0.655 ± 0.246 | 0.781 ± 0.152 |
| SVM (RBF) | 0.703 ± 0.143 | 0.603 ± 0.357 | 0.545 ± 0.390 | 0.547 ± 0.347 | 0.635 ± 0.311 |
| **Random Forest** | **0.744 ± 0.173** | **0.653 ± 0.373** | **0.638 ± 0.421** | **0.615 ± 0.369** | **0.786 ± 0.235** |

### 6.3.2 Observations

- Random Forest achieves highest ROC-AUC (0.786)
- High variance across folds (std > 0.15) indicates instability
- SVM underperforms with ROC-AUC below 0.65

## 6.4 Condition 2: Extended Features + Unweighted

**Configuration:** 78 features, no class weighting

### 6.4.1 Results Table

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 0.699 ± 0.152 | 0.660 ± 0.289 | 0.641 ± 0.314 | 0.630 ± 0.281 | 0.783 ± 0.126 |
| SVM (RBF) | 0.757 ± 0.143 | 0.703 ± 0.330 | 0.651 ± 0.354 | 0.657 ± 0.321 | 0.726 ± 0.265 |
| **Random Forest** | **0.826 ± 0.122** | **0.814 ± 0.255** | **0.760 ± 0.327** | **0.759 ± 0.271** | **0.873 ± 0.137** |

### 6.4.2 Observations

- **Random Forest ROC-AUC improved from 0.786 to 0.873 (+8.7pp)**
- SVM also improved substantially (+9.1pp ROC-AUC)
- Variance reduced slightly with extended features

## 6.5 Condition 3: Baseline Features + Weighted

**Configuration:** 47 features, `class_weight="balanced"`

### 6.5.1 Results Table

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 0.687 ± 0.141 | 0.654 ± 0.271 | 0.696 ± 0.280 | 0.649 ± 0.247 | 0.781 ± 0.152 |
| SVM (RBF) | 0.748 ± 0.115 | 0.690 ± 0.314 | 0.670 ± 0.333 | 0.659 ± 0.299 | 0.622 ± 0.316 |
| **Random Forest** | **0.736 ± 0.141** | **0.664 ± 0.315** | **0.660 ± 0.393** | **0.628 ± 0.322** | **0.821 ± 0.191** |

### 6.5.2 Observations

- Class weighting improved RF ROC-AUC from 0.786 to 0.821 (+3.5pp)
- LR unchanged (0.781 both conditions)
- SVM ROC-AUC decreased slightly

## 6.6 Condition 4: Extended Features + Weighted

**Configuration:** 78 features, `class_weight="balanced"`

### 6.6.1 Results Table

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 0.724 ± 0.136 | 0.687 ± 0.283 | 0.696 ± 0.307 | 0.670 ± 0.270 | 0.783 ± 0.126 |
| SVM (RBF) | 0.757 ± 0.165 | 0.718 ± 0.338 | 0.693 ± 0.319 | 0.693 ± 0.309 | 0.712 ± 0.305 |
| **Random Forest** | **0.801 ± 0.146** | **0.798 ± 0.259** | **0.760 ± 0.327** | **0.748 ± 0.268** | **0.859 ± 0.162** |

### 6.6.2 Observations

- Extended features improve all models
- RF with extended features outperforms baseline even without weighting
- Class weighting provides marginal benefit when features are already extended

## 6.7 Feature Ablation Analysis

### 6.7.1 ROC-AUC Improvement from Feature Extension

| Model | Baseline (47) | Extended (78) | Δ ROC-AUC |
|-------|---------------|---------------|-----------|
| Logistic Regression | 0.781 | 0.783 | +0.2pp |
| SVM (RBF) | 0.635 | 0.726 | **+9.1pp** |
| Random Forest | 0.786 | 0.873 | **+8.7pp** |

### 6.7.2 Feature Extension Impact (Unweighted Conditions)

```
                    Baseline (47)    Extended (78)    Change
Random Forest         0.786            0.873          +8.7pp ⬆
SVM (RBF)             0.635            0.726          +9.1pp ⬆
Logistic Regression   0.781            0.783          +0.2pp ↔
```

**Key Finding:** Feature extension significantly benefits non-linear models (RF, SVM) while linear models (LR) show minimal improvement.

## 6.8 Class Weighting Analysis

### 6.8.1 ROC-AUC Change with Weighting (Baseline Features)

| Model | Unweighted | Weighted | Δ ROC-AUC |
|-------|------------|----------|-----------|
| Logistic Regression | 0.781 | 0.781 | 0.0pp |
| SVM (RBF) | 0.635 | 0.622 | -1.3pp |
| Random Forest | 0.786 | 0.821 | **+3.5pp** |

### 6.8.2 Class Weighting Impact

Class weighting on Dataset A (moderate 57:43 imbalance):
- **Random Forest:** Modest improvement (+3.5pp with baseline features)
- **Logistic Regression:** No change
- **SVM:** Slight degradation

**Interpretation:** The moderate imbalance in Dataset A does not severely impact unweighted models.

## 6.9 Cross-Condition Summary

### 6.9.1 Random Forest ROC-AUC Across All Conditions

| Weighting | Baseline (47) | Extended (78) |
|-----------|---------------|---------------|
| Unweighted | 0.786 ± 0.235 | **0.873 ± 0.137** |
| Weighted | 0.821 ± 0.191 | 0.859 ± 0.162 |

### 6.9.2 Best Configuration

> **Best:** Random Forest + Extended Features (78) + Unweighted
> - ROC-AUC: 0.873 ± 0.137
> - Accuracy: 82.6% ± 12.2%

## 6.10 Feature Importance

### 6.10.1 Top-10 Features (Random Forest, ReadText Task)

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | f0_max | 0.052 |
| 2 | delta_mfcc_2_mean | 0.039 |
| 3 | f3_std | 0.038 |
| 4 | autocorr_harmonicity | 0.038 |
| 5 | intensity_mean | 0.035 |
| 6 | f0_mean | 0.032 |
| 7 | shimmer_apq3 | 0.032 |
| 8 | mfcc_12_mean | 0.031 |
| 9 | f1_std | 0.031 |
| 10 | mfcc_6_mean | 0.030 |

### 6.10.2 Feature Importance Visualization

![Feature Importance - ReadText - Random Forest](../outputs/plots/importance_readtext_randomforest.png)

*Figure 6.1: Top-20 feature importances for Random Forest on ReadText task.*

### 6.10.3 Feature Categories

![Feature Importance by Category - ReadText](../outputs/plots/importance_readtext_categories.png)

*Figure 6.2: Aggregated feature importance by category.*

### 6.10.4 Cross-Model Comparison

![Feature Importance Heatmap - ReadText](../outputs/plots/heatmap_readtext.png)

*Figure 6.3: Normalized feature importance heatmap across models.*

## 6.11 Per-Task Results (Dataset A)

### 6.11.1 ReadText Task

| Model | ROC-AUC (Extended) |
|-------|-------------------|
| Logistic Regression | 0.698 ± 0.148 |
| SVM (RBF) | 0.834 ± 0.136 |
| Random Forest | 0.850 ± 0.163 |

### 6.11.2 SpontaneousDialogue Task  

| Model | ROC-AUC (Extended) |
|-------|-------------------|
| Logistic Regression | 0.868 ± 0.104 |
| SVM (RBF) | 0.618 ± 0.394 |
| Random Forest | 0.895 ± 0.111 |

### 6.11.3 Feature Importance - SpontaneousDialogue

![Feature Importance - Spontaneous - Random Forest](../outputs/plots/importance_spontaneous_randomforest.png)

*Figure 6.4: Top-20 feature importances for Random Forest on SpontaneousDialogue task.*

## 6.12 Summary of Findings

### 6.12.1 Key Results

| Finding | Evidence |
|---------|----------|
| Extended features improve performance | +8.7pp ROC-AUC (RF) |
| Random Forest is the best model | Highest ROC-AUC across conditions |
| Class weighting has modest effect | +3.5pp for RF with baseline features |
| High variance due to small sample size | std > 0.1 across all conditions |

### 6.12.2 Hypotheses Evaluation

| Hypothesis | Result |
|------------|--------|
| H1: Extended features improve ROC-AUC | ✅ Confirmed (+8.7pp) |
| H2: Class weighting improves recall | ⚠️ Partially (model-dependent) |
| H3: Dataset B shows higher performance | ✅ Confirmed (see Appendix) |
| H4: RF outperforms LR and SVM | ✅ Confirmed |
