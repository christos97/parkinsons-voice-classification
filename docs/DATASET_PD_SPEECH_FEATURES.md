---
title: "PD Speech Features Dataset Data Card"
dataset_name: "Parkinson's Disease Speech Signal Features"
alias: "Dataset B"
last_updated: "2026-01-14"

source:
  primary: "UCI Machine Learning Repository"
  distribution: "Kaggle"
  url: "https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features"
  uci_url: "https://archive.ics.uci.edu/ml/datasets/Parkinson%27s+Disease+Classification"

local_path: "assets/PD_SPEECH_FEATURES.csv"

collection:
  institution: "Department of Neurology, Cerrahpaşa Faculty of Medicine, Istanbul University"
  subjects: { PD: 188, HC: 64 }
  age_range: { PD: "33-87", HC: "41-82" }
  task: "Sustained phonation of vowel /a/ (3 repetitions)"
  sample_rate: 44100

data_type: "Pre-extracted features (tabular CSV)"

features:
  types: ["Time-frequency", "MFCC", "Wavelet", "Vocal fold", "TQWT"]
  note: "Extraction pipeline not available for re-implementation"

labels:
  PD: 1
  HC: 0

limitations:
  - "No raw audio available"
  - "Subject IDs not provided (potential within-subject correlation)"
  - "Feature extraction cannot be verified or modified"
  - "Sustained vowel only (no natural speech)"
---

# PD Speech Features Dataset Documentation

## Overview

| Property | Value |
|----------|-------|
| **Name** | Parkinson's Disease Speech Signal Features |
| **Source** | [Kaggle](https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features) / UCI |
| **Local Path** | `assets/PD_SPEECH_FEATURES.csv` |
| **Type** | Pre-extracted features (CSV) |

## Collection Context

| Property | Value |
|----------|-------|
| **Institution** | Istanbul University, Cerrahpaşa Faculty of Medicine |
| **PD Subjects** | 188 |
| **HC Subjects** | 64 |
| **Age Range (PD)** | 33–87 years |
| **Age Range (HC)** | 41–82 years |
| **Task** | Sustained phonation of vowel /a/ |
| **Repetitions** | 3 per subject |

## Data Format

- **Format:** CSV
- **Rows:** Samples (multiple per subject)
- **Columns:** Numeric acoustic features + binary label
- **Label Column:** Binary (1 = PD, 0 = HC)

## Pre-Computed Features

Features were extracted by original authors and include:

- Time–frequency features
- Mel-Frequency Cepstral Coefficients (MFCCs)
- Wavelet transform–based features
- Vocal fold–related features
- Tunable Q-factor Wavelet Transform (TQWT) features

⚠️ **Important:** The exact feature extraction pipeline is not available for re-implementation. This dataset is treated as a fixed, externally produced representation.

## Usage in This Thesis

- **Pipeline:** CSV → Classification (no feature extraction)
- **Cross-validation:** Stratified 5-Fold (standard, no grouping)
- **Unit of analysis:** Row (sample)

## Known Limitations

1. **No raw audio** — Cannot verify or modify feature extraction
2. **No subject IDs** — Cannot group samples by subject in CV
3. **Sustained vowel only** — Does not represent natural speech
4. **Class imbalance** — 188 PD vs 64 HC
5. **Potential data leakage** — Multiple samples per subject without IDs

## Methodological Caveats

> **Results on this dataset may be optimistic** due to unknown within-subject sample correlation.

Standard stratified CV may place samples from the same subject in both train and test folds, leading to inflated performance metrics.

## Citation

```bibtex
@misc{pd_speech_features,
  title = {Parkinson's Disease Speech Signal Features},
  author = {Sakar, C. Okan and Serbes, Gorkem and others},
  year = {2019},
  howpublished = {UCI Machine Learning Repository / Kaggle},
  url = {https://archive.ics.uci.edu/ml/datasets/Parkinson%27s+Disease+Classification}
}
```
