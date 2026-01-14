# Flask Demo Application

Minimal web interface for Parkinson's Voice Classification research demonstration.

**Purpose:** Research demonstration for thesis defense  
**Key invariants:**
- Flask imports ONLY `inference_adapter` and `audio_utils`
- All audio normalized to mono 22050 Hz PCM-16 WAV
- Temp files cleaned in `finally` blocks
- Model switching requires zero Flask changes

## ⚠️ Important Disclaimer

**This application is a research demonstration developed as part of an MSc thesis.
It is NOT intended for medical diagnosis or clinical use.**

Parkinson's Disease can only be diagnosed by qualified medical professionals.

---

## Quick Start

```bash
make extract-readtext    # Extract features from Dataset A
make demo-install        # Install Flask dependency
make train-demo-model    # Train inference model
make demo                # Run at http://127.0.0.1:5000
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FLASK APP                                 │
│                          (app.py)                                   │
│  • Routes: /, /analyze, /about                                      │
│  • Imports: inference_adapter, audio_utils                          │
└─────────────────────────────────────────────────────────────────────┘
          │                                         │
          ▼                                         ▼
┌──────────────────────────┐        ┌──────────────────────────────────┐
│     AUDIO UTILS          │        │     INFERENCE ADAPTER            │
│   (audio_utils.py)       │        │   (inference_adapter.py)         │
│                          │        │                                  │
│  normalize_audio_file()  │        │  run_inference_with_features()   │
│  Any format → WAV        │        │  Enriches result for templates   │
│  Mono 22050 Hz           │        │  Loads feature importance        │
└──────────────────────────┘        └──────────────────────────────────┘
                                                    │
                                                    ▼
                                    ┌──────────────────────────────────┐
                                    │     CORE INFERENCE               │
                                    │   (inference.py)                 │
                                    │                                  │
                                    │  run_inference()                 │
                                    │  Model loading + prediction      │
                                    └──────────────────────────────────┘
```

### Design Principle

> **Flask imports ONLY the adapter and audio_utils modules.**

The Flask app has no knowledge of:
- Which features are extracted
- How many features exist
- Which model architecture is used
- Whether features are "baseline" or "extended"

This ensures **model/feature changes require zero Flask code changes**.

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask routes, file upload handling, template rendering |
| `inference_adapter.py` | Wraps core inference, enriches results with display data |
| `audio_utils.py` | Audio normalization (any format → mono 22050 Hz WAV) |
| `feature_metadata.py` | Display formatting for 8 curated features |
| `templates/index.html` | Upload form with recorder widget |
| `templates/result.html` | Prediction display with probabilities |
| `templates/about.html` | Project info and disclaimers |

---

## Configuration

Model selection is config-driven in `src/parkinsons_voice_classification/config.py`:

```python
INFERENCE_FEATURE_SET = "baseline"  # or "extended"
INFERENCE_MODEL_NAME = "RandomForest"
INFERENCE_TASK = "ReadText"
```

To switch models:
1. Update `config.py`
2. Run `make train-demo-model`
3. Restart demo (no code changes needed)

---

## Updating the Pipeline

When research improves feature extraction or models:

1. Update `features/` modules as needed
2. Re-extract features: `make extract-readtext`
3. Retrain model: `make train-demo-model`
4. **Flask app continues working unchanged**

If a change requires editing Flask routes or templates → the architecture is wrong.

---

## Dependencies

```bash
poetry install --with demo
```

This adds Flask to the project dependencies.

---

## See Also

- [docs/WEB_APP_ARCHITECTURE.md](../docs/WEB_APP_ARCHITECTURE.md) — Full architecture documentation
