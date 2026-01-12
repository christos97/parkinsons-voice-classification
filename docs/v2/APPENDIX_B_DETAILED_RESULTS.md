# Appendix B: Detailed Results Tables

## B.1 Overview

This appendix provides complete numerical results for all experimental conditions, including per-fold breakdowns and task-level performance.

## B.2 Condition 1: Baseline Features (47) + Unweighted

**Output directory:** `outputs/results/baseline/baseline/`

### B.2.1 Summary Statistics

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| LogisticRegression | 0.696 ± 0.133 | 0.657 ± 0.262 | 0.702 ± 0.284 | 0.655 ± 0.246 | 0.781 ± 0.152 |
| SVM_RBF | 0.703 ± 0.143 | 0.603 ± 0.357 | 0.545 ± 0.390 | 0.547 ± 0.347 | 0.635 ± 0.311 |
| RandomForest | 0.744 ± 0.173 | 0.653 ± 0.373 | 0.638 ± 0.421 | 0.615 ± 0.369 | 0.786 ± 0.235 |

---

## B.3 Condition 2: Extended Features (78) + Unweighted

**Output directory:** `outputs/results/baseline/extended/`

### B.3.1 Summary Statistics

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| LogisticRegression | 0.699 ± 0.152 | 0.660 ± 0.289 | 0.641 ± 0.314 | 0.630 ± 0.281 | 0.783 ± 0.126 |
| SVM_RBF | 0.757 ± 0.143 | 0.703 ± 0.330 | 0.651 ± 0.354 | 0.657 ± 0.321 | 0.726 ± 0.265 |
| RandomForest | 0.826 ± 0.122 | 0.814 ± 0.255 | 0.760 ± 0.327 | 0.759 ± 0.271 | 0.873 ± 0.137 |

### B.3.2 Improvement over Baseline

| Model | Δ Accuracy | Δ ROC-AUC |
|-------|------------|-----------|
| LogisticRegression | +0.3pp | +0.2pp |
| SVM_RBF | +5.4pp | **+9.1pp** |
| RandomForest | +8.2pp | **+8.7pp** |

---

## B.4 Condition 3: Baseline Features (47) + Weighted

**Output directory:** `outputs/results/weighted/baseline/`

### B.4.1 Summary Statistics

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| LogisticRegression | 0.687 ± 0.141 | 0.654 ± 0.271 | 0.696 ± 0.280 | 0.649 ± 0.247 | 0.781 ± 0.152 |
| SVM_RBF | 0.748 ± 0.115 | 0.690 ± 0.314 | 0.670 ± 0.333 | 0.659 ± 0.299 | 0.622 ± 0.316 |
| RandomForest | 0.736 ± 0.141 | 0.664 ± 0.315 | 0.660 ± 0.393 | 0.628 ± 0.322 | 0.821 ± 0.191 |

### B.4.2 Effect of Weighting (vs Condition 1)

| Model | Δ Accuracy | Δ ROC-AUC |
|-------|------------|-----------|
| LogisticRegression | -0.9pp | 0.0pp |
| SVM_RBF | +4.5pp | -1.3pp |
| RandomForest | -0.8pp | **+3.5pp** |

---

## B.5 Condition 4: Extended Features (78) + Weighted

**Output directory:** `outputs/results/weighted/extended/`

### B.5.1 Summary Statistics

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| LogisticRegression | 0.724 ± 0.136 | 0.687 ± 0.283 | 0.696 ± 0.307 | 0.670 ± 0.270 | 0.783 ± 0.126 |
| SVM_RBF | 0.757 ± 0.165 | 0.718 ± 0.338 | 0.693 ± 0.319 | 0.693 ± 0.309 | 0.712 ± 0.305 |
| RandomForest | 0.801 ± 0.146 | 0.798 ± 0.259 | 0.760 ± 0.327 | 0.748 ± 0.268 | 0.859 ± 0.162 |

### B.5.2 Effect of Weighting (vs Condition 2)

| Model | Δ Accuracy | Δ ROC-AUC |
|-------|------------|-----------|
| LogisticRegression | +2.5pp | 0.0pp |
| SVM_RBF | 0.0pp | -1.4pp |
| RandomForest | -2.5pp | -1.4pp |

---

## B.6 Cross-Condition Comparison Matrix

### B.6.1 Random Forest ROC-AUC

|                | Baseline Features | Extended Features |
|----------------|-------------------|-------------------|
| **Unweighted** | 0.786 ± 0.235     | **0.873 ± 0.137** |
| **Weighted**   | 0.821 ± 0.191     | 0.859 ± 0.162     |

### B.6.2 Random Forest Accuracy

|                | Baseline Features | Extended Features |
|----------------|-------------------|-------------------|
| **Unweighted** | 74.4% ± 17.3%     | **82.6% ± 12.2%** |
| **Weighted**   | 73.6% ± 14.1%     | 80.1% ± 14.6%     |

---

## B.7 Statistical Significance Notes

### B.7.1 Confidence Interval Overlap

Due to high standard deviations (often > 0.15), confidence intervals overlap across many comparisons. This limits the ability to make strong statistical claims about differences between conditions.

### B.7.2 Practical Significance

Despite overlapping CIs, the consistent pattern of:
- Extended > Baseline features
- Random Forest > other models

...suggests **practically meaningful** differences even if not statistically significant at conventional thresholds.

---

## B.8 Raw Data Files

All results are available in CSV format:

```
outputs/results/
├── baseline/
│   ├── baseline/
│   │   ├── all_results.csv      # Per-fold, per-metric details
│   │   └── summary.csv          # Aggregated statistics
│   ├── extended/
│   │   ├── all_results.csv
│   │   └── summary.csv
│   ├── importance_readtext.csv  # Feature importance (baseline)
│   ├── importance_spontaneous.csv
│   └── importance_pd_speech.csv
│
└── weighted/
    ├── baseline/
    │   ├── all_results.csv
    │   └── summary.csv
    └── extended/
        ├── all_results.csv
        └── summary.csv
```

### B.8.1 CSV Column Descriptions

**all_results.csv:**
| Column | Description |
|--------|-------------|
| model | Classifier name |
| fold | CV fold number (1-5) |
| metric | Evaluation metric |
| value | Metric value |
| dataset | Dataset name |
| task | Speech task (ReadText/SpontaneousDialogue) |

**summary.csv:**
| Column | Description |
|--------|-------------|
| model | Classifier name |
| metric | Evaluation metric |
| mean | Mean across folds |
| std | Standard deviation across folds |
| mean_std | Formatted string (mean ± std) |
