"""
Spectral Feature Extraction using Librosa

Feature sets:
- Baseline (26 features):
  - MFCC 0-12 mean: 13 features
  - Delta MFCC 0-12 mean: 13 features

- Extended (57 features):
  - MFCC 0-12 mean: 13 features
  - MFCC 0-12 std: 13 features
  - Delta MFCC 0-12 mean: 13 features
  - Delta-delta MFCC 0-12 mean: 13 features
  - Spectral shape: 5 features (centroid, bandwidth, rolloff, flatness, zcr)

Controlled by USE_EXTENDED_FEATURES in config.py
"""

import numpy as np
import librosa

from parkinsons_voice_classification.config import (
    TARGET_SAMPLE_RATE,
    MFCC_N_COEFFS,
    MFCC_N_FFT,
    MFCC_HOP_LENGTH,
    MFCC_N_MELS,
    USE_EXTENDED_FEATURES,
)


def get_spectral_feature_names() -> list[str]:
    """Return ordered list of spectral feature names (26 or 57 features)."""
    names = []

    # MFCC means (13) - always included
    for i in range(MFCC_N_COEFFS):
        names.append(f"mfcc_{i}_mean")

    # MFCC std (13) - extended only
    if USE_EXTENDED_FEATURES:
        for i in range(MFCC_N_COEFFS):
            names.append(f"mfcc_{i}_std")

    # Delta MFCC means (13) - always included
    for i in range(MFCC_N_COEFFS):
        names.append(f"delta_mfcc_{i}_mean")

    # Delta-delta MFCC means (13) - extended only
    if USE_EXTENDED_FEATURES:
        for i in range(MFCC_N_COEFFS):
            names.append(f"delta2_mfcc_{i}_mean")

    # Spectral shape features (5) - extended only
    if USE_EXTENDED_FEATURES:
        names.extend([
            "spectral_centroid_mean",
            "spectral_bandwidth_mean",
            "spectral_rolloff_mean",
            "spectral_flatness_mean",
            "zcr_mean",
        ])

    return names


def extract_spectral_features(audio_path: str) -> dict:
    """
    Extract spectral features from a single audio file.

    Parameters
    ----------
    audio_path : str
        Path to WAV file.

    Returns
    -------
    dict
        Dictionary with 26 (baseline) or 57 (extended) spectral features.
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

        # MFCC means (13) - always included
        for i in range(MFCC_N_COEFFS):
            features[f"mfcc_{i}_mean"] = np.mean(mfccs[i])

        # MFCC std (13) - extended only
        if USE_EXTENDED_FEATURES:
            for i in range(MFCC_N_COEFFS):
                features[f"mfcc_{i}_std"] = np.std(mfccs[i])

        # Delta MFCC means (13) - always included
        delta_mfccs = librosa.feature.delta(mfccs, order=1)
        for i in range(MFCC_N_COEFFS):
            features[f"delta_mfcc_{i}_mean"] = np.mean(delta_mfccs[i])

        # Delta-delta MFCC means (13) - extended only
        if USE_EXTENDED_FEATURES:
            delta2_mfccs = librosa.feature.delta(mfccs, order=2)
            for i in range(MFCC_N_COEFFS):
                features[f"delta2_mfcc_{i}_mean"] = np.mean(delta2_mfccs[i])

        # Spectral shape features (5) - extended only
        if USE_EXTENDED_FEATURES:
            # Spectral centroid
            centroid = librosa.feature.spectral_centroid(
                y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
            )
            features["spectral_centroid_mean"] = np.mean(centroid)

            # Spectral bandwidth
            bandwidth = librosa.feature.spectral_bandwidth(
                y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
            )
            features["spectral_bandwidth_mean"] = np.mean(bandwidth)

            # Spectral rolloff
            rolloff = librosa.feature.spectral_rolloff(
                y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
            )
            features["spectral_rolloff_mean"] = np.mean(rolloff)

            # Spectral flatness
            flatness = librosa.feature.spectral_flatness(
                y=y, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
            )
            features["spectral_flatness_mean"] = np.mean(flatness)

            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(
                y=y, frame_length=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
            )
            features["zcr_mean"] = np.mean(zcr)

    except Exception:
        # Fill with NaN on failure
        for name in get_spectral_feature_names():
            features[name] = np.nan

    return features
