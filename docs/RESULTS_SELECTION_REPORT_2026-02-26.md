# Results Selection Report for Thesis Integration

**Date:** 2026-02-26  
**Purpose:** Provide a comprehensive, thesis-safe evidence report so selected findings can be moved into Chapters 06–08 and appendices.

---

## 1) Scope and Evidence Base

### Scope used
- All 5 models: Logistic Regression, SVM (RBF), Random Forest, Gradient Boosting, XGBoost.
- Dataset A tasks: ReadText, SpontaneousDialogue.
- Dataset B: PD_SPEECH_FEATURES (N/A task).
- Primary evidence source: per-condition summaries (C1–C4).
- Sanity-check source: top-level baseline/weighted summaries.

### Files used as primary evidence
- `outputs/results/baseline/baseline/summary.csv` (C1)
- `outputs/results/weighted/baseline/summary.csv` (C2)
- `outputs/results/baseline/extended/summary.csv` (C3)
- `outputs/results/weighted/extended/summary.csv` (C4)

### Condition legend
- **C1:** Baseline features (47), unweighted.
- **C2:** Baseline features (47), class-weighted.
- **C3:** Extended features (78), unweighted.
- **C4:** Extended features (78), class-weighted.

---

## 2) Executive Findings (Thesis-Safe)

1. For **Dataset A / ReadText**, the strongest ROC-AUC values occur under extended features (C3/C4), with **SVM (RBF) = 0.834 ± 0.153** and **Random Forest = 0.822 ± 0.166 (C3)**.
2. For **Dataset A / SpontaneousDialogue**, the highest ROC-AUC is **Random Forest = 0.857 ± 0.171 (C3)**.
3. Moving from baseline to extended features shows a clear positive trend in **ReadText** for 4/5 models (largest deltas for RF, GB, SVM), while **SpontaneousDialogue** improvements are smaller and model-dependent.
4. Class weighting shows **inconsistent benefit** on Dataset A and does not provide a stable gain across tasks/models.
5. Dataset B shows high and low-variance scores (best ROC-AUC **XGBoost = 0.952 ± 0.015**), but interpretation should remain cautious due to unknown subject overlap.

---

## 3) Core Numeric Evidence You Can Reuse

## 3.1 Dataset A — ReadText (ROC-AUC, mean ± std)

| Model | C1 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.717 ± 0.139 | 0.717 ± 0.139 | 0.698 ± 0.132 | 0.698 ± 0.132 |
| SVM (RBF) | 0.614 ± 0.312 | 0.542 ± 0.312 | **0.834 ± 0.153** | **0.834 ± 0.153** |
| Random Forest | 0.590 ± 0.302 | 0.687 ± 0.258 | 0.822 ± 0.166 | 0.805 ± 0.182 |
| Gradient Boosting | 0.500 ± 0.159 | 0.500 ± 0.159 | 0.724 ± 0.214 | 0.724 ± 0.214 |
| XGBoost | 0.628 ± 0.203 | 0.628 ± 0.203 | 0.794 ± 0.186 | 0.794 ± 0.186 |

**Feature-set deltas (C3 − C1):**
- Logistic Regression: -0.019
- SVM (RBF): +0.220
- Random Forest: +0.232
- Gradient Boosting: +0.224
- XGBoost: +0.166

**Weighting deltas:**
- Baseline (C2 − C1): RF +0.097, SVM -0.072, others ~0.
- Extended (C4 − C3): RF -0.017, others ~0.

## 3.2 Dataset A — SpontaneousDialogue (ROC-AUC, mean ± std)

| Model | C1 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.760 ± 0.214 | 0.760 ± 0.214 | 0.783 ± 0.139 | 0.783 ± 0.139 |
| SVM (RBF) | 0.407 ± 0.309 | 0.423 ± 0.312 | 0.460 ± 0.294 | 0.403 ± 0.347 |
| Random Forest | 0.828 ± 0.148 | 0.827 ± 0.133 | **0.857 ± 0.171** | 0.823 ± 0.209 |
| Gradient Boosting | 0.615 ± 0.078 | 0.615 ± 0.078 | 0.638 ± 0.146 | 0.638 ± 0.146 |
| XGBoost | 0.723 ± 0.197 | 0.723 ± 0.197 | 0.687 ± 0.146 | 0.687 ± 0.146 |

**Feature-set deltas (C3 − C1):**
- Logistic Regression: +0.023
- SVM (RBF): +0.053
- Random Forest: +0.029
- Gradient Boosting: +0.023
- XGBoost: -0.036

**Weighting deltas:**
- Baseline (C2 − C1): very small (RF -0.001, SVM +0.016, others ~0).
- Extended (C4 − C3): RF -0.034, SVM -0.057, others ~0.

## 3.3 Dataset B — PD_SPEECH_FEATURES (ROC-AUC, mean ± std)

| Model | C1/C3 | C2/C4 |
|---|---:|---:|
| Logistic Regression | 0.867 ± 0.029 | 0.867 ± 0.029 |
| SVM (RBF) | 0.885 ± 0.025 | 0.900 ± 0.023 |
| Random Forest | 0.940 ± 0.013 | 0.949 ± 0.012 |
| Gradient Boosting | 0.937 ± 0.019 | 0.937 ± 0.019 |
| XGBoost | **0.952 ± 0.015** | **0.952 ± 0.015** |

**Observation:** Dataset B values are high with low std across models; report with explicit caveat on unknown subject overlap.

---

## 4) Stability and Uncertainty Notes (Use in Chapter 07/08)

- Dataset A shows materially larger fold variability (especially ROC-AUC and F1 std in several settings) than Dataset B.
- Example high-variance points: ReadText C1 RF ROC-AUC std = 0.302; Spontaneous C4 SVM ROC-AUC std = 0.347.
- Dataset B typically remains in low std bands (ROC-AUC approx. 0.012–0.029).
- Interpret differences as observed trends when uncertainty bands overlap.

---

## 5) Feature-Importance Synthesis (Cross-Model Patterns)

### Dataset A — ReadText
- Recurrent high-rank feature across all models: **f0_max**.
- Frequently recurring supporting features: **delta_mfcc_2_mean**, **f0_mean**, **intensity_min/intensity_mean**, selected MFCC means.
- Pattern suggests combined contribution of pitch-related and cepstral dynamics in structured speech.

### Dataset A — SpontaneousDialogue
- Strong recurring feature across all models: **mfcc_5_mean** (rank 1 for all four listed model families in the available top lists).
- Frequently recurring supporting features: **shimmer_apq11**, **delta_mfcc_8_mean**, **delta_mfcc_2_mean**, jitter-related features.
- Pattern suggests stronger role of spectral/perturbation dynamics in spontaneous speech.

### Dataset B
- Dominant features are mostly TQWT/entropy/energy and high-order cepstral-derived descriptors.
- This supports stronger separability in this dataset representation, while reducing direct interpretability relative to simpler acoustic sets.

---

## 6) Claim Bank (Ready to Pick for Thesis)

Use these as candidate statements and adapt tone to chapter context.

### High-confidence claims (main-text candidates)
1. Extended features are associated with substantial ReadText gains for non-linear models (RF/SVM/GB/XGB) under identical validation setup.
2. Random Forest under C3 achieves the highest ROC-AUC for SpontaneousDialogue in Dataset A (0.857 ± 0.171).
3. Class weighting does not show a consistent directional benefit on Dataset A across tasks/models.
4. Dataset B achieves higher and more stable internal CV scores than Dataset A but requires explicit caution due to unknown subject overlap.

### Moderate-confidence claims (prefer discussion/appendix context)
1. ReadText appears more responsive to feature extension than SpontaneousDialogue.
2. Task-dependent feature-importance profiles are observed, with pitch prominence in ReadText and MFCC/perturbation prominence in SpontaneousDialogue.

### Claims to avoid (or soften)
- Any strict model ranking language implying universal superiority.
- Causal statements attributing cross-dataset differences to one single factor.
- Diagnostic or clinical-effect wording.

---

## 7) Figure/Table Selection Matrix (Main vs Appendix)

## 7.1 Main chapter recommendations
- `outputs/plots/roc_curve_ReadText.pdf`
- `outputs/plots/roc_curve_SpontaneousDialogue.pdf`
- `outputs/plots/roc_curve_DatasetB.pdf`
- `outputs/plots/confusion_matrix_ReadText.pdf`
- `outputs/plots/confusion_matrix_SpontaneousDialogue.pdf`
- `outputs/plots/confusion_matrix_DatasetB.pdf`
- Keep compact comparison tables (best-per-task + RF across C1–C4).

## 7.2 Appendix recommendations
- `outputs/plots/heatmap_readtext.png`
- `outputs/plots/heatmap_spontaneous.png`
- Model-specific feature-importance figures for each task/dataset:
  - `outputs/plots/importance_readtext_*.png`
  - `outputs/plots/importance_spontaneous_*.png`
  - `outputs/plots/importance_pd_speech_*.png`
- Full per-model C1–C4 numeric tables (all mandatory metrics).

---

## 8) Suggested Insert Targets in Thesis (Where to Place Picked Items)

- **Chapter 06 (Results):** headline ROC-AUC tables, RF comparison table across C1–C4, ROC/confusion figures.
- **Chapter 07 (Discussion):** feature-extension effect interpretation, task-dependent feature-importance interpretation, uncertainty-overlap caution.
- **Chapter 08 (Limitations):** Dataset B optimistic-bias caveat, no external test set caveat, small-sample variance caveat for Dataset A.
- **Appendix B:** complete C1–C4 per-model per-metric tables.
- **Appendix A:** full feature-importance rankings and category summaries.

---

## 9) Sanity Check Notes

- Top-level `outputs/results/baseline/summary.csv` and `outputs/results/weighted/summary.csv` are consistent as aggregate views and were used only as cross-checks.
- Per-condition files remain the authoritative basis for claim-level reporting in this document.

---

## 10) Optional Next-Step Bundle (If Needed)

If desired, this report can be followed by a second deliverable containing:
1. 10–15 thesis-ready paragraph snippets (Chapter 06/07/08 grouped), and
2. a concise “insert checklist” with exact chapter anchors and suggested table/figure references.
