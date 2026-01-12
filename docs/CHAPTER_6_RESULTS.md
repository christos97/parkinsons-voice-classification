# Chapter 6: Results

**Note:** The results presented in this chapter are derived from the experimental pipeline described in Chapter 4. All experiments were conducted using a fixed random seed to ensure reproducibility. To support transparency, raw result files (`all_results.csv`) are available in the project repository.

## 6.1 Overview of Experimental Conditions

This chapter reports the performance of classical machine learning models across three distinct experimental conditions, designed to isolate the effects of data representation and speech tasks on classification performance.

The three experiments are:

1.  **Experiment A1 (MDVR-KCL, Read Text):** Binary classification of "Read Text" recordings from 37 subjects (21 HC, 16 PD) using 47 deterministic acoustic features.
2.  **Experiment A2 (MDVR-KCL, Spontaneous Dialogue):** Binary classification of "Spontaneous Dialogue" recordings from 36 subjects using the same feature set.
3.  **Experiment B (PD_SPEECH_FEATURES):** Binary classification of 756 pre-processed samples using 752 pre-extracted acoustic features.

### Controlled Variables
To ensure fair comparison within (though not necessarily across) datasets, the following variables were held constant:
*   **Models:** Logistic Regression, Support Vector Machine (RBF Kernel), Random Forest.
*   **Metrics:** Accuracy, Precision, Recall, F1-Score, ROC-AUC.
*   **Preprocessing:** StandardScaler applied to all features within each fold.
*   **Subject Handling:** Grouped Stratified Cross-Validation was strictly enforced for Dataset A to prevent subject leakage.

---

## 6.2 Dataset A: MDVR-KCL Results

Dataset A represents the "raw audio pipeline," where feature extraction was performed locally using a deterministic, transparent approach limited to 47 classical acoustic features.

### 6.2.1 ReadText Task (Experiment A1)

The "Read Text" task represents a standardized speech protocol where subjects read a fixed passage. This task minimizes linguistic variability.

**Table 6.1: Performance Metrics for ReadText Task (Mean ± Std Dev over 5 Folds)**

| Model | Accuracy | F1-Score | ROC-AUC | Precision | Recall |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.621 ± 0.05 | 0.542 ± 0.09 | 0.717 ± 0.12 | 0.620 ± 0.19 | 0.550 ± 0.18 |
| **SVM (RBF)** | 0.621 ± 0.09 | 0.333 ± 0.30 | 0.614 ± 0.28 | 0.367 ± 0.30 | 0.317 ± 0.27 |
| **Random Forest** | 0.628 ± 0.16 | 0.351 ± 0.33 | 0.590 ± 0.27 | 0.450 ± 0.40 | 0.333 ± 0.37 |

**Observations:**
*   **Performance is modest:** Accuracy hovers around 62%, which is better than random chance (approx. 57% given the class imbalance) but not diagnostically strong.
*   **High Variance:** The standard deviations are substantial (e.g., ±0.28 for SVM ROC-AUC). This reflects the small sample size ($N=37$) and the rigorous Grouped Cross-Validation strategy. With only ~7 subjects in a test fold, a single misclassification significantly impacts the score.
*   **Model Instability:** The SVM classifier showed extreme instability, with ROC-AUC values ranging from near-perfect (0.92) to well below chance (0.13) across different folds. This is characteristic of kernel methods operating in high-dimensional spaces with sparse data.

### 6.2.2 SpontaneousDialogue Task (Experiment A2)

The "Spontaneous Dialogue" task involves unstructured speech. Though one subject (ID18) was excluded due to missing data, the pipeline remained otherwise identical.

**Table 6.2: Performance Metrics for SpontaneousDialogue Task (Mean ± Std Dev over 5 Folds)**

| Model | Accuracy | F1-Score | ROC-AUC | Precision | Recall |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.639 ± 0.14 | 0.539 ± 0.29 | 0.760 ± 0.19 | 0.469 ± 0.26 | 0.667 ± 0.33 |
| **SVM (RBF)** | 0.636 ± 0.12 | 0.400 ± 0.23 | 0.407 ± 0.28 | 0.600 ± 0.37 | 0.333 ± 0.27 |
| **Random Forest** | **0.721 ± 0.16** | **0.567 ± 0.33** | **0.828 ± 0.13** | 0.633 ± 0.37 | 0.600 ± 0.37 |

**Observations:**
*   **Improved discriminability:** Random Forest achieved the highest results in the entire Dataset A suite, with an accuracy of 72.1% and a ROC-AUC of 0.828.
*   **SVM Failure:** The SVM model yielded a mean ROC-AUC of 0.407, which is worse than random guessing. This confirms the model's unsuitability for this specific feature/sample combination without extensive hyperparameter tuning (which was excluded to maintain methodological purity).
*   **Trend:** There is a slight trend suggesting spontaneous speech may offer better separability (ROC-AUC 0.76 & 0.83 vs 0.72 & 0.59) than read text, though the overlapping confidence intervals prevent a definitive statistical claim.

---

## 6.3 Dataset B: PD_SPEECH_FEATURES Results

Dataset B represents the "pre-extracted features pipeline." It differs significantly from Dataset A in scale ($N=756$) and dimension ($D=752$).

**Table 6.3: Performance Metrics for Dataset B (Mean ± Std Dev over 5 Folds)**

| Model | Accuracy | F1-Score | ROC-AUC | Precision | Recall |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.828 ± 0.006 | 0.885 ± 0.005 | 0.867 ± 0.026 | 0.881 ± 0.008 | 0.890 ± 0.015 |
| **SVM (RBF)** | 0.850 ± 0.020 | 0.908 ± 0.014 | 0.885 ± 0.023 | 0.841 ± 0.013 | 0.986 ± 0.017 |
| **Random Forest** | **0.882 ± 0.018** | **0.925 ± 0.012** | **0.939 ± 0.011** | 0.876 ± 0.012 | 0.980 ± 0.014 |

**Observations:**
*   **High Performance:** All models performed well, with Random Forest approaching 94% ROC-AUC.
*   **Stability:** Standard deviations are very low (< 0.03), indicating stable training convergence.
*   **Caveat:** As noted in the Methodology, these results must be interpreted with caution. The lack of subject identifiers in Dataset B means that stratified cross-validation was processed at the sample level. If the dataset contains multiple recordings per subject, these results may be optimistically biased due to leakage.

---

## 6.4 Cross-Dataset Comparison

Comparing Dataset A and Dataset B directly requires careful contextualization.

**Table 6.4: Summary Comparison (Best Model per Dataset)**

| Metric | Dataset A (Best: RF/Spontaneous) | Dataset B (Best: RF) | Difference |
| :--- | :--- | :--- | :--- |
| **Accuracy** | 0.721 | 0.882 | +16.1% |
| **F1-Score** | 0.567 | 0.925 | +35.8% |
| **ROC-AUC** | 0.828 | 0.939 | +11.1% |

**Interpretation of the Gap:**
The significantly higher performance on Dataset B is attributable to three confounding factors:
1.  **Sample Size:** Dataset B is 20x larger (756 vs 37 samples), stabilizing the decision boundaries.
2.  **Feature Richness:** Dataset B uses 752 state-of-the-art features compared to the 47 baseline features used for Dataset A.
3.  **Cross-Validation Severity:** Dataset A utilized strict subject-grouped CV. Dataset B utilized sample-stratified CV (due to missing IDs), which is inherently an easier task if subject overlap exists.

Therefore, we **cannot** conclude that the "pre-extracted features" are inherently superior to the "raw audio features" based solely on these numbers. We can only conclude that the larger, higher-dimensional dataset yields better classifier performance under its specific evaluation conditions.

## 6.5 Model Behaviour Analysis

*   **Logistic Regression:** Proved to be the most "honest" baseline. It provided consistent, low-variance estimates on Dataset A and solid performance on Dataset B. It was less prone to the extreme volatility seen in the SVM.
*   **SVM (RBF):** Exhibited significant fragility in the low-data regime (Dataset A), often performing worse than chance. However, on the larger Dataset B, it became highly effective (ROC-AUC 0.885). This validates the theoretical understanding that non-linear kernel methods require sufficient density of data points to form reliable support vectors.
*   **Random Forest:** Emerged as the most robust model overall. It handled the high dimensionality of Dataset B (feature selection is inherent to the algorithm) and provided the best signal extraction on the noisy, small Dataset A.
