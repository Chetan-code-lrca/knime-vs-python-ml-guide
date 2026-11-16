from pathlib import Path

import pandas as pd
import pytest

from python.train_model import load_data, run

ROOT = Path(__file__).resolve().parents[1]


def test_training_pipeline_runs_and_returns_finite_metrics() -> None:
    report = run(ROOT / "data" / "inventory_demand.csv")
    assert report["rows"] == {"total": 3120, "train": 2490, "test": 630}
    for model_name in ("dummy_median_baseline", "random_forest"):
        for metric in ("mae", "rmse", "r2"):
            assert isinstance(report["metrics"][model_name][metric], float)
            assert __import__("math").isfinite(report["metrics"][model_name][metric])


def test_load_data_rejects_rows_without_a_split_label(tmp_path: Path) -> None:
    path = tmp_path / "missing-split.csv"
    pd.DataFrame(
        {
            "demand_next_week": [10, 12, 14],
            "split": ["train", "test", None],
            "week_index": [0, 1, 2],
            "price": [2.0, 2.1, 2.2],
        }
    ).to_csv(path, index=False)

    with pytest.raises(ValueError, match="must not contain missing values"):
        load_data(path)


def test_load_data_rejects_overlapping_chronological_periods(tmp_path: Path) -> None:
    path = tmp_path / "overlapping-split.csv"
    pd.DataFrame(
        {
            "demand_next_week": [10, 12, 14, 16],
            "split": ["train", "train", "test", "test"],
            "week_index": [0, 2, 1, 3],
            "price": [2.0, 2.1, 2.2, 2.3],
        }
    ).to_csv(path, index=False)

    with pytest.raises(ValueError, match="chronologically separated"):
        load_data(path)


def test_load_data_rejects_non_numeric_week_index_when_present(tmp_path: Path) -> None:
    path = tmp_path / "invalid-week-index.csv"
    pd.DataFrame(
        {
            "demand_next_week": [10, 12],
            "split": ["train", "test"],
            "week_index": [0, "unknown"],
            "price": [2.0, 2.1],
        }
    ).to_csv(path, index=False)

    with pytest.raises(ValueError, match="finite numeric values"):
        load_data(path)
