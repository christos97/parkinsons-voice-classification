# Dataset Exploration Summary Report

**Date:** January 12, 2026  
**Phase:** Step 1 & Step 2 — Data Exploration  
**Status:** Complete — Awaiting Approval for Phase 3

---

## Executive Summary

This report documents the exploration of two datasets for a Master's thesis on **binary classification of Parkinson's Disease (PD) vs Healthy Controls (HC)** using voice data.

| Dataset | Type | Subjects/Rows | Class Balance | CV Strategy |
|---------|------|---------------|---------------|-------------|
| **A (MDVR-KCL)** | Raw WAV audio | 37 subjects | 57% HC / 43% PD | Grouped Stratified 5-Fold |
| **B (PD_SPEECH_FEATURES)** | Pre-extracted CSV | 756 rows | 25% HC / 75% PD | Stratified 5-Fold |

---

## Dataset A — MDVR-KCL (Raw Audio)

### Location

```
assets/DATASET_MDVR_KCL/
├── ReadText/
│   ├── HC/
│   └── PD/
└── SpontaneousDialogue/
    ├── HC/
    └── PD/
```

### Subject Registry

#### Healthy Controls (HC) — 21 Subjects

| Subject ID | ReadText | SpontaneousDialogue |
|------------|----------|---------------------|
| ID00 | ✅ | ✅ |
| ID01 | ✅ | ✅ |
| ID03 | ✅ | ✅ |
| ID05 | ✅ | ✅ |
| ID08 | ✅ | ✅ |
| ID09 | ✅ | ✅ |
| ID10 | ✅ | ✅ |
| ID11 | ✅ | ✅ |
| ID12 | ✅ | ✅ |
| ID14 | ✅ | ✅ |
| ID15 | ✅ | ✅ |
| ID19 | ✅ | ✅ |
| ID21 | ✅ | ✅ |
| ID22 | ✅ | ✅ |
| ID23 | ✅ | ✅ |
| ID25 | ✅ | ✅ |
| ID26 | ✅ | ✅ |
| ID28 | ✅ | ✅ |
| ID31 | ✅ | ✅ |
| ID35 | ✅ | ✅ |
| ID36 | ✅ | ✅ |

#### Parkinson's Disease (PD) — 16 Subjects

| Subject ID | ReadText | SpontaneousDialogue |
|------------|----------|---------------------|
| ID02 | ✅ | ✅ |
| ID04 | ✅ | ✅ |
| ID06 | ✅ | ✅ |
| ID07 | ✅ | ✅ |
| ID13 | ✅ | ✅ |
| ID16 | ✅ | ✅ |
| ID17 | ✅ | ✅ |
| **ID18** | ✅ | ❌ **Missing** |
| ID20 | ✅ | ✅ |
| ID24 | ✅ | ✅ |
| ID27 | ✅ | ✅ |
| ID29 | ✅ | ✅ |
| ID30 | ✅ | ✅ |
| ID32 | ✅ | ✅ |
| ID33 | ✅ | ✅ |
| ID34 | ✅ | ✅ |

### Recording Counts

| Task | HC Recordings | PD Recordings | Total |
|------|---------------|---------------|-------|
| ReadText | 21 | 16 | 37 |
| SpontaneousDialogue | 21 | 15 | 36 |
| **Total** | **42** | **31** | **73** |

### Class Distribution

```
HC: 21 subjects (56.8%)
PD: 16 subjects (43.2%)
──────────────────────────
Total: 37 subjects
```

### Filename Convention

**Standard pattern:**
```
IDxx_[class]_[num1]_[num2]_[num3].wav
```

**Components:**
- `IDxx` — Subject identifier (e.g., `ID02`, `ID36`)
- `[class]` — Class label: `hc` (Healthy Control) or `pd` (Parkinson's Disease)
- `[num1]_[num2]_[num3]` — Clinical metadata (likely UPDRS/H&Y scores; not used for classification)

**Examples:**
```
ID02_pd_2_0_0.wav  → Subject ID02, PD class
ID00_hc_0_0_0.wav  → Subject ID00, HC class
ID18_pd_4_3_3.wav  → Subject ID18, PD class
```

### Edge Cases Detected

#### Edge Case 1: Malformed Filename

| Filename | Location | Issue |
|----------|----------|-------|
| `ID22hc_0_0_0.wav` | `SpontaneousDialogue/HC/` | Missing underscore between ID and class |

**Expected:** `ID22_hc_0_0_0.wav`  
**Actual:** `ID22hc_0_0_0.wav`

**Resolution:** Parsing logic must handle this variant. The correct subject ID is `ID22` and the class is `HC`.

**Parsing rule:**
```
If filename does not match standard pattern:
  Check for pattern: ID[0-9]+hc_... → extract subject ID before "hc"
```

#### Edge Case 2: Missing Recording

| Subject | Class | ReadText | SpontaneousDialogue |
|---------|-------|----------|---------------------|
| ID18 | PD | ✅ `ID18_pd_4_3_3.wav` | ❌ Not present |

**Impact:** 
- ID18 has only 1 recording instead of 2
- SpontaneousDialogue/PD has 15 files instead of 16
- Total recordings: 73 instead of 74

**Resolution:** No code fix required. Document this asymmetry and proceed. Subject ID18 will still be included with its single recording.

---

## Dataset B — PD_SPEECH_FEATURES.csv

### Location

```
assets/PD_SPEECH_FEATURES.csv
```

### Structure Overview

| Property | Value |
|----------|-------|
| Total rows | 756 (excluding header) |
| Total columns | 755 |
| Feature columns | 752 |
| Metadata columns | 3 (`id`, `gender`, `class`) |

### Column Layout

| Position | Column Name | Type | Description |
|----------|-------------|------|-------------|
| 1 | `id` | Integer | Sample/subject identifier |
| 2 | `gender` | Binary (0/1) | Subject gender |
| 3–754 | (features) | Float | 752 acoustic features |
| 755 | `class` | Binary (0/1) | Target label |

### Label Encoding

| Value | Meaning | Count | Percentage |
|-------|---------|-------|------------|
| **0** | Healthy Control (HC) | 192 | 25.4% |
| **1** | Parkinson's Disease (PD) | 564 | 74.6% |
| | **Total** | **756** | 100% |

### Class Distribution

```
HC: 192 samples (25.4%)
PD: 564 samples (74.6%)
─────────────────────────
Total: 756 samples

Class imbalance ratio: ~1:3 (HC:PD)
```

### Feature Categories

The 752 features span multiple acoustic analysis domains:

#### 1. Baseline Voice Quality (3 features)
- `PPE` — Pitch Period Entropy
- `DFA` — Detrended Fluctuation Analysis
- `RPDE` — Recurrence Period Density Entropy

#### 2. Periodicity/Pulse Analysis (6 features)
- `numPulses`, `numPeriodsPulses`
- `meanPeriodPulses`, `stdDevPeriodPulses`

#### 3. Jitter Features (6 features)
- `locPctJitter`, `locAbsJitter`
- `rapJitter`, `ppq5Jitter`, `ddpJitter`

#### 4. Shimmer Features (6 features)
- `locShimmer`, `locDbShimmer`
- `apq3Shimmer`, `apq5Shimmer`, `apq11Shimmer`, `ddaShimmer`

#### 5. Harmonicity Features (3 features)
- `meanAutoCorrHarmonicity`
- `meanNoiseToHarmHarmonicity`
- `meanHarmToNoiseHarmonicity`

#### 6. Intensity Features (3 features)
- `minIntensity`, `maxIntensity`, `meanIntensity`

#### 7. Formant Features (8 features)
- Frequencies: `f1`, `f2`, `f3`, `f4`
- Bandwidths: `b1`, `b2`, `b3`, `b4`

#### 8. Glottal Features (12 features)
- `GQ_prc5_95`, `GQ_std_cycle_open`, `GQ_std_cycle_closed`
- `GNE_mean`, `GNE_std`, `GNE_SNR_TKEO`, `GNE_SNR_SEO`, etc.

#### 9. VFER Features (8 features)
- `VFER_mean`, `VFER_std`, `VFER_entropy`
- `VFER_SNR_TKEO`, `VFER_SNR_SEO`, etc.

#### 10. IMF Features (6 features)
- `IMF_SNR_SEO`, `IMF_SNR_TKEO`, `IMF_SNR_entropy`, etc.

#### 11. MFCC Features (84 features)
- Mean MFCC coefficients (0th–12th): 13 features
- Std MFCC coefficients: 13 features
- Mean delta coefficients: 14 features
- Std delta coefficients: 14 features
- Mean delta-delta coefficients: 14 features
- Std delta-delta coefficients: 14 features

#### 12. Wavelet Decomposition Features (132 features)
- `Ea`, `Ed_1_coef` through `Ed_10_coef`
- Shannon entropy, log entropy, TKEO mean/std for detail coefficients
- Approximation coefficient features

#### 13. TQWT Features (324 features)
- 36 decomposition levels × 9 statistics:
  - `tqwt_energy_dec_1` through `tqwt_energy_dec_36`
  - `tqwt_entropy_shannon_dec_*`
  - `tqwt_entropy_log_dec_*`
  - `tqwt_TKEO_mean_dec_*`, `tqwt_TKEO_std_dec_*`
  - `tqwt_medianValue_dec_*`, `tqwt_meanValue_dec_*`
  - `tqwt_stdValue_dec_*`, `tqwt_minValue_dec_*`, `tqwt_maxValue_dec_*`
  - `tqwt_skewnessValue_dec_*`, `tqwt_kurtosisValue_dec_*`

---

## Cross-Dataset Comparison

| Property | Dataset A (MDVR-KCL) | Dataset B (CSV) |
|----------|----------------------|-----------------|
| **Data format** | Raw WAV audio | Tabular numeric |
| **Sample unit** | Recording (WAV file) | Row |
| **Unique subjects** | 37 | Unknown (likely 756) |
| **Rows/recordings** | 73 | 756 |
| **HC samples** | 42 recordings (21 subjects) | 192 rows |
| **PD samples** | 31 recordings (16 subjects) | 564 rows |
| **Class balance** | 57% HC / 43% PD | 25% HC / 75% PD |
| **Features** | Must be extracted | 752 pre-extracted |
| **Grouping needed** | Yes (by subject) | No (1 row = 1 subject) |
| **CV strategy** | Grouped Stratified 5-Fold | Stratified 5-Fold |

### Key Observations

1. **Opposite class imbalance:** Dataset A has more HC, Dataset B has more PD
2. **Scale difference:** Dataset B is ~10× larger by sample count
3. **No shared subjects:** Datasets are independent; no cross-dataset subject matching
4. **Feature extraction required:** Dataset A needs acoustic feature extraction before ML

---

## Validation Strategy Confirmation

### Dataset A — Grouped Stratified 5-Fold Cross-Validation

**Rationale:** Each subject has multiple recordings. To prevent data leakage, all recordings from one subject must stay in the same fold.

**Implementation:**
```
Groups = Subject IDs (ID00, ID01, ..., ID36)
Stratification = Class labels (HC, PD)
k = 5 folds
```

### Dataset B — Stratified 5-Fold Cross-Validation

**Rationale:** One row per subject. No grouping needed; standard stratified CV preserves class balance.

**Implementation:**
```
Stratification = Class labels (0, 1)
k = 5 folds
```

---

## Confirmed Parsing Rules

### Dataset A Filename Parsing

```python
import re

def parse_mdvr_filename(filename: str) -> dict:
    """
    Parse MDVR-KCL filename to extract subject ID and class.
    
    Handles both standard and edge case formats:
    - Standard: ID02_pd_2_0_0.wav
    - Edge case: ID22hc_0_0_0.wav (missing underscore)
    """
    # Remove .wav extension
    name = filename.replace('.wav', '')
    
    # Try standard pattern first: IDxx_class_...
    standard_match = re.match(r'^(ID\d+)_(hc|pd)_', name, re.IGNORECASE)
    if standard_match:
        return {
            'subject_id': standard_match.group(1),
            'class': standard_match.group(2).lower()
        }
    
    # Try edge case pattern: IDxxclass_...
    edge_match = re.match(r'^(ID\d+)(hc|pd)_', name, re.IGNORECASE)
    if edge_match:
        return {
            'subject_id': edge_match.group(1),
            'class': edge_match.group(2).lower()
        }
    
    raise ValueError(f"Cannot parse filename: {filename}")
```

### Dataset B Label Mapping

```python
LABEL_MAP = {
    0: 'HC',  # Healthy Control
    1: 'PD'   # Parkinson's Disease
}
```

---

## Action Items for Phase 3

### Immediate Next Steps

1. **Lock random seed:** Define global seed (e.g., `RANDOM_SEED = 42`)
2. **Design feature extraction:** Select acoustic features for Dataset A
3. **Implement data loaders:** Create consistent loading functions for both datasets
4. **Build CV infrastructure:** Implement grouped stratified k-fold for Dataset A

### Decisions Required

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Speech task handling | ReadText only / SpontaneousDialogue only / Both separately | Evaluate both tasks as **separate experiments** |
| Feature aggregation | Per-file / Per-subject mean | **Per-file** (then grouped CV handles subject-level) |
| Feature set for Dataset A | Minimal / Comprehensive | Start with **MFCC + prosody** baseline |

---

## Appendix: Raw File Listings

### Dataset A — ReadText/HC (21 files)

```
ID00_hc_0_0_0.wav
ID01_hc_0_0_0.wav
ID03_hc_0_0_0.wav
ID05_hc_0_0_0.wav
ID08_hc_0_0_0.wav
ID09_hc_0_0_0.wav
ID10_hc_0_0_0.wav
ID11_hc_0_0_0.wav
ID12_hc_0_0_0.wav
ID14_hc_0_0_0.wav
ID15_hc_0_0_0.wav
ID19_hc_0_0_0.wav
ID21_hc_0_0_0.wav
ID22_hc_0_0_0.wav
ID23_hc_0_0_0.wav
ID25_hc_0_0_0.wav
ID26_hc_0_0_0.wav
ID28_hc_0_0_0.wav
ID31_hc_0_1_1.wav
ID35_hc_0_0_0.wav
ID36_hc_0_0_0.wav
```

### Dataset A — ReadText/PD (16 files)

```
ID02_pd_2_0_0.wav
ID04_pd_2_0_1.wav
ID06_pd_3_1_1.wav
ID07_pd_2_0_0.wav
ID13_pd_3_2_2.wav
ID16_pd_2_0_0.wav
ID17_pd_2_1_0.wav
ID18_pd_4_3_3.wav
ID20_pd_3_0_1.wav
ID24_pd_2_0_0.wav
ID27_pd_4_1_1.wav
ID29_pd_3_1_2.wav
ID30_pd_2_1_1.wav
ID32_pd_3_1_1.wav
ID33_pd_3_2_2.wav
ID34_pd_2_0_0.wav
```

### Dataset A — SpontaneousDialogue/HC (21 files)

```
ID00_hc_0_0_0.wav
ID01_hc_0_0_0.wav
ID03_hc_0_0_0.wav
ID05_hc_0_0_0.wav
ID08_hc_0_0_0.wav
ID09_hc_0_0_0.wav
ID10_hc_0_0_0.wav
ID11_hc_0_0_0.wav
ID12_hc_0_0_0.wav
ID14_hc_0_0_0.wav
ID15_hc_0_0_0.wav
ID19_hc_0_0_0.wav
ID21_hc_0_0_0.wav
ID22hc_0_0_0.wav       ← Edge case (malformed)
ID23_hc_0_0_0.wav
ID25_hc_0_0_0.wav
ID26_hc_0_0_0.wav
ID28_hc_0_0_0.wav
ID31_hc_0_1_1.wav
ID35_hc_0_0_0.wav
ID36_hc_0_0_0.wav
```

### Dataset A — SpontaneousDialogue/PD (15 files)

```
ID02_pd_2_0_0.wav
ID04_pd_2_0_1.wav
ID06_pd_3_1_1.wav
ID07_pd_2_0_0.wav
ID13_pd_3_2_2.wav
ID16_pd_2_0_0.wav
ID17_pd_2_1_0.wav
                       ← ID18 missing
ID20_pd_3_0_1.wav
ID24_pd_2_0_0.wav
ID27_pd_4_1_1.wav
ID29_pd_3_1_2.wav
ID30_pd_2_1_1.wav
ID32_pd_3_1_1.wav
ID33_pd_3_2_2.wav
ID34_pd_2_0_0.wav
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-12 | AI Assistant | Initial exploration report |

---

*End of Report*
