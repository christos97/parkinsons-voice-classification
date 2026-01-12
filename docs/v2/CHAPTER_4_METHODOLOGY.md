# Chapter 4: Methodology

## 4.1 Overview

This chapter describes the feature extraction pipeline, machine learning models, and evaluation framework used in this thesis. The methodology emphasizes reproducibility and methodological rigor over raw performance optimization.

## 4.2 Feature Extraction Pipeline

### 4.2.1 Pipeline Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Raw Audio      │ ──► │ Feature          │ ──► │ Feature         │
│  (WAV files)    │     │ Extraction       │     │ Matrix (X, y)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ • Prosodic Features  │
                    │ • Spectral Features  │
                    └──────────────────────┘
```

### 4.2.2 Audio Preprocessing

Prior to feature extraction:

1. **Load audio** at native sample rate (typically 44.1 kHz)
2. **Convert to mono** if stereo
3. **Normalize amplitude** to [-1, 1] range
4. **Trim silence** using energy-based detection

### 4.2.3 Prosodic Features (21 features)

Prosodic features capture suprasegmental voice characteristics:

| Feature Group | Count | Features | Tool |
|--------------|-------|----------|------|
| Pitch (F0) | 4 | mean, std, min, max | Parselmouth |
| Jitter | 3 | local, RAP, PPQ5 | Parselmouth |
| Shimmer | 5 | local, APQ3, APQ5, APQ11, DDA | Parselmouth |
| Harmonicity | 2 | HNR mean, autocorr | Parselmouth |
| Intensity | 3 | mean, std, range | Parselmouth |
| Formants | 6 | F1-F3 mean, F1-F3 std | Parselmouth |

### 4.2.4 Spectral Features

Spectral features capture frequency-domain characteristics using librosa.

#### Baseline Spectral Features (26 features)

| Feature | Count | Description |
|---------|-------|-------------|
| MFCC mean | 13 | Mean of MFCCs 0-12 |
| Delta MFCC mean | 13 | Mean of first-order derivatives |

#### Extended Spectral Features (57 features)

| Feature | Count | Description |
|---------|-------|-------------|
| MFCC mean | 13 | Mean of MFCCs 0-12 |
| **MFCC std** | **13** | **Standard deviation of MFCCs** |
| Delta MFCC mean | 13 | First-order derivatives |
| **Delta-Delta MFCC mean** | **13** | **Second-order derivatives** |
| **Spectral shape** | **5** | **Centroid, bandwidth, rolloff, flatness, ZCR** |

**New features in extended set are shown in bold.**

### 4.2.5 Total Feature Counts

| Configuration | Prosodic | Spectral | Total |
|--------------|----------|----------|-------|
| Baseline | 21 | 26 | **47** |
| Extended | 21 | 57 | **78** |

## 4.3 Feature Set Comparison

### 4.3.1 Baseline vs Extended Features

```
BASELINE (47 features)              EXTENDED (78 features)
├── Prosodic (21)                   ├── Prosodic (21)
│   ├── Pitch (4)                   │   ├── Pitch (4)
│   ├── Jitter (3)                  │   ├── Jitter (3)
│   ├── Shimmer (5)                 │   ├── Shimmer (5)
│   ├── Harmonicity (2)             │   ├── Harmonicity (2)
│   ├── Intensity (3)               │   ├── Intensity (3)
│   └── Formants (6)                │   └── Formants (6)
│                                   │
└── Spectral (26)                   └── Spectral (57)
    ├── MFCC mean (13)                  ├── MFCC mean (13)
    └── Delta MFCC mean (13)            ├── MFCC std (13)      ← NEW
                                        ├── Delta MFCC mean (13)
                                        ├── Delta-Delta MFCC (13) ← NEW
                                        └── Spectral shape (5)    ← NEW
```

### 4.3.2 Rationale for Extended Features

The extended feature set was designed as a **controlled ablation study**:

1. **MFCC std (13):** Captures within-utterance variability—important for detecting instability in PD speech
2. **Delta-Delta MFCC (13):** Captures acceleration of spectral changes—sensitive to temporal dynamics
3. **Spectral shape (5):** Provides complementary global spectral descriptors

## 4.4 Machine Learning Models

### 4.4.1 Model Selection Rationale

Three classical ML models were selected for:
- **Interpretability** — critical for clinical applications
- **Robustness** — well-understood behavior on small datasets
- **Diversity** — linear, kernel-based, and ensemble approaches

### 4.4.2 Model Specifications

| Model | Type | Key Parameters |
|-------|------|----------------|
| Logistic Regression | Linear | C=1.0, max_iter=1000 |
| SVM (RBF) | Kernel | C=1.0, gamma='scale' |
| Random Forest | Ensemble | n_estimators=100, max_depth=10 |

### 4.4.3 Class Weighting

Class imbalance is addressed via `class_weight` parameter:

```python
# Unweighted (baseline)
class_weight = None

# Weighted
class_weight = "balanced"  # Inversely proportional to class frequencies
```

All three models support the `class_weight` parameter natively.

## 4.5 ML Pipeline Architecture

### 4.5.1 Pipeline Structure

```python
Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', Model(class_weight=...))
])
```

### 4.5.2 Standardization

All features are standardized to zero mean and unit variance:

$$z = \frac{x - \mu}{\sigma}$$

Standardization is fitted **only on training data** and applied to test data to prevent leakage.

## 4.6 Evaluation Framework

### 4.6.1 Cross-Validation Strategy

| Dataset | Strategy | Folds | Grouping |
|---------|----------|-------|----------|
| Dataset A | GroupKFold + Stratified | 5 | By subject_id |
| Dataset B | StratifiedKFold | 5 | None (unavailable) |

### 4.6.2 Evaluation Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| Precision | TP/(TP+FP) | Positive predictive value |
| Recall | TP/(TP+FN) | Sensitivity |
| F1 Score | 2·(P·R)/(P+R) | Harmonic mean of P and R |
| ROC-AUC | Area under ROC curve | Discrimination ability |

**Primary metric:** ROC-AUC (threshold-independent, handles imbalance)

## 4.7 Experimental Conditions

### 4.7.1 2×2 Factorial Design

The experiments follow a 2×2 factorial design:

| | Baseline Features (47) | Extended Features (78) |
|---|------------------------|------------------------|
| **Unweighted** | Condition 1 | Condition 2 |
| **Weighted** | Condition 3 | Condition 4 |

### 4.7.2 Configuration Flags

Experiments are controlled via configuration flags:

```python
USE_CLASS_WEIGHT_BALANCED = False  # True for weighted conditions
USE_EXTENDED_FEATURES = False      # True for extended conditions
```

## 4.8 Implementation Details

### 4.8.1 Software Stack

| Component | Library | Version |
|-----------|---------|---------|
| Audio I/O | librosa | 0.10.x |
| Prosodic analysis | parselmouth | 0.4.x |
| ML models | scikit-learn | 1.4.x |
| Data handling | pandas, numpy | latest |

### 4.8.2 Reproducibility

- Random seed: 42 (fixed throughout)
- All experiments runnable via CLI: `pvc-experiment`
- Feature extraction: `pvc-extract --task all`

## 4.9 Summary

The methodology implements:

1. **Two-tier feature extraction** (47 baseline, 78 extended)
2. **Three classical ML models** with optional class weighting
3. **Grouped cross-validation** for Dataset A (subject-level)
4. **2×2 factorial design** for systematic comparison
