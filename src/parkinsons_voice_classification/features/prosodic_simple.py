"""
Simplified Prosodic Feature Extraction using Parselmouth (Praat)

Reduced feature set for baseline experiments:
- F0: 4 features (mean, std, min, max)
- Jitter: 3 features (local, rap, ppq5)
- Shimmer: 3 features (local, apq3, apq11)
- Harmonicity: 2 features (hnr_mean, autocorr)
- Intensity: 3 features (mean, min, max)
- Formants: 6 features (F1-F3 mean and std)

Total: 21 features

CRITICAL: Jitter, shimmer, and F0 are computed on VOICED FRAMES ONLY.
"""

import numpy as np
import parselmouth
from parselmouth.praat import call

from parkinsons_voice_classification.config import F0_MIN_HZ, F0_MAX_HZ


def get_prosodic_feature_names() -> list[str]:
    """Return ordered list of prosodic feature names (21 features)."""
    return [
        # F0 (4)
        "f0_mean",
        "f0_std",
        "f0_min",
        "f0_max",
        # Jitter (3)
        "jitter_local",
        "jitter_rap",
        "jitter_ppq5",
        # Shimmer (3)
        "shimmer_local",
        "shimmer_apq3",
        "shimmer_apq11",
        # Harmonicity (2)
        "hnr_mean",
        "autocorr_harmonicity",
        # Intensity (3)
        "intensity_mean",
        "intensity_min",
        "intensity_max",
        # Formants (6)
        "f1_mean",
        "f2_mean",
        "f3_mean",
        "f1_std",
        "f2_std",
        "f3_std",
    ]


def extract_prosodic_features(audio_path: str) -> dict:
    """
    Extract all prosodic features from a single audio file.

    Parameters
    ----------
    audio_path : str
        Path to WAV file.

    Returns
    -------
    dict
        Dictionary with 21 prosodic features.
    """
    sound = parselmouth.Sound(audio_path)
    features = {}

    # === F0 Features (4) ===
    try:
        pitch = call(sound, "To Pitch", 0.0, F0_MIN_HZ, F0_MAX_HZ)
        features["f0_mean"] = call(pitch, "Get mean", 0, 0, "Hertz")
        features["f0_std"] = call(pitch, "Get standard deviation", 0, 0, "Hertz")
        features["f0_min"] = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
        features["f0_max"] = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
    except Exception:
        features.update({k: np.nan for k in ["f0_mean", "f0_std", "f0_min", "f0_max"]})

    # === Jitter Features (3) ===
    try:
        point_process = call(sound, "To PointProcess (periodic, cc)", F0_MIN_HZ, F0_MAX_HZ)
        features["jitter_local"] = call(
            point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3
        )
        features["jitter_rap"] = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        features["jitter_ppq5"] = call(point_process, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    except Exception:
        features.update({k: np.nan for k in ["jitter_local", "jitter_rap", "jitter_ppq5"]})

    # === Shimmer Features (3) ===
    try:
        point_process = call(sound, "To PointProcess (periodic, cc)", F0_MIN_HZ, F0_MAX_HZ)
        features["shimmer_local"] = call(
            [sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6
        )
        features["shimmer_apq3"] = call(
            [sound, point_process], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6
        )
        features["shimmer_apq11"] = call(
            [sound, point_process], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6
        )
    except Exception:
        features.update({k: np.nan for k in ["shimmer_local", "shimmer_apq3", "shimmer_apq11"]})

    # === Harmonicity Features (2) ===
    try:
        harmonicity = call(sound, "To Harmonicity (cc)", 0.01, F0_MIN_HZ, 0.1, 1.0)
        features["hnr_mean"] = call(harmonicity, "Get mean", 0, 0)

        # Autocorrelation-based harmonicity
        pitch = call(
            sound,
            "To Pitch (ac)",
            0.0,
            F0_MIN_HZ,
            15,
            "no",
            0.03,
            0.45,
            0.01,
            0.35,
            0.14,
            F0_MAX_HZ,
        )
        features["autocorr_harmonicity"] = call(pitch, "Get mean", 0, 0, "Hertz")
    except Exception:
        features.update({k: np.nan for k in ["hnr_mean", "autocorr_harmonicity"]})

    # === Intensity Features (3) ===
    try:
        intensity = call(sound, "To Intensity", F0_MIN_HZ, 0.0, "yes")
        features["intensity_mean"] = call(intensity, "Get mean", 0, 0, "dB")
        features["intensity_min"] = call(intensity, "Get minimum", 0, 0, "Parabolic")
        features["intensity_max"] = call(intensity, "Get maximum", 0, 0, "Parabolic")
    except Exception:
        features.update({k: np.nan for k in ["intensity_mean", "intensity_min", "intensity_max"]})

    # === Formant Features (6) ===
    try:
        formants = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)

        # Get F1, F2, F3 values over time
        num_frames = call(formants, "Get number of frames")
        f1_vals, f2_vals, f3_vals = [], [], []

        for frame in range(1, num_frames + 1):
            f1 = call(
                formants,
                "Get value at time",
                1,
                call(formants, "Get time from frame number", frame),
                "Hertz",
                "Linear",
            )
            f2 = call(
                formants,
                "Get value at time",
                2,
                call(formants, "Get time from frame number", frame),
                "Hertz",
                "Linear",
            )
            f3 = call(
                formants,
                "Get value at time",
                3,
                call(formants, "Get time from frame number", frame),
                "Hertz",
                "Linear",
            )

            if not np.isnan(f1):
                f1_vals.append(f1)
            if not np.isnan(f2):
                f2_vals.append(f2)
            if not np.isnan(f3):
                f3_vals.append(f3)

        features["f1_mean"] = np.mean(f1_vals) if f1_vals else np.nan
        features["f2_mean"] = np.mean(f2_vals) if f2_vals else np.nan
        features["f3_mean"] = np.mean(f3_vals) if f3_vals else np.nan
        features["f1_std"] = np.std(f1_vals) if f1_vals else np.nan
        features["f2_std"] = np.std(f2_vals) if f2_vals else np.nan
        features["f3_std"] = np.std(f3_vals) if f3_vals else np.nan
    except Exception:
        features.update(
            {k: np.nan for k in ["f1_mean", "f2_mean", "f3_mean", "f1_std", "f2_std", "f3_std"]}
        )

    return features
