---
package: "parkinsons_voice_classification"
purpose: "Binary PD vs HC classification using voice features"
parent_rules: "../../../AGENTS.md"
last_updated: "2026-01-14"

public_api:
  inference:
    module: "inference.py"
    entry_point: "run_inference(wav_path: Path) -> InferenceResult"
    classes: ["InferenceResult", "InferenceError", "ModelNotFoundError"]
    caching: "Module-level model cache (singleton pattern)"

  cli_commands:
    - { name: "pvc-extract", module: "cli.extract_features", options: ["--task", "--jobs"] }
    - { name: "pvc-experiment", module: "cli.run_experiments", options: [] }
    - { name: "pvc-train", module: "cli.train_model", options: ["--task", "--model", "--feature-set"] }
    - { name: "pvc-importance", module: "cli.feature_importance", options: ["--permutation"] }

configuration:
  file: "config.py"
  critical_constants:
    RANDOM_SEED: 42
    N_FOLDS: 5
    SAMPLE_RATE: 22050
    BASELINE_FEATURE_COUNT: 47
    EXTENDED_FEATURE_COUNT: 78
  toggles:
    USE_EXTENDED_FEATURES: false
    USE_CLASS_WEIGHT_BALANCED: false
  inference_defaults:
    INFERENCE_FEATURE_SET: "baseline"
    INFERENCE_MODEL_NAME: "RandomForest"
    INFERENCE_TASK: "ReadText"

modules:
  data:
    mdvr_kcl: { purpose: "Dataset A loader (raw audio)", exports: ["load_recordings_as_features", "get_grouped_labels"] }
    pd_speech: { purpose: "Dataset B loader (pre-extracted features)", exports: ["load_dataset"] }

  features:
    extraction_simple: { purpose: "Main extraction pipeline", exports: ["extract_all_features", "get_feature_names"] }
    prosodic_simple: { purpose: "Praat/Parselmouth features (21)", exports: ["extract_prosodic_features"] }
    spectral_simple: { purpose: "Librosa MFCC features (26/57)", exports: ["extract_spectral_features"] }

  models:
    classifiers: { purpose: "Model pipeline factory", exports: ["get_model_pipelines"] }
    training: { purpose: "Cross-validation runner", exports: ["run_cross_validation", "aggregate_results"] }
    feature_importance: { purpose: "Importance extraction", exports: ["extract_importance", "plot_importance"] }

  visualization:
    plots: { purpose: "Publication-quality figures", exports: ["plot_feature_importance", "plot_comparison_heatmaps"] }

feature_pipeline:
  baseline_47:
    prosodic: 21
    spectral_mfcc: 26
  extended_78:
    prosodic: 21
    spectral_mfcc_extended: 57
  extraction_pattern: "Parallel processing → NaN on errors (never crash)"

dependencies:
  core: ["numpy", "pandas", "scipy", "scikit-learn", "librosa", "praat-parselmouth"]
  cli: ["tqdm"]
  visualization: ["matplotlib", "seaborn"]
  demo: ["flask"]
---

# Package-Level Agent Rules

## parkinsons_voice_classification

> This extends [../../../AGENTS.md](../../../AGENTS.md) with **implementation-level rules** for the Python package.

---

## 1. Module Architecture (DO/DON'T)

### ✅ Correct Import Patterns

```python
# External code (e.g., demo app)
from parkinsons_voice_classification.inference import run_inference, InferenceResult

# Internal module imports
from parkinsons_voice_classification import config
from parkinsons_voice_classification.features.extraction_simple import extract_all_features
from parkinsons_voice_classification.data.mdvr_kcl import load_recordings_as_features
```

### ❌ Forbidden Imports

```python
# NEVER import Flask or web frameworks in core package
from flask import Flask  # ❌ Breaks separation of concerns

# NEVER import from __pycache__ or internal modules
from parkinsons_voice_classification.inference import _extract_features  # ❌ Private function

# NEVER import legacy modules when _simple versions exist
from parkinsons_voice_classification.features.extraction import extract  # ❌ Use extraction_simple
```

---

## 2. Configuration Rules (CRITICAL)

> **config.py is the single source of truth for all reproducible parameters.**

### Non-Negotiable

- ❌ Never hardcode magic numbers (sample rates, feature counts, seeds)
- ❌ Never modify `config.py` at runtime (read-only contract)
- ❌ Never change `RANDOM_SEED` (breaks reproducibility)
- ✅ Always import constants: `from parkinsons_voice_classification import config`
- ✅ Use `config.get_features_path(feature_set)` for dynamic paths

### Toggle Effects

| Toggle | True | False |
|--------|------|-------|
| `USE_EXTENDED_FEATURES` | 78 features | 47 features |
| `USE_CLASS_WEIGHT_BALANCED` | Balanced class weights | No weighting |

---

## 3. Public Inference API

### Single Entry Point

```python
from parkinsons_voice_classification.inference import run_inference
from pathlib import Path

result = run_inference(Path("recording.wav"))
# Returns: InferenceResult(prediction="PD", probability=0.87, ...)
```

### Invariants

- Takes **Path** to WAV file (any sample rate, mono/stereo)
- Returns **InferenceResult** dataclass (never dict)
- Uses model specified in `config.INFERENCE_*` constants
- Caches model at module level (singleton pattern)
- Raises `ModelNotFoundError` if artifacts missing
- Raises `InferenceError` on extraction/prediction failures

### What NOT to Call Directly

❌ `_extract_features(wav_path)` — Private implementation  
❌ `_load_model()` — Internal caching logic  
✅ `run_inference(wav_path)` — Only public API

---

## 4. Feature Extraction Pipeline

### Architecture

```
WAV (any format) → Normalization (22050 Hz mono)
                 ↓
    Prosodic Features (21) + Spectral Features (26 or 57)
                 ↓
         Feature Vector (47 or 78) → ML Pipeline
```

### Parallel Extraction Pattern

```python
from parkinsons_voice_classification.features.extraction_simple import extract_features_parallel
import pandas as pd

df = extract_features_parallel(
    wav_files=wav_paths,
    n_jobs=4,  # Default from config.DEFAULT_N_JOBS
    task="ReadText"
)
# Returns: DataFrame with 47 or 78 columns + metadata
```

### Graceful Degradation

- **All extraction functions return NaN on errors** (never crash)
- Try-except blocks around Praat/librosa calls
- Missing files → NaN row with warning logged
- Invalid audio → NaN row with warning logged

### Adding New Features

✅ **DO:**
1. Add extraction function to `prosodic_simple.py` or `spectral_simple.py`
2. Update `get_feature_names()` to include new features
3. Update `BASELINE_FEATURE_COUNT` or `EXTENDED_FEATURE_COUNT` in `config.py`
4. Handle exceptions → return NaN (never raise)

❌ **DON'T:**
- Modify feature counts without updating config
- Raise exceptions on extraction errors
- Add features that break 47/78 contract

---

## 5. Model Training Workflow

### Cross-Validation Strategy

```python
from parkinsons_voice_classification.models.training import run_cross_validation
from parkinsons_voice_classification.data.mdvr_kcl import load_recordings_as_features

# Dataset A (subject-level splits)
X, y, groups = load_recordings_as_features(task="ReadText")
results = run_cross_validation(X, y, groups=groups)  # Uses GroupedStratifiedKFold

# Dataset B (row-level splits)
from parkinsons_voice_classification.data.pd_speech import load_dataset
X, y = load_dataset()
results = run_cross_validation(X, y, groups=None)  # Uses StratifiedKFold
```

### Critical Rules

- ✅ Dataset A **must** use `groups` parameter (subject-level splits)
- ✅ Dataset B **must** use `groups=None` (no subject IDs available)
- ❌ Never mix cross-validation strategies between datasets
- ❌ Never split recordings from same subject across folds

### Model Pipelines

All models follow: `StandardScaler → Classifier`

```python
from parkinsons_voice_classification.models.classifiers import get_model_pipelines

pipelines = get_model_pipelines()
# Returns: {"LogisticRegression": Pipeline, "SVM_RBF": Pipeline, "RandomForest": Pipeline}
```

**Immutable hyperparameters:**
- LogisticRegression: `max_iter=10000`, `random_state=42`
- SVM: `kernel='rbf'`, `random_state=42`
- RandomForest: `n_estimators=100`, `random_state=42`

---

## 6. CLI Command Patterns

### Feature Extraction

```bash
pvc-extract --task ReadText --jobs 4
pvc-extract --task all --jobs 8  # Both tasks
```

### Experiment Runner

```bash
pvc-experiment  # No options (runs all experiments)
```

### Model Training (for inference)

```bash
pvc-train --task ReadText --model RandomForest --feature-set baseline
```

### Feature Importance

```bash
pvc-importance --permutation  # Permutation importance
pvc-importance                # Native importance
```

---

## 7. Adapter Pattern (Demo App)

### Layer Separation

```
Flask (app.py) → Adapter (inference_adapter.py) → Core API (inference.py)
```

### Rules

- ✅ Flask imports **only** `inference_adapter.py`
- ✅ Adapter wraps `run_inference()` + enriches with display metadata
- ✅ Core package **never** depends on Flask
- ❌ Never import `flask` in `src/parkinsons_voice_classification/`
- ❌ Never import core package modules directly in `app.py`

### Benefit

Model switching requires **zero Flask changes** — all config in `config.py`.

---

## 8. Reproducibility Guarantees

### Fixed Seeds

```python
RANDOM_SEED = 42  # config.py
```

Used in:
- All model `random_state` parameters
- NumPy/scikit-learn operations
- Data splitting (StratifiedKFold seed)

### Deterministic Sorting

```python
# Always sort subject IDs before grouping
sorted(subject_ids)  # Ensures consistent fold assignment
```

### Version Locking

```toml
# pyproject.toml
numpy = "^1.24"
scikit-learn = "^1.3"
librosa = "^0.10.1"
praat-parselmouth = "^0.4.3"
```

---

## 9. Feature Count Validation

### Mandatory Checks

```python
assert len(feature_vector) == config.BASELINE_FEATURE_COUNT  # 47
# OR
assert len(feature_vector) == config.EXTENDED_FEATURE_COUNT  # 78
```

### Where Validation Occurs

- `inference.py`: Validates extracted features before prediction
- `extraction_simple.py`: Returns DataFrame with correct column count
- `training.py`: Sanity check before CV

### Failure Modes

- Too few features → `InferenceError` (likely extraction failure)
- Too many features → `InferenceError` (config mismatch)

---

## 10. Forbidden Modifications

### Never Change

❌ Random seeds (`RANDOM_SEED = 42`)  
❌ Sample rate (`SAMPLE_RATE = 22050`)  
❌ Number of folds (`N_FOLDS = 5`)  
❌ Feature extraction logic (breaks trained models)  
❌ Serialized model artifacts (`outputs/models/*.joblib`)  
❌ Hyperparameters in `get_model_pipelines()`

### Why?

Breaks reproducibility and invalidates published thesis results.

---

## 11. Extension Guidelines

### Adding New Models

```python
# models/classifiers.py

def get_model_pipelines() -> dict[str, Pipeline]:
    pipelines = {
        "LogisticRegression": ...,
        "SVM_RBF": ...,
        "RandomForest": ...,
        "NewModel": Pipeline([  # ✅ Follow pattern
            ("scaler", StandardScaler()),
            ("classifier", NewClassifier(random_state=config.RANDOM_SEED))
        ])
    }
    return pipelines
```

**Requirements:**
- Must use `StandardScaler` first stage
- Must set `random_state=config.RANDOM_SEED`
- Must test with both baseline and extended features
- Must update documentation in `AGENTS.md`

### Adding New Features

```python
# features/prosodic_simple.py or spectral_simple.py

def extract_new_feature(wav_path: Path) -> float:
    try:
        # Extraction logic
        return value
    except Exception as e:
        logger.warning(f"Failed: {e}")
        return np.nan  # ✅ Never raise
```

**Requirements:**
- Return `np.nan` on errors (never raise)
- Update `get_feature_names()` list
- Update `BASELINE_FEATURE_COUNT` or `EXTENDED_FEATURE_COUNT`
- Test extraction on all Dataset A recordings
- Document in feature table (thesis appendix)

### Adding New CLI Commands

```python
# cli/new_command.py

def main():
    parser = argparse.ArgumentParser(description="...")
    # ... argument parsing ...
    print(f"\n{'='*60}")
    print("NEW COMMAND")
    print(f"{'='*60}\n")
    # ... implementation ...

if __name__ == "__main__":
    main()
```

**Requirements:**
- Register in `pyproject.toml` `[tool.poetry.scripts]`
- Follow naming convention: `pvc-<command>`
- Use argparse (not click or other frameworks)
- Print structured output with dividers

---

## 12. Testing & Validation

### Manual Validation Checklist

```bash
# Feature extraction
pvc-extract --task ReadText --jobs 1
# Check: outputs/features/baseline/ReadText_features.csv exists
# Check: Feature count = 47 (or 78 if extended)

# Model training
pvc-train --task ReadText --model RandomForest --feature-set baseline
# Check: outputs/models/RandomForest_ReadText_baseline.joblib exists
# Check: metadata JSON has correct feature_count

# Inference
python -c "
from parkinsons_voice_classification.inference import run_inference
from pathlib import Path
result = run_inference(Path('assets/DATASET_MDVR_KCL/ReadText/ID01hc_ReadText.wav'))
print(result)
"
# Check: Returns InferenceResult with expected fields
# Check: Feature count in result matches config
```

### Unit Test Patterns

```python
# Recommended patterns (if adding tests)
def test_extract_features_returns_nan_on_error():
    result = extract_prosodic_features(Path("nonexistent.wav"))
    assert all(np.isnan(list(result.values())))

def test_inference_validates_feature_count():
    with pytest.raises(InferenceError):
        # Mock extraction returning wrong feature count
        ...
```

---

## 13. Common Pitfalls

### ❌ Mistake: Training on wrong splits

```python
# BAD: Dataset A without groups
X, y, groups = load_recordings_as_features(task="ReadText")
run_cross_validation(X, y, groups=None)  # ❌ Subject leakage!
```

```python
# GOOD: Dataset A with groups
run_cross_validation(X, y, groups=groups)  # ✅ Subject-level splits
```

### ❌ Mistake: Hardcoding paths

```python
# BAD
features = pd.read_csv("outputs/features/baseline/ReadText_features.csv")  # ❌

# GOOD
from parkinsons_voice_classification import config
features = pd.read_csv(config.get_features_path("baseline") / "ReadText_features.csv")  # ✅
```

### ❌ Mistake: Modifying config at runtime

```python
# BAD
from parkinsons_voice_classification import config
config.RANDOM_SEED = 123  # ❌ Breaks reproducibility

# GOOD
# Edit config.py directly, restart Python interpreter
```

### ❌ Mistake: Importing private functions

```python
# BAD
from parkinsons_voice_classification.inference import _load_model  # ❌ Private

# GOOD
from parkinsons_voice_classification.inference import run_inference  # ✅ Public
```

---

## 14. Documentation Sync Rule

> Any change affecting package behavior, API surface, or configuration **MUST** update this file and root [AGENTS.md](../../../AGENTS.md).

**Triggers:**
- Adding/removing modules or functions
- Changing feature extraction logic
- Adding/removing config constants
- Modifying CLI command signatures
- Changing inference API contract

**Non-optional** — keeps agent context accurate.

---

## End of Package-Level Rules
