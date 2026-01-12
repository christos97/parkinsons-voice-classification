---
project: "Parkinson’s Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson’s Disease vs Healthy Controls)"
language: "English"
last_updated: "2026-01-12"

repository_state:
  datasets_downloaded: true
  codebase_status: "Complete (experiments run, thesis chapters 3–8 drafted)"
  primary_entrypoints:
    extract_features_cli: "pvc-extract"
    run_experiments_cli: "pvc-experiment"
  cli_usage:
    extract: "pvc-extract --task [ReadText|SpontaneousDialogue|all] [--jobs N]"
    experiment: "pvc-experiment"
  make_targets:
    extract_all: "make extract-all"
    experiments: "make experiments"
    results: "make results"
    pipeline: "make pipeline  # extract-all + experiments"
    clean: "make clean  # remove all outputs"

datasets:
  dataset_a:
    name: "MDVR-KCL (Mobile Device Voice Recordings – King’s College London)"
    type: "Raw audio (WAV)"
    source: "Zenodo"
    zenodo_doi: "10.5281/zenodo.2867215"
    data_card_url: "https://zenodo.org/records/2867215"
    local_path: "assets/DATASET_MDVR_KCL/"
    tasks: ["ReadText", "SpontaneousDialogue"]
    subjects_per_task:
      ReadText: { total: 37, HC: 21, PD: 16 }
      SpontaneousDialogue: { total: 36, HC: 21, PD: 15 }
    unit_of_analysis: "Recording (WAV) grouped by subject"
    known_anomalies:
      - "ID22 filename parsing edge case (handled in code)"
      - "ID18 missing from SpontaneousDialogue task"
    description: >
      Raw voice recordings from Parkinson’s Disease patients and Healthy Controls.
      Multiple recordings per subject across two speech tasks. Subject identity is encoded
      in filenames and must be used for grouped cross-validation to prevent leakage.

  dataset_b:
    name: "Parkinson’s Disease Speech Signal Features"
    type: "Pre-extracted acoustic features (CSV)"
    source: "Kaggle"
    data_card_url: "https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features/data"
    example_notebook_url: "https://www.kaggle.com/code/parhamzm/parkinson-s-disease-pd-classification/notebook"
    local_path: "assets/PD_SPEECH_FEATURES.csv"
    unit_of_analysis: "Sample row (subject identifiers not provided)"
    description: >
      Tabular dataset containing 752 pre-extracted acoustic speech features for PD/HC classification.
      Used directly for classical ML. Subject identifiers are not provided; results may be optimistic
      if multiple samples per subject exist.

methodology_constraints:
  ml_type: "Classical ML only (Logistic Regression, SVM_RBF, Random Forest)"
  deep_learning_allowed: false
  deployment: false
  clinical_use: false
  leakage_prevention:
    dataset_a: "Grouped stratified 5-fold CV by subject_id"
    dataset_b: "Stratified 5-fold CV (subject IDs unavailable; caveat required in writeup)"

features:
  baseline:
    total: 47
    prosodic: 21
    spectral: 26
  extended:
    total: 78
    description: "Baseline + additional MFCC statistics and spectral features"
  config_reference: "src/parkinsons_voice_classification/config.py"

results_snapshot:
  date: "2026-01-12"
  dataset_a_best: "Random Forest / SpontaneousDialogue ≈ 0.83 ROC-AUC"
  dataset_b_best: "Random Forest ≈ 0.94 ROC-AUC"
  performance_gap_note: >
    Performance gap attributed to differences in sample size, feature dimensionality,
    and cross-validation rigor rather than feature extraction quality alone.
---

# Strict Rules for AI Coding Agents

## Parkinson’s Disease Voice Classification Thesis

---

## 0. Scope of This Repository

This repository supports a **Master’s thesis** focused on **binary classification of Parkinson’s Disease (PD) vs Healthy Controls (HC)** using **voice data**.

This is a **research-only project**.

❌ No application  
❌ No deployment  
❌ No clinical or diagnostic system  

---

## 1. Core ML Principle (Non-Negotiable)

> **Machine Learning models NEVER consume WAV files.**  
> **They ONLY consume numeric feature tables (`X`, `y`).**

- Dataset A **must** undergo feature extraction
- Dataset B **already contains features**

This is why all valid pipelines operate on **features**, not raw audio.

---

## 2. Pipeline Separation Rule (CRITICAL)

Two pipelines exist and must never be conflated:

### Pipeline A — Raw Audio

```txt
WAV → Feature Extraction → Feature Table → ML → Metrics
```

### Pipeline B — Pre-extracted Features

```txt
CSV → ML → Metrics
```

❌ Never train models directly on WAV files  
❌ Never mix pipelines during comparison  

---

## 3. Absolute DO NOTs (Hard Constraints)

The agent must **never**:

❌ Train models on raw audio  
❌ Treat WAV files as independent subjects  
❌ Perform file-level splits for Dataset A  
❌ Split recordings from the same subject across folds  
❌ Mix speech tasks without documentation  
❌ Assume Dataset A and Dataset B share subjects  
❌ Merge Dataset A and Dataset B at subject level  
❌ Use deep learning (CNNs, RNNs, Transformers)  
❌ Use spectrogram images as model input  
❌ Optimize for leaderboard performance  
❌ Make medical, diagnostic, or clinical claims  

Any violation **invalidates the experiment**.

---

## 4. Mandatory Subject-Level Handling (Dataset A)

For MDVR-KCL:

> **All data splits MUST be performed at the SUBJECT level.**

- All recordings of a subject must belong to **one fold only**
- This prevents **data leakage**

---

## 5. Speech Task Handling Rules

Dataset A contains two distinct speech tasks:

- `ReadText`
- `SpontaneousDialogue`

Allowed approaches (must be documented):

- Use only one task
- Treat tasks as separate experiments
- Encode task as an explicit feature

❌ Silent mixing is forbidden.

---

## 6. Feature Extraction Rules (Dataset A)

Feature extraction must be:

- deterministic
- reproducible
- uniformly applied
- fully documented

Rules:

- One WAV → one feature vector
- Output must be tabular numeric data
- Parameters must be fixed and recorded

---

## 7. Model Constraints

Only **classical, interpretable ML models** are allowed:

- Logistic Regression
- SVM (RBF)
- Random Forest

The **same model set** must be used across datasets.

---

## 8. Evaluation Rules

Metrics (mandatory):

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Cross-validation:

- Dataset A: Grouped Stratified K-Fold
- Dataset B: Stratified K-Fold (subject caveat required)

Random seeds must be fixed.

---

## 9. Results Interpretation Rules

### ROC-AUC < 0.5

Document as **model instability**, not pipeline failure.

### Overlapping confidence intervals

Use *“suggests”* or *“trend toward”*, never definitive claims.

### Dataset B subject independence

Always include:
> “Results may be optimistic due to unknown subject overlap.”

### Cross-dataset comparisons

Never attribute performance differences to a single factor.

---

## 10. Forbidden Language

❌ “X outperforms Y”  
❌ “This proves…”  
❌ “Clearly superior”  
❌ “This system diagnoses…”  

Allowed:
✅ “Results suggest…”  
✅ “Observed under identical classifiers…”  
✅ “Should be interpreted cautiously…”

---

## 11. Guiding Principle

> **Methodological validity and reproducibility  
> outweigh performance or complexity.**

If a choice risks leakage, bias, or ambiguity — **reject it**.

---

## End of Rules
