"""
Feature Metadata for Display

Static definitions for feature names, descriptions, and units.
Used by the Flask app to render interpretable feature tables.

Note: Descriptions are educational and non-clinical.
"""

# Features to display in the result page (curated subset for interpretability)
DISPLAY_FEATURES = [
    "f0_mean",
    "f0_max",
    "hnr_mean",
    "jitter_local",
    "shimmer_apq11",
    "intensity_mean",
    "mfcc_0_mean",
    "mfcc_5_mean",
]

# Human-readable metadata for each feature
FEATURE_METADATA = {
    # Prosodic: F0 (pitch)
    "f0_mean": {
        "description": "Average fundamental frequency (pitch)",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f0_std": {
        "description": "Pitch variability",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f0_min": {
        "description": "Minimum pitch",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f0_max": {
        "description": "Maximum pitch",
        "unit": "Hz",
        "category": "prosodic",
    },
    # Prosodic: Jitter (pitch perturbation)
    "jitter_local": {
        "description": "Cycle-to-cycle pitch variation",
        "unit": "%",
        "category": "prosodic",
    },
    "jitter_rap": {
        "description": "Relative average perturbation",
        "unit": "%",
        "category": "prosodic",
    },
    "jitter_ppq5": {
        "description": "5-point pitch perturbation quotient",
        "unit": "%",
        "category": "prosodic",
    },
    # Prosodic: Shimmer (amplitude perturbation)
    "shimmer_local": {
        "description": "Cycle-to-cycle amplitude variation",
        "unit": "%",
        "category": "prosodic",
    },
    "shimmer_apq3": {
        "description": "3-point amplitude perturbation",
        "unit": "%",
        "category": "prosodic",
    },
    "shimmer_apq11": {
        "description": "11-point amplitude perturbation",
        "unit": "%",
        "category": "prosodic",
    },
    # Prosodic: Harmonicity
    "hnr_mean": {
        "description": "Harmonic-to-noise ratio (voice clarity)",
        "unit": "dB",
        "category": "prosodic",
    },
    "autocorr_harmonicity": {
        "description": "Autocorrelation harmonicity",
        "unit": "",
        "category": "prosodic",
    },
    # Prosodic: Intensity
    "intensity_mean": {
        "description": "Average loudness",
        "unit": "dB",
        "category": "prosodic",
    },
    "intensity_min": {
        "description": "Minimum loudness",
        "unit": "dB",
        "category": "prosodic",
    },
    "intensity_max": {
        "description": "Maximum loudness",
        "unit": "dB",
        "category": "prosodic",
    },
    # Prosodic: Formants
    "f1_mean": {
        "description": "First formant frequency",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f1_std": {
        "description": "First formant variability",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f2_mean": {
        "description": "Second formant frequency",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f2_std": {
        "description": "Second formant variability",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f3_mean": {
        "description": "Third formant frequency",
        "unit": "Hz",
        "category": "prosodic",
    },
    "f3_std": {
        "description": "Third formant variability",
        "unit": "Hz",
        "category": "prosodic",
    },
    # Spectral: MFCCs (baseline)
    **{
        f"mfcc_{i}_mean": {
            "description": f"MFCC coefficient {i} (spectral shape)",
            "unit": "",
            "category": "spectral",
        }
        for i in range(13)
    },
    # Spectral: Delta MFCCs (baseline)
    **{
        f"delta_mfcc_{i}_mean": {
            "description": f"MFCC {i} rate of change",
            "unit": "",
            "category": "spectral",
        }
        for i in range(13)
    },
    # Extended: MFCC std
    **{
        f"mfcc_{i}_std": {
            "description": f"MFCC {i} variability",
            "unit": "",
            "category": "spectral",
        }
        for i in range(13)
    },
    # Extended: Delta-delta MFCCs
    **{
        f"delta_delta_mfcc_{i}_mean": {
            "description": f"MFCC {i} acceleration",
            "unit": "",
            "category": "spectral",
        }
        for i in range(13)
    },
    # Extended: Spectral shape features
    "spectral_centroid": {
        "description": "Spectral center of mass",
        "unit": "Hz",
        "category": "spectral",
    },
    "spectral_bandwidth": {
        "description": "Spectral spread",
        "unit": "Hz",
        "category": "spectral",
    },
    "spectral_rolloff": {
        "description": "Frequency below which 85% of energy lies",
        "unit": "Hz",
        "category": "spectral",
    },
    "spectral_flatness": {
        "description": "Spectral tonality measure",
        "unit": "",
        "category": "spectral",
    },
    "zero_crossing_rate": {
        "description": "Rate of signal sign changes",
        "unit": "",
        "category": "spectral",
    },
}


def get_feature_display_info(feature_name: str) -> dict:
    """
    Get display information for a feature.

    Returns default values if feature is not in metadata.
    """
    default = {
        "description": feature_name.replace("_", " ").title(),
        "unit": "",
        "category": "other",
    }
    return FEATURE_METADATA.get(feature_name, default)


def format_feature_value(value: float, unit: str) -> str:
    """Format a feature value with appropriate precision."""
    if abs(value) >= 100:
        return f"{value:.1f}"
    elif abs(value) >= 1:
        return f"{value:.2f}"
    else:
        return f"{value:.4f}"
