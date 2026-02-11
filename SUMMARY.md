# Voice-Based Classification of Parkinson's Disease Using Classical Machine Learning

**MSc Thesis Summary**

*January 2026*

> This document provides a condensed summary (~3 000 words) of the MSc thesis. For the full text, build the thesis PDF with `make thesis` from the repository root, or consult the LaTeX sources in `thesis/`.

---

## Abstract

Parkinson's Disease (PD) is the second most prevalent neurodegenerative disorder worldwide, and speech impairments — collectively termed hypokinetic dysarthria — affect 70–90 % of patients, often appearing years before formal diagnosis. Voice analysis therefore offers a promising avenue for non-invasive, low-cost screening. However, existing studies in the PD voice classification literature frequently suffer from methodological shortcomings: subject-level data leakage, unreported class imbalance handling, cherry-picked results, and opaque feature engineering choices.

This thesis applies three classical machine learning classifiers — Logistic Regression, Support Vector Machine (SVM, RBF kernel), and Random Forest — to two complementary datasets under a rigorous evaluation framework. A grouped stratified cross-validation scheme prevents subject leakage, and a controlled 2×2×3 factorial design isolates the effects of feature set extension and class weighting across models and speech tasks.

The best-performing configuration achieved a ROC-AUC of 0.857 ± 0.171 (Random Forest, extended features, spontaneous dialogue task) on Dataset A with grouped cross-validation. Extending the feature set from 47 to 78 acoustic features rescued the structured read-text task from near-chance performance (0.590 → 0.822 ROC-AUC, +23.2 percentage points). Dataset B, a larger pre-extracted benchmark, yielded 0.940 ± 0.013 — but these results may be optimistic due to unavailable subject identifiers.

The work prioritises methodological rigour and transparent reporting over leaderboard optimisation, contributing an evaluation framework, a reproducible pipeline, and a set of practical recommendations for future research.

---

## 1. Introduction & Motivation

Parkinson's Disease is a progressive neurodegenerative condition characterised by motor symptoms including tremor, bradykinesia, and rigidity. Among its less visible manifestations, speech degradation — reduced loudness, monotone pitch, imprecise articulation, and breathy voice quality — provides a rich source of quantifiable biomarkers. Voice recordings can be captured with commodity hardware (smartphones, laptops), making acoustic analysis an attractive complement to clinical examination.

Despite a growing body of research reporting high classification accuracies, a critical appraisal reveals four recurring methodological concerns:

1. **Subject-level data leakage.** Many studies split individual recordings rather than subjects across training and test folds, inflating reported performance.
2. **Small and imbalanced samples.** Datasets typically contain fewer than 50 subjects, yet variance is rarely reported alongside point estimates.
3. **Opaque feature engineering.** Feature sets vary widely across studies, with little controlled investigation of which features drive performance gains.
4. **Selective reporting.** Only the best model or configuration is presented, obscuring the sensitivity of results to design choices.

This thesis addresses these concerns through five research objectives: (i) build a reproducible, end-to-end classification pipeline; (ii) evaluate three classical ML classifiers under identical conditions; (iii) compare results across two datasets with different characteristics; (iv) conduct a controlled feature ablation study; and (v) assess the effect of class weighting on mildly imbalanced data.

The scope is deliberately bounded: deep learning is excluded (insufficient data for reliable training), no clinical or diagnostic claims are made, and severity prediction is left for future work.

---

## 2. Datasets

Two publicly available datasets provide complementary perspectives on the classification task.

**Dataset A — MDVR-KCL.** Collected at King's College London Hospital, this dataset contains smartphone recordings (Moto G4, September 2017) from 37 subjects performing two speech tasks:

- *ReadText*: 37 subjects (21 HC, 16 PD) reading a standardised passage.
- *SpontaneousDialogue*: 36 subjects (21 HC, 15 PD) in unscripted conversation.

Each subject contributed one or two recordings per task. Crucially, subject identifiers are available, enabling grouped cross-validation that prevents information from the same individual appearing in both training and test sets. The class ratio is approximately 57:43 (HC:PD), a mild imbalance.

**Dataset B — PD Speech Features.** Sourced from the UCI repository via Kaggle, this dataset provides 756 pre-extracted feature vectors (752 features) from sustained /a/ phonation recordings of 252 subjects (188 PD, 64 HC). The class ratio is inverted at roughly 25:75 (HC:PD). Subject identifiers are **not available**, meaning standard stratified cross-validation cannot guarantee that recordings from the same individual are excluded from the test fold. All results from Dataset B should therefore be interpreted with the caveat that they may be optimistically biased.

The two datasets are complementary: Dataset A offers rigorous subject-grouped evaluation on a small sample, while Dataset B provides statistical power through a larger sample at the cost of unknown subject overlap.

---

## 3. Methodology

### 3.1 Feature Engineering

For Dataset A, acoustic features are extracted from raw WAV files using a deterministic pipeline built on Parselmouth (Praat bindings) and librosa. Two feature sets are evaluated:

- **Baseline (47 features):** 21 prosodic features (fundamental frequency statistics, jitter variants, shimmer variants, harmonics-to-noise ratio, intensity statistics, formant frequencies F1–F3 with standard deviations) and 26 spectral features (13 MFCC means + 13 delta-MFCC means).
- **Extended (78 features):** The baseline set plus MFCC standard deviations (13), delta-delta MFCC means (13), and five spectral shape descriptors (spectral centroid, bandwidth, roll-off, flatness, zero-crossing rate) — totalling 31 additional features.

All extraction parameters are fixed: 22 050 Hz sample rate, F0 range 75–500 Hz, 13 MFCCs, 2 048-sample FFT window, 512-sample hop length, 128 mel filter bands.

Dataset B arrives pre-extracted and is used as-is; its 752 features include TQWT, wavelet, and numerous perturbation measures computed externally.

### 3.2 Classifiers

Three classical models are trained under identical conditions with fixed hyperparameters and no tuning:

| Model | Key Parameters | Rationale |
|---|---|---|
| Logistic Regression | C = 1.0, L2 penalty | Linear baseline; interpretable coefficients |
| SVM (RBF kernel) | C = 1.0, γ = scale | Non-linear boundary; strong on moderate-dimensional data |
| Random Forest | 100 trees, max depth = 10 | Ensemble averaging; robust to noise and overfitting |

All models use `random_state = 42` and are wrapped in sklearn `Pipeline` objects with `StandardScaler` normalisation. Hyperparameter tuning was deliberately omitted: with only 37 subjects in Dataset A, nested cross-validation would produce unreliable inner-loop estimates.

### 3.3 Evaluation Protocol

- **Dataset A:** Grouped Stratified 5-Fold cross-validation, ensuring all recordings from a given subject remain in the same fold. Fold composition is documented in the thesis (approximately 7–8 subjects per fold).
- **Dataset B:** Stratified 5-Fold cross-validation (grouped CV impossible without subject IDs).

Five metrics are computed per fold: Accuracy, Precision, Recall, F1-Score, and ROC-AUC (primary). All results are reported as **mean ± standard deviation** across folds — single-point estimates are never used.

Class weighting (`class_weight = 'balanced'` in sklearn) is included as a binary experimental factor alongside feature set, yielding a 2 × 2 × 3 factorial design (2 feature sets × 2 weighting schemes × 3 classifiers = 12 conditions per dataset/task combination).

---

## 4. Experimental Design

Five research questions structure the experiments:

- **RQ1:** How do classical ML models perform on voice-based PD classification with grouped cross-validation?
- **RQ2:** Does extending the feature set from 47 to 78 features improve classification?
- **RQ3:** Does class weighting improve performance under mild class imbalance?
- **RQ4:** How do grouped and standard CV compare across datasets?
- **RQ5:** Do different speech tasks (read vs. spontaneous) yield different performance?

A total of **180 experimental runs** were executed across three dataset–task combinations (ReadText, SpontaneousDialogue, Dataset B), each with 12 conditions and 5 folds. Total computation time was approximately 36 minutes.

---

## 5. Results

### 5.1 Headline Performance — Dataset A

The best ROC-AUC on Dataset A was achieved by Random Forest with extended features and no class weighting:

| Task | ROC-AUC | Accuracy |
|---|---|---|
| SpontaneousDialogue | 0.857 ± 0.171 | 77.9 % ± 16.1 % |
| ReadText | 0.822 ± 0.166 | 81.8 % ± 14.0 % |

SVM (RBF) also performed well on ReadText (0.834 ± 0.153) but collapsed on SpontaneousDialogue (0.460 ± 0.294), suggesting sensitivity to task-specific feature distributions. Logistic Regression was the most stable model across tasks (0.698–0.783 ROC-AUC) but did not reach the peaks achieved by Random Forest.

Standard deviations of 0.15–0.30 are observed throughout, reflecting the inherent instability of 5-fold evaluation with only 37 subjects (~7 per test fold). These results should be interpreted cautiously; relative comparisons between conditions are more informative than absolute values.

### 5.2 Feature Ablation

The most striking finding of the thesis is the task-dependent impact of feature extension:

| Task | Model | Baseline ROC-AUC | Extended ROC-AUC | Δ |
|---|---|---|---|---|
| ReadText | Random Forest | 0.590 ± 0.302 | 0.822 ± 0.166 | **+23.2 pp** |
| ReadText | SVM (RBF) | 0.614 ± 0.312 | 0.834 ± 0.153 | **+22.0 pp** |
| ReadText | Logistic Regression | 0.717 ± 0.139 | 0.698 ± 0.132 | −1.9 pp |
| SpontaneousDialogue | Random Forest | 0.828 ± 0.148 | 0.857 ± 0.171 | +2.9 pp |
| SpontaneousDialogue | Logistic Regression | 0.760 ± 0.214 | 0.783 ± 0.139 | +2.3 pp |

For ReadText, extending from 47 to 78 features rescued Random Forest and SVM from near-chance performance, with improvements exceeding 22 percentage points the ROC-AUC and simultaneous reductions in variance. The additional 31 features — MFCC standard deviations, delta-delta MFCCs, and spectral shape descriptors — capture temporal dynamics and spectral variability that appear critical for discriminating PD in structured reading.

For SpontaneousDialogue, the improvement was marginal (+2.9 pp for RF). Spontaneous speech apparently encodes PD-relevant cues (monotone prosody, reduced articulatory precision, diminished loudness variation) even in the baseline feature set, yielding diminishing returns from additional features.

Logistic Regression showed a slight degradation on ReadText with extended features (−1.9 pp), possibly due to overfitting on the additional 31 dimensions given only 37 subjects.

### 5.3 Dataset B — Benchmark Comparison

Dataset B's 756 pre-extracted samples produced substantially higher and more stable metrics:

| Model | ROC-AUC | Accuracy |
|---|---|---|
| **Random Forest** | **0.940 ± 0.013** | **88.2 % ± 1.9 %** |
| SVM (RBF) | 0.885 ± 0.025 | 85.1 % ± 2.4 % |
| Logistic Regression | 0.867 ± 0.029 | 82.8 % ± 0.8 % |

Variance is an order of magnitude lower than Dataset A (± 0.01 vs. ± 0.15), reflecting the 20× larger sample. However, these results may be optimistic due to unknown subject overlap across folds. The comparison between datasets is further confounded by different feature spaces (752 specialised vs. 47/78 acoustic), speech tasks (sustained phonation vs. read/spontaneous speech), and class distributions.

### 5.4 Class Weighting

Class weighting (`balanced`) was evaluated to address Dataset A's HC:PD ratio of approximately 1.3:1. The effect was negligible or negative:

- ReadText (RF, extended): unweighted 0.822 ± 0.166 vs. weighted 0.805 ± 0.182 → −1.7 pp
- SpontaneousDialogue (RF, extended): unweighted 0.857 ± 0.171 vs. weighted 0.823 ± 0.209 → −3.4 pp
- ReadText (RF, baseline): unweighted 0.590 ± 0.302 vs. weighted 0.687 ± 0.258 → +9.7 pp (only positive case, still below extended-unweighted)

The mild imbalance ratio does not appear to warrant reweighting. With extended features and grouped cross-validation, the unweighted configuration consistently performed best.

### 5.5 Hypothesis Summary

| Hypothesis | Result | Key Evidence |
|---|---|---|
| H1: Extended features improve ROC-AUC | Confirmed | +23.2 pp on ReadText (RF) |
| H2: Spontaneous speech yields better detection | Confirmed | 0.857 (Spontaneous) vs. 0.822 (ReadText), both RF extended |
| H3: Dataset B metrics are inflated vs. Dataset A | Confirmed | 0.940 (B) vs. 0.857 (A), confounded by design differences |
| H4: Random Forest yields highest ROC-AUC among classifiers | Confirmed | Highest or competitive ROC-AUC across all conditions |
| H5: Class weighting improves performance | **Rejected** | Marginal-to-negative impact under mild 1.3:1 imbalance |

---

## 6. Discussion

### Feature Extension Is Task-Dependent

The feature ablation results suggest that the discriminative value of extended spectral features depends critically on the speech task. Structured reading (ReadText) requires features that capture temporal dynamics and spectral variability — MFCC standard deviations, delta-delta coefficients, and spectral shape — to differentiate the subtle PD-related degradation in a constrained production. Spontaneous dialogue, by contrast, inherently exposes PD cues through natural prosodic variation (or lack thereof), reduced articulatory precision, and inconsistent loudness. The baseline 47 features are sufficient to capture these patterns.

This finding has practical implications: in screening scenarios where only short structured prompts are feasible, richer feature sets are essential. If spontaneous speech is available, simpler feature extraction may suffice.

### Model Hierarchy

Random Forest emerged as the most robust classifier, benefiting from ensemble averaging that stabilises predictions on small, noisy datasets. Logistic Regression provided a consistent but lower-ceiling baseline. SVM (RBF) showed high sensitivity to task and feature configuration — excellent on ReadText extended features (0.834) but collapsing on SpontaneousDialogue (0.460) — likely due to kernel sensitivity to the distributional properties of spontaneous speech features.

### Interpreting High Variance

Standard deviations of 0.15–0.30 on Dataset A are not a deficiency of the method but an honest reflection of fold-to-fold variability at n = 37. Some individual SVM folds produced ROC-AUC below 0.5, consistent with model instability rather than systematic failure. Dataset B's low variance (± 0.01–0.03) highlights the stabilising effect of larger sample sizes — but also underscores the risk that tight confidence intervals may mask optimistic bias from uncontrolled subject overlap.

### Feature Importance

Random Forest feature importance analysis revealed task-dependent patterns. For ReadText, the top features were F0 maximum (pitch ceiling), formant variability (F3 standard deviation), and autocorrelation-based harmonicity — aligning with clinical observations of reduced pitch range and voice quality degradation in PD. For SpontaneousDialogue, MFCC features (especially MFCC 5) and shimmer dominated, reflecting the broader spectral effects of PD on unscripted speech.

### Literature Context

The results are broadly consistent with prior work: Little et al. (2009) reported AUC 0.92 on sustained phonation with SVM, and Sakar et al. (2013) reported AUC 0.86 with multiple vocal features. Unlike these studies, the present work uses grouped cross-validation and reports all conditions, providing a more conservative but methodologically stronger estimate of generalisation performance.

---

## 7. Limitations

Several factors bound the interpretation of the results:

1. **Small sample size.** With 37 subjects in Dataset A, each test fold contains approximately 7 individuals. This produces high variance and limits statistical power for detecting meaningful differences between conditions.
2. **No hyperparameter tuning.** Fixed hyperparameters may underestimate the potential of each classifier. However, nested cross-validation at n = 37 would produce unreliable inner-loop estimates, and the risk of overfitting the validation scheme outweighs the potential benefit.
3. **Unknown subject identifiers in Dataset B.** Results from Dataset B (ROC-AUC 0.940 ± 0.013) may be optimistically biased due to potential subject leakage across folds.
4. **No external validation.** All evaluation is internal (cross-validation); performance on an entirely independent cohort remains unknown.
5. **Classical ML only.** Deep learning approaches (CNNs, RNNs, Transformers) were excluded by design given the data constraints but may yield improvements on larger datasets.
6. **Binary classification.** No attempt was made to predict disease severity, medication state, or progression.
7. **Single recording site and device.** Dataset A was collected at one hospital with one smartphone model, limiting generalisability to other acoustic environments.
8. **Deterministic feature set.** Feature engineering was hypothesis-driven; data-driven feature selection (e.g., recursive elimination, L1 regularisation) was not applied.

---

## 8. Conclusion

This thesis demonstrates that voice-based classification of Parkinson's Disease is feasible using classical machine learning with carefully engineered acoustic features. The four principal contributions are:

1. **A rigorous evaluation framework** using grouped stratified cross-validation that prevents subject leakage and reports all experimental conditions transparently.
2. **A controlled feature ablation study** showing that extending the feature set from 47 to 78 acoustic features improves ReadText ROC-AUC by up to 23.2 percentage points, while spontaneous dialogue benefits only marginally.
3. **A systematic class weighting analysis** demonstrating that mild class imbalance (1.3:1) does not require reweighting under grouped cross-validation.
4. **A fully reproducible pipeline** with CLI tools, fixed random seeds, and documented parameters, accompanied by a non-diagnostic research demonstration application.

The best configuration — Random Forest with 78 extended features on spontaneous dialogue — achieved ROC-AUC 0.857 ± 0.171 using grouped cross-validation, representing a conservative but methodologically sound estimate of out-of-subject generalisation.

### Future Directions

In the short term, hyperparameter tuning via nested cross-validation (on a larger dataset), feature selection, and multi-task fusion (combining ReadText and SpontaneousDialogue features) could extend the current framework. In the medium term, external validation on independent cohorts, exploration of deep learning with appropriate regularisation, and longitudinal tracking of disease progression would strengthen clinical relevance. The long-term vision includes integration into smartphone-based screening applications, multi-modal biomarker fusion (voice + gait + tremor), and formal clinical validation studies.

---

## How to Explore the Full Thesis

```bash
# Build the thesis PDF
make thesis

# Continuous rebuild on changes
make thesis-watch

# Run the full experimental pipeline
make pipeline

# Launch the research demonstration app
make demo
```

The LaTeX sources are located in `thesis/`, with individual chapters in `thesis/chapters/` and the bibliography in `thesis/references/references.bib`.
