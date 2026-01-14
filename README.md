# Parkinson's Disease Voice Classification

MSc thesis investigating classical ML approaches to PD/HC classification using voice data.

**Domain:** Speech Signal Processing / Classical Machine Learning  
**Task:** Binary classification (Parkinson's Disease vs Healthy Controls)  
**Status:** Complete (experiments run, thesis drafted)

## Research Objective

> Evaluate and compare classification performance using (a) features extracted from raw audio recordings and (b) pre-extracted acoustic features.

## Datasets

| Dataset | Source | Type | Local Path |
|---------|--------|------|------------|
| **A: MDVR-KCL** | [Zenodo](https://zenodo.org/records/2867215) (DOI: 10.5281/zenodo.2867215) | Raw WAV | `assets/DATASET_MDVR_KCL/` |
| **B: PD Speech Features** | [Kaggle](https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features) | Pre-extracted CSV | `assets/PD_SPEECH_FEATURES.csv` |

## Quick Start

### Run Experiments

```bash
make extract-all    # Extract features from Dataset A
make experiments    # Run all classification experiments
make results        # Display results summary
```

### Run Demo App

```bash
make extract-readtext    # Extract features (ReadText task)
make demo-install        # Install Flask
make train-demo-model    # Train inference model
make demo                # http://127.0.0.1:5000
```

### Build Thesis

```bash
make thesis         # Build PDF via latexmk
make thesis-watch   # Continuous rebuild on changes
```

## Repository Structure

```text
parkinsons-voice-classification/
├── assets/                           # Datasets
│   ├── DATASET_MDVR_KCL/            # Raw WAV recordings (Dataset A)
│   └── PD_SPEECH_FEATURES.csv       # Pre-extracted features (Dataset B)
├── demo_app/                         # Flask demo application
│   ├── app.py                       # Routes and upload handling
│   ├── inference_adapter.py         # Adapter layer (Flask → core inference)
│   ├── audio_utils.py               # Audio normalization (any format → WAV)
│   ├── feature_metadata.py          # Display formatting for curated features
│   └── templates/                   # HTML templates
├── docs/                             # Documentation
│   ├── CLI_REFERENCE.md             # CLI commands reference
│   ├── DATASET_MDVR_KCL.md          # Dataset A data card
│   ├── DATASET_PD_SPEECH_FEATURES.md # Dataset B data card
│   └── WEB_APP_ARCHITECTURE.md      # Demo app architecture
├── outputs/                          # Generated artifacts
│   ├── features/                    # Extracted features (baseline/extended)
│   ├── models/                      # Trained model artifacts (.joblib)
│   ├── results/                     # Experiment results (CSV)
│   └── plots/                       # Visualizations
├── scripts/
│   └── sync_figures.py              # Copy plots to thesis/figures/
├── src/parkinsons_voice_classification/
│   ├── cli/                         # CLI entry points (pvc-*)
│   ├── data/                        # Dataset loaders
│   ├── features/                    # Feature extraction
│   ├── models/                      # Classifier wrappers
│   ├── visualization/               # Plotting utilities
│   ├── config.py                    # Central configuration
│   └── inference.py                 # Core prediction API
├── thesis/                           # LaTeX thesis (source of truth)
│   ├── chapters/                    # Chapters 1-9
│   ├── appendices/                  # Appendices A-B
│   ├── references/                  # BibTeX bibliography
│   └── figures/                     # Auto-synced from outputs/plots/
├── _legacy_/v2/                      # DEPRECATED markdown drafts (read-only)
├── AGENTS.md                         # AI agent rules and constraints
├── Makefile                          # Automation targets
└── pyproject.toml                    # Poetry dependencies
```

## Makefile Targets

| Category | Command | Description |
|----------|---------|-------------|
| **Setup** | `make install` | Install dependencies via Poetry |
| | `make dev-install` | Install with dev dependencies |
| **Extraction** | `make extract-all` | Extract features for all tasks |
| | `make extract-readtext` | Extract ReadText features only |
| | `make extract-spontaneous` | Extract SpontaneousDialogue only |
| **Experiments** | `make experiments` | Run all classification experiments |
| | `make results` | Display results summary |
| **Demo** | `make demo-install` | Install Flask dependency |
| | `make train-demo-model` | Train inference model |
| | `make demo` | Run Flask demo app |
| | `make demo-dev` | Run in debug mode (auto-reload) |
| **Thesis** | `make thesis` | Build PDF (latexmk) |
| | `make thesis-watch` | Continuous rebuild |
| | `make thesis-clean` | Remove LaTeX artifacts |
| **QA** | `make test` | Run test suite |
| | `make lint` | Run ruff linter |
| | `make format` | Format with black |
| **Cleanup** | `make clean` | Remove outputs |
| | `make clean-all` | Remove outputs + cache |
| **Info** | `make help` | Show all commands |
| | `make info` | Project information |
| | `make check-dataset` | Verify dataset structure |

## CLI Commands

| Command | Purpose |
|---------|---------|
| `pvc-extract` | Extract acoustic features from MDVR-KCL dataset |
| `pvc-experiment` | Run all classification experiments |
| `pvc-train` | Train and serialize model for inference |
| `pvc-importance` | Run feature importance analysis |

See [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) for full usage.

## Documentation

| Document | Purpose |
|----------|---------|
| [AGENTS.md](AGENTS.md) | AI agent rules and constraints |
| [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) | CLI commands reference |
| [docs/DATASET_MDVR_KCL.md](docs/DATASET_MDVR_KCL.md) | Dataset A data card |
| [docs/DATASET_PD_SPEECH_FEATURES.md](docs/DATASET_PD_SPEECH_FEATURES.md) | Dataset B data card |
| [docs/WEB_APP_ARCHITECTURE.md](docs/WEB_APP_ARCHITECTURE.md) | Demo app architecture |
| [thesis/README.md](thesis/README.md) | Thesis build instructions |

## Demo App Disclaimers

⚠️ **Research Demonstration Only** — For thesis defense and academic presentation.

⚠️ **Not for Clinical Use** — No diagnostic validity claimed.

⚠️ **No Production Deployment** — Experimental research interface only.

## Requirements

- Python 3.10+
- Poetry
- LaTeX distribution (for thesis build)

## License

MIT License
