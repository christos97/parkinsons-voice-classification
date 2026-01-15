"""
Flask Demo Application for Parkinson's Voice Classification

A minimal web interface demonstrating the research inference pipeline.
This app imports ONLY the stable inference API — it has no knowledge of
feature extraction implementation or model internals.

Usage:
    cd demo_app
    flask run

Or via make:
    make demo
"""

import os
import tempfile
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash

# Import from the adapter layer (wraps core inference with display data)
from inference_adapter import (
    run_inference_with_features,
    get_model_info,
    InferenceError,
    ModelNotFoundError,
)

# Import audio preprocessing utilities
from audio_utils import (
    normalize_audio_file,
    cleanup_audio_file,
    AudioValidationError,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")


@app.route("/")
def index():
    """Render the upload form."""
    # Try to get model info for display
    model_info = None
    model_error = None
    try:
        model_info = get_model_info()
    except ModelNotFoundError as e:
        model_error = str(e)
    except Exception as e:
        model_error = f"Could not load model information: {e}"

    return render_template(
        "index.html",
        model_info=model_info,
        model_error=model_error,
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """Process uploaded or recorded audio and return prediction."""
    # Check if file was uploaded or recorded
    file = None
    filename = "recording"
    
    if "audio_file" in request.files:
        # Traditional file upload
        file = request.files["audio_file"]
        filename = file.filename or "upload"
            
    elif "recorded_audio" in request.files:
        # Browser recording (WebM or other native format)
        file = request.files["recorded_audio"]
        filename = file.filename or "recording"
    else:
        flash("No audio file provided", "error")
        return redirect(url_for("index"))

    # Temporary file paths
    original_tmp_path = None
    normalized_tmp_path = None

    try:
        # Save uploaded file to temporary location
        # Use generic suffix since we accept any audio format
        suffix = Path(filename).suffix if filename else ".audio"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            file.save(tmp.name)
            original_tmp_path = tmp.name

        try:
            # Normalize audio (convert to mono 22050 Hz PCM-16 WAV)
            # Input can be any format (WebM, MP3, etc.)
            # Output is ALWAYS a standard WAV file for feature extraction
            normalized_tmp_path, _ = normalize_audio_file(original_tmp_path)
            
            # Run inference through the adapter (returns enriched data)
            # normalized_tmp_path is guaranteed to be a PCM-16 WAV file
            result = run_inference_with_features(normalized_tmp_path, task="ReadText")

            return render_template(
                "result.html",
                result=result,
                filename=filename,
            )

        except AudioValidationError as e:
            flash(f"Invalid audio file: {e}", "error")
            return redirect(url_for("index"))

        finally:
            # Clean up both temporary files
            cleanup_audio_file(original_tmp_path)
            cleanup_audio_file(normalized_tmp_path)

    except ModelNotFoundError as e:
        flash(f"Model not available: {e}", "error")
        return redirect(url_for("index"))

    except InferenceError as e:
        flash(f"Analysis failed: {e}", "error")
        return redirect(url_for("index"))

    except Exception as e:
        flash(f"Unexpected error: {e}", "error")
        return redirect(url_for("index"))


@app.route("/about")
def about():
    """Render the about page with disclaimers."""
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
