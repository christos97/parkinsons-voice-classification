# Flask Demo Application

A minimal web interface for the Parkinson's Voice Classification research pipeline.

## ⚠️ Important Disclaimer

**This application is a research demonstration developed as part of an MSc thesis.
It is NOT intended for medical diagnosis or clinical use.**

Parkinson's Disease can only be diagnosed by qualified medical professionals through
comprehensive clinical assessment.

---

## Quick Start

From the project root directory:

```bash
# 1. Ensure features are extracted
make extract-readtext

# 2. Install Flask dependency
make demo-install

# 3. Train the inference model
make train-demo-model

# 4. Run the demo
make demo
```

Then open http://127.0.0.1:5000 in your browser.

---

## Architecture

The demo app is designed as a **thin wrapper** around the research inference pipeline:

```
demo_app/
├── app.py              # Flask routes (imports ONLY inference.py)
├── templates/
│   ├── index.html      # Upload form
│   ├── result.html     # Prediction display
│   └── about.html      # Project info & disclaimers
└── README.md           # This file

src/parkinsons_voice_classification/
├── inference.py        # Stable inference API (single entry point)
├── features/           # Feature extraction (not imported by app)
├── models/             # Model definitions (not imported by app)
└── config.py           # Config-driven model/feature selection
```

### Key Design Principle

> **The Flask app imports ONLY the inference module.**

It has no knowledge of:
- Which features are extracted
- How many features exist
- Which model architecture is used
- Whether features are "baseline" or "extended"

This ensures that **changes to feature extraction or models require zero changes
to the web application**.

---

## Inference API

The single public interface:

```python
from parkinsons_voice_classification.inference import run_inference

result = run_inference("/path/to/audio.wav")

# Returns:
# InferenceResult(
#     prediction="PD" or "HC",
#     probability=0.85,
#     probability_pd=0.85,
#     probability_hc=0.15,
#     model_name="RandomForest",
#     feature_set="baseline",
#     task="ReadText",
#     feature_count=47
# )
```

---

## Configuration

Model selection is config-driven in `config.py`:

```python
INFERENCE_FEATURE_SET = "baseline"  # or "extended"
INFERENCE_MODEL_NAME = "RandomForest"
INFERENCE_TASK = "ReadText"
```

To switch models:
1. Update config
2. Run `make train-demo-model`
3. Restart demo (no code changes needed)

---

## Updating the Pipeline

When research improves feature extraction or models:

1. Update `features/` modules as needed
2. Re-extract features: `make extract-readtext`
3. Retrain model: `make train-demo-model`
4. **Flask app continues working unchanged**

If a change requires editing Flask routes or templates → the design is wrong.

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask application with routes |
| `templates/index.html` | Upload form with model info |
| `templates/result.html` | Prediction display with probabilities |
| `templates/about.html` | Project info and disclaimers |

---

## Dependencies

The demo requires the `demo` extra group:

```bash
poetry install --with demo
```

This adds Flask to the project dependencies.

---

## Academic Use

This demo is suitable for:
- Thesis defense demonstrations
- Research presentations
- Educational purposes

It is **not suitable** for:
- Clinical trials
- Medical screening
- Patient diagnosis
- Production deployment
