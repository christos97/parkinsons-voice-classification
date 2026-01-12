# Chapter 7: Discussion

This chapter interprets the results presented in Chapter 6, analyzing the factors influencing classification performance, the validity of the methodological approach, and the implications of the findings for Parkinson's Disease (PD) voice analysis research.

## 7.1 Interpretation of Results

The experimental results demonstrate a clear dichotomy between the two data pipelines. The raw audio pipeline (Dataset A), which adhered to strict subject-level separation and used a limited set of classical acoustic features, yielded modest classification performance (Accuracy ~62-72%). In contrast, the pre-extracted feature pipeline (Dataset B), utilizing a larger sample size and a richer feature set, achieved high classification performance (Accuracy ~83-88%).

These findings should not be interpreted simply as one dataset being "better" than the other. Rather, they highlight the critical trade-off between experimental control and performance optimization. The results from Dataset A provide a conservative, lower-bound estimate of performance under rigorous anti-leakage constraints with small sample sizes ($N=37$). The results from Dataset B represent an upper-bound estimate where feature engineering is extensive and sample size is larger ($N=756$), though potentially at the cost of subject independence.

## 7.2 Methodological Validity

A primary contribution of this thesis is the implementation of a reproducible, methodologically sound pipeline for raw audio processing.

**Leakage Prevention:**
The central methodological constraint—preventing data leakage—was successfully enforced in Experiment A. By using Grouped Stratified Cross-Validation, the pipeline ensured that all recordings from a single subject were assigned exclusively to either the training or testing fold. The high variance observed in the results (e.g., standard deviations of ±0.16–0.30) is a direct, expected consequence of this strict validation strategy on a small dataset. It effectively prevents the over-optimistic results often seen in literature where recording-level splitting is used.

**Feature Extraction:**
The decision to limit Dataset A to 47 deterministic acoustic features versus 752 features (Dataset B) was a deliberate design choice to maintain interpretability and avoid the "curse of dimensionality" on the small MDVR-KCL dataset.

## 7.3 Explaining the Performance Gap

The substantial performance gap between Dataset A and Dataset B (approx. +16% accuracy, +11% ROC-AUC) is confounded by three distinct factors, meaning we cannot attribute the difference to feature quality alone.

1.  **Sample Size:** Dataset B contains 756 samples, approximately 20 times the volume of Dataset A. Machine learning models, particularly non-linear ones like Random Forest and SVM, require density in the feature space to define robust decision boundaries.
2.  **Feature Dimensionality:** Dataset B utilizes 752 features, covering a far broader spectrum of acoustic characteristics than the 47 baseline features extracted for Dataset A.
3.  **Cross-Validation Rigor:** As noted in the results, Dataset B does not provide subject identifiers. Stratified cross-validation was therefore performed at the sample level. If multiple samples originate from the same subject, this may introduce implicit subject overlap across folds, leading to optimistically biased performance metrics.

**Caveat:** Direct performance comparison between Dataset A and Dataset B is confounded by these differences. Higher performance on Dataset B should not be interpreted as evidence that pre-extracted features are inherently superior to the raw audio features extracted in this study.

## 7.4 Model Instability Analysis

The behavior of the Support Vector Machine (SVM) with an RBF kernel provides an important insight into the limitations of small datasets.

In Experiment A (Dataset A), the SVM exhibited extreme instability, with ROC-AUC values dropping below 0.5 (chance level) in several folds. This indicates that the model failed to find a generalizing decision boundary, likely fitting to noise or idiosyncratic variances in the small training set. This behavior is expected when kernel methods encounter high-dimensional, low-sample-size conditions.

In contrast, the Random Forest model demonstrated greater resilience across both datasets. Its ensemble nature and ability to perform implicit feature selection allowed it to extract signal even from the noisy, limited data of Dataset A, confirming its suitability for medical small-data conceptual proofs.

## 7.5 Speech Task Observations

The comparison between `ReadText` and `SpontaneousDialogue` in Dataset A reveals a notable trend. Spontaneous dialogue yielded consistently higher ROC-AUC scores (0.76–0.83) compared to read text (0.59–0.72) across the better-performing models.

While the confidence intervals overlap substantially, suggesting the difference is not statistically definitive, the trend aligns with clinical intuition. Spontaneous speech requires higher cognitive load and more complex motor planning than reading a fixed text, potentially unmasking subtle vocal impairments that a reading task might mask.

## 7.6 Implications for PD Voice Research

**No Clinical Claims:**
This research is exploratory and academic in nature. The models developed here are not validated for clinical use and should not inform medical decisions.

**Research Implications:**
1.  **Subject-Level Splitting:** Future studies must prioritize subject-level splitting. The variance seen in Dataset A is the "true" variance of the problem; methods that report high accuracy with recording-level splits on small datasets likely underestimate the generalization error.
2.  **Task Selection:** The findings suggest that spontaneous speech may be a more sensitive modality for PD detection than read speech, warranting further investigation with larger cohorts.
3.  **Data Requirements:** The instability of the SVM on Dataset A emphasizes that collecting larger datasets is more critical than developing more complex models.
