# ruff: noqa: I001
import pandas as pd
import pytest

from backend.app.services.feature_engineering.lag_features import \
    LagFeatureGenerator


@pytest.fixture
def sample_data():
    dates = pd.date_range("2023-01-01", periods=50, freq="D")
    return pd.DataFrame({"sales": range(50), "demand": range(50, 100)}, index=dates)


def test_lag_features_valid(sample_data):
    config = {"sales": [1, 7], "demand": [1]}
    generator = LagFeatureGenerator(config)
    result = generator.generate(sample_data)

    assert "sales_lag_1" in result.columns
    assert "sales_lag_7" in result.columns
    assert "demand_lag_1" in result.columns

    # Check values
    assert pd.isna(result["sales_lag_1"].iloc[0])
    assert result["sales_lag_1"].iloc[1] == 0
    assert result["sales_lag_7"].iloc[7] == 0
    assert result["demand_lag_1"].iloc[1] == 50


def test_invalid_config_empty():
    with pytest.raises(ValueError, match="lag_config must be a non-empty dictionary"):
        LagFeatureGenerator({})


def test_invalid_config_type():
    with pytest.raises(ValueError, match="lag_config must be a non-empty dictionary"):
        LagFeatureGenerator(None)


def test_invalid_lag_type():
    with pytest.raises(
        TypeError, match="Lags for column 'sales' must be a list of integers."
    ):
        LagFeatureGenerator({"sales": 1})


def test_invalid_lag_value():
    with pytest.raises(
        ValueError,
        match="Invalid lag value '-1' for column 'sales'.*",
    ):
        LagFeatureGenerator({"sales": [-1]})

    with pytest.raises(
        ValueError,
        match="Invalid lag value '0' for column 'sales'.*",
    ):
        LagFeatureGenerator({"sales": [0]})


def test_empty_dataframe():
    generator = LagFeatureGenerator({"sales": [1]})
    df = pd.DataFrame(columns=["sales"])
    with pytest.raises(ValueError, match="Input DataFrame is empty."):
        generator.generate(df)


def test_missing_columns(sample_data):
    generator = LagFeatureGenerator({"sales": [1], "inventory": [1]})
    with pytest.raises(
        ValueError,
        match="Missing required columns for lag generation: \\['inventory'\\]",
    ):
        generator.generate(sample_data)


def test_invalid_input_type():
    generator = LagFeatureGenerator({"sales": [1]})
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame."):
        generator.generate([1, 2, 3])
