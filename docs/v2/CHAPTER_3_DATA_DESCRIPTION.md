# Chapter 3: Data Description

## 3.1 Overview

This thesis utilizes two distinct datasets for Parkinson's Disease voice classification:

| Property | Dataset A (MDVR-KCL) | Dataset B (PD_SPEECH) |
|----------|---------------------|----------------------|
| Data Type | Raw audio (WAV) | Pre-extracted features (CSV) |
| Source | Zenodo | Kaggle |
| Unit of Analysis | Subject (multiple recordings) | Sample (row) |
| Subject IDs Available | Yes | No |
| Total Samples | 73 recordings (37 subjects) | 756 samples |

## 3.2 Dataset A: MDVR-KCL

### 3.2.1 Source and Collection

The Mobile Device Voice Recordings from King's College London (MDVR-KCL) dataset was collected for PD research using smartphone recordings. Available on Zenodo with DOI: `10.5281/zenodo.2867215`.

**Location:** `assets/DATASET_MDVR_KCL/`

### 3.2.2 Speech Tasks

The dataset includes two distinct speech tasks:

| Task | Description | Subjects | HC | PD |
|------|-------------|----------|----|----|
| ReadText | Reading a standardized passage | 37 | 21 | 16 |
| SpontaneousDialogue | Free conversation | 36 | 21 | 15 |

**Note:** Subject ID18 is missing from SpontaneousDialogue task.

### 3.2.3 Class Distribution

```
ReadText Task:
├── HC (Healthy Control): 21 subjects (56.8%)
└── PD (Parkinson's Disease): 16 subjects (43.2%)

SpontaneousDialogue Task:
├── HC (Healthy Control): 21 subjects (58.3%)
└── PD (Parkinson's Disease): 15 subjects (41.7%)
```

**Imbalance Ratio:** Moderate (~57:43), addressed via class weighting experiments.

### 3.2.4 File Structure

```
DATASET_MDVR_KCL/
├── ReadText/
│   ├── HC/
│   │   └── IDxx_hc_*.wav
│   └── PD/
│       └── IDxx_pd_*.wav
└── SpontaneousDialogue/
    ├── HC/
    └── PD/
```

### 3.2.5 Known Anomalies

- **ID22:** Non-standard filename pattern (handled in parsing code)
- **ID18:** Missing from SpontaneousDialogue task
- Multiple recordings per subject (requires grouped CV)

## 3.3 Dataset B: PD Speech Features

### 3.3.1 Source

Pre-extracted acoustic features from Kaggle, containing 752 features per sample.

**Location:** `assets/PD_SPEECH_FEATURES.csv`

### 3.3.2 Class Distribution

| Class | Samples | Percentage |
|-------|---------|------------|
| HC (0) | 192 | 25.4% |
| PD (1) | 564 | 74.6% |

**Imbalance Ratio:** Severe (~25:75), necessitating class weighting.

### 3.3.3 Feature Categories

The 752 features span multiple acoustic domains:

| Category | Count | Description |
|----------|-------|-------------|
| Baseline Features | 22 | Jitter, shimmer, HNR variants |
| Intensity | 3 | Intensity statistics |
| Formants | 36 | F1-F4 bandwidth features |
| MFCCs | 84 | MFCC coefficients |
| Wavelet | 182 | Wavelet decomposition features |
| TQWT | 432 | Tunable Q-factor features |

### 3.3.4 Important Caveat

> **⚠️ No Subject Identifiers Available**
> 
> Dataset B does not provide subject identifiers. If multiple samples originate from the same subject, stratified cross-validation may introduce optimistic bias due to implicit subject overlap across folds. Results should be interpreted with this caveat in mind.

## 3.4 Dataset Comparison

### 3.4.1 Key Differences

| Aspect | Dataset A | Dataset B |
|--------|-----------|-----------|
| Sample Size | 36-37 subjects | 756 samples |
| Features | 47-78 (extracted) | 752 (pre-extracted) |
| Subject Grouping | Available | Not available |
| CV Strategy | Grouped Stratified | Stratified |
| Imbalance | Moderate (57:43) | Severe (25:75) |

### 3.4.2 Implications for Analysis

1. **Direct comparison is limited** due to different feature sets and CV strategies
2. **Higher performance on Dataset B** may reflect larger sample size and/or subject leakage
3. **Dataset A results are more conservative** due to grouped CV

## 3.5 Data Preprocessing

### 3.5.1 Dataset A Preprocessing

1. Audio files loaded at native sample rate
2. Silence trimming applied (threshold-based)
3. Features extracted per recording
4. Subject-level aggregation for CV splitting

### 3.5.2 Dataset B Preprocessing

1. CSV loaded directly
2. Features standardized (z-score normalization)
3. No additional preprocessing required

## 3.6 Summary

The two datasets provide complementary perspectives:

- **Dataset A** enables rigorous grouped CV but has limited sample size
- **Dataset B** offers larger sample size but lacks subject identifiers

This thesis reports results on both, with appropriate caveats for each.
