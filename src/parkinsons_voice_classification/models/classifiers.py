"""
Classifier Definitions

Five classical ML models with default hyperparameters:
- Logistic Regression
- SVM (RBF kernel)
- Random Forest
- Gradient Boosting (sklearn)
- XGBoost

All wrapped in sklearn Pipelines with StandardScaler.
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from xgboost import XGBClassifier

from parkinsons_voice_classification.config import RANDOM_SEED, USE_CLASS_WEIGHT_BALANCED


def get_models() -> dict[str, Pipeline]:
    """
    Return dictionary of model pipelines.

    All models use:
    - StandardScaler preprocessing
    - Default hyperparameters
    - Fixed random seed for reproducibility
    - Optional class_weight="balanced" (controlled by USE_CLASS_WEIGHT_BALANCED)

    Returns
    -------
    dict[str, Pipeline]
        Mapping of model names to sklearn Pipelines.
    """
    # Determine class weighting strategy based on config
    class_weight = "balanced" if USE_CLASS_WEIGHT_BALANCED else None

    return {
        "LogisticRegression": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        random_state=RANDOM_SEED,
                        max_iter=1000,
                        solver="lbfgs",
                        class_weight=class_weight,
                    ),
                ),
            ]
        ),
        "SVM_RBF": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    SVC(
                        kernel="rbf",
                        random_state=RANDOM_SEED,
                        probability=True,  # For ROC-AUC
                        class_weight=class_weight,
                    ),
                ),
            ]
        ),
        "RandomForest": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=100,
                        random_state=RANDOM_SEED,
                        class_weight=class_weight,
                    ),
                ),
            ]
        ),
        # Note: Boosting classifiers do not support class_weight="balanced"
        # natively. When USE_CLASS_WEIGHT_BALANCED is True, the weighting
        # applies only to the three models above.
        "GradientBoosting": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    GradientBoostingClassifier(
                        n_estimators=100,
                        learning_rate=0.1,
                        random_state=RANDOM_SEED,
                    ),
                ),
            ]
        ),
        "XGBoost": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    XGBClassifier(
                        n_estimators=100,
                        learning_rate=0.1,
                        random_state=RANDOM_SEED,
                        eval_metric="logloss",
                    ),
                ),
            ]
        ),
    }
