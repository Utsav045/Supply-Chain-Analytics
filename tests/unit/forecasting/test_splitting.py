"""Tests for chronological time-series splitting."""

import pandas as pd
import pytest
from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.splitting import chronological_train_test_split


@pytest.fixture
def daily_demand() -> pd.Series:
    """Return ten days of demand observations."""
    return pd.Series(
        data=[
            10.0,
            12.0,
            14.0,
            16.0,
            18.0,
            20.0,
            22.0,
            24.0,
            26.0,
            28.0,
        ],
        index=pd.date_range(
            start="2026-01-01",
            periods=10,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_default_ratio_creates_expected_split(
    daily_demand: pd.Series,
) -> None:
    """A twenty-percent ratio should reserve two observations."""
    result = chronological_train_test_split(daily_demand)

    assert len(result.train_series) == 8
    assert len(result.test_series) == 2


def test_explicit_test_size_is_supported(
    daily_demand: pd.Series,
) -> None:
    """A fixed test size should be supported."""
    result = chronological_train_test_split(
        daily_demand,
        test_size=3,
    )

    assert len(result.train_series) == 7
    assert len(result.test_series) == 3


def test_split_preserves_chronological_order(
    daily_demand: pd.Series,
) -> None:
    """Training observations must precede test observations."""
    result = chronological_train_test_split(
        daily_demand,
        test_size=2,
    )

    assert result.train_series.index.max() < result.test_series.index.min()
    assert result.test_series.index[0] == pd.Timestamp("2026-01-09")


def test_exogenous_features_are_split_with_demand(
    daily_demand: pd.Series,
) -> None:
    """External variables should use the same split position."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * 10,
            "promotion": [0.0] * 8 + [1.0, 1.0],
        },
        index=daily_demand.index,
    )

    result = chronological_train_test_split(
        daily_demand,
        test_size=2,
        exogenous=exogenous,
    )

    assert result.train_exogenous is not None
    assert result.test_exogenous is not None
    assert len(result.train_exogenous) == 8
    assert len(result.test_exogenous) == 2
    assert result.test_exogenous.index.equals(result.test_series.index)


@pytest.mark.parametrize(
    "invalid_ratio",
    [0, 1, -0.2, 1.5, True],
)
def test_invalid_test_ratio_is_rejected(
    daily_demand: pd.Series,
    invalid_ratio: object,
) -> None:
    """The test ratio must be between zero and one."""
    with pytest.raises(ModelInputValidationError):
        chronological_train_test_split(
            daily_demand,
            test_ratio=invalid_ratio,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_size",
    [0, -1, 10, 11, 2.5, True],
)
def test_invalid_test_size_is_rejected(
    daily_demand: pd.Series,
    invalid_size: object,
) -> None:
    """The test size must leave sufficient training data."""
    with pytest.raises(ModelInputValidationError):
        chronological_train_test_split(
            daily_demand,
            test_size=invalid_size,  # type: ignore[arg-type]
        )


def test_misaligned_exogenous_data_is_rejected(
    daily_demand: pd.Series,
) -> None:
    """External variables must match demand dates."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * 10,
        },
        index=pd.date_range(
            start="2026-02-01",
            periods=10,
            freq="D",
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="must match",
    ):
        chronological_train_test_split(
            daily_demand,
            exogenous=exogenous,
        )
