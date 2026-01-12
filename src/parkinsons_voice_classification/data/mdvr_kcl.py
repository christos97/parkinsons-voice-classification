"""
MDVR-KCL Dataset Handler

This module provides utilities for loading and parsing the MDVR-KCL dataset.
The dataset contains voice recordings from Parkinson's Disease (PD) patients
and Healthy Controls (HC) across two speech tasks: ReadText and SpontaneousDialogue.

Key features:
- Filename parsing with edge case handling (ID22hc malformed filename)
- Subject registry building for grouped cross-validation
- Per-task file discovery

Reference:
- Dataset location: assets/DATASET_MDVR_KCL/
- Filename pattern: IDxx_[class]_[num1]_[num2]_[num3].wav
"""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from parkinsons_voice_classification.config import (
    MDVR_KCL_DIR,
    MDVR_KCL_READTEXT,
    MDVR_KCL_SPONTANEOUS,
    LABEL_MAP,
)


@dataclass
class RecordingInfo:
    """Information about a single recording."""
    filepath: Path
    filename: str
    subject_id: str
    label_str: str  # 'hc' or 'pd'
    label: int      # 0 or 1
    task: str       # 'ReadText' or 'SpontaneousDialogue'
    
    
def parse_mdvr_filename(filename: str) -> dict:
    """
    Parse MDVR-KCL filename to extract subject ID and class.
    
    Handles both standard and edge case formats:
    - Standard: ID02_pd_2_0_0.wav
    - Edge case: ID22hc_0_0_0.wav (missing underscore)
    
    Parameters
    ----------
    filename : str
        The WAV filename to parse.
        
    Returns
    -------
    dict
        Dictionary with 'subject_id' and 'class' keys.
        
    Raises
    ------
    ValueError
        If the filename cannot be parsed.
        
    Examples
    --------
    >>> parse_mdvr_filename("ID02_pd_2_0_0.wav")
    {'subject_id': 'ID02', 'class': 'pd'}
    
    >>> parse_mdvr_filename("ID22hc_0_0_0.wav")
    {'subject_id': 'ID22', 'class': 'hc'}
    """
    # Remove .wav extension
    name = filename.replace('.wav', '').replace('.WAV', '')
    
    # Try standard pattern first: IDxx_class_...
    standard_match = re.match(r'^(ID\d+)_(hc|pd)_', name, re.IGNORECASE)
    if standard_match:
        return {
            'subject_id': standard_match.group(1).upper(),
            'class': standard_match.group(2).lower()
        }
    
    # Try edge case pattern: IDxxclass_... (missing underscore)
    edge_match = re.match(r'^(ID\d+)(hc|pd)_', name, re.IGNORECASE)
    if edge_match:
        return {
            'subject_id': edge_match.group(1).upper(),
            'class': edge_match.group(2).lower()
        }
    
    raise ValueError(f"Cannot parse filename: {filename}")


def discover_recordings(
    task: str,
    base_dir: Optional[Path] = None
) -> list[RecordingInfo]:
    """
    Discover all recordings for a given speech task.
    
    Parameters
    ----------
    task : str
        Speech task: 'ReadText' or 'SpontaneousDialogue'.
    base_dir : Path, optional
        Base directory of MDVR-KCL dataset. Defaults to config path.
        
    Returns
    -------
    list[RecordingInfo]
        List of RecordingInfo objects for all discovered recordings.
        
    Raises
    ------
    ValueError
        If task is not 'ReadText' or 'SpontaneousDialogue'.
    """
    if base_dir is None:
        base_dir = MDVR_KCL_DIR
        
    if task == "ReadText":
        task_dir = base_dir / "ReadText"
    elif task == "SpontaneousDialogue":
        task_dir = base_dir / "SpontaneousDialogue"
    else:
        raise ValueError(f"Unknown task: {task}. Must be 'ReadText' or 'SpontaneousDialogue'.")
    
    recordings = []
    
    for class_dir in ["HC", "PD"]:
        class_path = task_dir / class_dir
        if not class_path.exists():
            continue
            
        for wav_file in class_path.glob("*.wav"):
            try:
                parsed = parse_mdvr_filename(wav_file.name)
                recordings.append(RecordingInfo(
                    filepath=wav_file,
                    filename=wav_file.name,
                    subject_id=parsed['subject_id'],
                    label_str=parsed['class'],
                    label=LABEL_MAP[parsed['class']],
                    task=task,
                ))
            except ValueError as e:
                print(f"Warning: Skipping file {wav_file.name}: {e}")
                
    return recordings


def build_subject_registry(
    recordings: list[RecordingInfo]
) -> dict[str, dict]:
    """
    Build a registry mapping subject IDs to their recordings and metadata.
    
    Parameters
    ----------
    recordings : list[RecordingInfo]
        List of recording info objects.
        
    Returns
    -------
    dict
        Dictionary mapping subject_id to {label, label_str, recordings: [...]}.
    """
    registry = {}
    
    for rec in recordings:
        if rec.subject_id not in registry:
            registry[rec.subject_id] = {
                'label': rec.label,
                'label_str': rec.label_str,
                'recordings': []
            }
        registry[rec.subject_id]['recordings'].append(rec)
        
    return registry


def load_dataset_manifest(
    task: str,
    base_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Load dataset manifest as a DataFrame.
    
    Parameters
    ----------
    task : str
        Speech task: 'ReadText' or 'SpontaneousDialogue'.
    base_dir : Path, optional
        Base directory of MDVR-KCL dataset.
        
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: filepath, filename, subject_id, label_str, label, task.
    """
    recordings = discover_recordings(task, base_dir)
    
    data = [
        {
            'filepath': str(rec.filepath),
            'filename': rec.filename,
            'subject_id': rec.subject_id,
            'label_str': rec.label_str,
            'label': rec.label,
            'task': rec.task,
        }
        for rec in recordings
    ]
    
    return pd.DataFrame(data)


def get_subject_labels(manifest: pd.DataFrame) -> tuple[list[str], list[int]]:
    """
    Extract unique subjects and their labels for cross-validation.
    
    Parameters
    ----------
    manifest : pd.DataFrame
        Dataset manifest from load_dataset_manifest().
        
    Returns
    -------
    tuple[list[str], list[int]]
        (subject_ids, labels) - Lists of unique subjects and their labels.
    """
    subject_labels = manifest.groupby('subject_id')['label'].first()
    return list(subject_labels.index), list(subject_labels.values)


# Alias for simplified API
build_manifest = load_dataset_manifest


def load_features(task: str) -> tuple:
    """
    Load extracted features for a speech task.
    
    Parameters
    ----------
    task : str
        'ReadText' or 'SpontaneousDialogue'
        
    Returns
    -------
    X : np.ndarray
        Feature matrix
    y : np.ndarray  
        Label array (0=HC, 1=PD)
    groups : np.ndarray
        Subject IDs for grouped CV
    """
    import numpy as np
    from parkinsons_voice_classification.config import FEATURES_OUTPUT_DIR
    
    csv_path = FEATURES_OUTPUT_DIR / f"features_{task.lower()}.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Features not found at {csv_path}. "
            f"Run feature extraction first."
        )
    
    df = pd.read_csv(csv_path)
    
    # Metadata columns
    meta_cols = ['subject_id', 'label', 'task', 'filename']
    feature_cols = [c for c in df.columns if c not in meta_cols]
    
    X = df[feature_cols].values
    y = df['label'].values
    groups = df['subject_id'].values
    
    return X, y, groups
