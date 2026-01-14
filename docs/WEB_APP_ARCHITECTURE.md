# Web App Architecture

This document describes the architecture of the Flask demo application and its integration with the research inference pipeline.

## Overview

The demo app is a **thin wrapper** around the research codebase, designed for thesis defense demonstrations. It exposes the classification pipeline through a simple web interface while maintaining strict separation between presentation and research logic.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLASK DEMO APP                              │
│                        (demo_app/app.py)                            │
│                                                                     │
│  • Handles HTTP requests (uploads + recordings)                     │
│  • Manages file uploads (any audio format)                          │
│  • Renders templates                                                │
│  • Imports ONLY inference_adapter.py                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ run_inference_with_features()
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INFERENCE ADAPTER                              │
│                  (demo_app/inference_adapter.py)                    │
│                                                                     │
│  • Wraps core inference + feature extraction                        │
│  • Enriches results with display metadata                           │
│  • Loads feature importance data                                    │
│  • Returns enhanced dict for Flask templates                        │
└─────────────────────────────────────────────────────────────────────┘
                    │                           │
                    ▼                           ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────────┐
│  CORE INFERENCE API          │  │  AUDIO NORMALIZATION             │
│  (inference.py)              │  │  (demo_app/audio_utils.py)       │
│                              │  │                                  │
│  • run_inference()           │  │  • Format conversion (librosa)   │
│  • Loads model (cached)      │  │  • Mono @ 22050 Hz → WAV         │
│  • Validates features        │  │  • Handles WebM/MP3/etc          │
│  • Returns InferenceResult   │  │  • File size/duration checks     │
└──────────────────────────────┘  └──────────────────────────────────┘
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
┌──────────────────────────────┐  ┌──────────────────────────────────┐
│     FAdapter Layer Pattern

The Flask app imports **only** the adapter module:

```python
# demo_app/app.py
from inference_adapter import (
    run_inference_with_features,
    get_model_info,
    InferenceError,
    ModelNotFoundError,
)
from audio_utils import (
    normalize_audio_file,
    cleanup_audio_file,
    AudioValidationError,
)
```

The adapter wraps the core inference API and adds:
- Feature value extraction for display
- Feature importance data loading
- Display metadata enrichment
- Flask-friendly response formatting

The Flask app Design Principles

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
adapter + audio_utils)
├── inference_adapter.py    # Adapter layer wrapping core inference
├── audio_utils.py          # Audio normalization (any format → WAV)
├── feature_metadata.py     # Display metadata for curated features
├── templates/
│   ├── index.html          # Upload form + recorder widget + model info
│   ├── result.html         # Prediction + probabilities + feature table
│   └── about.html          # Project info and disclaimers
└── README.md               # Usage documentation

src/parkinsons_voice_classification/
├── inference.py            # Core inference API (imported by adapter)
├── config.py               # Config-driven model/feature selection
├── features/
│   └── extraction_simple.py  # Feature extraction (imported by adapter

## File Structure

```/Records Audio

```
Browser → POST /analyze → Flask receives file (any format)
```

### 2. Flask Saves Original File

```python
# Accept any audio format (WebM, MP3, WAV, etc.)
suffix = Path(filename).suffix if filename else ".audio"
with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
    file.save(tmp.name)
    original_tmp_path = tmp.name
```

### 3. Audio Normalization

```python
# Convert any format → mono 22050 Hz PCM-16 WAV
normalized_tmp_path, audio_info = normalize_audio_file(original_tmp_path)
```

### 4. Flask Calls Adapter

```python
# Adapter returns enriched result with features + importance
result = run_inference_with_features(normalized_tmp_path, task="ReadText")
```

### 5. Adapter Executes

```
inference_adapter.py:
  1. Extract features (get raw values for display)
  2. Call core inference (validation + prediction)
  3. Build display feature list (8 curated features)
  4. Load feature importance from CSV (optional)
  5. Return enriched dict
```

### 6. Core Inference Executes

```
inference.py:
  1. Load model (cached after first call)
  2. Extract features (calls same extraction function)
  3. Validate feature count matches model
  4. Run sklearn pipeline (scale + predict)
  5. Return InferenceResult dataclass
```

### 7. Flask Renders Result

```python
return render_template("result.html", result=result)
```

### 8. Temp File Cleanup
Data Structures

### InferenceResult (Core API)

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

### Enriched Result (Adapter → Flask)

```python
{
    "prediction": {
        "class": "PD" or "HC",
        "probability": 0.0-1.0,
        "probability_pd": 0.0-1.0,
        "probability_hc": 0.0-1.0,
    },
    "model": {
        "name": "RandomForest",
        "task": "ReadText",
        "feature_set": "baseline",
        "feature_count": 47,
    },
    "features": {
        "displayed": [  # 8 curated features
            {
                "name": "f0_mean",
                "value": 123.45,
                "formatted_value": "123.5 Hz",
                "unit": "Hz",extraction_simple.py`
2. **Re-extract features**: `make extract-readtext`
3. **Retrain model**: `make train-demo-model`
4. **Adapter and Flask app continue unchanged**

If a change requires editing Flask routes or templates → **the architecture design is wrong**.

The only exception: if display features change, update `demo_app/feature_metadata.py`
        "all_count": 47,  # Total features extracted
    },
    "importance": {  # Optional, null if unavailable
        "available": true,
        "top_features": [  # Top 5 features
            {"name": "hnr_mean", "importance": 0.123, "rank": 1},
            ...
        ],
        "method": "gini",  # or "coefficient"
   AudioValidationError` | Invalid/corrupt audio | "Invalid audio file: [details]" |
| `InferenceError` | Feature extraction failed | "Analysis failed: [details]" |

All errors are caught in Flask routes and displayed via flash messages.
}

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
