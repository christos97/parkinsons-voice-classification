---
project: "Parkinson’s Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson’s Disease vs Healthy Controls)"

datasets:
  dataset_a:
    name: "MDVR-KCL (Mobile Device Voice Recordings – King’s College London)"
    type: "Raw audio (WAV)"
    source: "Kaggle"
    data_card_url: "https://www.kaggle.com/datasets/asthamishra96/parkinson-multi-model-dataset-2-0/data"
    local_path: "assets/DATASET_MDVR_KCL/"
    description: >
      Raw voice recordings from Parkinson’s Disease patients and Healthy Controls,
      recorded via smartphone in clinical conditions. Multiple recordings per subject
      across two speech tasks (ReadText, SpontaneousDialogue).

  dataset_b:
    name: "Parkinson’s Disease Speech Signal Features"
    type: "Pre-extracted acoustic features (CSV)"
    source: "Kaggle"
    data_card_url: "https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features/data"
    example_notebook_url: "https://www.kaggle.com/code/parhamzm/parkinson-s-disease-pd-classification/notebook"
    local_path: "assets/PD_SPEECH_FEATURES.csv"
    description: >
      Tabular dataset containing 752 pre-extracted acoustic speech features
      for Parkinson’s Disease classification. One row per subject/sample,
      used directly for classical ML.

reference_notebooks:
  - name: "Parkinson’s Disease (PD) Classification"
    url: "https://www.kaggle.com/code/parhamzm/parkinson-s-disease-pd-classification/notebook"
    role: "Reference for tabular ML pipeline (features → models → metrics)"
    applies_to: "Dataset B and post-extraction Dataset A"

data_availability:
  status: "Downloaded"
  note: "Both CSV and WAV datasets are already downloaded locally and must not be re-fetched."

methodology_constraints:
  ml_type: "Classical ML only (Logistic Regression, SVM, Random Forest)"
  deep_learning_allowed: false
  deployment: false
  clinical_use: false

last_updated: "2026-01-12"
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

## End of Rules

> Adherence to these strict rules is mandatory for all coding agents contributing to this thesis project. Violation of any rule invalidates the associated experiments and results.
