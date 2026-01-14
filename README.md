# Parkinson's Disease Classification from Voice Data

## Overview

This repository contains the implementation and documentation for a Master's thesis investigating machine learning approaches to Parkinson's Disease (PD) classification using voice data.

## Research Objective

> To evaluate and compare machine-learning performance for Parkinson's Disease classification using (a) raw voice recordings and (b) pre-extracted acoustic speech features.

The thesis explores whether classification performance differs when models are trained on:

1. Features extracted from raw audio recordings
2. Pre-computed acoustic speech features from existing datasets
3. Combined or compared datasets under controlled experimental conditions

## Datasets

This research utilises two publicly available datasets from Kaggle:

### Dataset A — Raw Audio Recordings

**URL:** <https://www.kaggle.com/datasets/asthamishra96/parkinson-multi-model-dataset-2-0>

- Contains raw `.wav` voice recordings
- Includes samples from Parkinson's Disease patients and Healthy Controls
- Requires acoustic feature extraction before classification

### Dataset B — Pre-Extracted Acoustic Features

**URL:** <https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features>

- Contains tabular acoustic speech features
- Labels are provided for binary classification
- Directly usable for machine learning without additional preprocessing

## Demo Application

A Flask-based web demonstration is included for thesis defense purposes.

### Quick Start

```bash
make extract-readtext    # Extract features from Dataset A ReadText task
make demo-install        # Install Flask dependency
make train-demo-model    # Train RandomForest model for inference
make demo                # Run demo app at http://127.0.0.1:5000
```

### Architecture Overview

The demo application follows a clean layered architecture:

```text
User Upload → Flask Validation → Adapter Enrichment → Core Inference → Feature Extraction → Model Prediction → Result Display
```

**Key Design Principles:**

- **Single Import Rule**: Flask app imports only the adapter module (not core inference directly)
- **Config-Driven**: Model selection, feature sets, and tasks configured in `src/parkinsons_voice_classification/config.py`
- **Zero Knowledge**: Web app has no knowledge of feature counts, extraction algorithms, or model internals
- **Metadata Validation**: Runtime checks prevent mismatches between trained model and configured features

**Components:**

- `demo_app/app.py` — Flask routes and file upload handling
- `demo_app/inference_adapter.py` — Enrichment layer between Flask and core inference
- `demo_app/feature_metadata.py` — Display formatting for 8 curated features (from 47 baseline)
- `src/parkinsons_voice_classification/inference.py` — Core prediction engine

### Important Disclaimers

⚠️ **Research Demonstration Only** — This web app is for thesis defense and academic presentation purposes.

⚠️ **Not for Clinical Use** — No diagnostic validity is claimed. Results should not be used for medical decision-making.

⚠️ **No Production Deployment** — This is an experimental interface for research evaluation only.

**Documentation:**

- [docs/WEB_APP_ARCHITECTURE.md](docs/WEB_APP_ARCHITECTURE.md) — Comprehensive architecture documentation
- [docs/DATASET_MDVR_KCL.md](docs/DATASET_MDVR_KCL.md) — **Dataset A** data card
- [docs/DATASET_PD_SPEECH_FEATURES.md](docs/DATASET_PD_SPEECH_FEATURES.md) — **Dataset B** data card

## Repository Structure

```text
parkinsons-voice-classification/
├── assets/                           # Datasets
│   ├── DATASET_MDVR_KCL/            # Raw voice recordings (Dataset A)
│   └── PD_SPEECH_FEATURES.csv       # Pre-extracted features (Dataset B)
├── demo_app/                         # Flask demonstration application
│   ├── app.py                       # Flask routes and upload handling
│   ├── inference_adapter.py         # Enrichment layer for display
│   ├── feature_metadata.py          # Display formatting for features
│   └── templates/                   # HTML templates (index, result, about)
├── docs/                             # Documentation
│   ├── v2/                          # Thesis chapters
│   │   ├── CHAPTER_1_INTRODUCTION.md
│   │   ├── CHAPTER_3_DATA_DESCRIPTION.md
│   │   ├── CHAPTER_4_METHODOLOGY.md
│   │   ├── CHAPTER_5_EXPERIMENTAL_DESIGN.md
│   │   ├── CHAPTER_6_RESULTS.md
│   │   ├── CHAPTER_7_DISCUSSION.md
│   │   ├── CHAPTER_8_LIMITATIONS.md
│   │   └── CHAPTER_9_CONCLUSION.md
│   ├── DATASET_MDVR_KCL.md          # Dataset A data card
│   ├── DATASET_PD_SPEECH_FEATURES.md # Dataset B data card
│   └── WEB_APP_ARCHITECTURE.md      # Demo app architecture
├── outputs/                          # Generated outputs
│   ├── features/                    # Extracted features from Dataset A
│   ├── models/                      # Trained model artifacts (.joblib + metadata)
│   ├── results/                     # Experiment results (CSV)
│   └── plots/                       # Visualizations
├── src/parkinsons_voice_classification/  # Main package
│   ├── cli/                         # Command-line interfaces (pvc-*)
│   ├── data/                        # Dataset loaders
│   ├── features/                    # Feature extraction modules
│   ├── models/                      # Classifier wrappers and evaluation
│   ├── visualization/               # Plotting utilities
│   ├── config.py                    # Central configuration
│   └── inference.py                 # Core prediction API
├── AGENTS.md                         # AI agent rules and constraints
├── Makefile                          # Automation targets
└── pyproject.toml                    # Poetry dependencies
```

**Key Documentation:**

- [docs/v2/CHAPTER_3_DATA_DESCRIPTION.md](docs/v2/CHAPTER_3_DATA_DESCRIPTION.md) — Dataset descriptions and characteristics
- [docs/v2/CHAPTER_4_METHODOLOGY.md](docs/v2/CHAPTER_4_METHODOLOGY.md) — Experimental design and approach
- [docs/v2/CHAPTER_5_EXPERIMENTAL_DESIGN.md](docs/v2/CHAPTER_5_EXPERIMENTAL_DESIGN.md) — Experiment protocols
- [docs/v2/CHAPTER_8_LIMITATIONS.md](docs/v2/CHAPTER_8_LIMITATIONS.md) — Scope boundaries and constraints
- [docs/DATASET_MDVR_KCL.md](docs/DATASET_MDVR_KCL.md) — Dataset A data card
- [docs/DATASET_PD_SPEECH_FEATURES.md](docs/DATASET_PD_SPEECH_FEATURES.md) — Dataset B data card
- [AGENTS.md](AGENTS.md) — AI coding agent rules and pipeline constraints

## Requirements

- Python 3.10+
- Poetry for dependency management

## License

This project is licensed under the MIT License. See LICENSE for details.

## Author

Master's Thesis Project — 2026
