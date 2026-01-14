---
title: "Demo App Architecture"
last_updated: "2026-01-14"
purpose: "Research demonstration for thesis defense"
status: "Production-complete for demo purposes"

architecture:
  layers:
    - { name: "Flask", file: "demo_app/app.py", role: "HTTP routes, file handling, template rendering" }
    - { name: "Adapter", file: "demo_app/inference_adapter.py", role: "Wraps core inference, enriches for display" }
    - { name: "Audio Utils", file: "demo_app/audio_utils.py", role: "Format conversion, normalization" }
    - { name: "Core Inference", file: "src/parkinsons_voice_classification/inference.py", role: "Model loading, prediction" }

data_flow: "Upload → Normalize → Extract Features → Predict → Enrich → Render"

invariants:
  - "Flask imports ONLY inference_adapter and audio_utils"
  - "All audio normalized to mono 22050 Hz PCM-16 WAV before processing"
  - "Temp files cleaned up in finally blocks"
  - "Model changes require zero Flask code changes"
---

# Demo App Architecture

Flask web application for Parkinson's voice classification research demonstration.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLASK APP                                   │
│                      (demo_app/app.py)                              │
│  • HTTP routes (/, /analyze, /about)                                │
│  • File upload handling (any audio format)                          │
│  • Template rendering                                               │
│  • Imports: inference_adapter, audio_utils                          │
└─────────────────────────────────────────────────────────────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
┌──────────────────────────────┐    ┌──────────────────────────────────┐
│     AUDIO UTILS              │    │     INFERENCE ADAPTER            │
│  (demo_app/audio_utils.py)   │    │  (demo_app/inference_adapter.py) │
│                              │    │                                  │
│  • normalize_audio_file()    │    │  • run_inference_with_features() │
│  • Any format → WAV          │    │  • Extracts features for display │
│  • Mono 22050 Hz PCM-16      │    │  • Loads importance data         │
│  • File size/duration limits │    │  • Returns enriched dict         │
└──────────────────────────────┘    └──────────────────────────────────┘
                                                      │
                            ┌─────────────────────────┴─────────────────────────┐
                            ▼                                                   ▼
              ┌──────────────────────────────┐            ┌──────────────────────────────┐
              │     CORE INFERENCE           │            │     FEATURE EXTRACTION       │
              │     (inference.py)           │            │     (extraction_simple.py)   │
              │                              │            │                              │
              │  • run_inference()           │            │  • extract_all_features()    │
              │  • Model loading (cached)    │            │  • Prosodic + spectral       │
              │  • Feature validation        │            │  • 47 baseline / 78 extended │
              │  • sklearn Pipeline          │            │  • Deterministic             │
              └──────────────────────────────┘            └──────────────────────────────┘
```

## Request Flow

### 1. User Uploads Audio

```
Browser → POST /analyze → Flask receives file
```

Accepts any audio format (WAV, MP3, WebM, FLAC, etc.).

### 2. Save Original to Temp File

```python
suffix = Path(filename).suffix if filename else ".audio"
with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
    file.save(tmp.name)
    original_tmp_path = tmp.name
```

### 3. Audio Normalization

```python
normalized_tmp_path, audio_info = normalize_audio_file(original_tmp_path)
```

Converts any input format to:

- Sample rate: 22050 Hz
- Channels: Mono
- Format: PCM-16 WAV

### 4. Inference via Adapter

```python
result = run_inference_with_features(normalized_tmp_path, task="ReadText")
```

Adapter internally:

1. Extracts features (for display values)
2. Calls core inference (validation + prediction)
3. Builds display feature list (8 curated features)
4. Loads feature importance from CSV (if available)
5. Returns enriched dict for templates

### 5. Core Inference

```
inference.py:
  1. Load model artifact (cached after first call)
  2. Validate feature count matches trained model
  3. Run sklearn Pipeline (StandardScaler + Classifier)
  4. Return InferenceResult dataclass
```

### 6. Render Result

```python
return render_template("result.html", result=result)
```

### 7. Temp File Cleanup

```python
finally:
    cleanup_audio_file(original_tmp_path)
    cleanup_audio_file(normalized_tmp_path)
```

## Data Structures

### InferenceResult (Core API)

```python
@dataclass
class InferenceResult:
    prediction: str         # "PD" or "HC"
    probability: float      # Confidence of prediction
    probability_pd: float   # P(Parkinson's Disease)
    probability_hc: float   # P(Healthy Control)
    model_name: str         # "RandomForest"
    feature_set: str        # "baseline" or "extended"
    task: str               # "ReadText"
    feature_count: int      # 47 (baseline) or 78 (extended)
```

### Enriched Result (Adapter → Flask)

```python
{
    "prediction": {
        "class": "PD",
        "probability": 0.85,
        "probability_pd": 0.85,
        "probability_hc": 0.15,
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
                "unit": "Hz",
                "description": "Mean fundamental frequency",
                "category": "Prosodic",
            },
            # ... 7 more features
        ],
        "all_count": 47,
    },
    "importance": {  # Optional
        "available": true,
        "top_features": [
            {"name": "hnr_mean", "importance": 0.123, "rank": 1},
        ],
        "method": "gini",
    },
}
```

## File Structure

```
demo_app/
├── app.py                  # Flask routes (imports adapter + audio_utils)
├── inference_adapter.py    # Wraps core inference, enriches for display
├── audio_utils.py          # Audio normalization (any format → WAV)
├── feature_metadata.py     # Display metadata for 8 curated features
├── templates/
│   ├── index.html          # Upload form + recorder widget
│   ├── result.html         # Prediction + probabilities + features
│   └── about.html          # Project info and disclaimers
└── README.md               # Usage documentation

src/parkinsons_voice_classification/
├── inference.py            # Core inference API
├── config.py               # Model/feature configuration
└── features/
    └── extraction_simple.py  # Feature extraction
```

## Model Artifacts

```python
# outputs/models/RandomForest_ReadText_baseline.joblib
{
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
```

## Configuration

Model selection via `config.py`:

```python
INFERENCE_FEATURE_SET = "baseline"  # or "extended"
INFERENCE_MODEL_NAME = "RandomForest"
INFERENCE_TASK = "ReadText"
```

To switch models:

1. Update `config.py`
2. Run `make train-demo-model`
3. Restart demo (no code changes)

## Error Handling

| Error Type | Cause | User Message |
|------------|-------|--------------|
| `ModelNotFoundError` | Model file missing | "Run `make train-demo-model` first" |
| `FeatureMismatchError` | Config/model mismatch | "Feature count mismatch" |
| `AudioValidationError` | Invalid/corrupt audio | "Invalid audio file: [details]" |
| `InferenceError` | Feature extraction failed | "Analysis failed: [details]" |

All errors caught in Flask routes, displayed via flash messages.

## Design Invariants

1. **Flask imports only adapter + audio_utils** — No direct imports from core package
2. **Audio always normalized** — Feature extraction requires consistent format
3. **Config-driven model selection** — No hardcoded model paths in Flask
4. **Temp file cleanup guaranteed** — Using `finally` blocks
5. **Feature counts from config** — Not hardcoded anywhere

## Non-Goals

This demo is NOT designed for:

- Production deployment
- High availability
- Multiple concurrent users
- Model versioning UI
- User authentication
- Result persistence

It exists solely as a **thesis defense demonstration tool**.
