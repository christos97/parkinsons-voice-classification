# Web App Architecture

This document describes the architecture of the Flask demo application and its integration with the research inference pipeline.

## Overview

The demo app is a **thin wrapper** around the research codebase, designed for thesis defense demonstrations. It exposes the classification pipeline through a simple web interface while maintaining strict separation between presentation and research logic.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLASK DEMO APP                              │
│                        (demo_app/app.py)                            │
│                                                                     │
│  • Handles HTTP requests                                            │
│  • Manages file uploads                                             │
│  • Renders templates                                                │
│  • Imports ONLY inference.py                                        │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ run_inference(wav_path)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INFERENCE API                                  │
│              (src/parkinsons_voice_classification/inference.py)     │
│                                                                     │
│  • Single public function: run_inference()                          │
│  • Loads model (cached)                                             │
│  • Validates features                                               │
│  • Returns InferenceResult dataclass                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
┌──────────────────────────────┐  ┌──────────────────────────────────┐
│     FEATURE EXTRACTION       │  │        TRAINED MODEL             │
│        (features/)           │  │    (outputs/models/*.joblib)     │
│                              │  │                                  │
│  • extract_all_features()    │  │  • sklearn Pipeline              │
│  • 47 or 78 features         │  │  • Scaler + Classifier           │
│  • Prosodic + Spectral       │  │  • Serialized with metadata      │
└──────────────────────────────┘  └──────────────────────────────────┘
```

## Design Principles

### 1. Single Import Rule

The Flask app imports **only** the inference module:

```python
# demo_app/app.py
from parkinsons_voice_classification.inference import run_inference
```

It has **no knowledge** of:
- Which features are extracted
- How many features exist
- Which model architecture is used
- Whether features are "baseline" or "extended"

### 2. Config-Driven Pipeline Selection

Model and feature configuration is managed in `config.py`:

```python
INFERENCE_FEATURE_SET = "baseline"  # or "extended"
INFERENCE_MODEL_NAME = "RandomForest"
INFERENCE_TASK = "ReadText"
```

To switch models:
1. Update config
2. Run `make train-demo-model`
3. Restart demo (**no code changes needed**)

### 3. Metadata Validation

The inference module validates that extracted features match the trained model's expectations:

```python
# inference.py
def _validate_features(features: dict, metadata: dict) -> None:
    expected_count = metadata.get("feature_count", 0)
    actual_count = len(features)
    if actual_count != expected_count:
        raise FeatureMismatchError(...)
```

This catches configuration mismatches at runtime.

## File Structure

```
demo_app/
├── app.py                  # Flask application (imports only inference.py)
├── templates/
│   ├── index.html          # Upload form with model info
│   ├── result.html         # Prediction display with probabilities
│   └── about.html          # Project info and disclaimers
└── README.md               # Usage documentation

src/parkinsons_voice_classification/
├── inference.py            # Stable inference API (single entry point)
├── config.py               # Config-driven model/feature selection
├── features/               # Feature extraction (not imported by app)
├── models/                 # Model definitions (not imported by app)
└── cli/
    └── train_model.py      # Model training and serialization
```

## Request Flow

### 1. User Uploads WAV File

```
Browser → POST /analyze → Flask receives file
```

### 2. Flask Saves to Temp File

```python
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    file.save(tmp.name)
```

### 3. Flask Calls Inference API

```python
result = run_inference(tmp_path, task="ReadText")
```

### 4. Inference Pipeline Executes

```
inference.py:
  1. Load model (cached after first call)
  2. Extract features from WAV
  3. Validate feature count matches model
  4. Run prediction
  5. Return InferenceResult
```

### 5. Flask Renders Result

```python
return render_template("result.html", result=result)
```

### 6. Temp File Cleanup

```python
finally:
    os.unlink(tmp_path)
```

## InferenceResult Dataclass

```python
@dataclass
class InferenceResult:
    prediction: str         # "PD" or "HC"
    probability: float      # Confidence of prediction
    probability_pd: float   # P(Parkinson's Disease)
    probability_hc: float   # P(Healthy Control)
    model_name: str         # e.g., "RandomForest"
    feature_set: str        # "baseline" or "extended"
    task: str               # e.g., "ReadText"
    feature_count: int      # Number of features extracted
```

## Model Artifact Structure

Trained models are saved with metadata for validation:

```python
artifact = {
    "pipeline": sklearn_pipeline,  # StandardScaler + Classifier
    "metadata": {
        "model_name": "RandomForest",
        "task": "ReadText",
        "feature_set": "baseline",
        "feature_count": 47,
        "feature_names": [...],
        "training_samples": 37,
        "trained_at": "2026-01-13T...",
    }
}
joblib.dump(artifact, "outputs/models/RandomForest_ReadText_baseline.joblib")
```

## Updating the Pipeline

When research improves feature extraction or models:

1. **Update feature extraction** in `features/` modules
2. **Re-extract features**: `make extract-readtext`
3. **Retrain model**: `make train-demo-model`
4. **Flask app continues unchanged**

If a change requires editing Flask routes or templates → **the architecture design is wrong**.

## Error Handling

| Error Type | Cause | User Message |
|------------|-------|--------------|
| `ModelNotFoundError` | Model file missing | "Run `make train-demo-model` first" |
| `FeatureMismatchError` | Config mismatch | "Feature count mismatch" |
| `InferenceError` | Feature extraction failed | "Analysis failed: [details]" |

## Safety & Disclaimers

Every page displays:

> **Research Demonstration Only.**
> This application is part of an MSc thesis and is not intended for medical diagnosis or clinical use.

The result page explicitly states:

> This result is generated by a research model and should not be interpreted as medical advice or diagnosis.

## Quick Start

```bash
# Prerequisites: features must be extracted
make extract-readtext

# Install Flask
make demo-install

# Train inference model
make train-demo-model

# Run demo
make demo
# Open http://127.0.0.1:5000
```

## Non-Goals

This demo is **not designed for**:
- Production deployment
- High availability
- Multiple concurrent users
- Model versioning UI
- User authentication
- Result persistence

It exists solely as a **thesis defense demonstration tool**.
