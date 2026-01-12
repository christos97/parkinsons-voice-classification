"""
Main Feature Extraction Pipeline

Combines prosodic (Parselmouth) and spectral (librosa) feature extraction
into a unified pipeline for the MDVR-KCL dataset.

Total features: 88
- Prosodic: 31 features (F0, jitter, shimmer, HNR, intensity, formants)
- Spectral: 57 features (MFCCs, delta MFCCs, spectral stats, ZCR)

Usage:
    from thesis.features import extract_features_from_file, extract_features_from_manifest
    
    # Single file
    features = extract_features_from_file("path/to/audio.wav")
    
    # Full dataset
    df = extract_features_from_manifest(manifest_df, output_path="features.csv")
"""

import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

from parkinsons_voice_classification.features.prosodic import (
    extract_prosodic_features,
    get_prosodic_feature_names,
)
from parkinsons_voice_classification.features.spectral import (
    extract_spectral_features_all,
    get_spectral_feature_names,
)
from parkinsons_voice_classification.config import FEATURES_OUTPUT_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_feature_names() -> list[str]:
    """
    Return the complete ordered list of feature names.
    
    Returns
    -------
    list[str]
        List of 88 feature names (31 prosodic + 57 spectral).
    """
    return get_prosodic_feature_names() + get_spectral_feature_names()


def extract_features_from_file(
    audio_path: str,
    include_metadata: bool = False
) -> dict:
    """
    Extract all features from a single audio file.
    
    Parameters
    ----------
    audio_path : str
        Path to the WAV file.
    include_metadata : bool
        If True, include filepath in the output.
        
    Returns
    -------
    dict
        Dictionary containing all 88 features (and optionally metadata).
        
    Raises
    ------
    Exception
        If feature extraction fails for the file.
    """
    features = {}
    
    if include_metadata:
        features['filepath'] = str(audio_path)
    
    # Extract prosodic features (Parselmouth/Praat)
    prosodic = extract_prosodic_features(audio_path)
    features.update(prosodic)
    
    # Extract spectral features (librosa)
    spectral = extract_spectral_features_all(audio_path)
    features.update(spectral)
    
    return features


def extract_features_from_manifest(
    manifest: pd.DataFrame,
    output_path: Optional[str] = None,
    skip_existing: bool = False,
) -> pd.DataFrame:
    """
    Extract features from all files in a dataset manifest.
    
    Parameters
    ----------
    manifest : pd.DataFrame
        Dataset manifest with columns: filepath, filename, subject_id, label, task.
    output_path : str, optional
        If provided, save results to this CSV path.
    skip_existing : bool
        If True and output_path exists, skip extraction and load existing.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with metadata columns + 88 feature columns.
    """
    # Check for existing output
    if skip_existing and output_path and Path(output_path).exists():
        logger.info(f"Loading existing features from {output_path}")
        return pd.read_csv(output_path)
    
    # Ensure output directory exists
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Extracting features from {len(manifest)} files...")
    
    results = []
    failed_files = []
    
    for idx, row in tqdm(manifest.iterrows(), total=len(manifest), desc="Extracting features"):
        filepath = row['filepath']
        
        try:
            features = extract_features_from_file(filepath, include_metadata=False)
            
            # Add metadata from manifest
            record = {
                'filepath': filepath,
                'filename': row['filename'],
                'subject_id': row['subject_id'],
                'label': row['label'],
                'label_str': row['label_str'],
                'task': row['task'],
            }
            record.update(features)
            results.append(record)
            
        except Exception as e:
            logger.warning(f"Failed to extract features from {filepath}: {e}")
            failed_files.append((filepath, str(e)))
            
            # Create a row with NaN features
            record = {
                'filepath': filepath,
                'filename': row['filename'],
                'subject_id': row['subject_id'],
                'label': row['label'],
                'label_str': row['label_str'],
                'task': row['task'],
            }
            for feature_name in get_feature_names():
                record[feature_name] = np.nan
            results.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Log summary
    n_success = len(df) - len(failed_files)
    logger.info(f"Feature extraction complete: {n_success}/{len(manifest)} successful")
    
    if failed_files:
        logger.warning(f"Failed files ({len(failed_files)}):")
        for filepath, error in failed_files:
            logger.warning(f"  - {filepath}: {error}")
    
    # Save if output path provided
    if output_path:
        df.to_csv(output_path, index=False)
        logger.info(f"Features saved to {output_path}")
    
    return df


def verify_feature_count():
    """
    Verify the total feature count matches the design specification.
    
    Raises
    ------
    AssertionError
        If feature count doesn't match expected 88.
    """
    feature_names = get_feature_names()
    prosodic_names = get_prosodic_feature_names()
    spectral_names = get_spectral_feature_names()
    
    assert len(prosodic_names) == 31, f"Expected 31 prosodic features, got {len(prosodic_names)}"
    assert len(spectral_names) == 57, f"Expected 57 spectral features, got {len(spectral_names)}"
    assert len(feature_names) == 88, f"Expected 88 total features, got {len(feature_names)}"
    
    logger.info("Feature count verification passed: 88 features (31 prosodic + 57 spectral)")
