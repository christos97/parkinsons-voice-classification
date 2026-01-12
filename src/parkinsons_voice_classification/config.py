"""
Global configuration and constants for the thesis project.

This module contains all locked parameters for reproducibility.
"""

from pathlib import Path

# =============================================================================
# RANDOM SEED (locked for reproducibility)
# =============================================================================
RANDOM_SEED = 42

# =============================================================================
# PROJECT PATHS
# =============================================================================
# config.py is at: src/parkinsons_voice_classification/config.py
# PROJECT_ROOT should be: /home/xsrm/repos/parkinsons-voice-classification
PROJECT_ROOT = Path(
    __file__
).parent.parent.parent  # src/parkinsons_voice_classification -> src -> root
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Dataset A paths
MDVR_KCL_DIR = ASSETS_DIR / "DATASET_MDVR_KCL"
MDVR_KCL_READTEXT = MDVR_KCL_DIR / "ReadText"
MDVR_KCL_SPONTANEOUS = MDVR_KCL_DIR / "SpontaneousDialogue"

# Dataset B path
PD_SPEECH_FEATURES_CSV = ASSETS_DIR / "PD_SPEECH_FEATURES.csv"

# =============================================================================
# FEATURE SET CONFIGURATION
# =============================================================================
# When True, use extended 78-feature set (baseline + MFCC std + delta-delta + spectral shape)
# When False, use baseline 47-feature set
# Features are saved to outputs/features/extended/ or outputs/features/baseline/
USE_EXTENDED_FEATURES = False

# Output paths (dynamic based on feature set)
_FEATURES_BASE_DIR = OUTPUTS_DIR / "features"


def get_features_output_dir() -> Path:
    """Get features output directory based on USE_EXTENDED_FEATURES flag."""
    subdir = "extended" if USE_EXTENDED_FEATURES else "baseline"
    return _FEATURES_BASE_DIR / subdir


# For backward compatibility (but prefer get_features_output_dir())
FEATURES_OUTPUT_DIR = _FEATURES_BASE_DIR

# =============================================================================
# FEATURE EXTRACTION PARAMETERS (locked)
# =============================================================================

# F0 (Fundamental Frequency) range in Hz
# Covers both male (~85-180 Hz) and female (~165-255 Hz) voices
# Extended range for pathological voices
F0_MIN_HZ = 75
F0_MAX_HZ = 500

# MFCC parameters
MFCC_N_COEFFS = 13  # Number of MFCC coefficients (0-12)
MFCC_N_FFT = 2048  # FFT window size
MFCC_HOP_LENGTH = 512  # Hop length (samples)
MFCC_WIN_LENGTH = 2048  # Window length (samples)
MFCC_N_MELS = 128  # Number of mel bands

# At 22050 Hz sample rate:
# - Window length: 2048/22050 ≈ 93ms (captures multiple pitch periods)
# - Hop length: 512/22050 ≈ 23ms (standard overlap)

# Target sample rate for all audio
TARGET_SAMPLE_RATE = 22050

# =============================================================================
# FEATURE COUNTS (for documentation)
# =============================================================================
# Baseline: 47 features (21 prosodic + 26 spectral)
# Extended: 78 features (21 prosodic + 57 spectral)
#   Added: MFCC std (13) + delta-delta MFCC mean (13) + spectral shape (5)
BASELINE_FEATURE_COUNT = 47
EXTENDED_FEATURE_COUNT = 78

# =============================================================================
# LABEL ENCODING
# =============================================================================

# Dataset A (MDVR-KCL) - derived from filenames
LABEL_HC = 0
LABEL_PD = 1

LABEL_MAP = {
    "hc": LABEL_HC,
    "pd": LABEL_PD,
}

LABEL_NAMES = {
    LABEL_HC: "HC",
    LABEL_PD: "PD",
}

# =============================================================================
# CROSS-VALIDATION PARAMETERS
# =============================================================================
N_FOLDS = 5

# =============================================================================
# CLASS IMBALANCE HANDLING
# =============================================================================
# When True, all classifiers use class_weight="balanced" to mitigate
# class imbalance. Results are saved to outputs/results/weighted/
# When False (baseline), no class weighting is applied.
# Results are saved to outputs/results/baseline/
USE_CLASS_WEIGHT_BALANCED = False
