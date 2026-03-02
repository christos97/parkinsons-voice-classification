---
project: "Parkinson's Disease Voice Classification Thesis"
degree: "MSc Thesis"
domain: "Speech Signal Processing / Classical Machine Learning"
task: "Binary classification (Parkinson's Disease vs Healthy Controls)"
datasets:
  dataset_a: { name: "MDVR-KCL", local_path: "assets/DATASET_MDVR_KCL/", subjects: { ReadText: { HC: 21, PD: 16 }, SpontaneousDialogue: { HC: 21, PD: 15 } } }
  dataset_b: { name: "PD Speech Features", local_path: "assets/PD_SPEECH_FEATURES.csv" }
thesis: { build_command: "make thesis", bibliography: "thesis/references/references.bib" }
config: { location: "src/parkinsons_voice_classification/config.py" }
---

# Strict Rules for AI Coding Agents — Parkinson's Voice Classification

**Always** use `poetry` for executing python scripts, never `python` directly.

For thesis/LaTeX work, refer to [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md).

## 0. Scope & Navigation

This repository supports an **MSc thesis** on **binary classification of PD vs HC using voice data**.

❌ No production deployment · ❌ No clinical or diagnostic system

| Context | File |
|---------|------|
| **Python Package / ML Pipeline** | [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md) |
| **LaTeX Thesis Writing** | [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md) |

**Quick Reference:**
- [config.py](src/parkinsons_voice_classification/config.py) — Reproducible parameters · [Makefile](Makefile) — Workflow automation
- [pyproject.toml](pyproject.toml) — Dependencies · [README.md](README.md) — Overview · [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) — CLI docs
- [assets/DATASET_MDVR_KCL/](assets/DATASET_MDVR_KCL/) — Dataset A · [assets/PD_SPEECH_FEATURES.csv](assets/PD_SPEECH_FEATURES.csv) — Dataset B
- [inference.py](src/parkinsons_voice_classification/inference.py) · [features/](src/parkinsons_voice_classification/features/) · [models/](src/parkinsons_voice_classification/models/)
- [outputs/results/](outputs/results/) — Results · [thesis/main.tex](thesis/main.tex) · [references.bib](thesis/references/references.bib)

---

## 0.6. LaTeX Thesis Rules

See [.github/skills/latex-thesis/SKILL.md](.github/skills/latex-thesis/SKILL.md) for full build, citation, and figure-sync guidance (`make thesis`).

**Citations:** Use `\cite{}` / `\citep{}` / `\citet{}` with BibTeX entries only. No `@software` (use `@misc`). Never cite `outputs/`, `assets/`, or GitHub URLs directly.

---

## 1. Core ML Principle (Non-Negotiable)

> **ML models consume FEATURE TABLES, not WAV files.**

- Dataset A → Feature Extraction → Feature Table → ML
- Dataset B → Already features → ML

---

## 2. Pipeline Separation (CRITICAL)

Pipeline A: `WAV → Feature Extraction → Features CSV → ML → Metrics`
Pipeline B: `CSV → ML → Metrics`

❌ Never train on WAV files directly · ❌ Never mix pipelines in comparisons

---

## 3. Absolute DO NOTs

❌ Train on raw audio · ❌ Treat WAV files as independent subjects
❌ Split recordings from same subject across folds · ❌ Mix speech tasks without documentation
❌ Merge Dataset A and B at subject level · ❌ Use deep learning (CNNs, RNNs, Transformers)
❌ Optimize for leaderboard performance · ❌ Make clinical/diagnostic claims

---

## 4. Subject-Level Handling (Dataset A)

> All splits MUST be at SUBJECT level.

All recordings from one subject → same fold. This prevents data leakage.

---

## 5. Speech Task Rules

Dataset A tasks: `ReadText`, `SpontaneousDialogue`. Use one task only; treat as separate experiments.

❌ Silent mixing of tasks forbidden.

---

## 6. Feature Extraction Rules

Deterministic, reproducible, uniform; one WAV → one feature vector; parameters fixed and documented.
See [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md#4-feature-extraction-pipeline) for full details.

---

## 7. Model Constraints

Allowed: Logistic Regression, SVM (RBF), Random Forest, Gradient Boosting (sklearn), XGBoost. Same set across all datasets.
See [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md#5-model-training-workflow) for hyperparameters.

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
| Dataset B | "Results may be optimistic due to unknown subject overlap" |
| Cross-dataset | Never attribute to single factor |

---

## 10. Reporting Standards

**Forbidden:** ❌ "X outperforms Y" · ❌ "This proves..." · ❌ "Clearly superior" · ❌ "This diagnoses..."
**Preferred:** ✅ "Results suggest..." · ✅ "Observed under identical classifiers..." · ✅ "Should be interpreted cautiously..."
**Variance:** All metrics as **mean ± std** across folds. Single-point estimates forbidden.

---

## 11. Code Standards

Use **poetry** (never `python` directly). PEP 8 + black. See [src/parkinsons_voice_classification/AGENTS.md](src/parkinsons_voice_classification/AGENTS.md) for package guidelines.

---

## 12. Documentation Sync Rule

> Any change affecting behavior, workflow, or constraints MUST update relevant documentation and agent files, including frontmatter. This is **non-optional**.