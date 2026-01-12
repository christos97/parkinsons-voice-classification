# Chapter 8: Limitations

This chapter defines the boundaries of the research findings, identifying factors that limit the generalizability, comparability, and clinical applicability of the results. Acknowledging these limitations is essential for defining the scope of the thesis and preventing misinterpretation of the experimental outcomes.

## 8.1 Sample Size Constraints

The most significant limitation of Experiment A (MDVR-KCL) is the small sample size ($N=37$ subjects).
*   **High Variance:** With strictly grouped cross-validation, each test fold contained only approximately 7 subjects. This granular split results in high variance in performance metrics (standard deviations between 0.15 and 0.36), as a single misclassified subject can swing accuracy by over 14%.
*   **Statistical Power:** The study is underpowered for establishing statistical significance. Confidence intervals for model performance frequently overlap, meaning that observed differences between speech tasks (Read Text vs. Spontaneous Dialogue) must be interpreted as trends rather than definitive effects.
*   **Model Training:** The limited number of training samples (~30 subjects per fold) is insufficient for complex non-linear models like SVM with RBF kernel to reliably establish decision boundaries without overfitting, as evidenced by the model's instability.

## 8.2 Feature Dimensionality Mismatch

There is a substantial disparity in feature representation between the two datasets:
*   **Dataset A:** 47 features (chosen for interpretability and simplicity).
*   **Dataset B:** 752 features (comprehensive state-of-the-art set).

This mismatch means the two datasets are not directly comparable on the basis of feature engineering quality. The "raw audio pipeline" (Dataset A) essentially tested a baseline feature set, whereas the "pre-extracted" pipeline (Dataset B) benefited from a much richer representation. Consequently, the performance gap cannot be attributed solely to the quality of the data itself but heavily reflects the breadth of the feature extraction vector.

## 8.3 Dataset B Subject Independence Uncertainty

A critical constraint concerns the independence of samples in Dataset B.

> **Caveat:** Since Dataset B does not provide subject identifiers, stratified cross-validation was performed at the sample level. If multiple samples originate from the same subject, this may introduce optimistic bias due to implicit subject overlap across folds (data leakage).

This uncertainty implies that the high accuracy (88%) and ROC-AUC (0.94%) obtained for Dataset B may be inflated compared to the rigorous subject-level validation applied to Dataset A.

## 8.4 Cross-Validation Strategy Differences

Due to the lack of subject IDs in Dataset B, the evaluation protocols necessarily differed:
*   **Dataset A:** Grouper Stratified K-Fold (Strict Subject Independence).
*   **Dataset B:** Stratified K-Fold (Sample Independence).

Grouped cross-validation is a significantly harder task for a classifier. Comparing results from these two strategies is inherently confounded. The lower performance on Dataset A likely reflects the "true" generalization difficulty of the task, while Dataset B's results may reflect an easier, seemingly independent task.

## 8.5 Model Selection Scope

The study was deliberately restricted to classical machine learning models (Logistic Regression, SVM, Random Forest) to establish a baseline and maintain interpretability.
*   **No Hyperparameter Optimization:** To test the robustness of the features rather than the tuning skill of the researcher, hyperparameters were largely kept fixed or at default values. It is possible that extensive grid search could improve the SVM performance on Dataset A.
*   **No Deep Learning:** Deep learning architectures (CNNs, RNNs, Transformers) were explicitly excluded. While these models represent the state-of-the-art, their application to a dataset of 37 subjects would likely lead to severe overfitting without extensive transfer learning or data augmentation, which were outside the scope of this thesis.

## 8.6 Recording Conditions

The raw audio in Dataset A (MDVR-KCL) consists of mobile device voice recordings.
*   **Uncontrolled Environment:** Unlike studio recordings, these files likely contain varying levels of background noise, microphone handling noise, and acoustic room reverberations.
*   **Preprocessing:** While basic feature extraction was performed, no advanced noise cancellation or source separation was applied. The extracted acoustic features (e.g., jitter, shimmer) are sensitive to environmental noise, which introduces unmodelled variance into the feature vectors.

## 8.7 Generalization Uncertainty

The models trained in this study are specific to the datasets provided. There was no external validation set (a third, independent dataset) to test true out-of-distribution generalization. Therefore, the reported metrics describe how well the models separate these specific recordings, not necessarily how well they would perform on a new patient in a clinical setting.

## 8.8 No Clinical Validation

Finally, it is imperative to state the non-clinical nature of this work.

> **Disclaimer:** This research is exploratory and academic in nature. The models developed here are not validated against clinical diagnostic criteria, have not been tested in clinical settings, and should not be used to inform medical decisions.

The classification outputs are research artifacts intended to evaluate signal processing and machine learning methodologies, not to diagnose Parkinson's Disease.
