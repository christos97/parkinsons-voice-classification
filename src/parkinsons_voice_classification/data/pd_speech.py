"""
Dataset B (PD_SPEECH_FEATURES.csv) Loader

Simple loader for the pre-extracted feature dataset.
One row per subject, no grouping needed.
"""

import pandas as pd
import numpy as np
from typing import Tuple

from parkinsons_voice_classification.config import PD_SPEECH_FEATURES_CSV


def load_features() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load Dataset B features and labels.
    
    Returns
    -------
    X : np.ndarray
        Feature matrix (756 × 752)
    y : np.ndarray
        Label array (756,) with 0=HC, 1=PD
    """
    df = pd.read_csv(PD_SPEECH_FEATURES_CSV)
    
    # Drop non-feature columns
    drop_cols = ['id', 'gender', 'class']
    feature_cols = [c for c in df.columns if c not in drop_cols]
    
    X = df[feature_cols].values
    y = df['class'].values
    
    return np.asarray(X), np.asarray(y)


def get_feature_names() -> list[str]:
    """Return list of feature column names."""
    df = pd.read_csv(PD_SPEECH_FEATURES_CSV, nrows=0)
    drop_cols = ['id', 'gender', 'class']
    return [c for c in df.columns if c not in drop_cols]


def get_dataset_info() -> dict:
    """Return basic dataset statistics."""
    X, y = load_features()
    return {
        'n_samples': len(y),
        'n_features': X.shape[1],
        'n_hc': (y == 0).sum(),
        'n_pd': (y == 1).sum(),
        'class_balance': f"{(y == 0).mean():.1%} HC / {(y == 1).mean():.1%} PD"
    }
