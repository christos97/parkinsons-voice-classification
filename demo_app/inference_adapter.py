"""
Inference Adapter for Flask Demo App

Thin wrapper around the core inference module that enriches results
with display-friendly feature information and optional importance data.

This adapter:
- Calls existing feature extraction (no duplication)
- Calls existing model inference (no duplication)
- Formats data for Jinja2 templates

Data flow:
    WAV file → extract_all_features() → run_inference() → enrich_result()
"""

import logging
from pathlib import Path
from typing import Optional
import csv

from parkinsons_voice_classification.inference import (
    run_inference as core_run_inference,
    get_model_info,
    InferenceResult,
    InferenceError,
    ModelNotFoundError,
)
from parkinsons_voice_classification.features.extraction_simple import (
    extract_all_features,
)

from feature_metadata import (
    DISPLAY_FEATURES,
    get_feature_display_info,
    format_feature_value,
)

logger = logging.getLogger(__name__)

# Path to pre-computed feature importance (relative to project root)
IMPORTANCE_CSV_PATH = Path(__file__).parent.parent / "outputs/results/baseline/importance_readtext.csv"


def run_inference_with_features(
    wav_path: str,
    task: str = "ReadText",
    model_path: Optional[Path] = None,
) -> dict:
    """
    Run inference and return enriched result for Flask templates.

    Parameters
    ----------
    wav_path : str
        Path to WAV file to analyze.
    task : str
        Speech task (currently only ReadText supported).
    model_path : Path, optional
        Override model path.

    Returns
    -------
    dict
        Enriched result containing:
        - prediction: Core inference result
        - features: List of displayed features with values
        - importance: Top important features for this model (if available)
    """
    # Step 1: Extract features (we need the raw values for display)
    features_dict = extract_all_features(wav_path)

    # Step 2: Run core inference (uses same features internally)
    result = core_run_inference(wav_path, task=task, model_path=model_path)

    # Step 3: Build display features list
    display_features = []
    for feature_name in DISPLAY_FEATURES:
        if feature_name in features_dict:
            info = get_feature_display_info(feature_name)
            value = features_dict[feature_name]
            display_features.append({
                "name": feature_name,
                "value": value,
                "formatted_value": format_feature_value(value, info["unit"]),
                "unit": info["unit"],
                "description": info["description"],
                "category": info["category"],
            })

    # Step 4: Load feature importance (optional, graceful degradation)
    importance_data = _load_importance_data(result.model_name)

    return {
        "prediction": {
            "class": result.prediction,
            "probability": result.probability,
            "probability_pd": result.probability_pd,
            "probability_hc": result.probability_hc,
        },
        "model": {
            "name": result.model_name,
            "task": result.task,
            "feature_set": result.feature_set,
            "feature_count": result.feature_count,
        },
        "features": {
            "displayed": display_features,
            "all_count": len(features_dict),
        },
        "importance": importance_data,
    }


def _load_importance_data(model_name: str, top_n: int = 5) -> Optional[dict]:
    """
    Load pre-computed feature importance from CSV.

    Returns None if file not found or model not present.
    """
    if not IMPORTANCE_CSV_PATH.exists():
        logger.warning(f"Importance file not found: {IMPORTANCE_CSV_PATH}")
        return None

    try:
        with open(IMPORTANCE_CSV_PATH, "r") as f:
            reader = csv.DictReader(f)
            rows = [r for r in reader if r["model"] == model_name]

        if not rows:
            logger.warning(f"No importance data for model: {model_name}")
            return None

        # Sort by rank and take top N
        rows.sort(key=lambda r: float(r["rank"]))
        top_features = []
        for row in rows[:top_n]:
            top_features.append({
                "name": row["feature"],
                "importance": float(row["mean"]),
                "rank": int(float(row["rank"])),
            })

        return {
            "available": True,
            "top_features": top_features,
            "method": "gini" if model_name == "RandomForest" else "coefficient",
        }

    except Exception as e:
        logger.warning(f"Failed to load importance data: {e}")
        return None


# Re-export core exceptions for Flask app
__all__ = [
    "run_inference_with_features",
    "get_model_info",
    "InferenceError",
    "ModelNotFoundError",
]
