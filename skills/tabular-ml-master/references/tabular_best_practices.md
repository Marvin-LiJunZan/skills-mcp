# Tabular Machine Learning Engineering Guide: Best Practices for Regression & Classification

## 1. Zero-Leakage Validation Architectures

Data leakage is the #1 silent killer of tabular machine learning models. 

### Common Leakage Traps:
1. **Global Imputation/Scaling Before Split**: Fitting `StandardScaler` or `SimpleImputer` on the entire dataframe before `train_test_split` leaks the mean/variance of the test set into training.
2. **Target Encoding Leakage**: Encoding categorical features with mean target values across the full dataset causes the model to memorize target values rather than learning generalized patterns.
3. **Temporal Leakage**: Random shuffling of time-series data or panel data allows the model to predict the past using future information.
4. **Group/Entity Bleed**: If multiple rows belong to the same patient, user, vehicle, or device, randomly splitting across rows allows the model to memorize subject-specific idiosyncrasies rather than universal features.

### Recommended Remedy:
- **Always encapsulate preprocessing inside `sklearn.pipeline.Pipeline`** or calculate transformation statistics strictly on the train folds during K-Fold.
- Use **`StratifiedKFold`** for classification to maintain class proportions.
- Use **`GroupKFold`** when sample dependencies exist across entities.
- Use **`TimeSeriesSplit`** or **`PurgedGroupTimeSeriesSplit`** for time-ordered data.

---

## 2. Gradient Boosting Tree Decision Matrix

| Dimension | LightGBM | XGBoost | CatBoost |
| :--- | :--- | :--- | :--- |
| **Split Strategy** | Leaf-wise (best-first) | Depth-wise / Loss-guide | Symmetric trees (oblivious) |
| **Categorical Support** | Integer category / histogram binning | Partition-based (experimental) | **Gold Standard** (ordered target encoding on the fly) |
| **Training Speed** | **Fastest** (histogram / GOSS) | Moderate / Fast on GPU | Slower on CPU / Fast on GPU |
| **Hyperparameter Sensitivity** | Sensitive to `num_leaves` & `learning_rate` | Sensitive to `max_depth` & `subsample` | **Robust default hyperparameters** |
| **Best Used When** | Large datasets (>50k rows), speed matters, numerical heavy | Established benchmarks, exact trees needed | Complex categorical columns, text columns, small-to-medium datasets |

---

## 3. High-Cardinality Categorical Feature Handling

When categorical features have hundreds or thousands of unique values (e.g., zip codes, product IDs, city names):
1. **Never use One-Hot Encoding**: Explodes memory, dilutes tree split gain.
2. **Frequency / Count Encoding**: Replaces each category with its frequency count in the dataset. Works well for tree models.
3. **Out-of-Fold Target Encoding**: Replace category with smoothed average target value:
   $$S_i = \frac{n \cdot \bar{y}_c + m \cdot \bar{y}_{global}}{n + m}$$
   where $m$ is the smoothing weight. Must be computed out-of-fold!
4. **CatBoost Native Categoricals**: Pass column names directly via `cat_features`—CatBoost handles target encoding without leakage using random permutations.

---

## 4. Addressing Extreme Class Imbalance

When positive rate is $< 5\%$:
1. **Never rely on Accuracy**: A trivial dummy classifier gets 99% accuracy on a 1% positive dataset.
2. **Loss Weighting**: Set `scale_pos_weight = (num_negative / num_positive)` in LightGBM/XGBoost, or `auto_class_weights='Balanced'` in CatBoost.
3. **Metric Selection**: Optimize **PR-AUC (Precision-Recall AUC)** or **F1-Macro** rather than ROC-AUC, because ROC-AUC can be overly optimistic when negatives vastly outnumber positives.
4. **Probability Calibration & Threshold Tuning**: Do not default to a cutoff of 0.5. Search for the optimal decision threshold $\tau \in [0.01, 0.99]$ on the validation fold that maximizes your custom utility or F1-score.

---

## 5. Tabular Foundation Models (TabPFN)

- **What is TabPFN?** Prior-data Fitted Network trained on millions of synthetic tabular tasks.
- **When to use?**
  - Sample size $N \le 10,000$, features $D \le 500$.
  - When fast prototyping is needed without running extensive grid search or Optuna loops.
  - As a diverse meta-learner inside an ensemble with GBDT models.
