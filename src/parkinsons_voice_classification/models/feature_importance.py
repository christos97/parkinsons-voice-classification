"""
Feature Importance Analysis

Extracts and aggregates feature importance scores from trained models:
- Random Forest: Gini importance (feature_importances_)
- Logistic Regression: Absolute coefficients (|coef_|)
- SVM (RBF): Permutation importance (model-agnostic)

All methods return importance scores aggregated across CV folds.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from sklearn.inspection import permutation_importance
from sklearn.base import clone

from parkinsons_voice_classification.config import RANDOM_SEED, N_FOLDS
from parkinsons_voice_classification.models.classifiers import get_models


def extract_model_importance(
    model, feature_names: list[str], method: str = "native"
) -> np.ndarray | None:
    """
    Extract feature importance from a fitted model.

    Parameters
    ----------
    model : sklearn Pipeline
        Fitted model pipeline
    feature_names : list[str]
        Names of features (for validation)
    method : str
        'native' for built-in importance, 'permutation' for permutation importance

    Returns
    -------
    np.ndarray or None
        Importance scores (shape: n_features) or None if not available
    """
    clf = model.named_steps["clf"]

    # Random Forest: Gini importance
    if hasattr(clf, "feature_importances_"):
        return clf.feature_importances_

    # Logistic Regression: Absolute coefficients
    if hasattr(clf, "coef_"):
        # For binary classification, coef_ has shape (1, n_features)
        return np.abs(clf.coef_).ravel()

    return None


def compute_permutation_importance(
    model,
    X_test: np.ndarray,
    y_test: np.ndarray,
    n_repeats: int = 10,
) -> np.ndarray:
    """
    Compute permutation importance for any model.

    Parameters
    ----------
    model : sklearn Pipeline
        Fitted model pipeline
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
    n_repeats : int
        Number of permutation repeats

    Returns
    -------
    np.ndarray
        Mean permutation importance scores
    """
    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=n_repeats,
        random_state=RANDOM_SEED,
        scoring="accuracy",
    )
    # result is a Bunch object with importances_mean attribute
    return np.asarray(result["importances_mean"])


def run_importance_cv(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: list[str],
    groups: np.ndarray | None = None,
    use_groups: bool = False,
    n_folds: int = N_FOLDS,
    use_permutation: bool = False,
) -> pd.DataFrame:
    """
    Run cross-validation and collect feature importance scores.

    Parameters
    ----------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Label array
    feature_names : list[str]
        Names of features
    groups : np.ndarray, optional
        Group labels for grouped CV
    use_groups : bool
        If True, use StratifiedGroupKFold
    n_folds : int
        Number of CV folds
    use_permutation : bool
        If True, also compute permutation importance for all models

    Returns
    -------
    pd.DataFrame
        Importance scores with columns: model, fold, feature, importance, method
    """
    # Select CV strategy
    if use_groups:
        if groups is None:
            raise ValueError("groups must be provided when use_groups=True")
        cv = StratifiedGroupKFold(n_splits=n_folds, shuffle=True, random_state=RANDOM_SEED)
        split_args = (X, y, groups)
    else:
        cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=RANDOM_SEED)
        split_args = (X, y)

    models = get_models()
    results = []

    for model_name, pipeline in models.items():
        for fold_idx, (train_idx, test_idx) in enumerate(cv.split(*split_args)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            # Clone and fit model
            model = clone(pipeline)
            model.fit(X_train, y_train)

            # Native importance (RF Gini or LR coef)
            native_importance = extract_model_importance(model, feature_names)
            if native_importance is not None:
                for i, fname in enumerate(feature_names):
                    results.append(
                        {
                            "model": model_name,
                            "fold": fold_idx + 1,
                            "feature": fname,
                            "importance": native_importance[i],
                            "method": "native",
                        }
                    )

            # Permutation importance (optional, for all models)
            if use_permutation:
                perm_importance = compute_permutation_importance(model, X_test, y_test)
                for i, fname in enumerate(feature_names):
                    results.append(
                        {
                            "model": model_name,
                            "fold": fold_idx + 1,
                            "feature": fname,
                            "importance": perm_importance[i],
                            "method": "permutation",
                        }
                    )

    return pd.DataFrame(results)


def summarize_importance(importance_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize importance scores with mean ± std across folds.

    Parameters
    ----------
    importance_df : pd.DataFrame
        Raw importance scores from run_importance_cv()

    Returns
    -------
    pd.DataFrame
        Summary with columns: model, method, feature, mean, std, rank
    """
    summary = (
        importance_df.groupby(["model", "method", "feature"])["importance"]
        .agg(["mean", "std"])
        .reset_index()
    )

    # Add ranking within each model/method group
    summary["rank"] = summary.groupby(["model", "method"])["mean"].rank(
        ascending=False, method="min"
    )

    # Sort by model, method, then rank
    summary = summary.sort_values(["model", "method", "rank"])

    return summary


def get_top_features(
    summary_df: pd.DataFrame,
    model: str,
    method: str = "native",
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Get top N most important features for a model.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores
    model : str
        Model name
    method : str
        Importance method ('native' or 'permutation')
    top_n : int
        Number of top features to return

    Returns
    -------
    pd.DataFrame
        Top N features with importance scores
    """
    mask = (summary_df["model"] == model) & (summary_df["method"] == method)
    return summary_df[mask].nsmallest(top_n, "rank")[
        ["feature", "mean", "std", "rank"]
    ].reset_index(drop=True)


def compare_feature_rankings(
    summary_df: pd.DataFrame,
    models: list[str] | None = None,
    method: str = "native",
) -> pd.DataFrame:
    """
    Compare feature rankings across models.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Summarized importance scores
    models : list[str], optional
        Models to compare (default: all)
    method : str
        Importance method

    Returns
    -------
    pd.DataFrame
        Wide-format table with feature ranks per model
    """
    df = summary_df[summary_df["method"] == method].copy()

    if models is not None:
        df = df[df["model"].isin(models)]

    # Pivot to wide format
    pivot = df.pivot_table(
        index="feature",
        columns="model",
        values=["mean", "rank"],
        aggfunc=lambda x: x.iloc[0] if len(x) > 0 else np.nan,
    )

    # Flatten column names
    pivot.columns = [f"{col[1]}_{col[0]}" for col in pivot.columns]

    return pivot.reset_index()
