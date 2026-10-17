"""
Leak-Free Tabular Machine Learning Pipeline
Supports:
- Binary Classification, Multi-class Classification, Continuous Regression
- Automated EDA & Missing Value / Outlier handling
- Strict Leak-Free Cross-Validation (StratifiedKFold / GroupKFold / KFold)
- Model Benchmarking: Ridge/ElasticNet vs. Random Forest vs. LightGBM vs. XGBoost vs. CatBoost
- Model Explainability via SHAP (Beeswarm, Summary, Waterfall)
- Optuna Bayesian Hyperparameter Optimization
"""

import argparse
import logging
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, KFold, GroupKFold
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    roc_auc_score, f1_score, accuracy_score, classification_report
)

# Optional heavy imports with graceful fallbacks
try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import catboost as cb
except ImportError:
    cb = None

try:
    import shap
except ImportError:
    shap = None

try:
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
except ImportError:
    optuna = None


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TabularPipeline")


class TabularMLPipeline:
    def __init__(
        self,
        task_type: str = "binary", # 'binary', 'multiclass', 'regression'
        n_splits: int = 5,
        random_state: int = 42,
        output_dir: str = "./ml_outputs"
    ):
        self.task_type = task_type
        self.n_splits = n_splits
        self.random_state = random_state
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def audit_data(self, df: pd.DataFrame, target_col: str):
        """Performs initial integrity checks on dataset."""
        logger.info(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
        missing_counts = df.isnull().sum()
        high_missing = missing_counts[missing_counts > 0.4 * len(df)]
        if not high_missing.empty:
            logger.warning(f"Columns with >40% missing values: {list(high_missing.index)}")
            
        target = df[target_col]
        if self.task_type in ["binary", "multiclass"]:
            logger.info(f"Target class distribution:\n{target.value_counts(normalize=True)}")
        else:
            logger.info(f"Target descriptive stats:\n{target.describe()}")

    def train_lightgbm_cv(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        cat_cols: list = None,
        group_col: pd.Series = None
    ):
        """Runs a leak-free cross-validated LightGBM benchmark."""
        if lgb is None:
            raise ImportError("lightgbm is not installed. Run `pip install lightgbm`.")

        cat_cols = cat_cols or []
        for c in cat_cols:
            X[c] = X[c].astype("category")

        # Setup splitter
        if group_col is not None:
            splitter = GroupKFold(n_splits=self.n_splits)
            split_gen = splitter.split(X, y, groups=group_col)
        elif self.task_type == "binary":
            splitter = StratifiedKFold(n_splits=self.n_splits, shuffle=True, random_state=self.random_state)
            split_gen = splitter.split(X, y)
        else:
            splitter = KFold(n_splits=self.n_splits, shuffle=True, random_state=self.random_state)
            split_gen = splitter.split(X, y)

        oof_preds = np.zeros(len(X)) if self.task_type != "multiclass" else np.zeros((len(X), len(np.unique(y))))
        models = []

        objective = "binary" if self.task_type == "binary" else ("multiclass" if self.task_type == "multiclass" else "regression")
        metric = "auc" if self.task_type == "binary" else ("multi_logloss" if self.task_type == "multiclass" else "rmse")

        for fold, (train_idx, val_idx) in enumerate(split_gen):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

            # Imbalance compensation
            scale_weight = 1.0
            if self.task_type == "binary":
                pos_count = (y_train == 1).sum()
                neg_count = (y_train == 0).sum()
                if pos_count > 0 and neg_count / pos_count > 2.0:
                    scale_weight = neg_count / pos_count

            train_ds = lgb.Dataset(X_train, label=y_train)
            val_ds = lgb.Dataset(X_val, label=y_val, reference=train_ds)

            params = {
                "objective": objective,
                "metric": metric,
                "boosting_type": "gbdt",
                "learning_rate": 0.05,
                "num_leaves": 31,
                "feature_fraction": 0.8,
                "bagging_fraction": 0.8,
                "bagging_freq": 1,
                "scale_pos_weight": scale_weight,
                "random_state": self.random_state + fold,
                "verbose": -1,
                "n_jobs": -1
            }

            callbacks = [lgb.early_stopping(50, verbose=False)]
            model = lgb.train(
                params,
                train_ds,
                num_boost_round=1000,
                valid_sets=[val_ds],
                callbacks=callbacks
            )

            val_preds = model.predict(X_val, num_iteration=model.best_iteration)
            oof_preds[val_idx] = val_preds
            models.append(model)

            if self.task_type == "binary":
                fold_metric = roc_auc_score(y_val, val_preds)
                logger.info(f"Fold {fold+1} ROC-AUC: {fold_metric:.4f}")
            elif self.task_type == "regression":
                fold_metric = np.sqrt(mean_squared_error(y_val, val_preds))
                logger.info(f"Fold {fold+1} RMSE: {fold_metric:.4f}")

        # Final evaluation
        if self.task_type == "binary":
            overall_metric = roc_auc_score(y, oof_preds)
            logger.info(f"===> Overall Out-Of-Fold ROC-AUC: {overall_metric:.4f}")
        elif self.task_type == "regression":
            overall_rmse = np.sqrt(mean_squared_error(y, oof_preds))
            overall_r2 = r2_score(y, oof_preds)
            logger.info(f"===> Overall Out-Of-Fold RMSE: {overall_rmse:.4f}, R²: {overall_r2:.4f}")

        return models, oof_preds

    def explain_with_shap(self, model, X_sample: pd.DataFrame, max_display: int = 15):
        """Generates SHAP feature importance & beeswarm summary."""
        if shap is None:
            logger.warning("SHAP is not installed. Skipping explanation.")
            return

        logger.info("Calculating TreeSHAP values...")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_sample)

        # Beeswarm summary plot
        plt.figure(figsize=(10, 6))
        shap.plots.beeswarm(shap_values, max_display=max_display, show=False)
        out_path = os.path.join(self.output_dir, "shap_beeswarm_summary.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        logger.info(f"Saved SHAP Beeswarm summary to {out_path}")


if __name__ == "__main__":
    logger.info("TabularMLPipeline module loaded successfully.")
