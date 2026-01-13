#!/usr/bin/env python
"""
Feature Importance Analysis CLI

Runs feature importance analysis on all experiments and generates:
- CSV tables with ranked features
- Bar charts for each model/dataset
- Comparison heatmaps
- Category-level importance plots
"""

import argparse
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for saving figures
import matplotlib.pyplot as plt

from parkinsons_voice_classification.config import OUTPUTS_DIR
from parkinsons_voice_classification.data.mdvr_kcl import (
    load_features as load_mdvr_features,
    get_feature_names as get_mdvr_feature_names,
)
from parkinsons_voice_classification.data.pd_speech import (
    load_features as load_pd_speech_features,
    get_feature_names as get_pd_speech_feature_names,
)
from parkinsons_voice_classification.models.feature_importance import (
    run_importance_cv,
    summarize_importance,
    get_top_features,
)
from parkinsons_voice_classification.visualization.plots import (
    plot_feature_importance,
    plot_importance_comparison,
    plot_top_features_heatmap,
    plot_feature_importance_by_category,
    plot_dataset_comparison,
)


def run_importance_analysis(
    X, y, feature_names, groups=None, use_groups=False, use_permutation=False
):
    """Run importance analysis and return raw + summarized results."""
    raw = run_importance_cv(
        X,
        y,
        feature_names,
        groups=groups,
        use_groups=use_groups,
        use_permutation=use_permutation,
    )
    summary = summarize_importance(raw)
    return raw, summary


def save_top_features_table(summary_df, output_path, top_n=20):
    """Save formatted top features table for all models."""
    tables = []
    for model in summary_df["model"].unique():
        for method in summary_df["method"].unique():
            top = get_top_features(summary_df, model, method, top_n)
            top["model"] = model
            top["method"] = method
            tables.append(top)

    combined = pd.concat(tables, ignore_index=True)
    combined = combined[["model", "method", "rank", "feature", "mean", "std"]]
    combined.to_csv(output_path, index=False)
    print(f"  Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Run feature importance analysis for PD voice classification"
    )
    parser.add_argument(
        "--permutation",
        action="store_true",
        help="Also compute permutation importance (slower)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of top features to display in plots (default: 20)",
    )
    args = parser.parse_args()

    # Setup output directories
    results_dir = OUTPUTS_DIR / "results"
    plots_dir = OUTPUTS_DIR / "plots"
    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 70)

    all_importance = []
    dataset_a_importance = None

    # =========================================================================
    # Dataset A - ReadText
    # =========================================================================
    print("\n[1/3] Dataset A - ReadText")
    print("-" * 70)

    try:
        X, y, groups = load_mdvr_features("ReadText")
        feature_names = get_mdvr_feature_names("ReadText")
        print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")

        raw, summary = run_importance_analysis(
            X, y, feature_names, groups=groups, use_groups=True, use_permutation=args.permutation
        )
        summary["dataset"] = "MDVR-KCL"
        summary["task"] = "ReadText"
        all_importance.append(summary)

        # Save tables
        save_top_features_table(summary, results_dir / "importance_readtext.csv", args.top_n)

        # Generate plots for each model
        for model in ["RandomForest", "LogisticRegression"]:
            fig = plot_feature_importance(
                summary,
                model,
                top_n=args.top_n,
                title=f"Top {args.top_n} Features - {model} (ReadText)",
                save_path=plots_dir / f"importance_readtext_{model.lower()}.png",
            )
            plt.close(fig)

        # Category plot for RF
        fig = plot_feature_importance_by_category(
            summary,
            "RandomForest",
            title="Feature Importance by Category - RF (ReadText)",
            save_path=plots_dir / "importance_readtext_categories.png",
        )
        plt.close(fig)

        print("  ✓ ReadText analysis complete")

    except FileNotFoundError as e:
        print(f"  ⚠ Skipped: {e}")

    # =========================================================================
    # Dataset A - SpontaneousDialogue
    # =========================================================================
    print("\n[2/3] Dataset A - SpontaneousDialogue")
    print("-" * 70)

    try:
        X, y, groups = load_mdvr_features("SpontaneousDialogue")
        feature_names = get_mdvr_feature_names("SpontaneousDialogue")
        print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")

        raw, summary = run_importance_analysis(
            X, y, feature_names, groups=groups, use_groups=True, use_permutation=args.permutation
        )
        summary["dataset"] = "MDVR-KCL"
        summary["task"] = "SpontaneousDialogue"
        all_importance.append(summary)
        dataset_a_importance = summary  # Save for cross-dataset comparison

        # Save tables
        save_top_features_table(summary, results_dir / "importance_spontaneous.csv", args.top_n)

        # Generate plots
        for model in ["RandomForest", "LogisticRegression"]:
            fig = plot_feature_importance(
                summary,
                model,
                top_n=args.top_n,
                title=f"Top {args.top_n} Features - {model} (Spontaneous)",
                save_path=plots_dir / f"importance_spontaneous_{model.lower()}.png",
            )
            plt.close(fig)

        fig = plot_feature_importance_by_category(
            summary,
            "RandomForest",
            title="Feature Importance by Category - RF (Spontaneous)",
            save_path=plots_dir / "importance_spontaneous_categories.png",
        )
        plt.close(fig)

        print("  ✓ SpontaneousDialogue analysis complete")

    except FileNotFoundError as e:
        print(f"  ⚠ Skipped: {e}")

    # =========================================================================
    # Dataset B - PD_SPEECH_FEATURES
    # =========================================================================
    print("\n[3/3] Dataset B - PD_SPEECH_FEATURES")
    print("-" * 70)

    X, y = load_pd_speech_features()
    feature_names = get_pd_speech_feature_names()
    print(f"  Loaded: {X.shape[0]} samples, {X.shape[1]} features")

    raw, summary = run_importance_analysis(
        X, y, feature_names, use_groups=False, use_permutation=args.permutation
    )
    summary["dataset"] = "PD_SPEECH_FEATURES"
    summary["task"] = "N/A"
    all_importance.append(summary)
    dataset_b_importance = summary

    # Save tables
    save_top_features_table(summary, results_dir / "importance_pd_speech.csv", args.top_n)

    # Generate plots (only top features, 752 is too many)
    for model in ["RandomForest", "LogisticRegression"]:
        fig = plot_feature_importance(
            summary,
            model,
            top_n=args.top_n,
            title=f"Top {args.top_n} Features - {model} (PD_SPEECH)",
            save_path=plots_dir / f"importance_pd_speech_{model.lower()}.png",
        )
        plt.close(fig)

    print("  ✓ PD_SPEECH_FEATURES analysis complete")

    # =========================================================================
    # Cross-model comparison for each dataset
    # =========================================================================
    print("\n[4/5] Generating comparison plots...")
    print("-" * 70)

    # Combine all results
    all_df = pd.concat(all_importance, ignore_index=True)
    all_df.to_csv(results_dir / "importance_all.csv", index=False)
    print(f"  Saved: {results_dir / 'importance_all.csv'}")

    # Heatmap for Dataset A (ReadText)
    try:
        readtext_df = all_df[(all_df["dataset"] == "MDVR-KCL") & (all_df["task"] == "ReadText")]
        if len(readtext_df) > 0:
            fig = plot_top_features_heatmap(
                readtext_df,
                models=["LogisticRegression", "RandomForest"],
                top_n=15,
                title="Feature Importance Heatmap - ReadText",
                save_path=plots_dir / "heatmap_readtext.png",
            )
            plt.close(fig)
    except Exception as e:
        print(f"  ⚠ Heatmap (ReadText) failed: {e}")

    # Heatmap for Dataset A (Spontaneous)
    try:
        spont_df = all_df[
            (all_df["dataset"] == "MDVR-KCL") & (all_df["task"] == "SpontaneousDialogue")
        ]
        if len(spont_df) > 0:
            fig = plot_top_features_heatmap(
                spont_df,
                models=["LogisticRegression", "RandomForest"],
                top_n=15,
                title="Feature Importance Heatmap - Spontaneous",
                save_path=plots_dir / "heatmap_spontaneous.png",
            )
            plt.close(fig)
    except Exception as e:
        print(f"  ⚠ Heatmap (Spontaneous) failed: {e}")

    # =========================================================================
    # Cross-dataset comparison (common features only)
    # =========================================================================
    print("\n[5/5] Cross-dataset comparison...")
    print("-" * 70)

    if dataset_a_importance is not None:
        # Find common features between datasets
        features_a = set(dataset_a_importance["feature"].unique())
        features_b = set(dataset_b_importance["feature"].unique())

        # Map common feature types (approximate matching)
        # Dataset A has: f0_mean, jitter_local, shimmer_local, hnr_mean, mfcc_0_mean, etc.
        # Dataset B has: locPctJitter, meanAutoCorrHarmonicity, mean_MFCC_0, etc.

        # Direct intersection (unlikely to have exact matches)
        common_features = list(features_a & features_b)

        if len(common_features) > 0:
            fig = plot_dataset_comparison(
                dataset_a_importance,
                dataset_b_importance,
                common_features,
                model="RandomForest",
                save_path=plots_dir / "comparison_datasets.png",
            )
            plt.close(fig)
            print(f"  Found {len(common_features)} common features for comparison")
        else:
            print("  ⚠ No exact feature name matches between datasets")
            print("  Feature comparison requires manual mapping (different naming conventions)")

    # =========================================================================
    # Summary output
    # =========================================================================
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\nOutputs saved to:")
    print(f"  Tables: {results_dir}/")
    print(f"  Plots:  {plots_dir}/")

    # Print top 5 features for each dataset/model (quick summary)
    print("\n" + "-" * 70)
    print("TOP 5 FEATURES BY DATASET (RandomForest, Gini Importance)")
    print("-" * 70)

    for dataset in list(all_df["dataset"].unique()):
        for task in list(all_df[all_df["dataset"] == dataset]["task"].unique()):
            mask = (
                (all_df["dataset"] == dataset)
                & (all_df["task"] == task)
                & (all_df["model"] == "RandomForest")
                & (all_df["method"] == "native")
            )
            df_subset = all_df[mask].nsmallest(5, "rank")
            if len(df_subset) > 0:
                print(f"\n{dataset} - {task}:")
                for _, row in df_subset.iterrows():
                    print(
                        f"  {int(row['rank']):2d}. {row['feature']:30s} {row['mean']:.4f} ± {row['std']:.4f}"
                    )


if __name__ == "__main__":
    main()
