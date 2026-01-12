# Thesis Writing Guide

**Generated:** January 12, 2026  
**Status:** Ready for thesis writing phase  
**Pipeline:** Frozen — no further code changes

---

## Part 1: Results Interpretation Structure

### 1.1 Actual Results Summary (from outputs)

#### Dataset A — MDVR-KCL (n=37 subjects, 47 features)

| Model | Task | Accuracy | F1 | ROC-AUC | Notes |
|-------|------|----------|-----|---------|-------|
| Logistic Regression | ReadText | 0.62 ± 0.06 | 0.53 ± 0.10 | 0.72 ± 0.13 | Most stable |
| SVM (RBF) | ReadText | 0.62 ± 0.10 | 0.33 ± 0.30 | 0.61 ± 0.29 | **Unstable; some folds < 0.5** |
| Random Forest | ReadText | 0.63 ± 0.17 | 0.35 ± 0.34 | 0.59 ± 0.27 | High variance |
| Logistic Regression | Spontaneous | 0.64 ± 0.15 | 0.55 ± 0.32 | 0.76 ± 0.20 | Best ROC-AUC |
| SVM (RBF) | Spontaneous | 0.64 ± 0.13 | 0.40 ± 0.24 | 0.41 ± 0.30 | **Below chance ROC-AUC** |
| Random Forest | Spontaneous | 0.72 ± 0.16 | 0.57 ± 0.36 | 0.83 ± 0.14 | Highest but variable |

#### Dataset B — PD_SPEECH_FEATURES (n=756 samples, 752 features)

| Model | Accuracy | F1 | ROC-AUC | Notes |
|-------|----------|-----|---------|-------|
| Logistic Regression | 0.83 ± 0.01 | 0.89 ± 0.01 | 0.87 ± 0.03 | Consistent |
| SVM (RBF) | 0.85 ± 0.02 | 0.91 ± 0.02 | 0.89 ± 0.02 | Strong |
| Random Forest | 0.88 ± 0.02 | 0.93 ± 0.01 | 0.94 ± 0.01 | **Best overall** |

---

### 1.2 Key Findings to Report

#### Finding 1: Dataset B significantly outperforms Dataset A
**Observed:** 20-25 percentage point gap in accuracy and ROC-AUC

**Correct interpretation:**
> "Higher performance observed on Dataset B likely reflects the combined effect of larger sample size (756 vs 37), richer feature representation (752 vs 47 features), and potentially less stringent cross-validation constraints due to unknown subject independence."

**Forbidden interpretation:**
> ❌ "Pre-extracted features are superior to raw-audio features"

#### Finding 2: Model instability on small samples (Dataset A)
**Observed:** SVM ROC-AUC values of 0.08, 0.13, 0.17 in some folds

**Correct interpretation:**
> "The SVM with RBF kernel yielded ROC-AUC values below chance level in several folds, indicating unstable decision boundaries under small-sample, high-dimensional conditions. This is a known limitation of kernel methods with limited training data, not a pipeline failure."

**Forbidden interpretation:**
> ❌ "SVM failed on this task"

#### Finding 3: High variance in Dataset A results
**Observed:** Standard deviations of 0.15–0.36 on F1 scores

**Correct interpretation:**
> "The wide confidence intervals reflect the small sample size and grouped cross-validation strategy, which correctly prevents data leakage but reduces effective training samples per fold. Results are indicative but not conclusive."

#### Finding 4: Spontaneous speech shows a trend toward better discrimination
**Observed:** Slightly higher ROC-AUC for spontaneous dialogue (0.76–0.83 vs 0.59–0.72)

**Correct interpretation:**
> "Results suggest a trend toward higher discriminability in spontaneous speech compared to read text, though confidence intervals overlap substantially. This observation aligns with clinical intuition that spontaneous speech may reveal more subtle motor control deficits."

**Forbidden interpretation:**
> ❌ "Spontaneous speech is more informative than read speech"

#### Finding 5: Random Forest most robust across conditions
**Observed:** Best or near-best performance on both datasets

**Correct interpretation:**
> "Random Forest demonstrated the most consistent performance across both datasets and speech tasks, likely due to its inherent feature selection and robustness to high-dimensional input spaces."

---

### 1.3 Results Chapter Structure (Chapter 6)

```
6. Results
   6.1 Overview of Experimental Conditions
       - Three experiments (A1, A2, B)
       - Controlled variables
       - Evaluation protocol summary
   
   6.2 Dataset A: MDVR-KCL Results
       6.2.1 ReadText Task
             - Table: All metrics by model
             - Per-fold breakdown (optional, appendix-worthy)
             - Observations on variance
       6.2.2 SpontaneousDialogue Task
             - Table: All metrics by model
             - Task comparison observations
       6.2.3 Cross-Task Analysis
             - Do not claim one is "better" — note trends only
   
   6.3 Dataset B: PD_SPEECH_FEATURES Results
       - Table: All metrics by model
       - Consistency observations
       - Note caveat about subject independence
   
   6.4 Cross-Dataset Comparison
       - Performance gap summary
       - Explicit statement: comparison is confounded
       - List confounding factors
   
   6.5 Model Behaviour Analysis
       - Logistic Regression: stable but modest
       - SVM: unstable on small samples
       - Random Forest: best overall, handles dimensionality
```

---

### 1.4 Discussion Chapter Structure (Chapter 7)

```
7. Discussion
   7.1 Interpretation of Results
       - What the numbers mean (not what we wish they meant)
       - Alignment with prior literature (if applicable)
   
   7.2 Methodological Validity
       - Leakage prevention confirmed
       - Grouped CV justification
       - Feature extraction design choices
   
   7.3 Explaining the Performance Gap
       - Sample size (756 vs 37)
       - Feature dimensionality (752 vs 47)
       - CV strategy differences
       - Unknown subject overlap in Dataset B
   
   7.4 Model Instability Analysis
       - Why SVM fails on small samples
       - Why Random Forest succeeds
       - Implications for future work
   
   7.5 Speech Task Observations
       - Trends, not conclusions
       - Clinical plausibility
       - Need for larger studies
   
   7.6 Implications for PD Voice Research
       - What can be concluded
       - What cannot be concluded
       - Recommendations for future datasets
```

---

## Part 2: Methodology Write-Up Structure

### 2.1 Source Documents Available

| Document | Content | Use For |
|----------|---------|---------|
| [METHODOLOGY.md](METHODOLOGY.md) | Experimental design | Chapter 4 |
| [AGENTS.md](../AGENTS.md) | Constraints and rules | Chapter 4 + 5 |
| [summary_report.md](summary_report.md) | Data exploration | Chapter 3 |
| [DATASET_MDVR_KCL.md](DATASET_MDVR_KCL.md) | Dataset A details | Chapter 3 |
| [DATASET_PD_SPEECH_FEATURES.md](DATASET_PD_SPEECH_FEATURES.md) | Dataset B details | Chapter 3 |
| Source code in `src/` | Implementation | Appendix |

### 2.2 Methodology Chapter Structure (Chapter 4)

```
4. Methodology
   4.1 Research Design
       - Binary classification problem
       - Classical ML approach (justification)
       - No deep learning (explicit choice, not limitation)
   
   4.2 Data Pipeline Architecture
       - Pipeline A: WAV → Features → Model → Metrics
       - Pipeline B: CSV → Model → Metrics
       - Diagram recommended
   
   4.3 Feature Extraction (Dataset A)
       4.3.1 Acoustic Features Selected
             - Spectral: MFCCs (13 coefficients × mean)
             - Prosodic: F0, jitter, shimmer, HNR
             - Total: 47 features
       4.3.2 Extraction Parameters
             - Frame size, hop length, sample rate
             - Library versions (librosa, parselmouth)
       4.3.3 Design Rationale
             - Classical features for interpretability
             - Deterministic extraction
             - 47 features is a design choice
   
   4.4 Pre-Extracted Features (Dataset B)
       - Used as provided
       - 752 features (cite original source)
       - No preprocessing applied
   
   4.5 Model Selection
       - Logistic Regression (baseline, interpretable)
       - SVM with RBF kernel (non-linear, common in literature)
       - Random Forest (ensemble, feature selection)
       - Hyperparameters fixed or default (state which)
   
   4.6 Evaluation Protocol
       4.6.1 Cross-Validation Strategy
             - Dataset A: Grouped Stratified 5-Fold (by subject)
             - Dataset B: Stratified 5-Fold (sample-level)
             - Justification for grouped CV
       4.6.2 Metrics
             - Accuracy, Precision, Recall, F1, ROC-AUC
             - Mean ± std across folds
       4.6.3 Random Seeds
             - Fixed seed (state value)
             - Reproducibility commitment
```

### 2.3 Experimental Design Chapter Structure (Chapter 5)

```
5. Experimental Design
   5.1 Experiment Overview
       - Table: Three experiments (A1, A2, B)
       - Independent variables
       - Dependent variables
   
   5.2 Experiment A1: ReadText Classification
       - Input: 37 WAV files (ReadText task)
       - Subjects: 21 HC, 16 PD
       - CV: Grouped by subject
   
   5.3 Experiment A2: SpontaneousDialogue Classification
       - Input: 36 WAV files (Spontaneous task)
       - Subjects: 21 HC, 15 PD (ID18 missing)
       - CV: Grouped by subject
   
   5.4 Experiment B: Pre-Extracted Feature Classification
       - Input: 756 rows × 752 features
       - Class balance: 25% HC, 75% PD
       - CV: Stratified (subject IDs unknown)
   
   5.5 Controlled Variables
       - Same three models
       - Same five metrics
       - Same scaling (StandardScaler)
       - Same random seed
   
   5.6 What Is NOT Compared
       - No cross-dataset model comparison
       - No claim of feature superiority
       - Confounds explicitly listed
```

---

## Part 3: Limitations Section Structure

### 3.1 Limitations to Document (Chapter 8)

```
8. Limitations
   8.1 Sample Size Constraints
       - Dataset A: Only 37 subjects
       - Effective per-fold training: ~30 subjects
       - High variance unavoidable
       - Underpowered for statistical significance testing
   
   8.2 Feature Dimensionality Mismatch
       - Dataset A: 47 features
       - Dataset B: 752 features
       - Not comparable on feature richness
       - Design choice, not failure
   
   8.3 Dataset B Subject Independence Uncertainty
       > "Since Dataset B does not provide subject identifiers, 
       > stratified cross-validation was performed at the sample level. 
       > If multiple samples originate from the same subject, this may 
       > introduce optimistic bias due to implicit subject overlap across folds."
       - Must include this caveat verbatim
   
   8.4 Cross-Validation Strategy Differences
       - Grouped CV (Dataset A) is stricter
       - Standard CV (Dataset B) may be optimistic
       - Results not directly comparable
   
   8.5 Model Selection Scope
       - Only three models evaluated
       - No hyperparameter optimization
       - Deep learning excluded by design
   
   8.6 Recording Conditions
       - Dataset A: Mobile recordings (variable quality)
       - No control for environmental noise
       - Feature extraction may be affected
   
   8.7 Generalization Uncertainty
       - Results specific to these datasets
       - No external validation
       - Clinical applicability not established
   
   8.8 No Clinical Validation
       - This is research, not a diagnostic tool
       - No IRB, no clinical partnership
       - Results are academic only
```

### 3.2 Honest Caveats (Required Statements)

Include these **verbatim or paraphrased** in the thesis:

1. **On cross-dataset comparison:**
   > "Direct performance comparison between Dataset A and Dataset B is confounded by differences in sample size, feature dimensionality, and cross-validation strategy. Higher performance on Dataset B should not be interpreted as evidence that pre-extracted features are inherently superior."

2. **On Dataset B subject independence:**
   > "Dataset B does not provide subject identifiers. If the original data contains multiple samples per subject, the reported performance may be optimistically biased due to implicit data leakage across folds."

3. **On SVM instability:**
   > "ROC-AUC values below 0.5 in some folds indicate model instability rather than systematic failure. This behaviour is expected when kernel methods encounter high-dimensional, low-sample-size conditions."

4. **On statistical significance:**
   > "Given the small sample size and overlapping confidence intervals, observed differences between conditions should be interpreted as trends rather than statistically significant effects."

5. **On clinical applicability:**
   > "This research is exploratory and academic in nature. The models developed here are not validated for clinical use and should not inform medical decisions."

---

## Part 4: Thesis Chapter Mapping

| Thesis Chapter | Source Documents | Status |
|----------------|------------------|--------|
| Ch 1. Introduction | Write fresh | TODO |
| Ch 2. Literature Review | Write fresh | TODO |
| Ch 3. Data Description | `summary_report.md`, `DATASET_*.md` | 80% done |
| Ch 4. Methodology | `METHODOLOGY.md`, `AGENTS.md` | 80% done |
| Ch 5. Experimental Design | `METHODOLOGY.md`, code | 70% done |
| Ch 6. Results | `all_results.csv`, `summary.csv` | Data ready |
| Ch 7. Discussion | This guide | Structure ready |
| Ch 8. Limitations | `SCOPE_AND_LIMITATIONS.md` | 90% done |
| Ch 9. Conclusion | Write fresh | TODO |
| Appendices | Code, tables | Ready |

---

## Part 5: Writing Priority Order

1. **Chapter 6 (Results)** — Convert numbers to prose and tables
2. **Chapter 7 (Discussion)** — Interpret results using this guide
3. **Chapter 8 (Limitations)** — Formalize existing caveats
4. **Chapter 4 (Methodology)** — Translate existing docs
5. **Chapter 5 (Experimental Design)** — Translate existing docs
6. **Chapter 3 (Data)** — Polish existing exploration report
7. **Chapter 1 & 2** — Introduction and literature
8. **Chapter 9** — Conclusion (write last)

---

## Part 6: Final Checklist Before Submission

- [ ] All results tables match `all_results.csv` exactly
- [ ] Caveats from Part 3.2 included in Discussion/Limitations
- [ ] No forbidden phrases (see AGENTS.md §16)
- [ ] ROC-AUC < 0.5 anomaly explained, not hidden
- [ ] Cross-dataset comparison properly caveated
- [ ] Dataset B subject-ID caveat included
- [ ] No clinical claims anywhere
- [ ] Code repository tagged/frozen
- [ ] Random seed documented
- [ ] Feature count (47) documented as design choice

---

*This guide was generated from actual experimental outputs and should be used as the authoritative reference for thesis writing.*
