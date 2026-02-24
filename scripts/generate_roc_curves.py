#!/usr/bin/env python
"""
Standalone script to generate ROC curve plots.

Uses Extended feature set (78 features, unweighted) — the best-performing
experimental condition — to produce publication-quality ROC curve figures
for all three datasets/tasks.

Each figure shows one mean ROC curve per classifier (bold) with per-fold
curves in the background (faint) and a ±1 std shaded band.

Outputs:
    outputs/plots/roc_curve_ReadText.pdf
    outputs/plots/roc_curve_SpontaneousDialogue.pdf
    outputs/plots/roc_curve_DatasetB.pdf
"""

from pathlib import Path

# Override config before any config-dependent imports
import parkinsons_voice_classification.config as _cfg
_cfg.USE_EXTENDED_FEATURES = True  # Use best condition: extended, unweighted

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt

from parkinsons_voice_classification.data.mdvr_kcl import load_features as load_mdvr_features
from parkinsons_voice_classification.data.pd_speech import load_features as load_pd_speech_features
from parkinsons_voice_classification.models.training import run_cv_for_roc
from parkinsons_voice_classification.visualization.plots import plot_roc_curves
from parkinsons_voice_classification.config import OUTPUTS_DIR


def main() -> None:
    plots_dir = OUTPUTS_DIR / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERATING ROC CURVES")
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
        roc_data = run_cv_for_roc(X, y, groups=groups, use_groups=True)
        save_path = plots_dir / "roc_curve_ReadText.pdf"
        fig = plot_roc_curves(
            roc_data,
            title="ROC Curves — ReadText (Extended, Grouped 5-Fold CV, $n=37$)",
            save_path=save_path,
        )
        plt.close(fig)
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
        roc_data = run_cv_for_roc(X, y, groups=groups, use_groups=True)
        save_path = plots_dir / "roc_curve_SpontaneousDialogue.pdf"
        fig = plot_roc_curves(
            roc_data,
            title="ROC Curves — Spontaneous Dialogue (Extended, Grouped 5-Fold CV, $n=36$)",
            save_path=save_path,
        )
        plt.close(fig)
        print(f"  ✓ Saved: {save_path.name}")
    except FileNotFoundError as exc:
        print(f"  ✗ Skipped: {exc}")

    # ------------------------------------------------------------------ #
    # Dataset B — PD Speech Features                                       #
    # ------------------------------------------------------------------ #
    print("\n[3/3] Dataset B — PD Speech Features (Stratified 5-Fold CV)")
    X, y = load_pd_speech_features()
    print(f"  Loaded {X.shape[0]} samples, {X.shape[1]} features")
    roc_data = run_cv_for_roc(X, y, use_groups=False)
    save_path = plots_dir / "roc_curve_DatasetB.pdf"
    fig = plot_roc_curves(
        roc_data,
        title="ROC Curves — Dataset B (Stratified 5-Fold CV, $n=756$)",
        save_path=save_path,
    )
    plt.close(fig)
    print(f"  ✓ Saved: {save_path.name}")

    plt.close("all")

    print("\n" + "=" * 65)
    print("Done. Run 'make sync-figures' to copy plots to thesis/figures/")
    print("=" * 65)


if __name__ == "__main__":
    main()
