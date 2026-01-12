# Chapter 9: Conclusion

## 9.1 Summary of Work

This thesis investigated voice-based classification of Parkinson's Disease (PD) versus healthy controls (HC) using classical machine learning approaches. The work addressed key methodological challenges in the field, including subject-level data leakage, class imbalance, and feature representation.

### 9.1.1 Contributions

1. **Rigorous Evaluation Framework**
   - Implemented grouped stratified cross-validation to prevent subject leakage
   - Systematic 2×2 factorial design (features × class weighting)
   - Transparent reporting of all conditions with confidence intervals

2. **Feature Engineering Investigation**
   - Extended feature set from 47 to 78 acoustic features
   - Demonstrated +8.7 percentage point ROC-AUC improvement
   - Identified most discriminative features (F0, MFCCs, harmonicity)

3. **Class Weighting Analysis**
   - Evaluated `class_weight="balanced"` across all models
   - Found modest effects on moderately imbalanced data
   - Documented interaction between features and weighting

4. **Reproducible Pipeline**
   - CLI-based tools for feature extraction and experiments
   - Fixed random seeds and documented parameters
   - Complete code repository with documentation

## 9.2 Key Findings

### 9.2.1 Primary Results

| Finding | Evidence |
|---------|----------|
| Best ROC-AUC: 0.873 ± 0.137 | Random Forest, Extended Features |
| Feature extension improves performance | +8.7pp ROC-AUC (baseline → extended) |
| Random Forest outperforms other models | Highest ROC-AUC across all conditions |
| Grouped CV is essential | Prevents optimistic bias from subject leakage |

### 9.2.2 Best Configuration

```
Model:           Random Forest
Features:        Extended (78)
Class Weighting: None
ROC-AUC:         0.873 ± 0.137
Accuracy:        82.6% ± 12.2%
```

### 9.2.3 Feature Importance Insights

The most discriminative features for PD detection include:

1. **f0_max** — Maximum fundamental frequency (pitch ceiling)
2. **delta_mfcc_2_mean** — Spectral dynamics
3. **autocorr_harmonicity** — Voice quality measure
4. **shimmer_apq3** — Amplitude perturbation
5. **intensity_mean** — Overall vocal intensity

These align with known clinical manifestations of PD: reduced pitch range, monotone speech, and hypophonia.

## 9.3 Research Questions Answered

### RQ1: How do classical ML models perform on PD voice classification?

Classical ML achieves **ROC-AUC up to 0.873** with Random Forest on the MDVR-KCL dataset using grouped cross-validation. This demonstrates the feasibility of voice-based PD screening, though performance varies substantially across folds due to small sample size.

### RQ2: Does feature set extension improve classification performance?

**Yes.** Extending from 47 baseline features to 78 features improved ROC-AUC by **+8.7 percentage points** for Random Forest. The additional features capturing spectral variability (MFCC std), temporal dynamics (delta-delta MFCC), and spectral shape contributed to this improvement.

### RQ3: Does class weighting improve performance on imbalanced datasets?

**Modestly.** On Dataset A (57:43 imbalance), class weighting improved Random Forest ROC-AUC by +3.5pp with baseline features. However, effects were inconsistent across models, and no benefit was observed when combined with extended features.

### RQ4: How do results compare between grouped and standard CV?

Dataset B (standard CV, no subject IDs) showed higher absolute performance than Dataset A (grouped CV), consistent with potential optimistic bias from subject leakage. **Grouped CV provides more conservative but more realistic estimates** of out-of-subject generalization.

## 9.4 Implications

### 9.4.1 For Researchers

- **Use grouped CV** when multiple recordings per subject exist
- **Include variability features** (std, delta-delta) in feature sets
- **Report all conditions** rather than cherry-picking best results
- **Acknowledge limitations** transparently

### 9.4.2 For Practitioners

- Voice-based PD screening is feasible but not yet clinical-grade
- Random Forest provides a robust baseline for similar tasks
- Feature interpretability supports clinical understanding
- Results require validation on independent cohorts

### 9.4.3 For Dataset Creators

- **Always include subject identifiers** to enable proper CV
- Document recording conditions and equipment
- Provide demographic information
- Consider longitudinal designs

## 9.5 Limitations Recap

Key limitations that bound the interpretation of results:

1. **Small sample size** (37 subjects) creates high variance
2. **No hyperparameter tuning** may underestimate potential
3. **Single dataset source** limits generalization claims
4. **Binary classification only** — no severity prediction
5. **No external validation** on independent test set

## 9.6 Future Directions

### 9.6.1 Short-term Extensions

- Hyperparameter optimization with nested CV
- Feature selection to reduce dimensionality
- Multi-task fusion (ReadText + SpontaneousDialogue)
- Additional acoustic features (wavelets, TQWT)

### 9.6.2 Medium-term Research

- External validation on independent datasets
- Deep learning with appropriate regularization
- Longitudinal tracking of disease progression
- Multi-class classification (severity levels)

### 9.6.3 Long-term Vision

- Integration into smartphone applications
- Multi-modal biomarkers (voice + gait + tremor)
- Personalized baselines for individual tracking
- Clinical validation studies

## 9.7 Closing Remarks

This thesis demonstrates that **voice-based Parkinson's Disease classification is feasible** using classical machine learning with carefully engineered acoustic features. The **+8.7pp improvement** from feature extension highlights the importance of capturing speech dynamics beyond simple statistical summaries.

However, the field faces significant challenges:

- Small datasets require rigorous methodology
- Subject identity must be tracked for valid evaluation
- Clinical deployment requires extensive validation

By prioritizing **methodological validity over performance optimization**, this work provides a foundation for future research that can build toward clinically useful applications. The transparent documentation of limitations ensures that results are interpreted appropriately and that subsequent studies can address identified gaps.

---

> *"The goal of rigorous science is not to claim perfection, but to understand the boundaries of our knowledge."*
