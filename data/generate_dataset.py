"""Generate the deterministic synthetic inventory-demand teaching dataset.

The data is synthetic and intended only for learning workflows. It is not
business data and must not be used for real purchasing or inventory decisions.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261115
OUTPUT = Path(__file__).with_name("inventory_demand.csv")


def build_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    categories = {
        "Beverages": (74.0, 1.8),
        "Snacks": (58.0, 1.2),
        "Personal Care": (33.0, 3.4),
        "Household": (27.0, 5.0),
        "Stationery": (19.0, 2.2),
    }
    regions = {"North": 1.08, "South": 0.98, "East": 0.91, "West": 1.13}
    formats = {"Small": 0.82, "Standard": 1.0, "Large": 1.24}

    stores = []
    for store_id in range(1, 7):
        region = list(regions)[(store_id - 1) % len(regions)]
        store_format = list(formats)[(store_id - 1) % len(formats)]
        stores.append((f"S{store_id:02d}", region, store_format))

    rows: list[dict[str, object]] = []
    start = pd.Timestamp("2024-01-01")
    weeks = 104

    for store_id, region, store_format in stores:
        for category, (base_demand, base_price) in categories.items():
            history: list[float] = []
            item_factor = rng.uniform(0.78, 1.25)
            for week in range(weeks):
                week_start = start + pd.Timedelta(weeks=week)
                forecast_date = week_start + pd.Timedelta(weeks=1)
                month = forecast_date.month
                seasonal = 1.0 + 0.13 * np.sin(2 * np.pi * (month - 1) / 12)
                holiday = int(month in (10, 11, 12) and rng.random() < 0.22)
                planned_promo = int(rng.random() < 0.24)
                discount = float(rng.choice([0, 5, 10, 15, 20, 25])) if planned_promo else 0.0
                price = max(1.0, base_price * rng.normal(1.0, 0.07))

                if history:
                    previous = history[-1]
                    recent = float(np.mean(history[-4:]))
                else:
                    previous = base_demand * item_factor * regions[region] * formats[store_format]
                    recent = previous

                price_effect = (base_price / price) ** 0.35
                promotion_effect = 1.0 + 0.12 * planned_promo + 0.006 * discount
                holiday_effect = 1.0 + 0.16 * holiday
                demand = (
                    base_demand
                    * item_factor
                    * regions[region]
                    * formats[store_format]
                    * seasonal
                    * price_effect
                    * promotion_effect
                    * holiday_effect
                    * 0.55
                    + previous * 0.25
                    + recent * 0.20
                    + rng.normal(0, max(2.0, base_demand * 0.10))
                )
                demand = max(0.0, float(demand))
                history.append(demand)

                rows.append(
                    {
                        "week_start": week_start.strftime("%Y-%m-%d"),
                        "week_index": week,
                        "store_id": store_id,
                        "region": region,
                        "store_format": store_format,
                        "product_category": category,
                        "price_next_week": round(price, 2),
                        "discount_pct_next_week": discount,
                        "promotion_next_week": planned_promo,
                        "holiday_next_week": holiday,
                        "forecast_month": month,
                        "previous_week_units": round(previous, 2),
                        "avg_4_week_units": round(recent, 2),
                        "demand_next_week": int(round(demand)),
                    }
                )

    df = pd.DataFrame(rows)

    # The final 20 weeks are held out as a chronological test period.
    df["split"] = np.where(df["week_index"] < int(weeks * 0.8), "train", "test")

    # Add realistic missingness only to input features, never to the target or split.
    for column, rate in {
        "region": 0.012,
        "store_format": 0.010,
        "product_category": 0.008,
        "price_next_week": 0.018,
        "discount_pct_next_week": 0.025,
        "previous_week_units": 0.020,
        "avg_4_week_units": 0.020,
    }.items():
        mask = rng.random(len(df)) < rate
        df.loc[mask, column] = np.nan

    return df


if __name__ == "__main__":
    frame = build_dataset()
    frame.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(frame):,} rows to {OUTPUT}")
    print(frame["split"].value_counts().to_string())
