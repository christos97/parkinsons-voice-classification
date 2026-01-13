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

# Import ONLY the stable inference interface
from parkinsons_voice_classification.inference import (
    run_inference,
    get_model_info,
    InferenceError,
    ModelNotFoundError,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")

# Allowed audio extensions
ALLOWED_EXTENSIONS = {".wav"}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


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
    """Process uploaded WAV file and return prediction."""
    # Check if file was uploaded
    if "audio_file" not in request.files:
        flash("No file uploaded", "error")
        return redirect(url_for("index"))

    file = request.files["audio_file"]

    # Check if file was selected
    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("index"))

    # Validate file extension
    if not file.filename or not allowed_file(file.filename):
        flash("Invalid file type. Please upload a WAV file.", "error")
        return redirect(url_for("index"))

    # Save to temp file and run inference
    try:
        # Create temp file with .wav extension (required by librosa)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Run inference through the stable API
            result = run_inference(tmp_path, task="ReadText")

            return render_template(
                "result.html",
                result=result,
                filename=file.filename,
            )

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

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
