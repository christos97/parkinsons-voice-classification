# Scope and Limitations

This document explicitly defines the boundaries of this Master's thesis project to protect its academic integrity and set appropriate expectations.

## Project Scope

### What This Thesis Includes

1. **Binary classification research**
   - Classification of subjects as Parkinson's Disease (PD) or Healthy Control (HC)
   - Based on acoustic features derived from voice recordings

2. **Comparative analysis**
   - Comparison between raw audio feature extraction and pre-extracted features
   - Evaluation of multiple classical machine learning models
   - Analysis of factors affecting classification performance

3. **Reproducible experiments**
   - Version-controlled code and documentation
   - Fixed random seeds and documented procedures
   - Clear methodology for replication

4. **Academic documentation**
   - Thesis-quality writeup of methods and results
   - Suitable for peer review and supervision

### What This Thesis Excludes

1. **Clinical applications**
   - No diagnostic tool is developed
   - No clinical validation is performed
   - No medical recommendations are made

2. **Deployed systems**
   - No real-time classification system
   - No web application or API
   - No mobile or edge deployment

3. **Deep learning (initial phase)**
   - Neural networks are out of scope for the initial thesis
   - Focus remains on classical ML for interpretability
   - Deep learning may be addressed in future work

4. **Data collection**
   - No new data is collected
   - Existing public datasets are used
   - No clinical partnerships or IRB protocols

## Explicit Limitations

### No Clinical Diagnosis

⚠️ **This research does not provide clinical diagnosis.**

The models developed in this thesis:
- Are not validated against clinical diagnostic criteria
- Have not been tested in clinical settings
- Should not be used to inform medical decisions
- Do not replace professional medical evaluation

Any classification outputs are **research artefacts only**.

### No Real-Time or Deployed System

⚠️ **No operational system is built or deployed.**

This thesis:
- Does not produce a usable application
- Does not include user interfaces
- Does not provide APIs or services
- Is purely experimental and offline

### Dataset-Dependent Results

⚠️ **Results depend entirely on dataset quality and characteristics.**

Limitations arising from the datasets include:
- **Sample size:** Medical voice datasets are typically small
- **Population representation:** Subjects may not represent the broader PD population
- **Recording conditions:** Variability in audio quality may affect features
- **Label accuracy:** Diagnostic labels are assumed correct but not verified
- **Secondary sources:** Kaggle datasets may be derived from other collections

### Model Constraints

⚠️ **Only classical machine learning models are evaluated.**

This choice means:
- State-of-the-art deep learning approaches are not compared
- End-to-end learning from raw audio is not explored
- Results may not reflect the best possible performance

This limitation is intentional for interpretability and sample size appropriateness.

### Generalisation Uncertainty

⚠️ **Generalisation to new data is not guaranteed.**

The trained models:
- Are evaluated only on the provided datasets
- May not perform similarly on different populations
- May be sensitive to recording equipment differences
- Have not been tested prospectively

## Methodological Constraints

### Classical ML Focus

The thesis deliberately constrains itself to classical machine learning because:

1. **Interpretability:** Feature importance and model behaviour can be examined
2. **Sample efficiency:** Classical models perform better with limited data
3. **Reproducibility:** Results are deterministic and hardware-independent
4. **Baseline value:** Provides foundations for future deep learning work

### Same Evaluation Protocol

All experiments use identical evaluation protocols to ensure:

1. **Fair comparison:** No experiment receives preferential treatment
2. **Valid conclusions:** Differences reflect data representation, not methodology
3. **Reproducibility:** Others can replicate the evaluation approach

### Comparison Over Optimisation

The thesis prioritises:

- **Understanding** over maximum performance
- **Comparison** over single-model optimisation
- **Interpretation** over black-box accuracy
- **Reproducibility** over computational sophistication

## Academic Protections

### Honest Reporting

This thesis commits to:

- Reporting all results, including negative findings
- Not cherry-picking favourable outcomes
- Acknowledging when results are inconclusive
- Discussing limitations transparently

### No Overclaiming

The thesis will not:

- Claim clinical applicability without validation
- Suggest deployment readiness
- Overstate the significance of results
- Ignore contradictory evidence

### Future Work Acknowledgment

The thesis recognises that:

- Deep learning approaches may improve results
- Larger datasets would strengthen conclusions
- Clinical validation would be needed for any application
- Multi-class or severity classification remains unexplored

## Summary of Boundaries

| Aspect | In Scope | Out of Scope |
|--------|----------|--------------|
| Task | Binary classification research | Clinical diagnosis |
| Models | Classical ML | Deep learning |
| Data | Public Kaggle datasets | New data collection |
| Output | Experimental results | Deployed system |
| Validation | Cross-validation | Clinical trials |
| Claims | Research findings | Medical recommendations |

---

This scope definition ensures the thesis maintains academic integrity while clearly communicating its boundaries to supervisors, reviewers, and future readers.
