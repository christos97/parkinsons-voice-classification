.PHONY: help install clean extract-all extract-readtext extract-spontaneous experiments test format lint check-types train-demo-model demo demo-dev demo-install thesis thesis-clean thesis-watch

# Default target
help:
	@echo "Parkinson's Voice Classification - Available Commands"
	@echo "======================================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install project dependencies via Poetry"
	@echo "  make dev-install          Install with development dependencies"
	@echo ""
	@echo "Feature Extraction (Dataset A - MDVR-KCL):"
	@echo "  make extract-all          Extract features for both speech tasks"
	@echo "  make extract-readtext     Extract features for ReadText task only"
	@echo "  make extract-spontaneous  Extract features for SpontaneousDialogue task only"
	@echo ""
	@echo "Experiments:"
	@echo "  make experiments          Run all experiments (Dataset A + Dataset B)"
	@echo "  make results              Display experiment results summary"
	@echo ""
	@echo "Demo Application:"
	@echo "  make demo-install         Install demo dependencies (Flask)"
	@echo "  make train-demo-model     Train inference model for demo"
	@echo "  make demo                 Run Flask demo application"
	@echo "  make demo-dev             Run Flask demo in debug mode (auto-reload)"
	@echo ""
	@echo "Quality Assurance:"
	@echo "  make test                 Run test suite"
	@echo "  make check-types          Run type checking with Pylance"
	@echo "  make lint                 Run code linting"
	@echo ""
	@echo "Thesis (LaTeX):"
	@echo "  make thesis               Build thesis PDF (latexmk)"
	@echo "  make thesis-watch         Build thesis with auto-rebuild on changes"
	@echo "  make thesis-clean         Remove LaTeX build artifacts"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean                Remove generated outputs (features + results)"
	@echo "  make clean-features       Remove only extracted features"
	@echo "  make clean-results        Remove only experiment results"
	@echo "  make clean-all            Remove outputs and Python cache files"
	@echo ""

# ============================================================================
# Installation & Setup
# ============================================================================

install:
	@echo "Installing project dependencies..."
	poetry install --no-dev

dev-install:
	@echo "Installing project with development dependencies..."
	poetry install

# ============================================================================
# Feature Extraction (Dataset A - MDVR-KCL)
# ============================================================================

extract-all:
	@echo "Extracting features for all speech tasks..."
	poetry run pvc-extract --task all

extract-readtext:
	@echo "Extracting features for ReadText task..."
	poetry run pvc-extract --task ReadText

extract-spontaneous:
	@echo "Extracting features for SpontaneousDialogue task..."
	poetry run pvc-extract --task SpontaneousDialogue

# ============================================================================
# Experiments
# ============================================================================

experiments:
	@echo "Running all experiments..."
	@echo "This will process:"
	@echo "  1. Dataset A - ReadText (Grouped CV)"
	@echo "  2. Dataset A - SpontaneousDialogue (Grouped CV)"
	@echo "  3. Dataset B - PD Speech Features (Standard CV)"
	@echo ""
	poetry run pvc-experiment

results:
	@echo "Experiment Results Summary:"
	@echo "============================"
	@if [ -f outputs/results/summary.csv ]; then \
		cat outputs/results/summary.csv | column -t -s','; \
	else \
		echo "No results found. Run 'make experiments' first."; \
	fi

# ============================================================================
# Demo Application
# ============================================================================

demo-install:
	@echo "Installing demo dependencies (Flask)..."
	poetry install --with demo
	@echo "Demo dependencies installed."

train-demo-model:
	@echo "Training inference model for demo app..."
	@echo "  Model: RandomForest"
	@echo "  Task: ReadText"
	@echo "  Features: baseline (47)"
	@echo ""
	@if [ ! -f outputs/features/baseline/features_readtext.csv ]; then \
		echo "Error: Features not found. Run 'make extract-readtext' first."; \
		exit 1; \
	fi
	poetry run pvc-train --task ReadText --model RandomForest --feature-set baseline
	@echo ""
	@echo "✓ Model trained and saved to outputs/models/"

demo: 
	@echo "Starting Flask demo application..."
	@if [ ! -f outputs/models/RandomForest_ReadText_baseline.joblib ]; then \
		echo "Error: Inference model not found."; \
		echo "Run 'make train-demo-model' first."; \
		exit 1; \
	fi
	@echo "Visit http://127.0.0.1:5000 in your browser"
	@echo "Press Ctrl+C to stop"
	@echo ""
	cd demo_app && poetry run flask --app app run --host 127.0.0.1 --port 5000

demo-dev:
	@echo "Starting Flask demo application in DEBUG mode..."
	@if [ ! -f outputs/models/RandomForest_ReadText_baseline.joblib ]; then \
		echo "Error: Inference model not found."; \
		echo "Run 'make train-demo-model' first."; \
		exit 1; \
	fi
	@echo "Visit http://127.0.0.1:5000 in your browser"
	@echo "Press Ctrl+C to stop"
	@echo "Debug mode: auto-reload enabled"
	@echo ""
	cd demo_app && FLASK_ENV=development poetry run flask --app app run --host 127.0.0.1 --port 5000 --debug

# ============================================================================
# Quality Assurance
# ============================================================================

test:
	@echo "Running test suite..."
	poetry run pytest -v

format:
	@echo "✨ Formatting code with black..."
	poetry run black src/ --line-length=100
	@echo "✓ Formatting complete"

check-types:
	@echo "Running type checks..."
	@echo "Note: This requires Pylance/Pyright to be installed"
	@command -v pyright >/dev/null 2>&1 && pyright src/ || echo "pyright not found. Install with: npm install -g pyright"

lint:
	@echo "Running linting checks..."
	@command -v ruff >/dev/null 2>&1 && ruff check src/ || echo "ruff not found. Install with: pip install ruff"

# ============================================================================
# Maintenance & Cleanup
# ============================================================================

clean-features:
	@echo "Removing extracted features..."
	rm -rf outputs/features/*.csv
	@echo "Features cleaned."

clean-results:
	@echo "Removing experiment results..."
	rm -rf outputs/results/*.csv
	@echo "Results cleaned."

clean:
	@echo "Removing all outputs..."
	rm -rf outputs/features/*.csv
	rm -rf outputs/results/*.csv
	@echo "Outputs cleaned."

clean-all: clean
	@echo "Removing Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "All cleaned."

# ============================================================================
# Quick Workflow Shortcuts
# ============================================================================

# Full pipeline: extract features and run experiments
pipeline: extract-all experiments
	@echo ""
	@echo "Pipeline complete! Results saved to outputs/results/"

# Quick check: verify dataset structure
check-dataset:
	@echo "Checking dataset structure..."
	@echo ""
	@echo "Dataset A (MDVR-KCL):"
	@find assets/DATASET_MDVR_KCL -type f -name "*.wav" | wc -l | xargs echo "  Total WAV files:"
	@find assets/DATASET_MDVR_KCL/ReadText -type f -name "*.wav" | wc -l | xargs echo "  ReadText:"
	@find assets/DATASET_MDVR_KCL/SpontaneousDialogue -type f -name "*.wav" | wc -l | xargs echo "  SpontaneousDialogue:"
	@echo ""
	@echo "Dataset B (PD Speech Features):"
	@if [ -f assets/PD_SPEECH_FEATURES.csv ]; then \
		wc -l assets/PD_SPEECH_FEATURES.csv | awk '{print "  Rows:", $$1-1, "(excluding header)"}'; \
	else \
		echo "  File not found!"; \
	fi
	@echo ""
	@echo "Extracted Features:"
	@if [ -d outputs/features ]; then \
		ls -lh outputs/features/*.csv 2>/dev/null || echo "  No features extracted yet"; \
	else \
		echo "  No features extracted yet"; \
	fi

# Show project information
info:
	@echo "Project Information"
	@echo "==================="
	@echo "Name: Parkinson's Disease Voice Classification"
	@echo "Type: Master's Thesis Research Project"
	@echo "Scope: Binary classification (PD vs HC)"
	@echo ""
	@echo "Datasets:"
	@echo "  - Dataset A: MDVR-KCL (raw audio, 2 tasks)"
	@echo "  - Dataset B: PD Speech Features (pre-extracted)"
	@echo ""
	@echo "Models: Logistic Regression, SVM, Random Forest"
	@echo "Evaluation: Stratified K-Fold Cross-Validation"
	@echo ""
	@poetry --version 2>/dev/null || echo "Poetry not installed"
	@python --version 2>/dev/null || echo "Python not found"

# ============================================================================
# Thesis (LaTeX)
# ============================================================================

.PHONY: sync-figures
sync-figures: ## Sync experiment figures to thesis folder
	poetry run python scripts/sync_figures.py

thesis: sync-figures
	@echo "Building thesis PDF (using latexmk)..."
	@cd thesis && latexmk -pdf -interaction=nonstopmode -quiet -f main.tex 2>/dev/null || latexmk -pdf -interaction=nonstopmode -quiet main.tex
	@echo "✓ Thesis PDF built successfully: thesis/main.pdf"
	@cd thesis && pdfinfo main.pdf 2>/dev/null | grep "Pages:" | awk '{print "  Pages:", $$2}' || true
	@cd thesis && test -s main.bbl && grep -c '\\bibitem\[' main.bbl 2>/dev/null | awk '{print "  Bibliography entries:", $$1}' || echo "  Bibliography entries: 0"

thesis-watch:
	@echo "Building thesis PDF with auto-rebuild (Ctrl+C to stop)..."
	cd thesis && latexmk -pdf -pvc -interaction=nonstopmode main.tex

thesis-clean:
	@echo "Cleaning LaTeX build artifacts..."
	@rm -f thesis/main.{aux,bbl,blg,log,out,toc,lof,lot,fls,fdb_latexmk,pdf}
	@rm -f thesis/chapters/*.aux
	@rm -f thesis/frontmatter/*.aux
	@rm -f thesis/appendices/*.aux
	@echo "✓ Cleaned all LaTeX build artifacts"
