# Methodology

This document describes the experimental design for the Master's thesis on Parkinson's Disease classification from voice data.

## Problem Definition

The research addresses a **binary classification problem**:

- **Class 0:** Healthy Control (HC)
- **Class 1:** Parkinson's Disease (PD)

The objective is to classify subjects based on acoustic characteristics derived from voice recordings, comparing performance across different data representations.

## Experimental Design

The thesis is structured around **three main experiments**, each designed to isolate specific variables while maintaining consistent evaluation protocols.

### Experiment 1: Raw Audio Pipeline

**Input:** Raw `.wav` voice recordings from Dataset A

**Process:**

1. Load and preprocess audio files
2. Extract acoustic features (e.g., MFCCs, spectral features, prosodic features)
3. Train classical machine learning classifiers
4. Evaluate using standardised metrics

**Purpose:** Assess classification performance when the researcher controls the entire feature extraction pipeline.

### Experiment 2: Pre-Extracted Features Pipeline

**Input:** Tabular acoustic features from Dataset B

**Process:**

1. Load pre-computed feature dataset
2. Apply necessary preprocessing (scaling, handling missing values)
3. Train the same classical machine learning classifiers
4. Evaluate using the same standardised metrics

**Purpose:** Assess classification performance when using professionally extracted features from a curated dataset.

### Experiment 3: Comparative Analysis

**Input:** Results from Experiments 1 and 2

**Process:**

1. Compare performance metrics across both pipelines
2. Analyse feature importance and model behaviour
3. Investigate dataset characteristics that influence results
4. Draw conclusions about data representation effects

**Purpose:** Determine whether raw audio or pre-extracted features yield better classification performance, and understand the factors contributing to any observed differences.

## Controlled Variables

To ensure valid comparisons, the following elements remain constant across experiments:

- **Machine learning models:** The same set of classical ML algorithms is applied to both data representations
- **Evaluation metrics:** Identical metrics are computed for all experiments
- **Cross-validation strategy:** Consistent data splitting approach across experiments
- **Random seeds:** Fixed for reproducibility

## Model Selection Rationale

This thesis focuses on **classical machine learning models** rather than deep learning approaches. This choice is motivated by:

1. **Interpretability:** Classical models provide clearer insight into feature importance
2. **Sample size constraints:** The available datasets may not support deep learning effectively
3. **Baseline establishment:** Classical methods serve as interpretable baselines for future work
4. **Computational accessibility:** Results can be reproduced without specialised hardware

## Evaluation Protocol

All experiments follow a standardised evaluation protocol:

1. **Data splitting:** Stratified splits to maintain class balance
2. **Cross-validation:** k-fold cross-validation for robust estimates
3. **Metric computation:** Standard classification metrics (accuracy, precision, recall, F1-score, AUC-ROC)
4. **Statistical comparison:** Appropriate tests for comparing model performances

## Limitations of the Methodology

- Feature extraction choices in Experiment 1 may influence results
- Pre-extracted features in Dataset B reflect specific extraction decisions made by the original authors
- Direct comparison assumes that both datasets represent similar underlying populations
- No deep learning baselines are included in this phase of the research
