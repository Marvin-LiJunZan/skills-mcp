"""
AutoGluon Tabular Multi-Layer Stacking Runner
Executes state-of-the-art automated tabular benchmarking with zero manual ensembling.
Supports:
- Automatic feature inference (numeric, categorical, text, datetime)
- Ensembling across LightGBM, CatBoost, XGBoost, TabPFN, PyTorch FastAI/Tabular Neural Nets
- Leaderboard ranking and out-of-fold calibration
"""

import os
import sys
import argparse
import pandas as pd

def run_autogluon_benchmark(
    train_data_path: str,
    target_column: str,
    test_data_path: str = None,
    problem_type: str = None, # 'binary', 'multiclass', 'regression'
    eval_metric: str = None,   # 'roc_auc', 'f1', 'root_mean_squared_error', 'r2'
    time_limit: int = 600,     # in seconds
    presets: str = "best_quality", # 'medium_quality', 'high_quality', 'best_quality'
    save_path: str = "./autogluon_output"
):
    try:
        from autogluon.tabular import TabularPredictor
    except ImportError:
        print("[ERROR] autogluon is not installed. Install with `pip install autogluon`.")
        sys.exit(1)

    print(f"Loading training data from {train_data_path}...")
    train_df = pd.read_csv(train_data_path)

    predictor = TabularPredictor(
        label=target_column,
        problem_type=problem_type,
        eval_metric=eval_metric,
        path=save_path
    )

    print(f"Beginning AutoGluon training with preset='{presets}', time_limit={time_limit}s...")
    predictor.fit(
        train_data=train_df,
        presets=presets,
        time_limit=time_limit
    )

    print("\nTraining complete! Generating model leaderboard:")
    leaderboard = predictor.leaderboard(silent=False)
    leaderboard.to_csv(os.path.join(save_path, "leaderboard.csv"), index=False)

    if test_data_path and os.path.exists(test_data_path):
        print(f"\nEvaluating on holdout test set from {test_data_path}...")
        test_df = pd.read_csv(test_data_path)
        perf = predictor.evaluate(test_df)
        print("Test Performance:", perf)
        preds = predictor.predict(test_df)
        preds.to_csv(os.path.join(save_path, "test_predictions.csv"), index=False)
        print(f"Saved test predictions to {save_path}/test_predictions.csv")

    return predictor

if __name__ == "__main__":
    print("AutoGluon runner module ready.")
