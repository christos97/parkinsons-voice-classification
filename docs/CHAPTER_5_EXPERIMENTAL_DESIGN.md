# Chapter 5: Experimental Design

This chapter specifies the structure of the three experiments conducted in this thesis. It details the input data, subject composition, and specific variables controlled in each experiment.

## 5.1 Experiment Overview

To address the research question, the study was divided into three distinct experimental runs.

| Experiment | Dataset | Task | Subjects (N) | Features (D) | CV Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A1** | MDVR-KCL | Read Text | 37 (21 HC, 16 PD) | 47 | Grouped Stratified |
| **A2** | MDVR-KCL | Spontaneous Dialogue | 36 (21 HC, 15 PD) | 47 | Grouped Stratified |
| **B** | PD_SPEECH_... | Mixed/Unknown | 756 samples | 752 | Stratified (Sample) |

## 5.2 Experiment A1: ReadText Classification

*   **Objective:** Assess classification performance on standardized reading tasks using the raw audio pipeline.
*   **Input Data:** 37 `.wav` files from the `ReadText` directory of Dataset A.
*   **Class Balance:** 57% Healthy Control, 43% Parkinson's Disease.
*   **Splitting:** 5-Fold Subject-Grouped.
    *   *Training:* ~30 subjects.
    *   *Testing:* ~7 subjects.
*   **Hypothesis:** Reading tasks reduce linguistic variability, potentially making acoustic prosodic features more reliable.

## 5.3 Experiment A2: SpontaneousDialogue Classification

*   **Objective:** Assess classification performance on unstructured speech using the same raw audio pipeline.
*   **Input Data:** 36 `.wav` files from the `SpontaneousDialogue` directory of Dataset A.
*   **Subject Note:** Subject `ID18` (PD) was excluded as the recording was missing from the source dataset.
*   **Class Balance:** 58% Healthy Control, 42% Parkinson's Disease.
*   **Splitting:** 5-Fold Subject-Grouped.
*   **Hypothesis:** Spontaneous speech places higher cognitive and motor demands on the speaker, potentially revealing subtle vocal impairments that reading tasks mask.

## 5.4 Experiment B: Pre-Extracted Feature Classification

*   **Objective:** Assess classification performance using a larger, professionally curated feature set (Dataset B).
*   **Input Data:** 756 rows of tabular data.
*   **Class Balance:** 25% Healthy Control, 75% Parkinson's Disease.
*   **Features:** 752 acoustic features (Baseline, Wavelet, TQWT, etc.).
*   **Splitting:** 5-Fold Stratified (Sample-level).
*   **Role:** Serves as a performance benchmark for what is achievable with high-dimensional feature engineering, subject to the limitations of unknown subject overlap.

## 5.5 Controlled Variables

To allow for meaningful analysis within each experiment, the following variables were strictly controlled:

1.  **Model Hyperparameters:** Default parameters were used across all experiments to avoid manual tuning bias.
    *   *Logistic Regression:* `solver='lbfgs'`, `max_iter=1000`.
    *   *SVM:* `kernel='rbf'`, `probability=True`.
    *   *Random Forest:* `n_estimators=100`.
2.  **Data Scaling:** All features were standardized to zero mean and unit variance.
3.  **Randomness:** The exact same random seed `42` was used to generate splits for all models.

## 5.6 What Is NOT Compared

The experimental design explicitly prohibits certain comparisons to maintain scientific integrity.

*   **No "Better vs. Worse" Feature Claims:** We do not claim that the 47 features in Experiment A are "better" or "worse" than the 752 features in Experiment B. They are simply different representations.
*   **No Cross-Task Mixing:** `ReadText` and `SpontaneousDialogue` samples were never mixed in the same training set. They were treated as separate tasks to prevent task type from becoming a confounding variable.
