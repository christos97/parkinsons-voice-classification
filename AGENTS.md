---
project: "Parkinson’s Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson’s Disease vs Healthy Controls)"
language: "English"
last_updated: "2026-01-12"
repository_state:
  datasets_downloaded: true
  codebase_status: "Complete (experiments run, thesis chapters 3-8 drafted)"
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
      ReadText: {total: 37, HC: 21, PD: 16}
      SpontaneousDialogue: {total: 36, HC: 21, PD: 15}  # ID18 missing
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

reference_notebooks:
  - name: "PD Classification (tabular pipeline reference)"
    url: "https://www.kaggle.com/code/parhamzm/parkinson-s-disease-pd-classification/notebook"
    role: "Reference for features → models → metrics pattern (not for deep learning or leaderboard chasing)"
    applies_to: ["Dataset B", "Dataset A after feature extraction"]

data_availability:
  status: "Downloaded"
  note: "Datasets are already present locally and must not be re-fetched."

methodology_constraints:
  ml_type: "Classical ML only (Logistic Regression, SVM_RBF, Random Forest)"
  deep_learning_allowed: false
  deployment: false
  clinical_use: false
  leakage_prevention:
    dataset_a: "Grouped stratified 5-fold CV by subject_id"
    dataset_b: "Stratified 5-fold CV (subject IDs unavailable; caveat required in writeup)"

features:
  total: 47
  prosodic: 21  # F0 stats, jitter (3), shimmer (3), HNR, intensity (3), formants F1-F3 (6)
  spectral: 26  # MFCC 0-12 mean (13) + Delta MFCC 0-12 mean (13)
  config_reference: "src/parkinsons_voice_classification/config.py"

artifacts:
  extracted_features:
    dataset_a_readtext: "outputs/features/features_readtext.csv"
    dataset_a_spontaneous: "outputs/features/features_spontaneousdialogue.csv"
  experiment_results:
    all_results: "outputs/results/all_results.csv"
    summary: "outputs/results/summary.csv"
  notes:
    parallel_extraction_supported: true
    extract_jobs_flag: "--jobs / -j"

results_snapshot:
  date: "2026-01-12"
  status: "Complete"
  experiments_run:
    A1_ReadText: {subjects: 37, cv: "GroupedStratified5Fold"}
    A2_SpontaneousDialogue: {subjects: 36, cv: "GroupedStratified5Fold"}
    B_PD_SPEECH_FEATURES: {samples: 756, cv: "Stratified5Fold"}
  key_results:
    dataset_a_best: "RF/Spontaneous: 72% accuracy, 0.83 ROC-AUC"
    dataset_b_best: "RF: 88% accuracy, 0.94 ROC-AUC"
    performance_gap: "20-25pp gap attributed to sample size (756 vs 36-37), feature dimensionality (752 vs 47), and CV rigor differences"
  note: "Re-running experiments will overwrite outputs/results/*.csv."

documentation:
  thesis_chapters_markdown:
    - {file: "docs/CHAPTER_3_DATA_DESCRIPTION.md", status: "Complete"}
    - {file: "docs/CHAPTER_4_METHODOLOGY.md", status: "Complete"}
    - {file: "docs/CHAPTER_5_EXPERIMENTAL_DESIGN.md", status: "Complete"}
    - {file: "docs/CHAPTER_6_RESULTS.md", status: "Complete"}
    - {file: "docs/CHAPTER_7_DISCUSSION.md", status: "Complete"}
    - {file: "docs/CHAPTER_8_LIMITATIONS.md", status: "Complete"}
  thesis_chapters_pdf:
    - "docs/Chapter 1_ Introduction.pdf"
    - "docs/Chapter 2 — Literature Review.pdf"
    - "docs/Chapter 9 – Conclusion.pdf"
  data_cards:
    - "docs/DATASET_MDVR_KCL.md"
    - "docs/DATASET_PD_SPEECH_FEATURES.md"
  guides:
    - "docs/THESIS_WRITING_GUIDE.md"
    - "docs/summary_report.md"
    - "docs/SCOPE_AND_LIMITATIONS.md"
---


# Strict Rules for AI Coding Agents

## Parkinson’s Disease Voice Classification Thesis

---

## 0. Scope of This Repository

This repository supports a **Master’s thesis** focused on **binary classification of Parkinson’s Disease (PD) vs Healthy Controls (HC)** using **voice data**.

The repository contains:

- **Dataset A:** Raw voice recordings (WAV files)
- **Dataset B:** Pre-extracted acoustic speech features (CSV)

This is a **research-only project**.

❌ No application  
❌ No deployment  
❌ No clinical or diagnostic system  

---

## 1. Datasets Under Management

### 1.1 Dataset A — MDVR-KCL (Raw Audio)

**Location:**

```

assets/DATASET_MDVR_KCL/

```

**Properties:**

- Raw `.wav` recordings
- Two speech tasks:
  - `ReadText`
  - `SpontaneousDialogue`
- Two classes:
  - `HC` (Healthy Control)
  - `PD` (Parkinson’s Disease)
- **Multiple recordings per subject**

**Filename format (with documented edge cases):**

```

IDxx_[hc|pd]_*.wav

```

Example:

```

ID02_pd_2_0_0.wav

```

Subject identity is encoded in filenames and **must be parsed correctly**.

---

### 1.2 Dataset B — PD_SPEECH_FEATURES (Pre-extracted Features)

**Location:**

```

assets/PD_SPEECH_FEATURES.csv

```

**Properties:**

- Tabular numeric data
- One row per sample (treated as one subject)
- 752 acoustic features
- Binary label column (`class`)
- No raw audio available

⚠️ Feature extraction for Dataset B is **already done by the original authors**  
⚠️ This dataset is used **as-is**

---

## 2. Core ML Principle (Non-Negotiable)

> **Machine Learning models NEVER consume WAV files.**  
> **They ONLY consume numeric feature tables (`X`, `y`).**

Implications:

- Dataset A **must** go through feature extraction
- Dataset B **already satisfies this requirement**

This explains why most Kaggle notebooks operate **only on features**.

---

## 3. Pipeline Separation Rule (CRITICAL)

There are **two pipelines** in this thesis.

They must remain conceptually separate.

### Pipeline A — Raw Audio

```

WAV → Feature Extraction → Feature Table → ML → Metrics

```

### Pipeline B — Pre-extracted Features

```

CSV → ML → Metrics

```

❌ Never train models directly on WAV files  
❌ Never compare pipelines with different ML setups  

---

## 4. Absolute DO NOTs (Hard Constraints)

The agent must **never**:

❌ Train models directly on raw audio  
❌ Treat WAV files as independent subjects  
❌ Perform file-level train/test splits for Dataset A  
❌ Split recordings from the same subject across folds  
❌ Mix speech tasks silently  
❌ Assume Dataset A and Dataset B share subjects  
❌ Merge Dataset A and Dataset B at subject level  
❌ Use deep learning (CNNs, RNNs, Transformers)  
❌ Use spectrogram images as model input  
❌ Chase Kaggle-style leaderboard accuracy  
❌ Make medical, diagnostic, or clinical claims  

Violation of any item **invalidates the experiment**.

---

## 5. Mandatory Subject-Level Handling (Dataset A)

For **MDVR-KCL**:

- Each subject (`IDxx`) has **multiple recordings**
- Some subjects have recordings for:
  - both speech tasks
  - only one task (documented asymmetry)

### Mandatory Rule

> **All data splits MUST be performed at the SUBJECT level.**

This means:

- all recordings of a subject go to **either** train **or** test
- never both

This is required to prevent **data leakage**.

---

## 6. Speech Task Handling Rules

Dataset A contains **two distinct speech tasks**:

- `ReadText`
- `SpontaneousDialogue`

The agent must explicitly choose and document **one** of the following:

### Allowed approaches

- Use **only ReadText**
- Use **only SpontaneousDialogue**
- Treat tasks as **separate experiments**
- Encode task type as an explicit feature

❌ Mixing tasks without documentation is forbidden.

---

## 7. Feature Extraction Rules (Dataset A)

Feature extraction for Dataset A must be:

- deterministic
- reproducible
- documented
- applied uniformly to all WAV files

Rules:

- Each WAV file → exactly **one feature vector**
- Output format must be **tabular numeric data**
- Feature parameters must be fixed and recorded

After extraction, Dataset A becomes:

```

features_A.csv → X, y

```

From that point onward, Dataset A is treated **identically** to Dataset B.

---

## 8. ML Model Constraints

Only **classical, interpretable ML models** are allowed.

### Approved models

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest

Rules:

- The **same models** must be used for:
  - Dataset A
  - Dataset B
- No additional models without explicit approval

---

## 9. Evaluation Protocol Rules

Evaluation must be:

- reproducible
- fair
- identical across datasets (where applicable)

### Required metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

### Cross-validation

- Dataset A: **Grouped Stratified K-Fold (by subject)**
- Dataset B: **Stratified K-Fold**

Random seeds must be fixed and documented.

---

## 10. Comparison Rules (Very Important)

Comparisons are valid **only if** all of the following match:

- model type
- feature representation
- split strategy
- evaluation protocol
- metrics

The agent must never compare:

❌ subject-level vs file-level results  
❌ different feature extraction pipelines  
❌ undocumented task mixtures  

---

## 11. Documentation Obligations

Every experiment must document:

- dataset used
- speech task(s)
- number of subjects
- number of recordings
- split strategy
- feature set
- model(s)
- metrics

Undocumented experiments are **invalid**.

---

## 12. Scope Protection

The thesis scope is strictly limited to:

- Binary classification (PD vs HC)
- Voice-based features
- Classical machine learning

Explicitly excluded:

❌ Disease severity prediction  
❌ Regression on UPDRS / H&Y  
❌ Clinical inference  
❌ Deployment or real-time systems  

---

## 13. Guiding Principle (Non-Negotiable)

> **Methodological validity and reproducibility  
> matter more than accuracy or complexity.**

If a design choice increases performance but risks:

- leakage
- bias
- ambiguity
- irreproducibility

➡️ **The choice must be rejected.**

---

## 14. When in Doubt

If uncertain, the agent must:

1. Stop
2. Ask for clarification
3. Document assumptions

Silent assumptions are not allowed.

---

## 15. Results Interpretation Rules

### 15.1 ROC-AUC Below Chance

If any model produces ROC-AUC < 0.5, document as:

- Model instability (not pipeline failure)
- Note sensitivity to hyperparameters on small samples
- Do NOT exclude from results

Example statement:

> "The SVM with RBF kernel yielded ROC-AUC values below chance level, indicating unstable decision boundaries under small-sample, high-dimensional conditions."

---

### 15.2 Confidence Interval Overlap

When comparing conditions (e.g., speech tasks):

- If standard deviations overlap substantially, use "suggests" or "trend toward"
- Do NOT claim one condition is definitively superior
- Statistical tests required for causal claims

Example:

- ❌ "Spontaneous speech is more informative than read speech"
- ✅ "Results suggest a trend toward higher discriminability in spontaneous speech, though confidence intervals overlap"

---

### 15.3 Dataset B Subject Independence

Dataset B has no subject identifiers. Always include this caveat:

> "Since Dataset B does not provide subject identifiers, stratified cross-validation was performed at the sample level. If multiple samples originate from the same subject, this may introduce optimistic bias due to implicit subject overlap across folds."

---

### 15.4 Cross-Dataset Comparisons

Never attribute performance differences to a single factor. Always acknowledge:

- Sample size differences (756 vs 37)
- Feature dimensionality differences (752 vs 47)
- CV strategy differences (grouped vs ungrouped)

Example:

- ❌ "Pre-extracted features outperform raw-audio features"
- ✅ "Higher performance on Dataset B likely reflects the combined effect of larger sample size, richer feature representation, and potentially less stringent cross-validation constraints"

---

## 16. Forbidden Language Patterns

The following phrases are **forbidden** in results interpretation:

❌ "X outperforms Y" (without confound acknowledgment)  
❌ "This proves..." (no clinical claims)  
❌ "Clearly superior..." (requires statistical test)  
❌ "Dataset A features are worse" (conflates multiple variables)  
❌ "This system can diagnose..." (clinical claim)  

The following phrases are **allowed**:

✅ "Higher performance was observed on..."  
✅ "Results suggest..."  
✅ "Under identical classifiers..."  
✅ "This trend should be interpreted cautiously given..."  
✅ "Indicative but not conclusive..."  

---

## 17. When in Doubt

If uncertain, the agent must:

1. Stop
2. Ask for clarification
3. Document assumptions

Silent assumptions are not allowed.

---

## End of Rules

> Adherence to these strict rules is mandatory for all coding agents contributing to this thesis project. Violation of any rule invalidates the associated experiments and results.
