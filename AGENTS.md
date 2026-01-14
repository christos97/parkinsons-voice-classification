---
project: "Parkinson’s Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson’s Disease vs Healthy Controls)"
language: "English"
last_updated: "2026-01-14"
thesis:
  source_of_truth: "thesis/"
  build_command: "make thesis"
  chapters: "thesis/chapters/*.tex"
  appendices: "thesis/appendices/*.tex"
  bibliography: "thesis/references/references.bib"
  deprecated_markdown: "docs/v2/ (read-only archive, see docs/v2/DEPRECATED.md)"
  citation_rule: >
    All external references must be cited via BibTeX entries in references.bib.
    Internal artifacts (outputs/, assets/, docs/v2/) are never cited as external sources.
repository_state:
  datasets_downloaded: true
  codebase_status: "Complete (experiments run, thesis chapters 3–8 drafted)"
  primary_entrypoints:
    extract_features_cli: "pvc-extract"
    run_experiments_cli: "pvc-experiment"
    train_model_cli: "pvc-train"
  cli_usage:
    extract: "pvc-extract --task [ReadText|SpontaneousDialogue|all] [--jobs N]"
    experiment: "pvc-experiment"
    train: "pvc-train --task ReadText --model RandomForest --feature-set baseline"
  make_targets:
    extract_all: "make extract-all"
    experiments: "make experiments"
    results: "make results"
    pipeline: "make pipeline  # extract-all + experiments"
    clean: "make clean  # remove all outputs"
    demo_install: "make demo-install  # install Flask"
    train_demo: "make train-demo-model  # train inference model"
    demo: "make demo  # run Flask demo app"

demo_app:
  purpose: "Research demonstration for thesis defense"
  location: "demo_app/"
  inference_api: "src/parkinsons_voice_classification/inference.py"
  adapter_layer: "demo_app/inference_adapter.py"
  model_config:
    default_model: "RandomForest"
    default_task: "ReadText"
    default_features: "baseline (47 features)"
  display_features:
    curated_count: 8
    source_total: 47  # baseline feature set
    selected: ["f0_mean", "f0_max", "hnr_mean", "jitter_local", "shimmer_apq11", "intensity_mean", "mfcc_0_mean", "mfcc_5_mean"]
    metadata_source: "demo_app/feature_metadata.py"
  architecture_principle: >
    Flask app imports ONLY the adapter module (demo_app/inference_adapter.py).
    Adapter imports ONLY the core inference API and feature extraction.
    Flask has zero knowledge of feature counts, extraction algorithms, or model internals.
    This ensures pipeline changes require zero web app modifications.
  flow:
    - "User uploads WAV file via browser (demo_app/templates/index.html)"
    - "Flask validates extension and saves to temporary location (app.py:analyze route)"
    - "Adapter extracts features via extraction_simple.py (inference_adapter.py:run_inference_with_features)"
    - "Core inference loads cached model and validates feature count (inference.py:run_inference)"
    - "sklearn Pipeline scales features and predicts class + probabilities"
    - "Adapter enriches result with display metadata (8 curated features, importance data)"
    - "Flask renders result with prediction card, probability bar, feature table (templates/result.html)"
    - "Temporary file cleanup in finally block"
  architectural_invariants:
    - "Flask app must import ONLY adapter module (not core inference directly)"
    - "Feature count determined by config.py, not hardcoded in templates"
    - "Model switching requires zero changes to Flask routes or templates"
    - "Feature extraction called exactly once per request (no duplication)"
    - "Temp file cleanup must happen in finally block (no leaks)"
    - "Model loading must be cached (not re-loaded per request)"
    - "Feature validation must happen before prediction (fail fast on mismatch)"
    - "Research disclaimers must appear on every page (index, result, about)"
  documentation: "docs/WEB_APP_ARCHITECTURE.md"
  quick_start:
    - "make extract-readtext  # Extract features from Dataset A"
    - "make demo-install      # Install Flask via poetry"
    - "make train-demo-model  # Train RandomForest for inference"
    - "make demo              # Run at http://127.0.0.1:5000"

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
  date: "2026-01-13"
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

❌ No production deployment  
❌ No clinical or diagnostic system  

✅ Research demonstration (Flask demo app) exists for thesis defense purposes only.
   See `docs/WEB_APP_ARCHITECTURE.md` for architecture details.

---

## 0.1 Thesis Content Source of Truth

> **The LaTeX thesis under `thesis/` is the single authoritative source for all thesis content.**

### Authoritative Sources

| Content Type | Location | Command |
|--------------|----------|---------|
| Thesis chapters | `thesis/chapters/*.tex` | `make thesis` |
| Appendices | `thesis/appendices/*.tex` | `make thesis` |
| Bibliography | `thesis/references/references.bib` | — |

### Deprecated Sources

| Location | Status |
|----------|--------|
| `docs/v2/*.md` | **DEPRECATED** — Read-only archive (see `docs/v2/DEPRECATED.md`) |

### Citation Rules

✅ External papers, datasets, and software **must** be cited via BibTeX in `references.bib`  
✅ Use `\cite{}` commands in LaTeX for all external references  
❌ Never cite internal artifacts (`outputs/`, `assets/`, `docs/v2/`) as external sources  
❌ Never cite GitHub URLs, local file paths, or markdown files as bibliography entries  

### Thesis Editing Rules

✅ Edit **only** LaTeX files under `thesis/` for thesis content changes  
✅ Add new references to `thesis/references/references.bib`  
❌ Do **not** edit deprecated markdown files in `docs/v2/`  
❌ Do **not** duplicate content between markdown and LaTeX  

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

### 14. Forbidden Language

❌ “X outperforms Y”  
❌ “This proves…”  
❌ “Clearly superior”  
❌ “This system diagnoses…”  

Allowed:
✅ “Results suggest…”  
✅ “Observed under identical classifiers…”  
✅ “Should be interpreted cautiously…”

### 15. Mandatory Variance Reporting

All reported performance metrics must be presented as mean ± standard deviation across cross-validation folds.

Single-point estimates are forbidden, including in:

- tables
- figures
- text
- summaries

This rule exists to prevent overinterpretation under small-sample conditions.

---

## 11. Guiding Principle

> **Methodological validity and reproducibility  
> outweigh performance or complexity.**

If a choice risks leakage, bias, or ambiguity — **reject it**.

---

- Use poetry for package management and running scripts directly (not python or python3 commands).
- If needed, create script with poetry in the `Makefile` to re-use common commands.
- Ensure all dependencies are declared in `pyproject.toml`.  
- Follow PEP 8 and use black for formatting.

---

If significant changes made, always update this file `AGENTS.md`, to reflect current rules, constraints, principles and the pipeline/workflow.

## End of Rules
