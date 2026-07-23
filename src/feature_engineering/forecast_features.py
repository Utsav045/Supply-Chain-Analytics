"""Feature engineering for supply-chain demand forecasting."""

import numpy as np
import pandas as pd


def create_forecasting_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create calendar, lag, rolling, inventory and promotion features.

    Args:
        dataframe: Regular time-indexed demand dataset.

    Returns:
        Dataset containing forecasting features.
    """
    if not isinstance(dataframe.index, pd.DatetimeIndex):
        raise ValueError(
            "Forecasting features require a DatetimeIndex."
        )

    featured = dataframe.copy()

    featured["day_of_week"] = featured.index.dayofweek
    featured["day_of_month"] = featured.index.day
    featured["week_of_year"] = featured.index.isocalendar().week.astype(
        int
    )
    featured["month"] = featured.index.month
    featured["quarter"] = featured.index.quarter
    featured["is_weekend"] = (
        featured.index.dayofweek >= 5
    ).astype(int)

    for lag in (1, 7, 14, 28):
        featured[f"demand_lag_{lag}"] = featured["demand"].shift(lag)

    for window in (7, 14, 28):
        shifted_demand = featured["demand"].shift(1)

        featured[f"demand_rolling_mean_{window}"] = (
            shifted_demand.rolling(window).mean()
        )

        featured[f"demand_rolling_std_{window}"] = (
            shifted_demand.rolling(window).std()
        )

    if "inventory_level" in featured.columns:
        featured["is_stockout"] = (
            featured["inventory_level"] <= 0
        ).astype(int)

        featured["inventory_to_demand_ratio"] = np.where(
            featured["demand"] > 0,
            featured["inventory_level"] / featured["demand"],
            np.nan,
        )

    if "price" in featured.columns:
        featured["price_change"] = featured["price"].pct_change()
        featured["price_lag_1"] = featured["price"].shift(1)

    if "promotion" in featured.columns:
        featured["promotion"] = (
            featured["promotion"]
            .fillna(False)
            .astype(int)
        )

        featured["promotion_lag_1"] = featured["promotion"].shift(1)

    if "holiday" in featured.columns:
        featured["holiday"] = (
            featured["holiday"]
            .fillna(False)
            .astype(int)
        )

        featured["pre_holiday"] = (
            featured["holiday"].shift(-1).fillna(0)
        ).astype(int)

        featured["post_holiday"] = (
            featured["holiday"].shift(1).fillna(0)
        ).astype(int)

    return featured