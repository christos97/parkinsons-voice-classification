"""
Simplified Spectral Feature Extraction using Librosa

Reduced feature set for baseline experiments:
- MFCC 0-12 mean: 13 features
- Delta MFCC 0-12 mean: 13 features

Total: 26 features

No std, no delta-delta — keeping it minimal.
"""

import numpy as np
import librosa

from parkinsons_voice_classification.config import (
    TARGET_SAMPLE_RATE,
    MFCC_N_COEFFS,
    MFCC_N_FFT,
    MFCC_HOP_LENGTH,
    MFCC_N_MELS,
)


def get_spectral_feature_names() -> list[str]:
    """Return ordered list of spectral feature names (26 features)."""
    names = []
    
    # MFCC means (13)
    for i in range(MFCC_N_COEFFS):
        names.append(f'mfcc_{i}_mean')
    
    # Delta MFCC means (13)
    for i in range(MFCC_N_COEFFS):
        names.append(f'delta_mfcc_{i}_mean')
    
    return names


def extract_spectral_features(audio_path: str) -> dict:
    """
    Extract all spectral features from a single audio file.
    
    Parameters
    ----------
    audio_path : str
        Path to WAV file.
        
    Returns
    -------
    dict
        Dictionary with 26 spectral features.
    """
    features = {}
    
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=TARGET_SAMPLE_RATE)
        
        # Compute MFCCs
        mfccs = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=MFCC_N_COEFFS,
            n_fft=MFCC_N_FFT,
            hop_length=MFCC_HOP_LENGTH,
            n_mels=MFCC_N_MELS,
        )
        
        # MFCC means (13)
        for i in range(MFCC_N_COEFFS):
            features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
        
        # Delta MFCC means (13)
        delta_mfccs = librosa.feature.delta(mfccs, order=1)
        for i in range(MFCC_N_COEFFS):
            features[f'delta_mfcc_{i}_mean'] = np.mean(delta_mfccs[i])
            
    except Exception:
        # Fill with NaN on failure
        for name in get_spectral_feature_names():
            features[name] = np.nan
    
    return features
