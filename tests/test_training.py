from pathlib import Path

from python.train_model import run

ROOT = Path(__file__).resolve().parents[1]


def test_training_pipeline_runs_and_returns_finite_metrics() -> None:
    report = run(ROOT / "data" / "inventory_demand.csv")
    assert report["rows"] == {"total": 3120, "train": 2490, "test": 630}
    for model_name in ("dummy_median_baseline", "random_forest"):
        for metric in ("mae", "rmse", "r2"):
            assert isinstance(report["metrics"][model_name][metric], float)
            assert __import__("math").isfinite(report["metrics"][model_name][metric])
