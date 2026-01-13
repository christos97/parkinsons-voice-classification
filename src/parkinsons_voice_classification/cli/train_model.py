"""
Train and Serialize Model for Inference

This CLI trains a single model on extracted features and saves it with metadata
for use by the inference API and Flask demo app.

Usage:
    pvc-train --task ReadText --model RandomForest --feature-set baseline

The trained model is saved to outputs/models/ with metadata for validation.
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from parkinsons_voice_classification.config import (
    MODELS_DIR,
    RANDOM_SEED,
    BASELINE_FEATURE_COUNT,
    EXTENDED_FEATURE_COUNT,
    get_features_output_dir,
)
from parkinsons_voice_classification.models.classifiers import get_models
from parkinsons_voice_classification.features.extraction_simple import get_all_feature_names

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_training_features(task: str, feature_set: str) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Load extracted features for training.

    Parameters
    ----------
    task : str
        Speech task: 'ReadText' or 'SpontaneousDialogue'.
    feature_set : str
        Feature set: 'baseline' or 'extended'.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, list[str]]
        X (features), y (labels), and feature column names.
    """
    # Determine feature file path
    features_dir = Path("outputs/features") / feature_set
    task_filename = f"features_{task.lower()}.csv"
    features_path = features_dir / task_filename

    if not features_path.exists():
        raise FileNotFoundError(
            f"Feature file not found: {features_path}\n"
            f"Run 'pvc-extract --task {task}' first to extract features."
        )

    logger.info(f"Loading features from {features_path}")
    df = pd.read_csv(features_path)

    # Separate features from metadata
    metadata_cols = ["subject_id", "label", "task", "filename"]
    feature_cols = [c for c in df.columns if c not in metadata_cols]

    X = np.array(df[feature_cols].values)
    y = np.array(df["label"].values)

    logger.info(f"Loaded {len(X)} samples with {X.shape[1]} features")
    return X, y, feature_cols


def train_and_save_model(
    task: str,
    model_name: str,
    feature_set: str,
    output_dir: Path | None = None,
) -> Path:
    """
    Train a model and save it with metadata.

    Parameters
    ----------
    task : str
        Speech task the model is trained on.
    model_name : str
        Name of the model (e.g., 'RandomForest').
    feature_set : str
        Feature set used ('baseline' or 'extended').
    output_dir : Path, optional
        Output directory for model. Defaults to MODELS_DIR.

    Returns
    -------
    Path
        Path to the saved model file.
    """
    if output_dir is None:
        output_dir = MODELS_DIR

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load features
    X, y, feature_names = load_training_features(task, feature_set)

    # Get the model pipeline
    models = get_models()
    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(models.keys())}")

    pipeline = models[model_name]

    # Train on full dataset (for inference, not evaluation)
    logger.info(f"Training {model_name} on {task} ({feature_set} features)...")
    pipeline.fit(X, y)

    # Prepare metadata for validation at inference time
    metadata = {
        "model_name": model_name,
        "task": task,
        "feature_set": feature_set,
        "feature_count": len(feature_names),
        "feature_names": feature_names,
        "training_samples": len(X),
        "class_distribution": {
            "HC": int(np.sum(y == 0)),
            "PD": int(np.sum(y == 1)),
        },
        "random_seed": RANDOM_SEED,
        "trained_at": datetime.now().isoformat(),
        "version": "1.0.0",
    }

    # Save model and metadata together
    model_filename = f"{model_name}_{task}_{feature_set}.joblib"
    model_path = output_dir / model_filename

    artifact = {
        "pipeline": pipeline,
        "metadata": metadata,
    }

    joblib.dump(artifact, model_path)
    logger.info(f"Model saved to {model_path}")

    # Also save metadata as JSON for inspection
    metadata_path = output_dir / f"{model_name}_{task}_{feature_set}_metadata.json"
    with open(metadata_path, "w") as f:
        # Convert feature_names to list for JSON serialization
        json.dump(metadata, f, indent=2, default=str)
    logger.info(f"Metadata saved to {metadata_path}")

    return model_path


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Train and save a model for inference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--task",
        type=str,
        default="ReadText",
        choices=["ReadText", "SpontaneousDialogue"],
        help="Speech task to train on (default: ReadText)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="RandomForest",
        choices=["LogisticRegression", "SVM_RBF", "RandomForest"],
        help="Model to train (default: RandomForest)",
    )
    parser.add_argument(
        "--feature-set",
        type=str,
        default="baseline",
        choices=["baseline", "extended"],
        help="Feature set to use (default: baseline)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: outputs/models/)",
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else None

    model_path = train_and_save_model(
        task=args.task,
        model_name=args.model,
        feature_set=args.feature_set,
        output_dir=output_dir,
    )

    print(f"\n✓ Model trained and saved to: {model_path}")
    print(f"  Task: {args.task}")
    print(f"  Model: {args.model}")
    print(f"  Feature set: {args.feature_set}")


if __name__ == "__main__":
    main()
