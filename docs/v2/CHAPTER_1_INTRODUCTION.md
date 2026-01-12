# Chapter 1: Introduction

## 1.1 Background and Motivation

Parkinson's Disease (PD) is the second most prevalent neurodegenerative disorder globally, affecting approximately 1% of the population over 60 years of age. Early and accurate detection remains a critical clinical challenge, as motor symptoms often manifest only after substantial neurological damage has occurred. Among the earliest observable symptoms are changes in speech and voice production, which can precede motor symptoms by several years.

Voice-based biomarkers offer a promising non-invasive avenue for PD detection. The disease affects the laryngeal muscles and respiratory control, resulting in measurable changes to prosodic features (pitch, intensity, rhythm) and spectral characteristics (formants, harmonics). These acoustic signatures can be captured using standard recording equipment, making voice analysis a cost-effective and accessible screening approach.

## 1.2 Problem Statement

Despite advances in voice-based PD classification, several methodological challenges persist:

1. **Small sample sizes** in raw audio datasets limit model generalizability
2. **Subject identity leakage** when multiple recordings per subject are split across folds
3. **Class imbalance** between PD and healthy control (HC) groups
4. **Feature representation choices** significantly impact classification performance

This thesis addresses these challenges through a rigorous experimental framework that prioritizes methodological validity over raw performance metrics.

## 1.3 Research Objectives

The primary objectives of this research are:

1. **Develop a reproducible pipeline** for extracting acoustic features from voice recordings
2. **Evaluate classical machine learning models** (Logistic Regression, SVM, Random Forest) for PD vs HC classification
3. **Compare performance** across two distinct datasets with different characteristics
4. **Investigate the impact** of feature set extension (47 → 78 features) through controlled ablation
5. **Assess the effect** of class weighting on imbalanced datasets

## 1.4 Contributions

This thesis makes the following contributions:

- A **subject-grouped cross-validation framework** that prevents data leakage in multi-recording datasets
- A **controlled feature ablation study** demonstrating +8.7 percentage points ROC-AUC improvement with extended features
- **Systematic comparison** of class weighting strategies across different imbalance levels
- **Transparent documentation** of methodological constraints and their implications

## 1.5 Thesis Organization

The remainder of this thesis is organized as follows:

| Chapter | Title | Description |
|---------|-------|-------------|
| 2 | Literature Review | Survey of voice-based PD detection methods |
| 3 | Data Description | Detailed analysis of datasets used |
| 4 | Methodology | Feature extraction and ML pipeline design |
| 5 | Experimental Design | Cross-validation and evaluation protocols |
| 6 | Results | Quantitative findings across all conditions |
| 7 | Discussion | Interpretation and comparison with literature |
| 8 | Limitations | Constraints and threats to validity |
| 9 | Conclusion | Summary and future directions |

## 1.6 Scope Boundaries

This research is explicitly bounded by the following constraints:

- **Binary classification only** (PD vs HC) — no severity prediction
- **Classical ML only** — no deep learning or end-to-end models
- **Research context only** — no clinical deployment or diagnostic claims
- **Reproducibility prioritized** — over leaderboard-style accuracy maximization
