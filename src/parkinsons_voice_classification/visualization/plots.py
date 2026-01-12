"""
Plotting Functions for Feature Importance

Creates publication-quality figures for:
- Feature importance bar charts
- Cross-model comparison heatmaps
- Feature category breakdowns
"""

from typing import Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from pathlib import Path

# Use a clean style for thesis figures
plt.style.use("seaborn-v0_8-whitegrid")

# Feature category definitions (for Dataset A features)
FEATURE_CATEGORIES = {
    "Pitch (F0)": ["f0_mean", "f0_std", "f0_min", "f0_max"],
    "Jitter": ["jitter_local", "jitter_rap", "jitter_ppq5"],
    "Shimmer": ["shimmer_local", "shimmer_apq3", "shimmer_apq5"],
    "Harmonicity": ["hnr_mean", "autocorr_harmonicity"],
    "Intensity": ["intensity_mean", "intensity_std", "intensity_range"],
    "Formants": ["f1_mean", "f2_mean", "f3_mean", "f1_std", "f2_std", "f3_std"],
    "MFCC": [f"mfcc_{i}_mean" for i in range(13)],
    "Delta MFCC": [f"delta_mfcc_{i}_mean" for i in range(13)],
}

# Color palette for categories
CATEGORY_COLORS = {
    "Pitch (F0)": "#E63946",
    "Jitter": "#F4A261",
    "Shimmer": "#E9C46A",
    "Harmonicity": "#2A9D8F",
    "Intensity": "#264653",
    "Formants": "#8338EC",
    "MFCC": "#3A86FF",
    "Delta MFCC": "#06D6A0",
    "Other": "#6C757D",
}


def get_feature_category(feature_name: str) -> str:
    """Get the category for a feature name."""
    for category, features in FEATURE_CATEGORIES.items():
        if feature_name in features:
            return category
    return "Other"


def plot_feature_importance(
    summary_df: pd.DataFrame,
    model: str,
    method: str = "native",
    top_n: int = 20,
    title: str | None = None,
    figsize: tuple = (10, 8),
    save_path: Path | str | None = None,
) -> Figure:
    """
    Plot horizontal bar chart of feature importance.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores (from summarize_importance)
    model : str
        Model name to plot
    method : str
        Importance method ('native' or 'permutation')
    top_n : int
        Number of top features to show
    title : str, optional
        Plot title
    figsize : tuple
        Figure size
    save_path : Path or str, optional
        Path to save figure

    Returns
    -------
    Figure
        Matplotlib figure object
    """
    # Filter data
    mask = (summary_df["model"] == model) & (summary_df["method"] == method)
    df = summary_df[mask].nsmallest(top_n, "rank").copy()

    # Sort by importance for plotting
    df = df.sort_values("mean", ascending=True)

    # Get colors by category
    colors = [CATEGORY_COLORS.get(get_feature_category(f), "#6C757D") for f in df["feature"]]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot bars with error bars
    y_pos = np.arange(len(df))
    bars = ax.barh(y_pos, df["mean"], xerr=df["std"], color=colors, alpha=0.8, capsize=3)

    # Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["feature"])
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("Feature")

    if title is None:
        method_label = "Gini Importance" if method == "native" and "Random" in model else "Importance"
        if method == "permutation":
            method_label = "Permutation Importance"
        elif "Logistic" in model:
            method_label = "|Coefficient|"
        title = f"Top {top_n} Features - {model} ({method_label})"

    ax.set_title(title, fontsize=12, fontweight="bold")

    # Add legend for categories
    present_categories = set(get_feature_category(f) for f in df["feature"])
    legend_patches = [
        mpatches.Patch(color=CATEGORY_COLORS.get(cat, "#6C757D"), label=cat)
        for cat in present_categories
        if cat != "Other"
    ]
    if legend_patches:
        ax.legend(handles=legend_patches, loc="lower right", fontsize=9)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"  Saved: {save_path}")

    return fig


def plot_importance_comparison(
    summary_df: pd.DataFrame,
    models: list[str],
    method: str = "native",
    top_n: int = 15,
    title: str | None = None,
    figsize: tuple = (12, 8),
    save_path: Path | str | None = None,
) -> Figure:
    """
    Plot side-by-side comparison of feature importance across models.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores
    models : list[str]
        Models to compare
    method : str
        Importance method
    top_n : int
        Number of top features per model
    title : str, optional
        Plot title
    figsize : tuple
        Figure size
    save_path : Path or str, optional
        Path to save figure

    Returns
    -------
    Figure
        Matplotlib figure object
    """
    # Get union of top features across models
    top_features: set[str] = set()
    for model in models:
        mask = (summary_df["model"] == model) & (summary_df["method"] == method)
        model_df = summary_df[mask].nsmallest(top_n, "rank")
        top_features.update(model_df["feature"])

    # Filter to top features
    mask = (summary_df["method"] == method) & (summary_df["feature"].isin(top_features))
    df = summary_df[mask].copy()

    # Pivot for grouped bar chart
    pivot = df.pivot_table(index="feature", columns="model", values="mean", aggfunc=lambda x: x.iloc[0] if len(x) > 0 else np.nan)

    # Sort by average importance across models
    pivot["_avg"] = pivot.mean(axis=1)
    pivot = pivot.sort_values("_avg", ascending=True).drop("_avg", axis=1)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Bar positions
    y_pos = np.arange(len(pivot))
    bar_width = 0.8 / len(models)
    colors = ["#3A86FF", "#E63946", "#2A9D8F"]

    for i, model in enumerate(models):
        if model in pivot.columns:
            offset = (i - len(models) / 2 + 0.5) * bar_width
            ax.barh(
                y_pos + offset,
                pivot[model],
                height=bar_width,
                label=model,
                color=colors[i % len(colors)],
                alpha=0.8,
            )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel("Importance Score (normalized)")
    ax.set_ylabel("Feature")

    if title is None:
        title = f"Feature Importance Comparison ({len(top_features)} features)"
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(loc="lower right")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"  Saved: {save_path}")

    return fig


def plot_top_features_heatmap(
    summary_df: pd.DataFrame,
    models: list[str],
    method: str = "native",
    top_n: int = 20,
    title: str | None = None,
    figsize: tuple = (10, 10),
    save_path: Path | str | None = None,
) -> Figure:
    """
    Plot heatmap of normalized feature importance across models.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores
    models : list[str]
        Models to include
    method : str
        Importance method
    top_n : int
        Number of features to show
    title : str, optional
        Plot title
    figsize : tuple
        Figure size
    save_path : Path or str, optional
        Path to save figure

    Returns
    -------
    Figure
        Matplotlib figure object
    """
    # Get union of top features
    top_features: set[str] = set()
    for model in models:
        mask = (summary_df["model"] == model) & (summary_df["method"] == method)
        model_df = summary_df[mask].nsmallest(top_n, "rank")
        top_features.update(model_df["feature"])

    # Filter and pivot
    mask = (summary_df["method"] == method) & (summary_df["feature"].isin(top_features))
    df = summary_df[mask].copy()

    pivot = df.pivot_table(index="feature", columns="model", values="mean", aggfunc=lambda x: x.iloc[0] if len(x) > 0 else np.nan)
    pivot = pivot[models]  # Reorder columns

    # Normalize each column to [0, 1]
    pivot_norm = pivot.apply(lambda x: (x - x.min()) / (x.max() - x.min() + 1e-10))

    # Sort by average normalized importance
    pivot_norm["_avg"] = pivot_norm.mean(axis=1)
    pivot_norm = pivot_norm.sort_values("_avg", ascending=False).drop("_avg", axis=1)

    # Create heatmap
    fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(pivot_norm.values, cmap="YlOrRd", aspect="auto")

    # Labels
    ax.set_xticks(np.arange(len(models)))
    ax.set_xticklabels(models, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(pivot_norm)))
    ax.set_yticklabels(pivot_norm.index)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Normalized Importance", rotation=270, labelpad=15)

    # Add text annotations
    values_array = pivot_norm.to_numpy()
    for i in range(len(pivot_norm)):
        for j in range(len(models)):
            val = values_array[i, j]
            color = "white" if val > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8)

    if title is None:
        title = "Feature Importance Heatmap (Normalized)"
    ax.set_title(title, fontsize=12, fontweight="bold")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"  Saved: {save_path}")

    return fig


def plot_feature_importance_by_category(
    summary_df: pd.DataFrame,
    model: str,
    method: str = "native",
    title: str | None = None,
    figsize: tuple = (10, 6),
    save_path: Path | str | None = None,
) -> Figure:
    """
    Plot aggregated feature importance by category.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores
    model : str
        Model name
    method : str
        Importance method
    title : str, optional
        Plot title
    figsize : tuple
        Figure size
    save_path : Path or str, optional
        Path to save figure

    Returns
    -------
    Figure
        Matplotlib figure object
    """
    mask = (summary_df["model"] == model) & (summary_df["method"] == method)
    df: pd.DataFrame = summary_df[mask].copy()

    # Add category column
    df["category"] = df["feature"].apply(get_feature_category)

    # Aggregate by category (sum of importance)
    category_importance = df.groupby("category")["mean"].sum().sort_values(ascending=True)

    # Filter out categories with no features
    category_importance = category_importance[category_importance > 0]

    # Get colors
    colors = [CATEGORY_COLORS.get(cat, "#6C757D") for cat in category_importance.index]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.barh(list(category_importance.index), list(category_importance.values), color=colors, alpha=0.8)

    ax.set_xlabel("Aggregated Importance Score")
    ax.set_ylabel("Feature Category")

    if title is None:
        title = f"Feature Importance by Category - {model}"
    ax.set_title(title, fontsize=12, fontweight="bold")

    # Add value labels
    for bar, val in zip(bars, category_importance.values):
        ax.text(val + 0.01 * max(category_importance), bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=9)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"  Saved: {save_path}")

    return fig


def plot_dataset_comparison(
    importance_a: pd.DataFrame,
    importance_b: pd.DataFrame,
    common_features: list[str],
    model: str = "RandomForest",
    title: str | None = None,
    figsize: tuple = (10, 8),
    save_path: Path | str | None = None,
) -> Figure:
    """
    Compare feature importance rankings between Dataset A and Dataset B.

    Only compares features that exist in both datasets.

    Parameters
    ----------
    importance_a : pd.DataFrame
        Summarized importance for Dataset A
    importance_b : pd.DataFrame
        Summarized importance for Dataset B
    common_features : list[str]
        Features present in both datasets
    model : str
        Model to compare
    title : str, optional
        Plot title
    figsize : tuple
        Figure size
    save_path : Path or str, optional
        Path to save figure

    Returns
    -------
    Figure
        Matplotlib figure object
    """
    # Filter to common features and model
    mask_a = (
        (importance_a["model"] == model)
        & (importance_a["method"] == "native")
        & (importance_a["feature"].isin(common_features))
    )
    mask_b = (
        (importance_b["model"] == model)
        & (importance_b["method"] == "native")
        & (importance_b["feature"].isin(common_features))
    )

    df_a = importance_a[mask_a].set_index("feature")["mean"]
    df_b = importance_b[mask_b].set_index("feature")["mean"]

    # Normalize to [0, 1]
    df_a_norm = (df_a - df_a.min()) / (df_a.max() - df_a.min() + 1e-10)
    df_b_norm = (df_b - df_b.min()) / (df_b.max() - df_b.min() + 1e-10)

    # Combine
    combined = pd.DataFrame({"Dataset A": df_a_norm, "Dataset B": df_b_norm})
    combined = combined.dropna()

    # Sort by average
    combined["_avg"] = combined.mean(axis=1)
    combined = combined.sort_values("_avg", ascending=True).drop("_avg", axis=1)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    y_pos = np.arange(len(combined))
    bar_width = 0.35

    ax.barh(y_pos - bar_width / 2, combined["Dataset A"], bar_width, label="Dataset A (MDVR-KCL)", color="#3A86FF", alpha=0.8)
    ax.barh(y_pos + bar_width / 2, combined["Dataset B"], bar_width, label="Dataset B (PD_SPEECH)", color="#E63946", alpha=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(combined.index)
    ax.set_xlabel("Normalized Importance")
    ax.set_ylabel("Feature")
    ax.legend(loc="lower right")

    if title is None:
        title = f"Feature Importance: Dataset A vs Dataset B ({model})"
    ax.set_title(title, fontsize=12, fontweight="bold")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"  Saved: {save_path}")

    return fig
