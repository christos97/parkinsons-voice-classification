---
project: "Parkinson's Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson's Disease vs Healthy Controls)"
language: "English"
last_updated: "2026-01-15"

thesis:
  source_of_truth: "thesis/"
  build_command: "make thesis"
  watch_command: "make thesis-watch"
  clean_command: "make thesis-clean"
  chapters: "thesis/chapters/*.tex"
  appendices: "thesis/appendices/*.tex"
  bibliography: "thesis/references/references.bib"
  deprecated_markdown: "_legacy_/v2/"
  citation_rule: "All external references must be cited via BibTeX. Internal artifacts are never cited."

repository_state:
  datasets_downloaded: true
  codebase_status: "Complete (experiments run, thesis chapters drafted)"

datasets:
  dataset_a:
    name: "MDVR-KCL"
    type: "Raw audio (WAV)"
    source: "Zenodo"
    doi: "10.5281/zenodo.2867215"
    url: "https://zenodo.org/records/2867215"
    local_path: "assets/DATASET_MDVR_KCL/"
    tasks: ["ReadText", "SpontaneousDialogue"]
    subjects:
      ReadText: { total: 37, HC: 21, PD: 16 }
      SpontaneousDialogue: { total: 36, HC: 21, PD: 15 }
    unit_of_analysis: "Recording grouped by subject"

  dataset_b:
    name: "PD Speech Features"
    type: "Pre-extracted features (CSV)"
    source: "Kaggle/UCI"
    url: "https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features"
    local_path: "assets/PD_SPEECH_FEATURES.csv"
    unit_of_analysis: "Sample row (subject IDs unavailable)"

cli:
  extract: { command: "pvc-extract", options: ["--task ReadText|SpontaneousDialogue|all", "--jobs N"] }
  experiment: { command: "pvc-experiment", options: [] }
  train: { command: "pvc-train", options: ["--task", "--model", "--feature-set"] }
  importance: { command: "pvc-importance", options: ["--permutation"] }

make_targets:
  extract_all: "make extract-all"
  experiments: "make experiments"
  results: "make results"
  pipeline: "make pipeline"
  clean: "make clean"
  demo_install: "make demo-install"
  train_demo: "make train-demo-model"
  demo: "make demo"
  thesis: "make thesis"
  thesis_clean: "make thesis-clean"
  thesis_watch: "make thesis-watch"

config:
  location: "src/parkinsons_voice_classification/config.py"
  key_options:
    RANDOM_SEED: 42
    USE_EXTENDED_FEATURES: false
    USE_CLASS_WEIGHT_BALANCED: false
    INFERENCE_FEATURE_SET: "baseline"
    INFERENCE_MODEL_NAME: "RandomForest"
    INFERENCE_TASK: "ReadText"

features:
  baseline: { count: 47, prosodic: 21, spectral: 26 }
  extended: { count: 78, description: "Baseline + MFCC std + delta-delta + spectral shape" }

demo_app:
  purpose: "Research demonstration for thesis defense"
  location: "demo_app/"
  architecture: "Flask → inference_adapter.py → inference.py → sklearn Pipeline"
  files:
    - { file: "app.py", purpose: "Flask routes and upload handling" }
    - { file: "inference_adapter.py", purpose: "Adapter wrapping core inference + display enrichment" }
    - { file: "audio_utils.py", purpose: "Audio normalization (any format → mono 22050 Hz WAV)" }
    - { file: "feature_metadata.py", purpose: "Display formatting for 8 curated features" }
  invariants:
    - "Flask imports ONLY adapter module"
    - "Feature count from config.py, not hardcoded"
    - "Model switching requires zero Flask changes"
    - "Temp file cleanup in finally block"
---

# Strict Rules for AI Coding Agents

## Parkinson's Disease Voice Classification Thesis

> **Agent Visibility Note:** Critical rules from nested `AGENTS.md` files are inlined below with cross-references. Full context available in [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md), [demo_app/AGENTS.md](demo_app/AGENTS.md), and [thesis/AGENTS.md](thesis/AGENTS.md).

**Always** use `poetry` for executing python scripts, never `python` directly. This ensures correct environment and dependency management.

If requested to write/update the thesis, tex files etc., refer to [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md) for detailed guidelines.

## 0. Scope & Navigation

This repository supports an **MSc thesis** on **binary classification of PD vs HC using voice data**.

❌ No production deployment  
❌ No clinical or diagnostic system  
✅ Research demonstration (Flask demo) for thesis defense only

### Nested Agent Rules (Task-Specific)

This root file contains **project-wide scientific and methodological constraints**. For implementation-level guidance, refer to:

| Context | File | When to Use |
|---------|------|-------------|
| **Python Package Development** | [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md) | Working with core ML pipeline, feature extraction, model training, inference API, CLI commands |
| **Flask Web Application** | [demo_app/AGENTS.md](demo_app/AGENTS.md) | Working with HTML templates, Jinja2, Tailwind CSS, vanilla JS, audio upload/recording, result display |
| **LaTeX Thesis Writing** | [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md) | Writing/editing thesis chapters, managing bibliography, compiling PDF, formatting figures/tables |

### Quick Reference Links

**Configuration & Documentation:**

- [src/parkinsons_voice_classification/config.py](src/parkinsons_voice_classification/config.py) — All reproducible parameters (seeds, paths, feature counts)
- [Makefile](Makefile) — Workflow automation (extraction, experiments, demo, thesis build)
- [pyproject.toml](pyproject.toml) — Dependencies, CLI entry points, project metadata
- [README.md](README.md) — Project overview and getting started

**Datasets & Assets:**

- [assets/DATASET_MDVR_KCL/](assets/DATASET_MDVR_KCL/) — Dataset A: Raw audio (ReadText, SpontaneousDialogue)
- [assets/PD_SPEECH_FEATURES.csv](assets/PD_SPEECH_FEATURES.csv) — Dataset B: Pre-extracted features
- [docs/DATASET_MDVR_KCL.md](docs/DATASET_MDVR_KCL.md) — Dataset A documentation
- [docs/DATASET_PD_SPEECH_FEATURES.md](docs/DATASET_PD_SPEECH_FEATURES.md) — Dataset B documentation

**Core Implementation:**

- [src/parkinsons_voice_classification/inference.py](src/parkinsons_voice_classification/inference.py) — Public inference API
- [src/parkinsons_voice_classification/features/](src/parkinsons_voice_classification/features/) — Feature extraction modules
- [src/parkinsons_voice_classification/models/](src/parkinsons_voice_classification/models/) — Model training and evaluation
- [src/parkinsons_voice_classification/data/](src/parkinsons_voice_classification/data/) — Dataset loaders

**Outputs & Results:**

- [outputs/features/](outputs/features/) — Extracted feature CSVs (baseline/extended)
- [outputs/models/](outputs/models/) — Trained model artifacts (.joblib + metadata)
- [outputs/results/](outputs/results/) — Experiment results (metrics, importance)
- [outputs/plots/](outputs/plots/) — Generated figures for thesis

**Demo Application:**

- [demo_app/app.py](demo_app/app.py) — Flask routes and upload handling
- [demo_app/inference_adapter.py](demo_app/inference_adapter.py) — Adapter wrapping core inference
- [demo_app/templates/](demo_app/templates/) — HTML templates (index, result, about)
- [docs/WEB_APP_ARCHITECTURE.md](docs/WEB_APP_ARCHITECTURE.md) — Full demo architecture documentation

**Thesis LaTeX:**

- [thesis/main.tex](thesis/main.tex) — Thesis master file
- [thesis/chapters/](thesis/chapters/) — Individual chapter files (.tex)
- [thesis/appendices/](thesis/appendices/) — Appendix files
- [thesis/references/references.bib](thesis/references/references.bib) — BibTeX bibliography
- [thesis/figures/](thesis/figures/) — Figures for thesis (copied from outputs/plots/)

**CLI Commands:**

- [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) — Comprehensive CLI documentation

---

## 0.5. Flask Web App Critical Rules (REQUIRED)

When working in [demo_app/](demo_app/) — See full rules in [demo_app/AGENTS.md](demo_app/AGENTS.md).

### Import Boundaries (HARD RULE)

```python
# demo_app/app.py — CORRECT
from inference_adapter import run_inference_with_features, get_model_info
from audio_utils import normalize_audio_file

# demo_app/app.py — FORBIDDEN ❌
from parkinsons_voice_classification.inference import run_inference  # ❌
from parkinsons_voice_classification.features import extract_all_features  # ❌
from parkinsons_voice_classification import config  # ❌
```

**Why:** Adapter pattern ensures **model switching requires zero Flask/template changes**.

### Audio Processing Contract

```python
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file.save(original_tmp_path)
        normalized_wav = normalize_audio_file(original_tmp_path)  # Always normalize
        result = run_inference_with_features(normalized_wav)      # Then infer
        return render_template("result.html", result=result)
    finally:
        cleanup_audio_file(original_tmp_path)
        cleanup_audio_file(normalized_wav)
```

**Rules:**

- ✅ Input: ANY format (WAV, MP3, WebM, Opus, FLAC)
- ✅ Output: ALWAYS mono 22050 Hz PCM-16 WAV
- ✅ Cleanup in `finally` block (non-negotiable)
- ❌ Never skip normalization

### Frontend Constraints

- **Styling:** Tailwind CSS (via CDN) — utility classes only
- **JavaScript:** Vanilla JS (no external library)
- **Templates:** Jinja2 conditionals for model status and prediction styling
- **Disclaimer:** Required on ALL pages: "Research Demonstration Only. Not for clinical use."

---

## 0.6. LaTeX Thesis Critical Rules (REQUIRED)

When working in [thesis/](thesis/) — See full rules in [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md).

### Build System

```bash
make thesis           # Build PDF (auto figure sync + latexmk)
make thesis-watch     # Continuous rebuild on changes
make thesis-clean     # Remove all artifacts
```

### Citations (HARD RULE)

```latex
% CORRECT — Use BibTeX entries
\cite{little2009suitability}    % Author et al. [1]
\citep{author2023}               % [1] (parenthetical)
\citet{author2023}               % Author et al. [1] (textual)
```

**Requirements:**

- ⚠️ Bibliography requires **at least one `\cite{}` command** in chapters
- ✅ Allowed types: `@article`, `@book`, `@inproceedings`, `@misc`
- ❌ Forbidden: `@software` — use `@misc` with `howpublished = {Software}`
- ❌ Never cite internal artifacts (`outputs/`, `assets/`, `_legacy_/`)

### Figure Workflow

```latex
% 1. Generate plot → outputs/plots/my_figure.png
% 2. Update FIGURE_MAPPING in scripts/sync_figures.py
% 3. Run: make thesis (auto-syncs to thesis/figures/)
% 4. Use in LaTeX:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_my_figure.png}
    \caption{My figure caption}
    \label{fig:my-figure}
\end{figure}
```

**Rules:**

- ✅ Use `[H]` placement (float package loaded)
- ✅ No path prefix needed (graphics path configured)
- ✅ Label format: `\label{fig:descriptive-name}`
- ❌ Never manually copy figures (use `make sync-figures`)
- ❌ Never reference figures that don't exist in `thesis/figures/`

---

## 1. Core ML Principle (Non-Negotiable)

> **ML models consume FEATURE TABLES, not WAV files.**

- Dataset A → Feature Extraction → Feature Table → ML
- Dataset B → Already features → ML

---

## 2. Pipeline Separation (CRITICAL)

### Pipeline A — Raw Audio

```
WAV → Feature Extraction → Features CSV → ML → Metrics
```

### Pipeline B — Pre-extracted Features

```
CSV → ML → Metrics
```

❌ Never train on WAV files directly  
❌ Never mix pipelines in comparisons

---

## 3. Absolute DO NOTs

❌ Train on raw audio  
❌ Treat WAV files as independent subjects  
❌ Split recordings from same subject across folds  
❌ Mix speech tasks without documentation  
❌ Merge Dataset A and B at subject level  
❌ Use deep learning (CNNs, RNNs, Transformers)  
❌ Optimize for leaderboard performance  
❌ Make clinical/diagnostic claims

---

## 4. Subject-Level Handling (Dataset A)

> All splits MUST be at SUBJECT level.

All recordings from one subject → same fold. This prevents data leakage.

---

## 5. Speech Task Rules

Dataset A tasks: `ReadText`, `SpontaneousDialogue`

Allowed:

- Use one task only
- Treat as separate experiments
- Encode task as feature

❌ Silent mixing forbidden

---

## 6. Feature Extraction Rules

- Deterministic, reproducible, uniform
- One WAV → one feature vector
- Parameters fixed and documented

**Implementation details:** See [src/parkinsons_voice_classification/features/](src/parkinsons_voice_classification/features/) and [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md#4-feature-extraction-pipeline)

---

## 7. Model Constraints

Allowed models only:

- Logistic Regression
- SVM (RBF kernel)
- Random Forest

Same model set across all datasets.

**Implementation details:** See [src/parkinsons_voice_classification/models/classifiers.py](src/parkinsons_voice_classification/models/classifiers.py) and [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md#5-model-training-workflow)

---

## 8. Evaluation Rules

**Metrics (mandatory):** Accuracy, Precision, Recall, F1, ROC-AUC

**Cross-validation:**

- Dataset A: Grouped Stratified 5-Fold
- Dataset B: Stratified 5-Fold (subject caveat required)

Random seeds fixed.

---

## 9. Results Interpretation

| Scenario | Guidance |
|----------|----------|
| ROC-AUC < 0.5 | Document as model instability, not failure |
| Overlapping CIs | Use "suggests" / "trend toward" |
| Dataset B | Caveat: "Results may be optimistic due to unknown subject overlap" |
| Cross-dataset | Never attribute to single factor |

---

## 10. Forbidden Language

❌ "X outperforms Y"  
❌ "This proves..."  
❌ "Clearly superior"  
❌ "This diagnoses..."

✅ "Results suggest..."  
✅ "Observed under identical classifiers..."  
✅ "Should be interpreted cautiously..."

---

## 11. Variance Reporting

All metrics: **mean ± std** across folds.

Single-point estimates forbidden in tables, figures, text.

---

## 12. Citation Rules

✅ External sources via BibTeX in [thesis/references/references.bib](thesis/references/references.bib)  
✅ Use `\cite{}` commands in LaTeX

❌ Never cite internal artifacts ([outputs/](outputs/), [assets/](assets/), [_legacy_/](_legacy_/))  
❌ Never cite GitHub URLs directly

**LaTeX writing guidelines:** See [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md)

---

## 13. Code Standards

- Use **poetry** for package management (see [pyproject.toml](pyproject.toml))
- [Makefile](Makefile) targets for common workflows
- Dependencies in [pyproject.toml](pyproject.toml)
- PEP 8 + black formatting

**Package development guidelines:** See [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md)

---

## 14. Documentation Sync Rule

> Any change affecting behavior, workflow, or constraints MUST update relevant documentation and agent files, including frontmatter.

This is **non-optional**.

---

## Additional Context: Detailed Nested Rules

This root file contains **critical rules** necessary for all agents. For **implementation-level details**, refer to:

| When Working In | Read This File | Topics Covered |
|-----------------|----------------|----------------|
| Python package development, ML pipeline, CLI | [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md) | Config rules, feature extraction, model training, inference API, cross-validation strategy, adapter pattern |
| Flask web application, HTML templates, JavaScript | [demo_app/AGENTS.md](demo_app/AGENTS.md) | Import boundaries, audio processing, frontend stack (Tailwind/jQuery), template patterns, audio recorder implementation |
| LaTeX thesis writing, chapter editing, bibliography | [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md) | Build system, citations (BibTeX), figure synchronization, label conventions, troubleshooting |

---

## End of Rules
