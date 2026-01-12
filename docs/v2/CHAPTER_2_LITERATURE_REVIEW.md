# Chapter 2: Literature Review

## 2.1 Overview

Voice-based detection of Parkinson's Disease has been an active research area since the seminal work of Little et al. (2009), who demonstrated that dysphonia measures could discriminate PD patients from healthy controls with accuracies exceeding 90%. Since then, numerous studies have explored various acoustic features and machine learning approaches.

## 2.2 Acoustic Manifestations of Parkinson's Disease

### 2.2.1 Prosodic Changes

PD affects the laryngeal muscles and respiratory control, leading to characteristic voice changes:

- **Reduced pitch variability** (monotone speech)
- **Decreased intensity** and loudness control
- **Increased jitter and shimmer** (cycle-to-cycle perturbations)
- **Reduced Harmonics-to-Noise Ratio (HNR)** indicating breathiness

### 2.2.2 Spectral Changes

The disease also manifests in spectral characteristics:

- **Altered formant frequencies** (F1, F2, F3)
- **Changes in Mel-Frequency Cepstral Coefficients (MFCCs)**
- **Modified spectral envelope** characteristics

## 2.3 Feature Extraction Approaches

### 2.3.1 Traditional Acoustic Features

Early studies relied on clinically-motivated features:

| Feature Category | Examples | Physiological Basis |
|-----------------|----------|---------------------|
| Fundamental Frequency | F0 mean, F0 std | Vocal fold tension |
| Perturbation | Jitter, Shimmer | Neuromuscular control |
| Noise | HNR, NHR | Incomplete glottal closure |
| Formants | F1, F2, F3 | Vocal tract configuration |

### 2.3.2 Spectral Features

Modern approaches incorporate signal processing features:

- **MFCCs** (Mel-Frequency Cepstral Coefficients) — compact spectral representation
- **Delta and Delta-Delta MFCCs** — temporal dynamics
- **Spectral shape features** — centroid, bandwidth, rolloff, flatness

### 2.3.3 Deep Learning Features

Recent work has explored end-to-end learning from spectrograms. However, these approaches require large datasets and lack interpretability—both significant limitations for clinical applications.

## 2.4 Machine Learning Approaches

### 2.4.1 Classical Methods

Classical ML remains dominant in clinical applications due to interpretability:

| Method | Strengths | Limitations |
|--------|-----------|-------------|
| Logistic Regression | Interpretable coefficients | Linear decision boundary |
| SVM | Effective in high dimensions | Kernel selection critical |
| Random Forest | Handles non-linearity, feature importance | Less interpretable than linear models |

### 2.4.2 Deep Learning

CNNs and RNNs have been applied to PD detection but face challenges:
- Require large labeled datasets
- Prone to overfitting on small samples
- Limited interpretability for clinical validation

## 2.5 Methodological Concerns in Literature

### 2.5.1 Data Leakage

Many published studies fail to account for subject identity when splitting data:

> "When multiple recordings exist per subject, random train/test splits can place recordings from the same subject in both sets, leading to optimistic performance estimates."

This thesis addresses this through **grouped stratified cross-validation**.

### 2.5.2 Class Imbalance

Imbalanced class distributions are common but often unaddressed:

- Simple accuracy can be misleading
- Class weighting or resampling strategies needed
- This thesis investigates `class_weight="balanced"` as a mitigation

### 2.5.3 Reproducibility

Many studies lack sufficient detail for reproduction:
- Feature extraction parameters unspecified
- Random seeds not fixed
- Cross-validation strategy unclear

## 2.6 Benchmark Datasets

### 2.6.1 UCI Parkinson's Dataset

The most widely used benchmark, containing 195 samples with pre-extracted features. Limitations include lack of subject identifiers and dated feature set.

### 2.6.2 MDVR-KCL Dataset

Mobile device recordings from King's College London, providing raw audio with subject identifiers. Used as Dataset A in this thesis.

### 2.6.3 PD Speech Features Dataset

Kaggle-hosted dataset with 752 pre-extracted features. Used as Dataset B for comparison.

## 2.7 Research Gap

While numerous studies report high classification accuracies, few address:

1. **Grouped cross-validation** for multi-recording datasets
2. **Controlled feature ablation** studies
3. **Systematic class weighting** analysis
4. **Transparent limitations** acknowledgment

This thesis aims to fill these gaps through rigorous experimental design prioritizing methodological validity over performance optimization.

## 2.8 Summary

The literature demonstrates that voice-based PD detection is feasible, with classical ML achieving competitive results. However, methodological rigor varies significantly across studies. This thesis adopts a conservative approach, prioritizing reproducibility and valid comparison over state-of-the-art claims.
