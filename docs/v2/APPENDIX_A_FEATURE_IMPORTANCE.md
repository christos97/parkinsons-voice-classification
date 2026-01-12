# Appendix A: Feature Importance Tables

## A.1 Overview

This appendix presents the top-20 most important features for each experimental condition, as determined by model-native importance measures:

- **Logistic Regression:** Absolute coefficient values
- **Random Forest:** Gini importance (mean decrease in impurity)

## A.2 Dataset A — ReadText Task

### A.2.1 Random Forest — Top 20 Features

| Rank | Feature | Importance | Std |
|------|---------|------------|-----|
| 1 | f0_max | 0.052 | 0.019 |
| 2 | delta_mfcc_2_mean | 0.039 | 0.018 |
| 3 | f3_std | 0.038 | 0.011 |
| 4 | autocorr_harmonicity | 0.038 | 0.017 |
| 5 | intensity_mean | 0.035 | 0.021 |
| 6 | f0_mean | 0.032 | 0.012 |
| 7 | shimmer_apq3 | 0.032 | 0.013 |
| 8 | mfcc_12_mean | 0.031 | 0.007 |
| 9 | f1_std | 0.031 | 0.022 |
| 10 | mfcc_6_mean | 0.030 | 0.024 |

**Visualization:**

![Feature Importance - ReadText - Random Forest](../outputs/plots/importance_readtext_randomforest.png)

*Figure A.1: Top-20 feature importances for Random Forest on ReadText task.*

### A.2.2 Logistic Regression — Top 20 Features

| Rank | Feature | |Coefficient| | Std |
|------|---------|-------------|-----|
| 1 | f0_max | 0.754 | 0.203 |
| 2 | hnr_mean | 0.649 | 0.178 |
| 3 | shimmer_apq11 | 0.553 | 0.145 |
| 4 | delta_mfcc_4_mean | 0.496 | 0.163 |
| 5 | delta_mfcc_2_mean | 0.492 | 0.103 |
| 6 | delta_mfcc_1_mean | 0.474 | 0.273 |
| 7 | mfcc_5_mean | 0.470 | 0.127 |
| 8 | mfcc_4_mean | 0.426 | 0.233 |
| 9 | mfcc_10_mean | 0.418 | 0.221 |
| 10 | mfcc_11_mean | 0.388 | 0.192 |

**Visualization:**

![Feature Importance - ReadText - Logistic Regression](../outputs/plots/importance_readtext_logisticregression.png)

*Figure A.2: Top-20 feature importances for Logistic Regression on ReadText task.*

### A.2.3 Feature Importance by Category

![Feature Importance by Category - ReadText](../outputs/plots/importance_readtext_categories.png)

*Figure A.3: Aggregated feature importance by category for ReadText task.*

### A.2.4 Cross-Model Heatmap

![Feature Importance Heatmap - ReadText](../outputs/plots/heatmap_readtext.png)

*Figure A.4: Normalized feature importance heatmap comparing models on ReadText task.*

---

## A.3 Dataset A — SpontaneousDialogue Task

### A.3.1 Random Forest — Top 20 Features

| Rank | Feature | Importance | Std |
|------|---------|------------|-----|
| 1 | mfcc_5_mean | 0.080 | 0.022 |
| 2 | shimmer_apq11 | 0.069 | 0.007 |
| 3 | delta_mfcc_8_mean | 0.051 | 0.015 |
| 4 | jitter_local | 0.041 | 0.012 |
| 5 | delta_mfcc_2_mean | 0.040 | 0.018 |
| 6 | autocorr_harmonicity | 0.037 | 0.011 |
| 7 | shimmer_local | 0.036 | 0.017 |
| 8 | mfcc_1_mean | 0.034 | 0.010 |
| 9 | f0_std | 0.032 | 0.022 |
| 10 | f0_mean | 0.031 | 0.013 |

**Visualization:**

![Feature Importance - Spontaneous - Random Forest](../outputs/plots/importance_spontaneous_randomforest.png)

*Figure A.5: Top-20 feature importances for Random Forest on SpontaneousDialogue task.*

### A.3.2 Logistic Regression — Top 20 Features

| Rank | Feature | |Coefficient| | Std |
|------|---------|-------------|-----|
| 1 | mfcc_5_mean | 0.722 | 0.039 |
| 2 | delta_mfcc_8_mean | 0.615 | 0.121 |
| 3 | shimmer_apq11 | 0.559 | 0.136 |
| 4 | delta_mfcc_2_mean | 0.493 | 0.196 |
| 5 | intensity_min | 0.459 | 0.170 |
| 6 | mfcc_3_mean | 0.388 | 0.271 |
| 7 | delta_mfcc_11_mean | 0.381 | 0.102 |
| 8 | delta_mfcc_7_mean | 0.380 | 0.150 |
| 9 | hnr_mean | 0.379 | 0.175 |
| 10 | delta_mfcc_1_mean | 0.352 | 0.123 |

**Visualization:**

![Feature Importance - Spontaneous - Logistic Regression](../outputs/plots/importance_spontaneous_logisticregression.png)

*Figure A.6: Top-20 feature importances for Logistic Regression on SpontaneousDialogue task.*

### A.3.3 Feature Importance by Category

![Feature Importance by Category - Spontaneous](../outputs/plots/importance_spontaneous_categories.png)

*Figure A.7: Aggregated feature importance by category for SpontaneousDialogue task.*

### A.3.4 Cross-Model Heatmap

![Feature Importance Heatmap - Spontaneous](../outputs/plots/heatmap_spontaneous.png)

*Figure A.8: Normalized feature importance heatmap comparing models on SpontaneousDialogue task.*

---

## A.4 Dataset B — PD Speech Features

### A.4.1 Random Forest — Top 20 Features

| Rank | Feature | Importance | Std |
|------|---------|------------|-----|
| 1 | std_delta_log_energy | 0.013 | 0.004 |
| 2 | std_delta_delta_log_energy | 0.013 | 0.003 |
| 3 | tqwt_entropy_shannon_dec_12 | 0.012 | 0.001 |
| 4 | tqwt_TKEO_std_dec_11 | 0.010 | 0.004 |
| 5 | tqwt_TKEO_mean_dec_12 | 0.010 | 0.001 |
| 6 | mean_MFCC_2nd_coef | 0.008 | 0.003 |
| 7 | tqwt_entropy_log_dec_11 | 0.008 | 0.003 |
| 8 | tqwt_stdValue_dec_12 | 0.008 | 0.003 |
| 9 | tqwt_stdValue_dec_13 | 0.008 | 0.003 |
| 10 | tqwt_energy_dec_12 | 0.007 | 0.003 |

**Note:** Dataset B uses 752 pre-extracted features including TQWT (Tunable Q-factor Wavelet Transform) coefficients not present in Dataset A.

**Visualization:**

![Feature Importance - PD Speech - Random Forest](../outputs/plots/importance_pd_speech_randomforest.png)

*Figure A.9: Top-20 feature importances for Random Forest on Dataset B.*

### A.4.2 Logistic Regression — Top 20 Features

| Rank | Feature | |Coefficient| | Std |
|------|---------|-------------|-----|
| 1 | tqwt_kurtosisValue_dec_33 | 0.733 | 0.161 |
| 2 | tqwt_entropy_log_dec_33 | 0.694 | 0.084 |
| 3 | mean_MFCC_7th_coef | 0.614 | 0.148 |
| 4 | std_delta_delta_log_energy | 0.588 | 0.133 |
| 5 | std_MFCC_2nd_coef | 0.567 | 0.202 |
| 6 | tqwt_meanValue_dec_16 | 0.551 | 0.114 |
| 7 | tqwt_medianValue_dec_25 | 0.540 | 0.209 |
| 8 | mean_MFCC_3rd_coef | 0.538 | 0.155 |
| 9 | tqwt_meanValue_dec_22 | 0.528 | 0.172 |
| 10 | std_9th_delta | 0.526 | 0.103 |

**Visualization:**

![Feature Importance - PD Speech - Logistic Regression](../outputs/plots/importance_pd_speech_logisticregression.png)

*Figure A.10: Top-20 feature importances for Logistic Regression on Dataset B.*

---

## A.5 Cross-Task Feature Consistency

### A.5.1 Features Appearing in Top-10 Across Multiple Tasks

| Feature | ReadText RF | Spontaneous RF | Consistent |
|---------|-------------|----------------|------------|
| f0_mean | Rank 6 | Rank 10 | ✅ |
| delta_mfcc_2_mean | Rank 2 | Rank 5 | ✅ |
| autocorr_harmonicity | Rank 4 | Rank 6 | ✅ |
| shimmer_apq3/local | Rank 7 | Rank 7 | ✅ |

### A.5.2 Interpretation

The consistency of certain features (F0, delta MFCCs, harmonicity, shimmer) across tasks suggests these capture **task-general** acoustic signatures of Parkinson's Disease rather than task-specific artifacts.

---

## A.6 Feature Category Summary

### A.6.1 Category Rankings by Aggregated Importance

| Category | ReadText | Spontaneous | Overall |
|----------|----------|-------------|---------|
| MFCC | 1 | 1 | **1** |
| Pitch (F0) | 2 | 3 | **2** |
| Shimmer | 4 | 2 | **3** |
| Delta MFCC | 3 | 4 | **4** |
| Formants | 5 | 6 | **5** |
| Harmonicity | 6 | 5 | **6** |

### A.6.2 Key Observation

MFCC-based features (mean, std, delta) consistently dominate across all tasks and models, highlighting the importance of spectral envelope characteristics for PD voice classification.
