"""Train and evaluate a reproducible inventory-demand regression baseline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "inventory_demand.csv"
TARGET = "demand_next_week"
SPLIT_COLUMN = "split"
EXCLUDED_COLUMNS = {"week_start", "week_index", "store_id", SPLIT_COLUMN, TARGET}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run: python data/generate_dataset.py"
        )
    frame = pd.read_csv(path)
    required = {TARGET, SPLIT_COLUMN}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    if frame[TARGET].isna().any():
        raise ValueError(f"Target column {TARGET!r} must not contain missing values.")
    if set(frame[SPLIT_COLUMN].dropna().unique()) != {"train", "test"}:
        raise ValueError("The split column must contain both 'train' and 'test'.")
    return frame


def build_pipeline(X_train: pd.DataFrame) -> Pipeline:
    """Build preprocessing + model pipeline; fit transforms on training data only."""
    numeric_features = X_train.select_dtypes(include=[np.number, "bool"]).columns.tolist()
    categorical_features = X_train.select_dtypes(exclude=[np.number, "bool"]).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )
    model = RandomForestRegressor(
        n_estimators=250,
        min_samples_leaf=2,
        max_features=0.85,
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def calculate_metrics(actual: pd.Series, predicted: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(actual, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "r2": float(r2_score(actual, predicted)),
    }


def run(path: Path = DATA_PATH) -> dict[str, Any]:
    frame = load_data(path)
    train = frame.loc[frame[SPLIT_COLUMN] == "train"].copy()
    test = frame.loc[frame[SPLIT_COLUMN] == "test"].copy()

    # Never feed identifiers, time markers, the split label, or the target to the model.
    feature_columns = [c for c in frame.columns if c not in EXCLUDED_COLUMNS]
    X_train = train[feature_columns]
    X_test = test[feature_columns]
    y_train = train[TARGET]
    y_test = test[TARGET]

    pipeline = build_pipeline(X_train)
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    baseline = DummyRegressor(strategy="median")
    baseline.fit(np.zeros((len(y_train), 1)), y_train)
    baseline_predictions = baseline.predict(np.zeros((len(y_test), 1)))

    report = {
        "dataset": path.name,
        "rows": {"total": int(len(frame)), "train": int(len(train)), "test": int(len(test))},
        "target": TARGET,
        "model": {
            "name": "RandomForestRegressor",
            "n_estimators": 250,
            "min_samples_leaf": 2,
            "random_state": 42,
        },
        "features": feature_columns,
        "metrics": {
            "dummy_median_baseline": calculate_metrics(y_test, baseline_predictions),
            "random_forest": calculate_metrics(y_test, predictions),
        },
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA_PATH, help="Path to the CSV dataset")
    args = parser.parse_args()
    try:
        report = run(args.data)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
