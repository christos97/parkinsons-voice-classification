# Chapter 3: Data Description

This chapter describes the two distinct datasets utilized in this thesis. The use of dual datasets facilitates two complementary investigations:
1.  **MDVR-KCL (Dataset A):** Enables the end-to-end development of a raw audio processing pipeline.
2.  **PD_SPEECH_FEATURES (Dataset B):** Provides a high-dimensional, pre-extracted benchmark for comparison.

## 3.1 Dataset A: MDVR-KCL

**Full Name:** Mobile Device Voice Recordings at King’s College London
**Type:** Raw Audio (.wav)
**Source:** Zenodo (DOI: 10.5281/zenodo.2867215)

The MDVR-KCL dataset serves as the primary resource for this thesis, allowing for full control over the signal processing and feature extraction methodologies.

### 3.1.1 Collection Protocol
The data was collected at King’s College London Hospital from 37 participants (16 PD, 21 HC). Recordings were captured using a standard smartphone (Motorola Moto G4) in a clinical examination room to simulate realistic, low-cost telemedicine conditions.

Each participant performed multiple speech tasks:
1.  **Read Text:** Reading a standard passage ("The North Wind and the Sun"). This task minimizes linguistic variability, allowing classifiers to focus on acoustic properties.
2.  **Spontaneous Dialogue:** A semi-structured conversation with the examiner. This task imposes a higher cognitive load, potentially unmasking subtle motor control deficits associated with PD.

### 3.1.2 Audio Specifications
*   **Format:** Uncompressed WAV
*   **Sample Rate:** 44.1 kHz
*   **Bit Depth:** 16-bit Mono
*   **Environment:** Quiet clinical room (reverberation time ~500ms)

### 3.1.3 Subject Demographics & Structure
The dataset comprises 37 unique subjects.

| Class | Subjects | Description |
| :--- | :--- | :--- |
| **Healthy Controls (HC)** | 21 | No neurological diagnosis. |
| **Parkinson's Disease (PD)** | 16 | Clinically diagnosed with PD. |
| **Total** | **37** | |

**IMPORTANT:** The dataset provides multiple recordings per subject. Strict subject-level splitting was enforced during experiments to prevent data leakage (see Chapter 4).

### 3.1.4 Data Cleaning & Anomaly Resolution
During the initial exploration phase (January 2026), two anomalies were identified and resolved:
1.  **Parsing Error:** File `ID22hc_0_0_0.wav` lacked the standard underscore separator. A custom parser was implemented to correctly map this to Subject `ID22` (HC).
2.  **Missing Data:** Subject `ID18` (PD) is missing the `SpontaneousDialogue` recording. This subject was excluded from the Spontaneous Dialogue experiment (Experiment A2) but retained for the Read Text experiment (Experiment A1).

---

## 3.2 Dataset B: PD_SPEECH_FEATURES

**Common Name:** UCI Parkinson’s Disease Classification Dataset
**Type:** Tabular Pre-extracted Features (.csv)
**Source:** UCI Machine Learning Repository / Kaggle

Dataset B is used as a benchmark to represent the "state-of-the-art" in classical feature engineering. Unlike Dataset A, it does not contain raw audio.

### 3.2.1 Content Overview
This dataset contains **756 pre-processed samples** derived from 188 PD patients and 64 healthy controls.
*   **Features:** 752 columns representing a comprehensive array of acoustic algorithms, including:
    *   MFCCs (Mel-Frequency Cepstral Coefficients)
    *   Wavelet Transforms
    *   Vocal fold features
    *   TQWT (Tunable Q-factor Wavelet Transform)
*   **Target:** Binary class label (0 = HC, 1 = PD).

### 3.2.2 Critical Limitations
While this dataset offers a rich feature set, it presents a significant methodological challenge: **Subject Identifiers are not provided.**

It is known from the source metadata that each of the 252 subjects provided 3 repetitions of the phonation task (sustained vowel /a/). This implies that the 756 rows are **not independent**. Since rows cannot be grouped by subject, standard cross-validation may mix samples from the same subject into both training and test sets.

**Implication:** Results derived from Dataset B must be interpreted with the caveat that they may be optimistically biased due to implicit subject leakage. This thesis utilizes Dataset B primarily to validate model stability on high-dimensional data, rather than to make definitive diagnostic claims.

## 3.3 Summary of Datasets

| Feature | Dataset A (Primary) | Dataset B (Benchmark) |
| :--- | :--- | :--- |
| **Format** | Raw Audio (.wav) | Tabular Features (.csv) |
| **Subjects** | 37 (Known IDs) | ~252 (Unknown IDs) |
| **Samples** | 73 recordings | 756 rows |
| **Features** | 47 (Extracted by Thesis Pipeline) | 752 (Pre-extracted) |
| **Tasks** | Read Text, Spontaneous Dialogue | Sustained Vowel (/a/) |
| **Class Balance** | 57% HC / 43% PD | 25% HC / 75% PD |
| **Subject Independence** | **Guaranteed (Grouped CV)** | **Unknown (Potential Leakage)** |

This dual-dataset approach allows the thesis to contrast the performance of a rigidly controlled, interpretable pipeline (Dataset A) against a high-performance, high-dimensionality benchmark (Dataset B).
