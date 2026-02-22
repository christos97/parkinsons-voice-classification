#!/usr/bin/env python
"""
Standalone script to generate confusion matrix plots.

Uses Extended feature set (78 features, unweighted) — the best-performing
experimental condition — to produce publication-quality confusion matrices
for all three datasets/tasks.

Outputs:
    outputs/plots/confusion_matrix_ReadText.pdf
    outputs/plots/confusion_matrix_SpontaneousDialogue.pdf
    outputs/plots/confusion_matrix_DatasetB.pdf
"""

import sys
from pathlib import Path

# Temporarily override config flag before any imports that depend on config
import parkinsons_voice_classification.config as _cfg
_cfg.USE_EXTENDED_FEATURES = True  # Use best condition: extended, unweighted

from parkinsons_voice_classification.data.mdvr_kcl import load_features as load_mdvr_features
from parkinsons_voice_classification.data.pd_speech import load_features as load_pd_speech_features
from parkinsons_voice_classification.models.training import run_cv
from parkinsons_voice_classification.visualization.plots import plot_confusion_matrix
from parkinsons_voice_classification.config import OUTPUTS_DIR

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend


def main() -> None:
    plots_dir = OUTPUTS_DIR / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERATING CONFUSION MATRICES")
    print("Feature set : Extended (78 features)")
    print("Weighting   : Unweighted (baseline class weights)")
    print(f"Output dir  : {plots_dir}")
    print("=" * 65)

    # ------------------------------------------------------------------ #
    # Dataset A — ReadText                                                 #
    # ------------------------------------------------------------------ #
    print("\n[1/3] Dataset A — ReadText (Grouped 5-Fold CV)")
    try:
        X, y, groups = load_mdvr_features("ReadText")
        print(f"  Loaded {X.shape[0]} samples, {X.shape[1]} features, "
              f"{len(set(groups))} subjects")
        _, preds = run_cv(X, y, groups=groups, use_groups=True,
                          collect_predictions=True)
        save_path = plots_dir / "confusion_matrix_ReadText.pdf"
        plot_confusion_matrix(
            preds,
            title="Confusion Matrices — ReadText (Extended, Grouped 5-Fold CV)",
            save_path=save_path,
        )
        print(f"  ✓ Saved: {save_path.name}")
    except FileNotFoundError as exc:
        print(f"  ✗ Skipped: {exc}")

    # ------------------------------------------------------------------ #
    # Dataset A — SpontaneousDialogue                                      #
    # ------------------------------------------------------------------ #
    print("\n[2/3] Dataset A — SpontaneousDialogue (Grouped 5-Fold CV)")
    try:
        X, y, groups = load_mdvr_features("SpontaneousDialogue")
        print(f"  Loaded {X.shape[0]} samples, {X.shape[1]} features, "
              f"{len(set(groups))} subjects")
        _, preds = run_cv(X, y, groups=groups, use_groups=True,
                          collect_predictions=True)
        save_path = plots_dir / "confusion_matrix_SpontaneousDialogue.pdf"
        plot_confusion_matrix(
            preds,
            title="Confusion Matrices — Spontaneous Dialogue (Extended, Grouped 5-Fold CV)",
            save_path=save_path,
        )
        print(f"  ✓ Saved: {save_path.name}")
    except FileNotFoundError as exc:
        print(f"  ✗ Skipped: {exc}")

    # ------------------------------------------------------------------ #
    # Dataset B — PD Speech Features                                       #
    # ------------------------------------------------------------------ #
    print("\n[3/3] Dataset B — PD Speech Features (Stratified 5-Fold CV)")
    X, y = load_pd_speech_features()
    print(f"  Loaded {X.shape[0]} samples, {X.shape[1]} features")
    _, preds = run_cv(X, y, use_groups=False, collect_predictions=True)
    save_path = plots_dir / "confusion_matrix_DatasetB.pdf"
    plot_confusion_matrix(
        preds,
        title="Confusion Matrices — Dataset B (Stratified 5-Fold CV)",
        save_path=save_path,
    )
    print(f"  ✓ Saved: {save_path.name}")

    import matplotlib.pyplot as plt
    plt.close("all")

    print("\n" + "=" * 65)
    print("Done. Run 'make sync-figures' to copy plots to thesis/figures/")
    print("=" * 65)


if __name__ == "__main__":
    main()
