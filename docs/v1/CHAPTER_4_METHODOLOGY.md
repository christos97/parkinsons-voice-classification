# Chapter 4: Methodology

This chapter details the methodological framework used to process voice data, extract features, and train classification models. The approach prioritizes reproducibility, interpretability, and the prevention of data leakage.

## 4.1 Research Design

The study is designed as a **binary classification problem**, distinguishing between subjects with Parkinson's Disease (PD) and Healthy Controls (HC) based on acoustic characteristics.

The specific operational choices were:
*   **Approach:** Classical Machine Learning (vs. Deep Learning).
*   **Rationale:** Classical models (Logistic Regression, SVM, Random Forest) were selected to provide interpretable baselines suitable for small datasets ($N < 100$), where deep learning models are prone to overfitting.
*   **Pipeline Strategy:** Two parallel pipelines were established to handle the disparate nature of the source data (Raw Audio vs. Pre-extracted Features).

## 4.2 Data Pipeline Architecture

### Pipeline A: Raw Audio Processing (Dataset A)
This pipeline handles the MDVR-KCL dataset. It is responsible for the end-to-end transformation of raw signals into result metrics.
1.  **Ingestion:** Parse filenames to extract Subject ID and Class.
2.  **Extraction:** Compute tabular acoustic features from `.wav` files.
3.  **Splitting:** Apply Grouped Stratified splitting (by Subject ID).
4.  **Training:** Train and predict.

### Pipeline B: Pre-Extracted Features (Dataset B)
This pipeline handles the PD_SPEECH_FEATURES dataset.
1.  **Ingestion:** Load CSV data.
2.  **Splitting:** Apply Stratified splitting (Subject IDs unavailable).
3.  **Training:** Train and predict (using identical models to Pipeline A).

## 4.3 Feature Extraction (Dataset A)

For Pipeline A, feature extraction was performed deterministically using Python libraries `librosa` and `parselmouth` (Praat interface). A compact set of **47 acoustic features** was selected to capture standard spectral vs. prosodic characteristics.

### 4.3.1 Acoustic Features Selected
The feature vector for each recording includes:

*   **Spectral Features (26):**
    *   **MFCCs:** 13 Mel-frequency cepstral coefficients (mean values).
    *   **Delta MFCCs:** 13 first-order derivatives of the MFCCs (mean values).
    *   *Purpose:* To capture the timbre and resonance characteristics of the vocal tract.

*   **Prosodic & Phonation Features (21):**
    *   **Fundamental Frequency (F0):** Mean, Standard Deviation, Minimum, Maximum.
    *   **Jitter:** local, local (absolute), rap, ppq5, ddp.
    *   **Shimmer:** local, local (dB), apq3, apq5, apq11, dda.
    *   **Harmonic-to-Noise Ratio (HNR):** Mean and standard deviation.
    *   *Purpose:* To capture dysphonia, instability, and tremor associated with PD vocal impairment.

### 4.3.2 Extraction Parameters
To ensure reproducibility, extraction parameters were fixed:
*   Sample Rate: Preserved at native rate (typically 44.1kHz).
*   Frame Size / Hop Length: Standard `librosa` defaults.
*   Aggregation: All time-series features were aggregated into a single vector per recording using the arithmetic mean (and std dev where specified).

## 4.4 Pre-Extracted Features (Dataset B)

Dataset B was used "as-is" without re-extraction. It contains **752 features** derived from various state-of-the-art speech analysis algorithms (including baseline features, wavelet transforms, and TQWT). No preprocessing was applied other than standard scaling during the cross-validation loop.

## 4.5 Model Selection

Three classifiers were chosen to represent different decision boundaries:

1.  **Logistic Regression:**
    *   *Role:* Linear baseline.
    *   *Strengths:* Highly interpretable, less prone to overfitting on small data.
2.  **Support Vector Machine (SVM):**
    *   *Kernel:* Radial Basis Function (RBF).
    *   *Role:* Non-linear classifier.
    *   *Strengths:* Theoretically robust in high-dimensional spaces, though sensitive to sample size.
3.  **Random Forest:**
    *   *Role:* Ensemble method.
    *   *Strengths:* Robust to outliers, performs implicit feature selection, handles non-linearities well.

## 4.6 Evaluation Protocol

### 4.6.1 Cross-Validation Strategy
*   **Dataset A:** **Grouped Stratified 5-Fold Cross-Validation.**
    *   Records are grouped by `Subject ID`.
    *   Crucially, this ensures that a subject appears in the Test set OR the Train set, never both. This prevents "subject leakage," where a model memorizes a specific person's voice rather than learning disease features.
*   **Dataset B:** **Stratified 5-Fold Cross-Validation.**
    *   Standard stratification by class label.

### 4.6.2 Metrics
Performance is reported using standard binary classification metrics:
*   Accuracy
*   Precision
*   Recall (Sensitivity)
*   F1-Score
*   ROC-AUC (Area Under the Receiver Operating Characteristic Curve)

All metrics are reported as the **Mean ± Standard Deviation** across the 5 folds.

### 4.6.3 Reproducibility
*   **Random Seed:** A fixed random seed (42) was used for all splitters and model initializers.
*   **Scaling:** `StandardScaler` (z-score normalization) was fit on the training folds and transformed to the test folds to prevent data leakage from the test set statistics.

## 4.7 Class Imbalance Mitigation

### 4.7.1 Observed Imbalance
Both datasets exhibit class imbalance:
*   **Dataset A (MDVR-KCL):** 57% HC / 43% PD — moderate imbalance.
*   **Dataset B (PD_SPEECH_FEATURES):** 25% HC / 75% PD — substantial imbalance.

Class imbalance can bias classifiers toward predicting the majority class, leading to inflated accuracy but poor minority-class recall.

### 4.7.2 Mitigation Strategy
To assess sensitivity to class imbalance, all experiments were conducted under two conditions:

1.  **Baseline (Unweighted):** Standard classifiers without class balancing. This represents the default behavior when imbalance is not explicitly addressed.
2.  **Class-Weighted:** All classifiers were configured with `class_weight="balanced"`, which adjusts the loss function to weight misclassifications inversely proportional to class frequency.

The `class_weight="balanced"` approach was selected over resampling methods (e.g., SMOTE) for the following reasons:
*   **No synthetic data:** Unlike oversampling, class weighting does not generate synthetic samples, avoiding potential artifacts.
*   **No leakage risk:** Resampling within cross-validation folds requires careful implementation to avoid leakage; class weighting is applied at the model level.
*   **Simplicity:** Built into scikit-learn classifiers with no additional dependencies.

### 4.7.3 Implementation
The same pipeline was used for both conditions. Only the `class_weight` parameter was toggled:
*   Baseline: `class_weight=None`
*   Weighted: `class_weight="balanced"`

Results from both conditions are reported separately to enable direct comparison of the effect of class weighting on classification performance.
