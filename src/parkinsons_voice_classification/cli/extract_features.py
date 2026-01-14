#!/usr/bin/env python
"""
Feature Extraction Script for MDVR-KCL Dataset (Simplified)

Extracts 47 acoustic features per recording:
- 21 prosodic (parselmouth/Praat)
- 26 spectral (librosa MFCCs)

Usage:
    pvc-extract
    pvc-extract --task ReadText
    pvc-extract --task SpontaneousDialogue

Output:
    outputs/features/features_readtext.csv (37 rows × 51 columns)
    outputs/features/features_spontaneousdialogue.csv (36 rows × 51 columns)
"""

import argparse
import os

from parkinsons_voice_classification.features.extraction_simple import (
    run_extraction,
    get_all_feature_names,
)
from parkinsons_voice_classification.data.mdvr_kcl import load_dataset_manifest
from parkinsons_voice_classification.config import (
    USE_EXTENDED_FEATURES,
    get_features_output_dir,
    BASELINE_FEATURE_COUNT,
    EXTENDED_FEATURE_COUNT,
)

# Default number of parallel workers
_CPU_COUNT = os.cpu_count() or 4
_DEFAULT_JOBS = min(15, max(1, _CPU_COUNT - 1))


def main():
    parser = argparse.ArgumentParser(description="Extract acoustic features from MDVR-KCL dataset")
    parser.add_argument(
        "--task",
        type=str,
        choices=["ReadText", "SpontaneousDialogue", "all"],
        default="all",
        help="Speech task to process (default: all)",
    )
    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=_DEFAULT_JOBS,
        help=f"Number of parallel workers (default: {_DEFAULT_JOBS})",
    )

    args = parser.parse_args()

    # Show feature configuration
    feature_names = get_all_feature_names()
    feature_mode = "EXTENDED" if USE_EXTENDED_FEATURES else "BASELINE"
    expected_count = EXTENDED_FEATURE_COUNT if USE_EXTENDED_FEATURES else BASELINE_FEATURE_COUNT
    output_dir = get_features_output_dir()

    print(f"Feature set: {feature_mode} ({len(feature_names)} features)")
    if USE_EXTENDED_FEATURES:
        print(f"  - Prosodic: 21 (F0, jitter, shimmer, HNR, intensity, formants)")
        print(f"  - Spectral: 57 (MFCC mean/std + delta/delta2 + spectral shape)")
    else:
        print(f"  - Prosodic: 21 (F0, jitter, shimmer, HNR, intensity, formants)")
        print(f"  - Spectral: 26 (MFCC 0-12 mean + delta MFCC 0-12 mean)")
    print(f"Output directory: {output_dir}")
    print()

    # Determine tasks to process
    if args.task == "all":
        tasks = ["ReadText", "SpontaneousDialogue"]
    else:
        tasks = [args.task]

    for task in tasks:
        print(f"\n{'='*60}")
        print(f"Processing task: {task}")
        print(f"{'='*60}")

        # Load manifest for summary
        manifest = load_dataset_manifest(task)
        print(f"Found {len(manifest)} recordings")
        print(f"  - HC: {(manifest['label'] == 0).sum()}")
        print(f"  - PD: {(manifest['label'] == 1).sum()}")
        print(f"  - Subjects: {manifest['subject_id'].nunique()}")

        # Extract features
        print(f"\nExtracting features with {args.jobs} parallel workers...")
        df = run_extraction(task, jobs=args.jobs)

        # Summary
        meta_cols = ["subject_id", "label", "task", "filename"]
        feature_cols = [c for c in df.columns if c not in meta_cols]

        print(f"\nFeature matrix shape: {df.shape}")
        print(f"  - Rows (recordings): {len(df)}")
        print(f"  - Columns: {len(df.columns)} (4 metadata + {len(feature_cols)} features)")

        # Check for NaN features
        nan_counts = df[feature_cols].isna().sum()
        if nan_counts.sum() > 0:
            print(f"\nWarning: {nan_counts.sum()} NaN values in features")
            cols_with_nan = nan_counts[nan_counts > 0]
            print("Features with NaN:")
            for col, count in cols_with_nan.items():
                print(f"  - {col}: {count} NaN values")

    print(f"\n{'='*60}")
    print("Feature extraction complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
