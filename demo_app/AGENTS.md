---
app: "Flask Demo Application"
purpose: "Research demonstration for thesis defense"
parent_rules: "../../AGENTS.md"
last_updated: "2026-01-15"

architecture:
  framework: "Flask + Jinja2 + Tailwind CSS + Vanilla JS"
  pattern: "Adapter isolation (Flask never imports core package directly)"
  entry_point: "app.py"
  modules:
    - { file: "app.py", purpose: "Flask routes and upload handling" }
    - { file: "inference_adapter.py", purpose: "Core inference wrapper + display enrichment" }
    - { file: "audio_utils.py", purpose: "Audio normalization (any format → mono 22050 Hz WAV)" }
    - { file: "feature_metadata.py", purpose: "Display formatting for 8 curated features" }
  
routes:
  - { path: "/", method: "GET", handler: "index()", purpose: "Upload form with recorder widget" }
  - { path: "/analyze", method: "POST", handler: "analyze()", purpose: "Process audio and return prediction" }
  - { path: "/about", method: "GET", handler: "about()", purpose: "Project info and disclaimers" }

frontend:
  styling: "Tailwind CSS (via CDN)"
  javascript: "Vanilla JS (no external library)"
  templates:
    - { file: "index.html", purpose: "Upload/record interface with tabs" }
    - { file: "result.html", purpose: "Prediction display with probabilities and features" }
    - { file: "about.html", purpose: "Research context and limitations" }

data_flow:
  upload: "Browser → Flask POST → audio_utils (normalize) → adapter (extract+infer) → result.html"
  record: "MediaRecorder API → Blob → FormData → Form POST (same as upload)"

invariants:
  - "Flask imports ONLY inference_adapter and audio_utils (never core package)"
  - "All audio normalized to mono 22050 Hz PCM-16 WAV before feature extraction"
  - "Temp files cleaned in finally blocks"
  - "Model switching requires zero Flask/template changes"
  - "Display features curated subset (8 of 47/78)"
  - "Recording submission uses form POST (not AJAX) to maintain navigation behavior"

deployment:
  dev_server: "flask run (default port 5000)"
  make_target: "make demo"
  dependencies: "poetry install --with demo"
---

# Flask Demo Agent Rules

## Parkinson's Voice Classification Web App

> Extends [../../AGENTS.md](../../AGENTS.md) and [../../src/parkinsons_voice_classification/AGENTS.md](../../src/parkinsons_voice_classification/AGENTS.md) with **Flask/frontend implementation rules**.

---

## 1. Import Boundaries (CRITICAL)

### ✅ Allowed in [app.py](app.py)

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from inference_adapter import run_inference_with_features, get_model_info
from audio_utils import normalize_audio_file, cleanup_audio_file
```

### ❌ FORBIDDEN in [app.py](app.py)

```python
from parkinsons_voice_classification.inference import run_inference  # ❌
from parkinsons_voice_classification.features import extract_all_features  # ❌
from parkinsons_voice_classification import config  # ❌
```

**Why:** Adapter pattern ensures model/feature changes require zero Flask edits.

---

## 2. Audio Processing Contract

### Normalization ([audio_utils.py](audio_utils.py))

- **Input:** ANY format (WAV, MP3, WebM, Opus, FLAC)
- **Output:** ALWAYS mono 22050 Hz PCM-16 WAV
- **Error handling:** AudioValidationError for invalid/silent audio

### File Upload Flow ([app.py](app.py))

```python
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file.save(original_tmp_path)  # 1. Save any format
        normalized_tmp_path = normalize_audio_file(original_tmp_path)  # 2. Normalize
        result = run_inference_with_features(normalized_tmp_path)  # 3. Infer
        return render_template("result.html", result=result)  # 4. Render
    finally:
        cleanup_audio_file(original_tmp_path)  # 5. ALWAYS cleanup
        cleanup_audio_file(normalized_tmp_path)
```

**Rules:**

- ✅ Use `finally` blocks for cleanup
- ✅ Pass normalized WAV to inference (never original)
- ❌ Never skip normalization

---

## 3. Frontend Stack

### Tailwind CSS (via CDN)

```html
<script src="https://cdn.tailwindcss.com"></script>
```

- ✅ Utility classes only: `bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded`
- ✅ Responsive: `grid grid-cols-1 xl:grid-cols-2 gap-6`
- ✅ Color palette: `blue` (primary), `orange` (PD), `green` (HC), `amber` (warnings)
- ❌ No custom CSS files
- ❌ No inline `<style>` blocks

### Vanilla JavaScript

```html
<!-- No external JS library required -->
```

- ✅ DOM manipulation, event handling
- ✅ Scripts in template files (no separate JS files)
- ❌ No React/Vue/Angular

---

## 4. Template Patterns

### Jinja2 Conditional Rendering

```html
<!-- Model status -->
{% if model_error %}
<div class="bg-red-50">{{ model_error }}</div>
{% else %}
<!-- Upload form -->
{% endif %}

<!-- Prediction styling -->
<div class="{% if result.prediction.class == 'PD' %}bg-orange-50{% else %}bg-green-50{% endif %}">
  {{ result.prediction.class }}
</div>
```

### Flash Messages

```html
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
  {% for category, message in messages %}
  <div class="{% if category == 'error' %}bg-red-100 text-red-700{% endif %}">
    {{ message }}
  </div>
  {% endfor %}
{% endif %}
{% endwith %}
```

### Disclaimer Banner (REQUIRED)

```html
<!-- MUST appear on ALL pages -->
<div class="bg-amber-50 border-l-4 border-amber-400 p-4 mb-6 rounded">
  <strong>Research Demonstration Only.</strong> Not for clinical use.
</div>
```

---

## 5. Audio Recorder Implementation

### Recording Flow ([templates/index.html](templates/index.html))

```javascript
let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  
  mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
  mediaRecorder.onstop = () => {
    recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
    // Show playback UI
    document.getElementById('recorded-audio').src = URL.createObjectURL(recordedBlob);
  };
  
  mediaRecorder.start();
}

function stopRecording() {
  mediaRecorder.stop();
}
```

### Submission via Form POST (NOT AJAX)

```javascript
function submitRecording() {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/analyze';
  form.enctype = 'multipart/form-data';
  
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.name = 'recorded_audio';
  
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(new File([recordedBlob], 'recording.webm', { type: 'audio/webm' }));
  fileInput.files = dataTransfer.files;
  
  form.appendChild(fileInput);
  document.body.appendChild(form);
  form.submit();  // Standard form POST (not AJAX)
}
```

**Rules:**

- ✅ Use `audio/webm` MIME type
- ✅ Field name: `recorded_audio`
- ✅ Submit via form POST (maintains navigation behavior)
- ❌ Never assume WAV format from browser

---

## 6. Result Display

### Prediction Card ([templates/result.html](templates/result.html))

```html
<!-- Color-coded header -->
<div class="{% if result.prediction.class == 'PD' %}bg-orange-50{% else %}bg-green-50{% endif %}">
  <p class="text-4xl font-bold">{{ result.prediction.class }}</p>
</div>

<!-- Probability bar -->
<div class="flex h-8 rounded-lg overflow-hidden">
  <div class="bg-orange-500" style="width: {{ (result.prediction.probability_pd * 100)|round|int }}%">
    PD {{ "%.0f"|format(result.prediction.probability_pd * 100) }}%
  </div>
  <div class="bg-green-500" style="width: {{ (result.prediction.probability_hc * 100)|round|int }}%">
    HC {{ "%.0f"|format(result.prediction.probability_hc * 100) }}%
  </div>
</div>
```

### Feature Table (8 curated features)

```html
<table>
  {% for feature in result.features %}
  <tr>
    <td class="{% if feature.category == 'prosodic' %}bg-blue-50{% else %}bg-purple-50{% endif %}">
      {{ feature.name }}
    </td>
    <td>{{ feature.formatted_value }}</td>
    <td>{{ feature.description }}</td>
  </tr>
  {% endfor %}
</table>
```

### Model Info (config-driven)

```html
<dl>
  <dt>Model:</dt>
  <dd>{{ result.model.name }}</dd>
  <dt>Feature Set:</dt>
  <dd>{{ result.model.feature_set }} ({{ result.model.feature_count }} features)</dd>
</dl>
```

---

## 7. Loading States

### Full-Screen Overlay

```html
<div id="loading-overlay" class="hidden fixed inset-0 bg-black bg-opacity-70 z-50">
  <div class="w-12 h-12 border-4 border-white rounded-full animate-spin"></div>
  <p class="text-white">Analyzing voice recording...</p>
</div>

<script>
document.getElementById('analysis-form').addEventListener('submit', () => {
  document.getElementById('loading-overlay').classList.remove('hidden');
});
</script>
```

---

## 8. Error Handling

### Model Not Found

```html
{% if model_error %}
<div class="bg-red-50">
  <p>{{ model_error }}</p>
  <p>Run <code>make train-demo-model</code></p>
</div>
{% endif %}
```

### Audio Validation

```python
try:
    normalized_tmp_path = normalize_audio_file(original_tmp_path)
except AudioValidationError as e:
    flash(str(e), "error")
    return redirect(url_for("index"))
```

---

## 9. Display Feature Curation

### 8 Selected Features ([feature_metadata.py](feature_metadata.py))

```python
DISPLAY_FEATURES = [
    "f0_mean", "f0_max", "hnr_mean",  # Prosodic
    "jitter_local", "shimmer_apq11", "intensity_mean",  # Prosodic
    "mfcc_0_mean", "mfcc_5_mean",  # Spectral
]

FEATURE_METADATA = {
    "f0_mean": {
        "description": "Average fundamental frequency (pitch)",
        "unit": "Hz",
        "category": "prosodic",
    },
}
```

**Rules:**

- ✅ Curate for interpretability
- ✅ Educational descriptions (not clinical)
- ❌ Never display all 47/78 features

---

## 10. Configuration-Driven Display

### Model Info from Adapter

```python
model_info = get_model_info()
# Returns: {"name": "RandomForest", "task": "ReadText", 
#           "feature_set": "baseline", "feature_count": 47}
```

### Switching Models (Zero Code Changes)

1. Edit [src/parkinsons_voice_classification/config.py](../src/parkinsons_voice_classification/config.py):

   ```python
   INFERENCE_MODEL_NAME = "SVM_RBF"
   INFERENCE_FEATURE_SET = "extended"
   ```

2. Run: `make train-demo-model`
3. Restart: `make demo`
4. ✅ Templates auto-update

---

## 11. Responsive Design

### Mobile-First Grid

```html
<div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
  <div>Left (stacks on mobile)</div>
  <div>Right (side-by-side on desktop)</div>
</div>
```

### Container Widths

```html
<div class="container mx-auto px-4 py-8 max-w-2xl">  <!-- Forms -->
<div class="container mx-auto px-4 py-8 max-w-6xl">  <!-- Results -->
```

---

## 12. Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Import core package in Flask | Import only [inference_adapter.py](inference_adapter.py) |
| Skip audio normalization | Always normalize before inference |
| Not cleaning temp files | Use `finally` blocks with `cleanup_audio_file()` |
| Hardcode feature count | Use `{{ result.model.feature_count }}` |
| Remove disclaimer banners | Keep on ALL pages (legal requirement) |

---

## 13. Testing Checklist

```bash
make train-demo-model && make demo  # Start app
```

**Manual tests:**

1. Upload WAV from [assets/DATASET_MDVR_KCL/ReadText/](../assets/DATASET_MDVR_KCL/ReadText/) → Check result page
2. Record 3-5 seconds → Check same result flow
3. Upload empty file → Check error flash
4. Resize window → Check mobile/desktop layouts

---

## 14. Extension Guidelines

### Add Route

```python
@app.route("/new-page")
def new_page():
    return render_template("new_page.html")  # Keep adapter imports only
```

### Add Display Feature

```python
# feature_metadata.py
DISPLAY_FEATURES.append("new_feature_name")
FEATURE_METADATA["new_feature_name"] = {"description": "...", "unit": "...", "category": "prosodic"}
```

### Modify Adapter Response

```python
# inference_adapter.py
return {
    "prediction": {...},
    "model": {...},
    "features": [...],
    "new_field": data,  # Update templates to consume
}
```

---

## 15. Documentation Sync

> Any change to routes, templates, or adapter interface **MUST** update this file.

---

## End of Flask Demo Rules
