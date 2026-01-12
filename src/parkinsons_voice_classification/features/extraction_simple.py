"""
Simplified Feature Extraction Pipeline

Combines prosodic (21 features) and spectral (26 features) extraction.
Total: 47 features per WAV file.

Usage:
    from thesis.features.extraction_simple import extract_all_features, run_extraction
    
    # Single file
    features = extract_all_features("path/to/audio.wav")
    
    # Full dataset
    run_extraction("ReadText", "outputs/features/features_readtext.csv")
"""

import logging
import os
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

from parkinsons_voice_classification.features.prosodic_simple import (
    extract_prosodic_features,
    get_prosodic_feature_names,
)
from parkinsons_voice_classification.features.spectral_simple import (
    extract_spectral_features,
    get_spectral_feature_names,
)
from parkinsons_voice_classification.data.mdvr_kcl import build_manifest
from parkinsons_voice_classification.config import get_features_output_dir, USE_EXTENDED_FEATURES

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_all_feature_names() -> list[str]:
    """Return complete ordered list of feature names (47 features)."""
    return get_prosodic_feature_names() + get_spectral_feature_names()


def extract_all_features(audio_path: str) -> dict:
    """
    Extract all features from a single audio file.

    Parameters
    ----------
    audio_path : str
        Path to WAV file.

    Returns
    -------
    dict
        Dictionary with 47 features.
    """
    features = {}

    # Prosodic features (21)
    prosodic = extract_prosodic_features(audio_path)
    features.update(prosodic)

    # Spectral features (26)
    spectral = extract_spectral_features(audio_path)
    features.update(spectral)

    return features


def _extract_single_file(row: dict) -> dict | None:
    """
    Worker function to extract features from a single audio file.

    Parameters
    ----------
    row : dict
        Manifest row with 'filepath', 'subject_id', 'label', 'task', 'filename'.

    Returns
    -------
    dict or None
        Feature dictionary with metadata, or None if extraction failed.
    """
    try:
        features = extract_all_features(str(row["filepath"]))
        features["subject_id"] = row["subject_id"]
        features["label"] = row["label"]
        features["task"] = row["task"]
        features["filename"] = row["filename"]
        return features
    except Exception as e:
        logger.warning(f"Failed to extract features from {row['filename']}: {e}")
        return None


def run_extraction(
    task: str, output_path: str | None = None, jobs: int | None = None
) -> pd.DataFrame:
    """
    Run feature extraction for a speech task.

    Parameters
    ----------
    task : str
        'ReadText' or 'SpontaneousDialogue'
    output_path : str, optional
        Path to save CSV. If None, saves to default location.
    jobs : int, optional
        Number of parallel workers. Defaults to min(8, cpu_count - 1).

    Returns
    -------
    pd.DataFrame
        DataFrame with features and metadata.
    """
    # Determine number of parallel workers
    if jobs is None:
        cpu_count = os.cpu_count() or 4
        jobs = min(8, max(1, cpu_count - 1))
    logger.info(f"Using {jobs} parallel workers")

    # Build manifest
    manifest = build_manifest(task)
    logger.info(f"Found {len(manifest)} recordings for task: {task}")

    # Convert manifest rows to list of dicts for parallel processing
    manifest_rows = manifest.to_dict("records")

    # Extract features in parallel with progress bar
    results = Parallel(n_jobs=jobs, backend="loky")(
        delayed(_extract_single_file)(row) for row in tqdm(manifest_rows, desc=f"Extracting {task}")
    )

    # Filter out failed extractions (None values)
    rows = [r for r in results if r is not None]

    if len(rows) < len(manifest_rows):
        logger.warning(f"Failed to extract {len(manifest_rows) - len(rows)} files")

    # Create DataFrame and sort deterministically by filename for reproducibility
    df = pd.DataFrame(rows)
    df = df.sort_values("filename").reset_index(drop=True)

    # Reorder columns: metadata first, then features
    meta_cols = ["subject_id", "label", "task", "filename"]
    feature_cols = get_all_feature_names()
    df = df[meta_cols + feature_cols]

    # Save to CSV
    if output_path is None:
        features_dir = get_features_output_dir()
        features_dir.mkdir(parents=True, exist_ok=True)
        output_path_obj = features_dir / f"features_{task.lower()}.csv"
    else:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path_obj, index=False)
    logger.info(f"Saved features to: {output_path_obj}")
    logger.info(f"Shape: {df.shape} (rows × columns)")

    return df


if __name__ == "__main__":
    # Extract features for both tasks
    run_extraction("ReadText")
    run_extraction("SpontaneousDialogue")
