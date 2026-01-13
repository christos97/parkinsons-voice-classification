"""
Inference API Module

Provides a stable, abstract interface for running predictions on WAV files.
This module is the ONLY entry point that external consumers (Flask app, CLI)
should use for inference.

Design principles:
- Single public function: run_inference()
- Config-driven model and feature selection
- No implementation details exposed to callers
- Metadata validation to catch pipeline mismatches

Usage:
    from parkinsons_voice_classification.inference import run_inference

    result = run_inference("/path/to/audio.wav")
    print(result.prediction)  # "PD" or "HC"
    print(result.probability)  # 0.0 to 1.0
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import logging

import joblib
import numpy as np

from parkinsons_voice_classification.config import (
    INFERENCE_MODEL_PATH,
    INFERENCE_FEATURE_SET,
    INFERENCE_MODEL_NAME,
    INFERENCE_TASK,
    LABEL_NAMES,
    BASELINE_FEATURE_COUNT,
    EXTENDED_FEATURE_COUNT,
)
from parkinsons_voice_classification.features.extraction_simple import (
    extract_all_features,
    get_all_feature_names,
)

logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    """
    Result of running inference on a single audio file.

    Attributes
    ----------
    prediction : str
        Predicted class label ("PD" or "HC").
    probability : float
        Probability of the predicted class (0.0 to 1.0).
    probability_pd : float
        Probability of Parkinson's Disease specifically.
    probability_hc : float
        Probability of Healthy Control specifically.
    model_name : str
        Name of the model used (e.g., "RandomForest").
    feature_set : str
        Feature set used ("baseline" or "extended").
    task : str
        Speech task the model was trained on.
    feature_count : int
        Number of features extracted.
    """

    prediction: str
    probability: float
    probability_pd: float
    probability_hc: float
    model_name: str
    feature_set: str
    task: str
    feature_count: int


class InferenceError(Exception):
    """Raised when inference fails."""

    pass


class ModelNotFoundError(InferenceError):
    """Raised when the inference model is not found."""

    pass


class FeatureMismatchError(InferenceError):
    """Raised when extracted features don't match model expectations."""

    pass


# Module-level cache for loaded model
_cached_model = None
_cached_model_path = None


def _load_model(model_path: Optional[Path] = None) -> tuple:
    """
    Load the inference model with caching.

    Parameters
    ----------
    model_path : Path, optional
        Path to model file. Defaults to INFERENCE_MODEL_PATH.

    Returns
    -------
    tuple
        (pipeline, metadata) from the saved artifact.

    Raises
    ------
    ModelNotFoundError
        If the model file does not exist.
    """
    global _cached_model, _cached_model_path

    if model_path is None:
        model_path = INFERENCE_MODEL_PATH

    # Return cached model if path matches
    if _cached_model is not None and _cached_model_path == model_path:
        return _cached_model

    if not model_path.exists():
        raise ModelNotFoundError(
            f"Inference model not found at {model_path}\n"
            f"Run 'pvc-train --task {INFERENCE_TASK} --model {INFERENCE_MODEL_NAME} "
            f"--feature-set {INFERENCE_FEATURE_SET}' to train the model."
        )

    logger.info(f"Loading model from {model_path}")
    artifact = joblib.load(model_path)

    pipeline = artifact["pipeline"]
    metadata = artifact["metadata"]

    # Cache for future calls
    _cached_model = (pipeline, metadata)
    _cached_model_path = model_path

    return pipeline, metadata


def _validate_features(features: dict, metadata: dict) -> None:
    """
    Validate extracted features against model metadata.

    Parameters
    ----------
    features : dict
        Extracted features from audio file.
    metadata : dict
        Model metadata with expected feature information.

    Raises
    ------
    FeatureMismatchError
        If feature count or names don't match expectations.
    """
    expected_count = metadata.get("feature_count", 0)
    actual_count = len(features)

    if actual_count != expected_count:
        raise FeatureMismatchError(
            f"Feature count mismatch: model expects {expected_count} features, "
            f"but extraction produced {actual_count}. "
            f"Check that USE_EXTENDED_FEATURES config matches the trained model."
        )

    # Optionally validate feature names if strict validation is needed
    expected_names = metadata.get("feature_names", [])
    if expected_names:
        actual_names = list(features.keys())
        if actual_names != expected_names:
            missing = set(expected_names) - set(actual_names)
            extra = set(actual_names) - set(expected_names)
            raise FeatureMismatchError(
                f"Feature name mismatch. Missing: {missing}, Extra: {extra}"
            )


def run_inference(
    wav_path: str,
    task: str = "ReadText",
    model_path: Optional[Path] = None,
) -> InferenceResult:
    """
    Run inference on a single WAV file.

    This is the ONLY public inference entry point. It abstracts away:
    - Feature extraction implementation
    - Model loading and caching
    - Feature validation
    - Probability computation

    Parameters
    ----------
    wav_path : str
        Path to the WAV audio file to analyze.
    task : str, optional
        Speech task context (for documentation, not used in inference).
        Default: "ReadText".
    model_path : Path, optional
        Override path to model file. Defaults to config-driven path.

    Returns
    -------
    InferenceResult
        Dataclass containing prediction, probabilities, and metadata.

    Raises
    ------
    ModelNotFoundError
        If the inference model is not found.
    FeatureMismatchError
        If extracted features don't match model expectations.
    InferenceError
        For other inference failures (e.g., audio loading, feature extraction).

    Examples
    --------
    >>> result = run_inference("/path/to/recording.wav")
    >>> print(f"Prediction: {result.prediction}")
    >>> print(f"Confidence: {result.probability:.2%}")
    """
    # Load model (cached after first call)
    pipeline, metadata = _load_model(model_path)

    # Extract features from audio
    try:
        features = extract_all_features(wav_path)
    except Exception as e:
        raise InferenceError(f"Feature extraction failed: {e}") from e

    # Validate features match model expectations
    _validate_features(features, metadata)

    # Prepare feature vector in correct order
    feature_names = metadata.get("feature_names", list(features.keys()))
    X = np.array([[features[name] for name in feature_names]])

    # Run prediction
    prediction_label = pipeline.predict(X)[0]
    probabilities = pipeline.predict_proba(X)[0]

    # Map to class names
    prediction_str = LABEL_NAMES[prediction_label]
    prob_hc = float(probabilities[0])
    prob_pd = float(probabilities[1])

    # Probability of the predicted class
    prediction_prob = prob_pd if prediction_label == 1 else prob_hc

    return InferenceResult(
        prediction=prediction_str,
        probability=prediction_prob,
        probability_pd=prob_pd,
        probability_hc=prob_hc,
        model_name=metadata.get("model_name", "Unknown"),
        feature_set=metadata.get("feature_set", "Unknown"),
        task=metadata.get("task", task),
        feature_count=len(features),
    )


def get_model_info(model_path: Optional[Path] = None) -> dict:
    """
    Get information about the loaded inference model.

    Useful for displaying model metadata in the UI without running inference.

    Parameters
    ----------
    model_path : Path, optional
        Override path to model file.

    Returns
    -------
    dict
        Model metadata including name, task, feature set, and training info.
    """
    _, metadata = _load_model(model_path)
    return metadata
