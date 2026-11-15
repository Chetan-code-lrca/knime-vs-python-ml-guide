from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "inventory_demand.csv"


def test_dataset_has_expected_shape_and_columns() -> None:
    frame = pd.read_csv(DATA)
    assert len(frame) == 3120
    assert "demand_next_week" in frame.columns
    assert "split" in frame.columns
    assert frame["demand_next_week"].notna().all()


def test_dataset_uses_chronological_train_test_split() -> None:
    frame = pd.read_csv(DATA)
    train = frame.loc[frame["split"] == "train", "week_index"]
    test = frame.loc[frame["split"] == "test", "week_index"]
    assert len(train) == 2490
    assert len(test) == 630
    assert train.max() < test.min()


def test_dataset_contains_missing_values_in_features() -> None:
    frame = pd.read_csv(DATA)
    assert frame.drop(columns=["demand_next_week", "split"]).isna().any().any()


def test_metadata_is_not_a_model_feature() -> None:
    frame = pd.read_csv(DATA)
    excluded = {"week_start", "week_index", "store_id", "split", "demand_next_week"}
    features = set(frame.columns) - excluded
    assert "demand_next_week" not in features
    assert "split" not in features
    assert "store_id" not in features
