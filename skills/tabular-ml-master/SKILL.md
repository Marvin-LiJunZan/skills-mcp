---
name: tabular-ml-master
description: End-to-end master skill for classical and modern machine learning on tabular data (regression, binary/multi-class classification, imbalanced learning). Covers leak-free cross-validation, feature engineering, SOTA models (LightGBM, XGBoost, CatBoost, TabPFN, AutoGluon, Scikit-learn), Optuna Bayesian hyperparameter optimization, and SHAP explainability. Trigger when the user mentions machine learning, regression, classification, tabular data, 表格数据, 机器学习, 回归, 分类, LightGBM, XGBoost, CatBoost, TabPFN, AutoGluon, or Kaggle-style pipelines.
---

# Tabular ML Master: Classical & Modern Machine Learning Suite

> **Production & Competition-grade workflow for Tabular Machine Learning (Regression, Classification & Multi-Class), integrating Gradient Boosted Decision Trees (GBDT), Tabular Foundation Models (TabPFN), Automated Multi-Layer Stacking (AutoGluon), and Explainable AI (SHAP).**

---

## 1. When to Use This Skill

Activate this skill whenever the task involves structured/tabular data:
- **Regression Tasks**: Predicting continuous variables (e.g., prices, physical properties, energy consumption, survival times, financial yields).
- **Classification Tasks**: 
  - Binary classification (fraud detection, default prediction, disease diagnosis, churn).
  - Multi-class classification (category assignment, fault diagnosis).
  - Extreme imbalanced classification (rare event detection, fraud, anomalies).
- **Tooling Selection**: Choosing or building pipelines using **LightGBM, XGBoost, CatBoost, TabPFN, AutoGluon, Scikit-learn, Optuna, or SHAP**.
- **Kaggle / Academic Benchmark Workflows**: Requiring leak-free cross-validation, feature engineering, and publication-ready evaluation reports.

---

## 2. Model Selection Matrix: What to Pick?

| Scenario / Constraint | Primary Recommendation | Secondary / Fallback | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Small-to-Medium Tabular** (<10,000 rows, <500 features) | **TabPFN (v2)** | CatBoost / LightGBM | **Zero-shot foundation model**, zero hyperparameter tuning needed, instantaneous inference, often outperforms tuned GBDTs. |
| **Medium-to-Large Tabular** (>10,000 rows, mixed categorical/numerical) | **LightGBM / CatBoost** | XGBoost | Industry standard GBDT speed and accuracy. CatBoost excels with high-cardinality categories; LightGBM excels with speed and scalability. |
| **Maximum Predictive Accuracy (Kaggle / SOTA Challenge)** | **AutoGluon (`TabularPredictor`)** | Stacking Ensemble (LGBM + XGB + CatBoost) | Automated multi-layer stack ensembling, out-of-fold cross-validation, handles heterogeneous columns automatically. |
| **Extreme High Interpretability / Regulatory Compliance** | **EBM (Explainable Boosting Machine) / Penalized GLM** | LightGBM + TreeSHAP | Exact additive feature contributions, transparent decision boundaries. |
| **High Imbalance (e.g. positive rate < 1%)** | **CatBoost / LightGBM with focal loss / `scale_pos_weight`** | BalancedRandomForest + PR-AUC threshold tuning | Prevents majority-class collapse, optimizes Area Under Precision-Recall Curve. |

---

## 3. The 6-Stage Standard Engineering Pipeline

Every regression and classification task MUST strictly adhere to this 6-stage lifecycle to prevent **Data Leakage** and ensure robust generalization:

```
[Raw Tabular Data]
       │
       ▼
[Stage 1: Exploratory Data Analysis & Integrity Audit]
  ├── Target distribution skewness (Log/Yeo-Johnson check)
  ├── Missing value mechanism (MCAR, MAR, MNAR)
  ├── High-cardinality & ID leakage check
  └── Adversarial Validation (detect train-test distribution shift)
       │
       ▼
[Stage 2: Strict Leak-Free Cross-Validation Scheme]
  ├── Classification: StratifiedKFold (maintains class ratio)
  ├── Grouped Entities: GroupKFold (prevents patient/device/client bleed)
  ├── Temporal Data: TimeSeriesSplit / PurgedGroupTimeSeriesSplit
  └── GOLDEN RULE: All encoders, imputers, and scalers MUST be fit ONLY on train folds!
       │
       ▼
[Stage 3: Tabular Feature Engineering]
  ├── Categorical: Out-Of-Fold Target Encoding, Frequency Encoding, WoE
  ├── Numerical: Robust Scaling, Quantile Transformation, Polynomial/Ratios
  ├── Datetime: Cyclical Sin/Cos encoding (hour, day of week, month), elapsed time
  └── Feature Selection: Mutual Information, Recursive Feature Elimination (RFE)
       │
       ▼
[Stage 4: Model Training & Benchmark Matrix]
  ├── Level 0 Baselines: Ridge / Logistic Regression, Random Forest
  ├── Level 1 SOTA Trees: LightGBM, XGBoost, CatBoost (Early Stopping on Val Fold)
  ├── Level 1 SOTA Foundation: TabPFN (for small/medium datasets)
  └── Level 2 Ensembling: AutoGluon multi-layer stacking or rank averaging
       │
       ▼
[Stage 5: Hyperparameter Optimization (Optuna)]
  ├── Bayesian Optimization (TPESampler) with MedianPruner
  └── Joint objective: Cross-Validated Out-Of-Fold Metric (NOT single test set)
       │
       ▼
[Stage 6: Comprehensive Metric Evaluation & SHAP Interpretability]
  ├── Metric Matrix (RMSE, MAE, R² / ROC-AUC, PR-AUC, F1-macro, Brier Score)
  └── TreeSHAP: Beeswarm summary, global importance, local waterfall plots
```

---

## 4. Production Code Recipes

### Recipe A: SOTA Gradient Boosting (LightGBM / XGBoost / CatBoost) with Leak-Free Stratified K-Fold

```python
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, log_loss

def train_leak_free_lgbm(
    X: pd.DataFrame, 
    y: pd.Series, 
    cat_cols: list, 
    n_splits: int = 5,
    random_state: int = 42
):
    """
    Trains LightGBM with leak-free out-of-fold cross validation.
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    oof_preds = np.zeros(len(X))
    models = []
    
    # Ensure categorical types for LightGBM native categorical handling
    for col in cat_cols:
        X[col] = X[col].astype('category')
        
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        # Calculate class balance ratio for scale_pos_weight if imbalanced
        neg_count = (y_train == 0).sum()
        pos_count = (y_train == 1).sum()
        scale_weight = neg_count / max(pos_count, 1)
        
        train_data = lgb.Dataset(X_train, label=y_train)
        val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
        
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'learning_rate': 0.03,
            'num_leaves': 31,
            'max_depth': -1,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 1,
            'scale_pos_weight': scale_weight if scale_weight > 2.0 else 1.0,
            'random_state': random_state + fold,
            'verbose': -1,
            'n_jobs': -1
        }
        
        callbacks = [lgb.early_stopping(stopping_rounds=50, verbose=False)]
        
        gbm = lgb.train(
            params,
            train_data,
            num_boost_round=1500,
            valid_sets=[val_data],
            callbacks=callbacks
        )
        
        val_preds = gbm.predict(X_val, num_iteration=gbm.best_iteration)
        oof_preds[val_idx] = val_preds
        models.append(gbm)
        
        fold_auc = roc_auc_score(y_val, val_preds)
        print(f"Fold {fold+1} ROC-AUC: {fold_auc:.4f}")
        
    overall_auc = roc_auc_score(y, oof_preds)
    print(f"\n---> Overall Out-of-Fold ROC-AUC: {overall_auc:.4f}")
    return models, oof_preds
```

---

### Recipe B: Zero-Shot Tabular Foundation Model (TabPFN)

For datasets with $N \le 10,000$ and $D \le 500$, TabPFN delivers near-optimal Bayesian prediction without iterative training or hyperparameter search:

```python
from tabpfn import TabPFNClassifier, TabPFNRegressor
from sklearn.metrics import classification_report, r2_score

# Classification
tabpfn_clf = TabPFNClassifier(device='cuda') # or 'cpu'
tabpfn_clf.fit(X_train, y_train)
y_pred_proba = tabpfn_clf.predict_proba(X_test)
y_pred = tabpfn_clf.predict(X_test)

# Regression
tabpfn_reg = TabPFNRegressor(device='cuda')
tabpfn_reg.fit(X_train, y_train)
y_pred_reg = tabpfn_reg.predict(X_test)
print("TabPFN R2 Score:", r2_score(y_test, y_pred_reg))
```

---

### Recipe C: Maximum Performance Multi-Layer Stacking (AutoGluon)

When maximum Kaggle-grade accuracy or production robustness is required without manual ensembling:

```python
from autogluon.tabular import TabularPredictor

# Train multi-layer stacking ensemble across GBDT + Neural Nets + TabPFN
predictor = TabularPredictor(
    label='target_column', 
    problem_type='regression', # or 'binary' / 'multiclass'
    eval_metric='root_mean_squared_error' # or 'roc_auc' / 'f1'
).fit(
    train_data=train_df,
    presets='best_quality', # automatic bagging & multi-layer stacking
    time_limit=3600 # 1 hour budget
)

# Benchmark leaderboard across all sub-models and stacked ensembles
leaderboard = predictor.leaderboard(test_df, silent=False)
predictions = predictor.predict(test_df)
```

---

### Recipe D: TreeSHAP Model Interpretability & Publication Figures

```python
import shap
import matplotlib.pyplot as plt

# Works seamlessly with LightGBM, XGBoost, and CatBoost models
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_val)

# 1. Global Feature Importance & Directionality (Beeswarm)
plt.figure(figsize=(10, 6))
shap.plots.beeswarm(shap_values, max_display=15, show=False)
plt.tight_layout()
plt.savefig("shap_beeswarm.png", dpi=300)
plt.close()

# 2. Local Explanation for Individual Case (Waterfall)
plt.figure(figsize=(10, 6))
shap.plots.waterfall(shap_values[0], max_display=10, show=False)
plt.tight_layout()
plt.savefig("shap_waterfall_sample0.png", dpi=300)
plt.close()
```

---

## 5. Metrics & Loss Functions Decision Guide

### Regression Tasks:
- **Default / Symmetric Error**: Root Mean Squared Error (`RMSE`) + Coefficient of Determination ($R^2$).
- **Robust to Outliers**: Mean Absolute Error (`MAE`) or Huber Loss / Median Absolute Error (`MedAE`).
- **Percentage-based Error**: Mean Absolute Percentage Error (`MAPE`) or Symmetric MAPE (`sMAPE`).
- **Poisson / Claim / Count Data**: Poisson deviance or Tweedie loss (power parameter $1 < p < 2$).

### Classification Tasks:
- **Balanced Binary**: `ROC-AUC`, Log-Loss, Accuracy.
- **Imbalanced Binary**: `PR-AUC` (Area Under Precision-Recall Curve), `F1-macro`, Matthews Correlation Coefficient (`MCC`), Cost-weighted profit curve.
- **Multi-Class**: Macro-averaged `F1-score`, Cohen's Kappa, Log-Loss.
- **Probability Calibration**: Brier Score, Reliability Curves (`calibration_curve`).

---

## 6. Self-Audit Checklist Before Submitting Code

- [ ] **No Leakage in Preprocessing**: Are scalers, target encoders, and imputers isolated inside each CV fold?
- [ ] **Group Separation**: If the data has subject/user/session IDs, is `GroupKFold` utilized to prevent sample bleed?
- [ ] **Target Transformation**: If the regression target has heavy positive skew, was `np.log1p(y)` or Box-Cox evaluated?
- [ ] **Categorical Integrity**: Are categorical features appropriately passed to native handlers (`categorical_feature` for LGBM, `cat_features` for CatBoost) instead of arbitrarily treated as ordinal numbers?
- [ ] **Class Balance Calibration**: In imbalanced classification, is threshold tuning applied instead of blindly trusting default 0.5?
- [ ] **Interpretability**: Are feature importance rankings backed by SHAP or Permutation Importance rather than split-count gain alone?
