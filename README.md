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

**URL:** https://www.kaggle.com/datasets/asthamishra96/parkinson-multi-model-dataset-2-0

- Contains raw `.wav` voice recordings
- Includes samples from Parkinson's Disease patients and Healthy Controls
- Requires acoustic feature extraction before classification

### Dataset B — Pre-Extracted Acoustic Features

**URL:** https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features

- Contains tabular acoustic speech features
- Labels are provided for binary classification
- Directly usable for machine learning without additional preprocessing

## Scope

This project is strictly **research-oriented** and aims to:

- Compare classification approaches across different data representations
- Evaluate classical machine learning models under controlled conditions
- Provide reproducible experimental results for academic review

### Important Disclaimers

⚠️ **This is not a diagnostic tool.** The models and results presented in this repository are intended solely for academic research purposes.

⚠️ **Results are research-only.** No clinical validity is claimed, and the outputs should not be used for medical decision-making.

⚠️ **No deployment or real-time system is provided.** This repository contains experimental code for thesis evaluation only.

## Repository Structure

Detailed documentation is provided in the following files:

- [METHODOLOGY.md](METHODOLOGY.md) — Experimental design and approach
- [DATASETS.md](DATASETS.md) — Data cards and dataset descriptions
- [EXPERIMENTS.md](EXPERIMENTS.md) — Experiment definitions and protocols
- [SCOPE_AND_LIMITATIONS.md](SCOPE_AND_LIMITATIONS.md) — Boundaries and constraints

## Requirements

- Python 3.10+
- Poetry for dependency management

## License

This project is licensed under the MIT License. See LICENSE for details.

## Author

Master's Thesis Project — 2026
