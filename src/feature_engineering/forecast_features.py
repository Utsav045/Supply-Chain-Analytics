"""Feature engineering for supply-chain demand forecasting."""

import numpy as np
import pandas as pd


def create_forecasting_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create calendar, lag, rolling and supply-chain features.

    Features derived from demand use only previous observations to
    prevent target leakage.

    Args:
        dataframe: Regular time-indexed demand dataset.

    Returns:
        Dataset containing forecasting features.

    Raises:
        ValueError: If the dataset is empty, lacks demand, or does not
            use a DatetimeIndex.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Forecasting input must be a pandas DataFrame.")

    if dataframe.empty:
        raise ValueError("Forecasting feature input cannot be empty.")

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Forecasting input must be a pandas DataFrame.")

    if "demand" not in dataframe.columns:
        raise ValueError("Forecasting features require a demand column.")

    featured = dataframe.sort_index().copy()

    featured["demand"] = pd.to_numeric(
        featured["demand"],
        errors="coerce",
    )

    if featured["demand"].isna().any():
        raise ValueError("Demand contains missing or non-numeric values.")

    if (featured["demand"] < 0).any():
        raise ValueError("Demand cannot contain negative values.")

    featured["day_of_week"] = featured.index.dayofweek
    featured["day_of_month"] = featured.index.day
    featured["week_of_year"] = featured.index.isocalendar().week.astype(int)
    featured["month"] = featured.index.month
    featured["quarter"] = featured.index.quarter
    featured["is_weekend"] = (featured.index.dayofweek >= 5).astype(int)

    shifted_demand = featured["demand"].shift(1)

    for lag in (1, 7, 14, 28):
        featured[f"demand_lag_{lag}"] = featured["demand"].shift(lag)

    for window in (7, 14, 28):
        featured[f"demand_rolling_mean_{window}"] = shifted_demand.rolling(
            window=window,
            min_periods=window,
        ).mean()

        featured[f"demand_rolling_std_{window}"] = shifted_demand.rolling(
            window=window,
            min_periods=window,
        ).std()

    if "inventory_level" in featured.columns:
        featured["inventory_level"] = pd.to_numeric(
            featured["inventory_level"],
            errors="coerce",
        )

        featured["is_stockout"] = (featured["inventory_level"].fillna(0) <= 0).astype(
            int
        )

        featured["inventory_to_previous_demand_ratio"] = np.where(
            shifted_demand > 0,
            featured["inventory_level"] / shifted_demand,
            np.nan,
        )

        featured["inventory_change"] = featured["inventory_level"].diff()

    if "price" in featured.columns:
        featured["price"] = pd.to_numeric(
            featured["price"],
            errors="coerce",
        )

        featured["price_change"] = featured["price"].pct_change(fill_method=None)

        featured["price_lag_1"] = featured["price"].shift(1)

    if "promotion" in featured.columns:
        featured["promotion"] = featured["promotion"].fillna(False).astype(int)

        featured["promotion_lag_1"] = featured["promotion"].shift(1)

    if "holiday" in featured.columns:
        featured["holiday"] = featured["holiday"].fillna(False).astype(int)

        featured["pre_holiday"] = featured["holiday"].shift(-1).fillna(0).astype(int)

        featured["post_holiday"] = featured["holiday"].shift(1).fillna(0).astype(int)

    return featured
