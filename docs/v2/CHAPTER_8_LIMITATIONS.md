# Chapter 8: Limitations and Threats to Validity

## 8.1 Overview

This chapter provides a transparent assessment of the limitations and potential threats to validity in this research. Acknowledging these constraints is essential for appropriate interpretation of results and identification of future research directions.

## 8.2 Sample Size Limitations

### 8.2.1 Dataset A: Small Subject Pool

| Metric | Value |
|--------|-------|
| Total subjects | 37 |
| Subjects per test fold | ~7 |
| PD subjects (minority) | 15-16 |

**Implications:**

- High variance in fold-level metrics (std > 0.15 common)
- Limited statistical power for detecting small effects
- Results may not generalize to broader populations

### 8.2.2 Effect on Statistical Confidence

With 37 subjects and 5-fold CV:

- Each fold has only ~7 test subjects
- A single misclassification shifts accuracy by ~14%
- Confidence intervals are wide by design

**Mitigation:** Results focus on **relative comparisons** rather than absolute performance claims.

## 8.3 Subject Identifier Limitations

### 8.3.1 Dataset B: Missing Subject IDs

Dataset B (PD_SPEECH) provides no subject identifiers. This creates potential for:

- **Subject leakage:** Same subject in train and test sets
- **Optimistic bias:** Inflated performance estimates
- **Unknown generalization:** Cannot assess new-subject performance

**Caveat Statement:**

> "Results on Dataset B may be optimistic due to unknown subject overlap across folds. The absence of subject identifiers prevents validation of true out-of-subject generalization."

### 8.3.2 Comparison Limitations

Direct comparison between Dataset A (grouped CV) and Dataset B (standard CV) is confounded by:

- Different CV strategies
- Different feature dimensionalities (78 vs 752)
- Different sample sizes (37 vs 756)

## 8.4 Feature Extraction Limitations

### 8.4.1 Deterministic Feature Set

The feature set was designed a priori based on literature review, not data-driven optimization. Limitations include:

- **Potentially suboptimal features:** Other features may be more discriminative
- **Fixed parameters:** Librosa/Parselmouth defaults used without tuning
- **No feature selection:** All 78 features used without reduction

### 8.4.2 Audio Quality Assumptions

Feature extraction assumes:

- Reasonable signal-to-noise ratio
- Consistent recording conditions
- No severe clipping or distortion

The MDVR-KCL dataset's smartphone recordings may violate these assumptions.

## 8.5 Model Limitations

### 8.5.1 No Hyperparameter Tuning

All models used default or fixed hyperparameters:

| Model | Fixed Parameters |
|-------|-----------------|
| Logistic Regression | C=1.0, max_iter=1000 |
| SVM (RBF) | C=1.0, gamma='scale' |
| Random Forest | n_estimators=100, max_depth=10 |

**Implications:**

- Performance may be suboptimal
- Results represent lower bounds
- Tuned models might change rankings

**Rationale for not tuning:** Nested CV on 37 subjects would lead to extreme variance; fixed parameters ensure reproducibility.

### 8.5.2 Classical ML Only

This thesis explicitly excludes deep learning. Potential missed opportunities:

- End-to-end learning from spectrograms
- Transfer learning from speech models
- Attention mechanisms for temporal modeling

**Rationale:** Deep learning typically requires larger datasets and offers reduced interpretability.

## 8.6 Methodological Limitations

### 8.6.1 No External Validation

All results use internal cross-validation. Limitations:

- No held-out test set from different source
- No multi-site validation
- Generalization to clinical settings unknown

### 8.6.2 Binary Classification Only

The task is limited to PD vs HC classification. Not addressed:

- Disease severity prediction
- Progression monitoring
- Differential diagnosis (PD vs other conditions)

### 8.6.3 Single Speech Tasks

Each task analyzed separately. Not addressed:

- Task fusion strategies
- Multi-task learning
- Optimal task selection

## 8.7 Threats to Validity

### 8.7.1 Internal Validity

| Threat | Status | Mitigation |
|--------|--------|------------|
| Subject leakage | Controlled (Dataset A) | Grouped CV |
| Label noise | Unknown | Assumed correct |
| Feature bugs | Possible | Unit tests, manual verification |

### 8.7.2 External Validity

| Threat | Status | Mitigation |
|--------|--------|------------|
| Population bias | Likely | Document dataset demographics |
| Recording variability | Present | Standardized extraction |
| Temporal stability | Unknown | Single recording session |

### 8.7.3 Construct Validity

| Threat | Status | Mitigation |
|--------|--------|------------|
| Feature relevance | Assumed | Literature-based selection |
| Metric appropriateness | Addressed | Multiple metrics reported |
| Class definition | Accepted | Binary PD/HC from source |

## 8.8 Reproducibility Considerations

### 8.8.1 Strengths

- Fixed random seeds (42)
- Version-controlled code
- CLI-based pipeline
- Documented dependencies

### 8.8.2 Limitations

- Library version drift may affect results
- Hardware differences in audio processing
- Dataset access may change

## 8.9 Interpretation Guidelines

Given the limitations, results should be interpreted as follows:

### 8.9.1 Appropriate Claims

✅ "Extended features improved ROC-AUC on this dataset"
✅ "Random Forest outperformed other models under these conditions"
✅ "Grouped CV provides more conservative estimates than random splits"

### 8.9.2 Inappropriate Claims

❌ "This system diagnoses Parkinson's Disease"
❌ "82.6% accuracy is clinically sufficient"
❌ "These results will generalize to other populations"

## 8.10 Future Work to Address Limitations

| Limitation | Potential Solution |
|------------|--------------------|
| Small sample size | Multi-site data collection |
| Missing subject IDs | Require IDs in future datasets |
| No hyperparameter tuning | Bayesian optimization with nested CV |
| No external validation | Independent test cohort |
| Classical ML only | Careful deep learning with augmentation |

## 8.11 Summary

This research has significant limitations including:

1. **Small sample size** (37 subjects) leading to high variance
2. **Missing subject IDs** in Dataset B preventing leakage control
3. **No hyperparameter tuning** potentially limiting performance
4. **No external validation** limiting generalization claims
5. **Binary classification only** excluding severity/progression

These limitations are acknowledged to ensure appropriate interpretation of results. Despite constraints, the methodology prioritizes **validity over optimization**, providing a rigorous foundation for future work.
