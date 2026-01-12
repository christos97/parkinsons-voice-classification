# Dataset Documentation  

## Parkinson’s Disease Speech Signal Features (PD_SPEECH_FEATURES)

---

## Dataset Overview

**Name:**  
Parkinson’s Disease Speech Signal Features

**Common Reference:**  
UCI Parkinson’s Disease Classification Dataset

**Source (as distributed):**  
Kaggle  
<https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features>

**Original Repository:**  
UCI Machine Learning Repository  
<https://archive.ics.uci.edu/ml/datasets/Parkinson%27s+Disease+Classification>

---

## Dataset Description

This dataset consists of **pre-extracted acoustic speech features** derived from voice recordings of individuals diagnosed with Parkinson’s Disease (PD) and from Healthy Control (HC) participants.

Unlike raw audio datasets, this dataset **does not include WAV recordings**.  
Instead, it provides a **tabular numeric representation** of speech characteristics, suitable for direct use in classical machine-learning algorithms.

The dataset is widely used in the literature as a **baseline benchmark** for Parkinson’s Disease voice classification.

---

## Data Collection Context

According to the original dataset description:

- Data were collected at the **Department of Neurology, Cerrahpaşa Faculty of Medicine, Istanbul University**
- Participants included:
  - **188 Parkinson’s Disease patients**
  - **64 Healthy Controls**
- Age range:
  - PD: 33–87 years
  - HC: 41–82 years
- Speech task:
  - Sustained phonation of the vowel **/a/**
  - Each subject performed three repetitions
- Recording settings:
  - Sampling rate: 44.1 kHz
  - Clinical examination conditions

---

## Feature Extraction (Pre-Computed)

Feature extraction was performed **prior to dataset publication** by the original authors.

The dataset includes features derived from multiple speech signal processing techniques, including:

- Time–frequency features
- Mel-Frequency Cepstral Coefficients (MFCCs)
- Wavelet transform–based features
- Vocal fold–related features
- Tunable Q-factor Wavelet Transform (TQWT) features

⚠️ **Important:**  
The exact feature extraction pipeline is **not re-implemented** in this thesis.  
The dataset is treated as a **fixed, externally produced feature representation**.

---

## Data Format

**File location in this repository:**

`assets/PD_SPEECH_FEATURES.csv`

**Format:**

- Tabular CSV
- Rows correspond to **subjects**
- Columns correspond to **numeric acoustic features**
- One column corresponds to the **binary class label**

---

## Labels Used in This Thesis

The dataset provides labels for binary classification:

- **PD** — Parkinson’s Disease
- **HC** — Healthy Control

Within this thesis:

- Labels are encoded as a binary target variable
- No severity prediction or regression is performed

---

## Intended Use in This Thesis

Within this thesis, the PD_SPEECH_FEATURES dataset is used as:

- A **benchmark dataset** with pre-extracted features
- A comparison point for experiments using raw audio feature extraction (MDVR-KCL)
- Input for classical machine-learning classifiers, including:
  - Logistic Regression
  - Support Vector Machines (SVM)
  - Random Forest

The dataset supports **Experiment 2 (Pre-Extracted Feature Pipeline)**.

---

## Methodological Constraints

When using this dataset, the following constraints apply:

- No feature re-engineering is performed
- No access to raw audio is assumed
- One sample corresponds to one subject
- Standard train/test or cross-validation splits are applied at the **row (subject) level**

This contrasts with raw audio datasets, where subject-level grouping must be inferred.

---

## Known Limitations

- Raw speech recordings are not available
- Feature extraction methodology cannot be modified or verified
- The sustained vowel task does not reflect natural or spontaneous speech
- Dataset distribution is imbalanced between PD and HC participants
- Demographic and linguistic diversity may be limited

These limitations are considered when interpreting results.

---

## Ethical Considerations

- Dataset is publicly available for research use
- No personally identifiable information is included
- No attempt is made to re-identify participants
- Results derived from this dataset are **non-diagnostic** and **research-only**

---

## Relevance to Research Question

This dataset enables investigation of:

- Classification performance using established acoustic feature sets
- Baseline performance of classical ML models
- Comparison against features extracted directly from raw speech recordings

It provides a controlled reference point for evaluating the impact of feature provenance on PD classification performance.

---

## Citation

If this dataset is used, the following publication should be cited as requested by the original authors:

Sakar, C.O., Serbes, G., Gunduz, A., Tunc, H.C., Nizam, H., Sakar, B.E., Tutuncu, M., Aydin, T., Isenkul, M.E., Apaydin, H.  
*A comparative analysis of speech signal processing algorithms for Parkinson’s disease classification and the use of the tunable Q-factor wavelet transform.*  
Applied Soft Computing, 2019.  
DOI: <https://doi.org/10.1016/j.asoc.2018.10.022>
