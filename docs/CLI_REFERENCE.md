---
title: "CLI Reference"
last_updated: "2026-01-14"

commands:
  - { name: "pvc-extract", entry_point: "parkinsons_voice_classification.cli.extract_features:main" }
  - { name: "pvc-experiment", entry_point: "parkinsons_voice_classification.cli.run_experiments:main" }
  - { name: "pvc-train", entry_point: "parkinsons_voice_classification.cli.train_model:main" }
  - { name: "pvc-importance", entry_point: "parkinsons_voice_classification.cli.feature_importance:main" }
---

# CLI Reference

Command-line tools for the Parkinson's Voice Classification pipeline.

## Overview

| Command | Purpose |
|---------|---------|
| `pvc-extract` | Extract acoustic features from MDVR-KCL dataset |
| `pvc-experiment` | Run all classification experiments |
| `pvc-train` | Train and serialize model for inference |
| `pvc-importance` | Run feature importance analysis |

All commands are installed via Poetry and available after `poetry install`.

---

## pvc-extract

Extract acoustic features from raw audio files (Dataset A).

### Usage

```bash
pvc-extract [OPTIONS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--task` | `all` | Speech task: `ReadText`, `SpontaneousDialogue`, or `all` |
| `--jobs` | `4` | Number of parallel workers |

### Examples

```bash
# Extract features for both tasks
pvc-extract

# Extract ReadText features only
pvc-extract --task ReadText

# Extract SpontaneousDialogue with 8 workers
pvc-extract --task SpontaneousDialogue --jobs 8
```

### Output

Features are saved to:
- `outputs/features/baseline/features_readtext.csv`
- `outputs/features/baseline/features_spontaneousdialogue.csv`

Or if `USE_EXTENDED_FEATURES=True` in config:
- `outputs/features/extended/features_readtext.csv`
- `outputs/features/extended/features_spontaneousdialogue.csv`

### Makefile Equivalents

```bash
make extract-all          # pvc-extract --task all
make extract-readtext     # pvc-extract --task ReadText
make extract-spontaneous  # pvc-extract --task SpontaneousDialogue
```

---

## pvc-experiment

Run all classification experiments across datasets.

### Usage

```bash
pvc-experiment
```

### What It Does

1. Loads extracted features (Dataset A) and CSV (Dataset B)
2. Trains Logistic Regression, SVM (RBF), Random Forest
3. Runs Grouped Stratified 5-Fold CV (Dataset A) or Stratified 5-Fold (Dataset B)
4. Computes metrics: Accuracy, Precision, Recall, F1, ROC-AUC
5. Saves results to CSV

### Output

Results saved to:
- `outputs/results/baseline/` (or `weighted/` if class weights enabled)
- `outputs/results/all_results.csv`
- `outputs/results/summary.csv`

Plots saved to:
- `outputs/plots/heatmap_readtext.png`
- `outputs/plots/heatmap_spontaneous.png`

### Makefile Equivalent

```bash
make experiments
```

---

## pvc-train

Train a model and serialize it for inference.

### Usage

```bash
pvc-train [OPTIONS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--task` | `ReadText` | Speech task the model is trained on |
| `--model` | `RandomForest` | Model architecture: `LogisticRegression`, `SVM`, `RandomForest` |
| `--feature-set` | `baseline` | Feature set: `baseline` (47) or `extended` (78) |

### Examples

```bash
# Train default model (RandomForest, ReadText, baseline)
pvc-train

# Train SVM on SpontaneousDialogue
pvc-train --task SpontaneousDialogue --model SVM

# Train with extended features
pvc-train --feature-set extended --model RandomForest
```

### Output

Model artifact saved to:
- `outputs/models/{model}_{task}_{feature-set}.joblib`
- `outputs/models/{model}_{task}_{feature-set}_metadata.json`

### Makefile Equivalent

```bash
make train-demo-model   # pvc-train --task ReadText --model RandomForest --feature-set baseline
```

---

## pvc-importance

Run feature importance analysis.

### Usage

```bash
pvc-importance [OPTIONS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--permutation` | `false` | Use permutation importance (slower, more accurate) |

### Methods

- **Default (Gini):** Uses model's built-in feature importances (Random Forest, Logistic Regression coefficients)
- **Permutation:** Shuffles each feature and measures performance drop (works with any model)

### Examples

```bash
# Run with default Gini importance
pvc-importance

# Run with permutation importance
pvc-importance --permutation
```

### Output

CSVs saved to:
- `outputs/results/importance_readtext.csv`
- `outputs/results/importance_spontaneous.csv`
- `outputs/results/importance_pd_speech.csv`
- `outputs/results/importance_all.csv`

Plots saved to:
- `outputs/plots/importance_readtext_randomforest.png`
- `outputs/plots/importance_spontaneous_randomforest.png`
- `outputs/plots/importance_pd_speech_randomforest.png`

---

## Full Pipeline

To run the complete pipeline:

```bash
# Option 1: Individual commands
pvc-extract --task all
pvc-experiment
pvc-importance

# Option 2: Make shortcut
make pipeline   # Runs extract-all + experiments
```

---

## Configuration

CLI behavior is influenced by `src/parkinsons_voice_classification/config.py`:

| Setting | Effect |
|---------|--------|
| `USE_EXTENDED_FEATURES` | Switches between 47/78 feature sets |
| `USE_CLASS_WEIGHT_BALANCED` | Enables class weighting in classifiers |
| `RANDOM_SEED` | Ensures reproducibility (fixed at 42) |
| `N_FOLDS` | Number of CV folds (fixed at 5) |

---

## See Also

- [README.md](../README.md) — Project overview and quick start
- [AGENTS.md](../AGENTS.md) — AI agent rules and constraints
