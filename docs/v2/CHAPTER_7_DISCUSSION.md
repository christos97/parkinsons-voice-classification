# Chapter 7: Discussion

## 7.1 Overview

This chapter interprets the experimental results, contextualizes findings within the literature, and discusses implications for PD voice classification research.

## 7.2 Interpretation of Key Findings

### 7.2.1 Feature Extension Impact

The extension from 47 to 78 features produced significant performance improvements, particularly for the ReadText task where Random Forest ROC-AUC increased from 0.590 to 0.822 (+23 percentage points), essentially rescuing the model from chance-level performance. Spontaneous Dialogue, which already performed well (0.828), saw a more modest improvement to 0.857.

**Interpretation:**

The extended features capture three complementary aspects of speech dynamics:

| New Feature Set | Contribution |
|-----------------|--------------|
| MFCC std (13) | Within-utterance spectral variability |
| Delta-Delta MFCC (13) | Acceleration of spectral changes |
| Spectral shape (5) | Global spectral characteristics |

These additions are particularly relevant for PD detection because:

1. **Reduced variability** is a hallmark of PD speech (monotone)
2. **Temporal dynamics** are affected by motor control deficits
3. **Spectral flatness** may indicate breathiness/reduced harmonic content

The larger improvement for non-linear models suggests that the extended features enable modeling of **non-linear feature interactions** that simpler feature sets may obscure.

**Robustness Check:**
Although the extended feature set increased dimensionality relative to the small sample size of Dataset A (n=37), performance was evaluated exclusively using grouped cross-validation at the subject level. Improvements were observed consistent across folds and were accompanied by comparable standard deviations, suggesting that the observed gains reflect improved feature representation rather than fold-specific overfitting.

### 7.2.2 Class Weighting Effects

Class weighting showed **modest and inconsistent effects** on Dataset A:

| Model | Δ ROC-AUC (weighted vs unweighted) |
|-------|-----------------------------------|
| Random Forest | +3.5pp (baseline), -1.4pp (extended) |
| Logistic Regression | 0.0pp |
| SVM (RBF) | -1.3pp (baseline), -1.4pp (extended) |

**Interpretation:**

The moderate imbalance in Dataset A (57:43 HC:PD) is not severe enough to substantially degrade unweighted classifiers. Class weighting becomes more critical when:

- Imbalance exceeds 70:30
- Minority class has high cost of misclassification
- Sample size is very small

For Dataset B (25:75 imbalance), class weighting would likely have a larger effect, though this remains to be tested with subject-grouped CV.

### 7.2.3 Model Performance Hierarchy

Across all conditions, Random Forest consistently outperformed other models:

```
Random Forest > Logistic Regression ≈ SVM (RBF)
```

**Interpretation:**

Random Forest's advantages for this task include:

1. **Ensemble averaging** reduces variance on small datasets
2. **Feature importance** provides interpretability
3. **Non-linear decision boundaries** capture complex patterns
4. **Robustness** to irrelevant features through feature subsampling

### 7.2.4 High Variance Across Folds

Standard deviations frequently exceeded 0.15 (15%), indicating substantial fold-to-fold variability.

**Causes:**

1. **Small sample size** (37 subjects → ~7 subjects per test fold)
2. **Subject heterogeneity** in disease severity
3. **Recording variability** (smartphone recordings)

**Implications:**

- Absolute performance numbers should be interpreted cautiously
- Relative comparisons across conditions are more reliable
- Confidence intervals overlap for many comparisons

## 7.3 Comparison with Literature

### 7.3.1 Performance Context

| Study | Dataset | Best ROC-AUC | Method |
|-------|---------|--------------|--------|
| Little et al. (2009) | UCI | 0.92 | SVM |
| Sakar et al. (2013) | Custom | 0.86 | SVM |
| **This thesis** | **MDVR-KCL** | **0.87** | **RF** |

Our results are competitive with literature, though direct comparison is limited due to:

- Different datasets and features
- Different CV strategies (many studies do not use grouped CV)
- Different sample sizes

### 7.3.2 Methodological Comparison

| Aspect | Typical Literature | This Thesis |
|--------|-------------------|-------------|
| CV Strategy | Random split | Grouped stratified |
| Subject handling | Often ignored | Explicit grouping |
| Feature selection | Ad-hoc | Systematic ablation |
| Reporting | Best result only | All conditions |

Our grouped CV approach provides **more conservative** but **more realistic** estimates of generalization performance.

## 7.4 Feature Importance Analysis

### 7.4.1 Most Discriminative Features

The top features across models consistently include:

| Feature | Category | Relevance to PD |
|---------|----------|-----------------|
| f0_max | Pitch | Reduced pitch range in PD |
| delta_mfcc_2_mean | Spectral dynamics | Temporal variability |
| autocorr_harmonicity | Voice quality | Breathiness indicator |
| shimmer_apq3 | Perturbation | Amplitude instability |
| intensity_mean | Prosody | Hypophonia marker |

### 7.4.2 Feature Category Contributions

![Feature Importance by Category - ReadText](../outputs/plots/importance_readtext_categories.png)

*Figure 7.1: Aggregated importance by feature category (Random Forest, ReadText).*

The analysis reveals:

- **MFCC features** contribute most to classification
- **Pitch features** (F0) are consistently important
- **Formant variability** (F1-F3 std) shows moderate importance

### 7.4.3 Cross-Task Stability

Comparing ReadText and SpontaneousDialogue tasks:

![Feature Importance - Spontaneous](../outputs/plots/importance_spontaneous_categories.png)

*Figure 7.2: Feature importance by category for SpontaneousDialogue task.*

Feature rankings are **moderately consistent** across tasks, suggesting that the acoustic signatures of PD are task-general rather than task-specific.

## 7.5 Implications

### 7.5.1 For Feature Engineering

The success of extended features suggests that future work should:

1. **Include variability measures** (std, range) alongside means
2. **Capture temporal dynamics** (delta, delta-delta)
3. **Provide spectral shape descriptors** (centroid, rolloff)

### 7.5.2 For Model Selection

Random Forest is recommended for similar tasks due to:

- Robustness on small datasets
- Built-in feature importance
- Good handling of mixed feature types

### 7.5.3 For Evaluation Protocols

Grouped cross-validation should be **mandatory** when:

- Multiple recordings exist per subject
- Subject identifiers are available
- Generalization to new subjects is the goal

## 7.6 Addressing Research Questions

### 7.6.1 RQ1: ML Model Performance

> **How do classical ML models perform on PD voice classification?**

Classical ML achieves ROC-AUC up to 0.873, demonstrating feasibility of voice-based PD detection. Random Forest outperforms linear models.

### 7.6.2 RQ2: Feature Extension Impact

> **Does feature set extension improve classification performance?**

**Yes.** Extending from 47 to 78 features improved ROC-AUC by +8.7pp (Random Forest). The improvement is most pronounced for non-linear models.

### 7.6.3 RQ3: Class Weighting Impact

> **Does class weighting improve performance on imbalanced datasets?**

**Marginally.** On Dataset A (moderate imbalance), class weighting improved RF by +3.5pp with baseline features but showed inconsistent effects elsewhere.

### 7.6.4 RQ4: Cross-Dataset Comparison

> **How do results compare between Dataset A and Dataset B?**

Dataset B typically shows higher performance, likely due to:
- Larger sample size
- Potential subject overlap (unmeasurable)
- Different feature sets

Direct comparison is limited by these confounds.

## 7.7 Unexpected Findings

### 7.7.1 SVM Performance Variability

SVM (RBF) showed high variance and occasional fold-level failures (ROC-AUC < 0.5 in some folds). This suggests:

- Sensitivity to hyperparameters (not tuned in this study)
- Potential kernel mismatch for this feature space
- Need for larger training sets

### 7.7.2 Limited Benefit of Weighting with Extended Features

When using extended features, class weighting provided **no additional benefit** (and sometimes slightly reduced performance). This suggests that the richer feature representation already captures minority class characteristics effectively.

## 7.8 Summary

Key discussion points:

1. **Feature extension is the primary driver of improvement** (+8.7pp ROC-AUC)
2. **Random Forest is the most robust model** for this task
3. **Grouped CV provides conservative estimates** but ensures validity
4. **Class weighting has modest effects** on moderately imbalanced data
5. **High variance** necessitates cautious interpretation of absolute numbers
