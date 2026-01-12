"""
Spectral Feature Extraction using Librosa

This module extracts spectral and cepstral features commonly used
in speech and speaker recognition:

- MFCCs: Mel-frequency cepstral coefficients (vocal tract shape)
- Delta MFCCs: First-order derivatives (temporal dynamics)
- Spectral features: Centroid, bandwidth, rolloff, flatness
- Zero-crossing rate: High-frequency content / noisiness

Feature count: 57 features
- MFCCs: 26 features (13 mean + 13 std)
- Delta MFCCs: 26 features (13 mean + 13 std)
- Spectral: 4 features (centroid, bandwidth, rolloff, flatness)
- ZCR: 1 feature
"""

import numpy as np
import librosa

from parkinsons_voice_classification.config import (
    TARGET_SAMPLE_RATE,
    MFCC_N_COEFFS,
    MFCC_N_FFT,
    MFCC_HOP_LENGTH,
    MFCC_WIN_LENGTH,
    MFCC_N_MELS,
)


def extract_mfcc_features(y: np.ndarray, sr: int) -> dict:
    """
    Extract MFCC statistics from audio signal.
    
    MFCCs capture the spectral envelope of speech, representing
    the configuration of the vocal tract. They are standard features
    in speech and speaker recognition.
    
    Parameters
    ----------
    y : np.ndarray
        Audio signal (mono, float).
    sr : int
        Sample rate in Hz.
        
    Returns
    -------
    dict
        MFCC features: mean and std for 13 coefficients.
    """
    mfccs = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=MFCC_N_COEFFS,
        n_fft=MFCC_N_FFT,
        hop_length=MFCC_HOP_LENGTH,
        win_length=MFCC_WIN_LENGTH,
        n_mels=MFCC_N_MELS,
    )
    
    features = {}
    
    for i in range(MFCC_N_COEFFS):
        features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
        features[f'mfcc_{i}_std'] = np.std(mfccs[i])
    
    return features


def extract_delta_mfcc_features(y: np.ndarray, sr: int) -> dict:
    """
    Extract delta (velocity) MFCC features.
    
    Delta MFCCs capture the temporal dynamics of the spectral envelope,
    which is important for detecting bradykinetic (slow) speech patterns
    characteristic of PD.
    
    Parameters
    ----------
    y : np.ndarray
        Audio signal (mono, float).
    sr : int
        Sample rate in Hz.
        
    Returns
    -------
    dict
        Delta MFCC features: mean and std for 13 coefficients.
    """
    mfccs = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=MFCC_N_COEFFS,
        n_fft=MFCC_N_FFT,
        hop_length=MFCC_HOP_LENGTH,
        win_length=MFCC_WIN_LENGTH,
        n_mels=MFCC_N_MELS,
    )
    
    # Compute first-order difference (delta)
    delta_mfccs = librosa.feature.delta(mfccs, order=1)
    
    features = {}
    
    for i in range(MFCC_N_COEFFS):
        features[f'delta_mfcc_{i}_mean'] = np.mean(delta_mfccs[i])
        features[f'delta_mfcc_{i}_std'] = np.std(delta_mfccs[i])
    
    return features


def extract_spectral_features(y: np.ndarray, sr: int) -> dict:
    """
    Extract spectral shape features.
    
    These features characterize the overall spectral shape:
    - Spectral centroid: "Center of mass" of spectrum (brightness)
    - Spectral bandwidth: Spectral spread
    - Spectral rolloff: Frequency below which 85% of energy is contained
    - Spectral flatness: How noise-like vs tonal the signal is
    
    Parameters
    ----------
    y : np.ndarray
        Audio signal (mono, float).
    sr : int
        Sample rate in Hz.
        
    Returns
    -------
    dict
        Spectral features: centroid, bandwidth, rolloff, flatness.
    """
    # Spectral centroid
    centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
    )
    
    # Spectral bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(
        y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
    )
    
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(
        y=y, sr=sr, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
    )
    
    # Spectral flatness
    flatness = librosa.feature.spectral_flatness(
        y=y, n_fft=MFCC_N_FFT, hop_length=MFCC_HOP_LENGTH
    )
    
    return {
        'spectral_centroid_mean': np.mean(centroid),
        'spectral_bandwidth_mean': np.mean(bandwidth),
        'spectral_rolloff_mean': np.mean(rolloff),
        'spectral_flatness_mean': np.mean(flatness),
    }


def extract_zcr_features(y: np.ndarray) -> dict:
    """
    Extract zero-crossing rate feature.
    
    ZCR indicates the rate at which the signal changes sign,
    correlating with high-frequency content and noisiness.
    
    Parameters
    ----------
    y : np.ndarray
        Audio signal (mono, float).
        
    Returns
    -------
    dict
        Zero-crossing rate: mean.
    """
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=MFCC_HOP_LENGTH)
    
    return {
        'zcr_mean': np.mean(zcr),
    }


def extract_spectral_features_all(audio_path: str) -> dict:
    """
    Extract all spectral features from an audio file.
    
    This is the main entry point for spectral feature extraction.
    Audio is resampled to TARGET_SAMPLE_RATE for consistency.
    
    Parameters
    ----------
    audio_path : str
        Path to the WAV file.
        
    Returns
    -------
    dict
        Dictionary containing all 57 spectral features.
    """
    # Load audio and resample to target rate
    y, sr = librosa.load(audio_path, sr=TARGET_SAMPLE_RATE, mono=True)
    
    features = {}
    
    # Extract each feature group
    features.update(extract_mfcc_features(y, int(sr)))
    features.update(extract_delta_mfcc_features(y, int(sr)))
    features.update(extract_spectral_features(y, int(sr)))
    features.update(extract_zcr_features(y))
    
    return features


def get_spectral_feature_names() -> list[str]:
    """
    Return the ordered list of spectral feature names.
    
    Returns
    -------
    list[str]
        List of 57 feature names in extraction order.
    """
    names = []
    
    # MFCCs (26)
    for i in range(MFCC_N_COEFFS):
        names.append(f'mfcc_{i}_mean')
        names.append(f'mfcc_{i}_std')
    
    # Delta MFCCs (26)
    for i in range(MFCC_N_COEFFS):
        names.append(f'delta_mfcc_{i}_mean')
        names.append(f'delta_mfcc_{i}_std')
    
    # Spectral (4)
    names.extend([
        'spectral_centroid_mean',
        'spectral_bandwidth_mean',
        'spectral_rolloff_mean',
        'spectral_flatness_mean',
    ])
    
    # ZCR (1)
    names.append('zcr_mean')
    
    return names
