"""
Training and Evaluation Pipeline

Cross-validation runner for both datasets:
- Dataset A: StratifiedGroupKFold (grouped by subject)
- Dataset B: StratifiedKFold (standard)

Metrics: Accuracy, Precision, Recall, F1, ROC-AUC
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.base import clone

from parkinsons_voice_classification.config import RANDOM_SEED, N_FOLDS
from parkinsons_voice_classification.models.classifiers import get_models


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None = None) -> dict:
    """
    Compute all evaluation metrics.
    
    Parameters
    ----------
    y_true : np.ndarray
        Ground truth labels
    y_pred : np.ndarray
        Predicted labels
    y_prob : np.ndarray, optional
        Predicted probabilities for positive class (for ROC-AUC)
        
    Returns
    -------
    dict
        Dictionary with metric names and values
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0),
    }
    
    if y_prob is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_prob)
        except ValueError:
            metrics['roc_auc'] = np.nan
    else:
        metrics['roc_auc'] = np.nan
    
    return metrics


def run_cv(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray | None = None,
    use_groups: bool = False,
    n_folds: int = N_FOLDS,
) -> pd.DataFrame:
    """
    Run cross-validation for all models.
    
    Parameters
    ----------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Label array
    groups : np.ndarray, optional
        Group labels for grouped CV (e.g., subject IDs)
    use_groups : bool
        If True, use StratifiedGroupKFold; else use StratifiedKFold
    n_folds : int
        Number of CV folds
        
    Returns
    -------
    pd.DataFrame
        Results with columns: model, fold, metric, value
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
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Get probabilities for ROC-AUC
            if hasattr(model, 'predict_proba'):
                y_prob = model.predict_proba(X_test)[:, 1]
            else:
                y_prob = None
            
            # Compute metrics
            metrics = compute_metrics(y_test, y_pred, y_prob)
            
            # Store results
            for metric_name, value in metrics.items():
                results.append({
                    'model': model_name,
                    'fold': fold_idx + 1,
                    'metric': metric_name,
                    'value': value,
                })
    
    return pd.DataFrame(results)


def summarize_results(results_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize CV results with mean ± std.
    
    Parameters
    ----------
    results_df : pd.DataFrame
        Raw results from run_cv()
        
    Returns
    -------
    pd.DataFrame
        Summary with mean and std per model/metric
    """
    summary = results_df.groupby(['model', 'metric'])['value'].agg(['mean', 'std'])
    summary['mean_std'] = summary.apply(
        lambda row: f"{row['mean']:.3f} ± {row['std']:.3f}", axis=1
    )
    return summary.reset_index()
