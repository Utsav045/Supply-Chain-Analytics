"""Tests for forecasting feature engineering."""

import numpy as np
import pandas as pd
import pytest

from src.feature_engineering.forecast_features import (
    create_forecasting_features,
)


@pytest.fixture
def forecasting_data() -> pd.DataFrame:
    """Return a regular supply-chain forecasting dataset."""
    dates = pd.date_range(
        start="2026-01-01",
        periods=35,
        freq="D",
    )

    return pd.DataFrame(
        {
            "demand": list(range(10, 45)),
            "inventory_level": list(range(100, 65, -1)),
            "price": [50.0] * 20 + [55.0] * 15,
            "promotion": [False] * 10 + [True] * 5 + [False] * 20,
            "holiday": [False] * 34 + [True],
        },
        index=dates,
    )


def test_calendar_features_are_created(
    forecasting_data: pd.DataFrame,
) -> None:
    """Calendar variables should be derived from the index."""
    result = create_forecasting_features(forecasting_data)

    expected_columns = {
        "day_of_week",
        "day_of_month",
        "week_of_year",
        "month",
        "quarter",
        "is_weekend",
    }

    assert expected_columns.issubset(result.columns)


def test_demand_lag_features_are_created(
    forecasting_data: pd.DataFrame,
) -> None:
    """Required demand lags should exist."""
    result = create_forecasting_features(forecasting_data)

    assert "demand_lag_1" in result.columns
    assert "demand_lag_7" in result.columns
    assert "demand_lag_14" in result.columns
    assert "demand_lag_28" in result.columns

    assert result.iloc[1]["demand_lag_1"] == 10


def test_rolling_features_exclude_current_demand(
    forecasting_data: pd.DataFrame,
) -> None:
    """Rolling statistics should use only previous observations."""
    result = create_forecasting_features(forecasting_data)

    expected_mean = np.mean(
        forecasting_data["demand"].iloc[0:7]
    )

    assert result.iloc[7]["demand_rolling_mean_7"] == pytest.approx(
        expected_mean
    )


def test_inventory_ratio_uses_previous_demand(
    forecasting_data: pd.DataFrame,
) -> None:
    """Inventory ratio must not use the current target demand."""
    result = create_forecasting_features(forecasting_data)

    expected_ratio = (
        forecasting_data.iloc[1]["inventory_level"]
        / forecasting_data.iloc[0]["demand"]
    )

    assert result.iloc[1][
        "inventory_to_previous_demand_ratio"
    ] == pytest.approx(expected_ratio)


def test_price_features_are_created(
    forecasting_data: pd.DataFrame,
) -> None:
    """Price movement and lag features should be available."""
    result = create_forecasting_features(forecasting_data)

    assert "price_change" in result.columns
    assert "price_lag_1" in result.columns


def test_promotion_and_holiday_features_are_created(
    forecasting_data: pd.DataFrame,
) -> None:
    """Event-based variables should be included."""
    result = create_forecasting_features(forecasting_data)

    assert "promotion_lag_1" in result.columns
    assert "pre_holiday" in result.columns
    assert "post_holiday" in result.columns


def test_non_datetime_index_is_rejected() -> None:
    """Feature generation requires chronological indexing."""
    dataframe = pd.DataFrame(
        {
            "demand": [10, 20, 30],
        }
    )

    with pytest.raises(
        TypeError,
        match="DatetimeIndex",
    ):
        create_forecasting_features(dataframe)


def test_missing_demand_column_is_rejected() -> None:
    """A forecasting dataset must include demand."""
    dataframe = pd.DataFrame(
        {
            "price": [20.0, 25.0],
        },
        index=pd.date_range(
            "2026-01-01",
            periods=2,
            freq="D",
        ),
    )

    with pytest.raises(
        ValueError,
        match="demand column",
    ):
        create_forecasting_features(dataframe)