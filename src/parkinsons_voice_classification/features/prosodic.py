"""
Prosodic Feature Extraction using Parselmouth (Praat)

This module extracts voice quality features that are clinically relevant
for Parkinson's Disease detection:

- Fundamental Frequency (F0): Pitch statistics
- Jitter: Cycle-to-cycle pitch variation (vocal fold instability)
- Shimmer: Cycle-to-cycle amplitude variation (laryngeal control)
- Harmonicity (HNR): Voice quality / breathiness
- Intensity: Loudness measures (hypophonia detection)
- Formants: Articulatory precision

CRITICAL: Jitter, shimmer, and F0 are computed on VOICED FRAMES ONLY.
This is the standard approach in voice pathology research and is handled
automatically by Praat/Parselmouth.

Feature count: 31 features
- F0: 5 features
- Jitter: 5 features
- Shimmer: 6 features  
- Harmonicity: 3 features
- Intensity: 4 features
- Formants: 8 features
"""

import numpy as np
import parselmouth
from parselmouth.praat import call

from parkinsons_voice_classification.config import F0_MIN_HZ, F0_MAX_HZ


def extract_f0_features(sound: parselmouth.Sound) -> dict:
    """
    Extract fundamental frequency (F0) statistics.

    F0 variability is a key biomarker for PD - patients often show
    reduced pitch range and monotonic speech.

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        F0 features: mean, std, min, max, range.
    """
    pitch = call(sound, "To Pitch", 0.0, F0_MIN_HZ, F0_MAX_HZ)

    f0_mean = call(pitch, "Get mean", 0, 0, "Hertz")
    f0_std = call(pitch, "Get standard deviation", 0, 0, "Hertz")
    f0_min = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
    f0_max = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")

    # Handle undefined values (completely unvoiced)
    if np.isnan(f0_min) or np.isnan(f0_max):
        f0_range = np.nan
    else:
        f0_range = f0_max - f0_min

    return {
        "f0_mean": f0_mean,
        "f0_std": f0_std,
        "f0_min": f0_min,
        "f0_max": f0_max,
        "f0_range": f0_range,
    }


def extract_jitter_features(sound: parselmouth.Sound) -> dict:
    """
    Extract jitter (pitch perturbation) features.

    Jitter measures cycle-to-cycle variation in fundamental frequency,
    reflecting vocal fold instability common in PD due to rigidity
    and tremor affecting the laryngeal muscles.

    Computed on VOICED FRAMES ONLY (Praat default).

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        Jitter features: local, local_abs, rap, ppq5, ddp.
    """
    point_process = call(sound, "To PointProcess (periodic, cc)", F0_MIN_HZ, F0_MAX_HZ)

    # Local jitter (relative, %)
    jitter_local = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)

    # Local absolute jitter (seconds)
    jitter_local_abs = call(point_process, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)

    # RAP (Relative Average Perturbation)
    jitter_rap = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)

    # PPQ5 (5-point Period Perturbation Quotient)
    jitter_ppq5 = call(point_process, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)

    # DDP (average absolute difference of differences of periods)
    jitter_ddp = call(point_process, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)

    return {
        "jitter_local": jitter_local,
        "jitter_local_abs": jitter_local_abs,
        "jitter_rap": jitter_rap,
        "jitter_ppq5": jitter_ppq5,
        "jitter_ddp": jitter_ddp,
    }


def extract_shimmer_features(sound: parselmouth.Sound) -> dict:
    """
    Extract shimmer (amplitude perturbation) features.

    Shimmer measures cycle-to-cycle variation in amplitude,
    reflecting reduced laryngeal control and incomplete vocal fold
    closure in PD patients.

    Computed on VOICED FRAMES ONLY (Praat default).

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        Shimmer features: local, local_db, apq3, apq5, apq11, dda.
    """
    point_process = call(sound, "To PointProcess (periodic, cc)", F0_MIN_HZ, F0_MAX_HZ)

    # Local shimmer (relative, %)
    shimmer_local = call(
        [sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6
    )

    # Local shimmer in dB
    shimmer_local_db = call(
        [sound, point_process], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6
    )

    # APQ3 (3-point Amplitude Perturbation Quotient)
    shimmer_apq3 = call([sound, point_process], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    # APQ5 (5-point Amplitude Perturbation Quotient)
    shimmer_apq5 = call([sound, point_process], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    # APQ11 (11-point Amplitude Perturbation Quotient)
    shimmer_apq11 = call(
        [sound, point_process], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6
    )

    # DDA (average absolute difference of differences of amplitudes)
    shimmer_dda = call([sound, point_process], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return {
        "shimmer_local": shimmer_local,
        "shimmer_local_db": shimmer_local_db,
        "shimmer_apq3": shimmer_apq3,
        "shimmer_apq5": shimmer_apq5,
        "shimmer_apq11": shimmer_apq11,
        "shimmer_dda": shimmer_dda,
    }


def extract_harmonicity_features(sound: parselmouth.Sound) -> dict:
    """
    Extract harmonicity (HNR) features.

    Harmonics-to-Noise Ratio quantifies voice quality, specifically
    breathiness and hoarseness. PD patients often show reduced HNR
    due to incomplete glottal closure.

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        Harmonicity features: hnr_mean, nhr_mean, autocorr_harmonicity.
    """
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, F0_MIN_HZ, 0.1, 1.0)

    # Mean HNR (dB) - higher is better voice quality
    hnr_mean = call(harmonicity, "Get mean", 0, 0)

    # Convert to NHR (Noise-to-Harmonics Ratio) for compatibility
    # NHR = 10^(-HNR/10)
    if not np.isnan(hnr_mean):
        nhr_mean = 10 ** (-hnr_mean / 10)
    else:
        nhr_mean = np.nan

    # Standard deviation of harmonicity
    hnr_std = call(harmonicity, "Get standard deviation", 0, 0)

    return {
        "hnr_mean": hnr_mean,
        "nhr_mean": nhr_mean,
        "hnr_std": hnr_std,
    }


def extract_intensity_features(sound: parselmouth.Sound) -> dict:
    """
    Extract intensity (loudness) features.

    Hypophonia (reduced vocal loudness) is a cardinal symptom of PD.
    These features capture overall loudness and its variability.

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        Intensity features: mean, std, min, max.
    """
    intensity = call(sound, "To Intensity", F0_MIN_HZ, 0.0, "yes")

    intensity_mean = call(intensity, "Get mean", 0, 0, "dB")
    intensity_std = call(intensity, "Get standard deviation", 0, 0)
    intensity_min = call(intensity, "Get minimum", 0, 0, "Parabolic")
    intensity_max = call(intensity, "Get maximum", 0, 0, "Parabolic")

    return {
        "intensity_mean": intensity_mean,
        "intensity_std": intensity_std,
        "intensity_min": intensity_min,
        "intensity_max": intensity_max,
    }


def extract_formant_features(sound: parselmouth.Sound) -> dict:
    """
    Extract formant frequency features.

    Formants reflect articulatory configuration. PD patients often show
    reduced vowel space and articulatory undershoot, affecting formant
    frequencies and their variability.

    Parameters
    ----------
    sound : parselmouth.Sound
        Loaded audio as Parselmouth Sound object.

    Returns
    -------
    dict
        Formant features: f1-f4 mean and std.
    """
    formants = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)

    features = {}

    for i in range(1, 5):  # F1, F2, F3, F4
        # Get all formant values across time
        n_frames = call(formants, "Get number of frames")

        if n_frames > 0:
            formant_values = []
            for frame in range(1, n_frames + 1):
                value = call(
                    formants,
                    "Get value at time",
                    i,
                    call(formants, "Get time from frame number", frame),
                    "Hertz",
                    "Linear",
                )
                if not np.isnan(value):
                    formant_values.append(value)

            if formant_values:
                features[f"f{i}_mean"] = np.mean(formant_values)
                features[f"f{i}_std"] = np.std(formant_values)
            else:
                features[f"f{i}_mean"] = np.nan
                features[f"f{i}_std"] = np.nan
        else:
            features[f"f{i}_mean"] = np.nan
            features[f"f{i}_std"] = np.nan

    return features


def extract_prosodic_features(audio_path: str) -> dict:
    """
    Extract all prosodic features from an audio file.

    This is the main entry point for prosodic feature extraction.

    Parameters
    ----------
    audio_path : str
        Path to the WAV file.

    Returns
    -------
    dict
        Dictionary containing all 31 prosodic features.
    """
    sound = parselmouth.Sound(audio_path)

    features = {}

    # Extract each feature group
    features.update(extract_f0_features(sound))
    features.update(extract_jitter_features(sound))
    features.update(extract_shimmer_features(sound))
    features.update(extract_harmonicity_features(sound))
    features.update(extract_intensity_features(sound))
    features.update(extract_formant_features(sound))

    return features


def get_prosodic_feature_names() -> list[str]:
    """
    Return the ordered list of prosodic feature names.

    Returns
    -------
    list[str]
        List of 31 feature names in extraction order.
    """
    return [
        # F0 (5)
        "f0_mean",
        "f0_std",
        "f0_min",
        "f0_max",
        "f0_range",
        # Jitter (5)
        "jitter_local",
        "jitter_local_abs",
        "jitter_rap",
        "jitter_ppq5",
        "jitter_ddp",
        # Shimmer (6)
        "shimmer_local",
        "shimmer_local_db",
        "shimmer_apq3",
        "shimmer_apq5",
        "shimmer_apq11",
        "shimmer_dda",
        # Harmonicity (3)
        "hnr_mean",
        "nhr_mean",
        "hnr_std",
        # Intensity (4)
        "intensity_mean",
        "intensity_std",
        "intensity_min",
        "intensity_max",
        # Formants (8)
        "f1_mean",
        "f1_std",
        "f2_mean",
        "f2_std",
        "f3_mean",
        "f3_std",
        "f4_mean",
        "f4_std",
    ]
