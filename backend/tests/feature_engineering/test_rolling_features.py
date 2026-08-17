# ruff: noqa: I001
import pandas as pd
import pytest

from backend.app.services.feature_engineering.rolling_features import \
    RollingFeatureGenerator


@pytest.fixture
def sample_data():
    dates = pd.date_range("2023-01-01", periods=50, freq="D")
    return pd.DataFrame({"sales": range(50), "demand": [1] * 50}, index=dates)


def test_rolling_features_valid(sample_data):
    config = {"sales": [3, 7], "demand": [3]}
    generator = RollingFeatureGenerator(config)
    result = generator.generate(sample_data)

    # Check if columns are created
    metrics = ["mean", "sum", "std", "min", "max", "median"]
    for metric in metrics:
        assert f"sales_rolling_{metric}_3" in result.columns
        assert f"sales_rolling_{metric}_7" in result.columns
        assert f"demand_rolling_{metric}_3" in result.columns

    # Values check
    # sales: 0, 1, 2. rolling mean 3 should be 1.0 for the third row
    assert pd.isna(result["sales_rolling_mean_3"].iloc[1])  # Needs 3 periods by default
    assert result["sales_rolling_mean_3"].iloc[2] == 1.0
    assert result["sales_rolling_sum_3"].iloc[2] == 3.0
    assert result["sales_rolling_max_3"].iloc[2] == 2.0
    assert result["sales_rolling_min_3"].iloc[2] == 0.0
    assert (
        result["demand_rolling_std_3"].iloc[2] == 0.0
    )  # Standard deviation of [1, 1, 1] is 0


def test_invalid_config_empty():
    with pytest.raises(
        ValueError, match="rolling_config must be a non-empty dictionary"
    ):
        RollingFeatureGenerator({})


def test_invalid_config_type():
    with pytest.raises(
        ValueError, match="rolling_config must be a non-empty dictionary"
    ):
        RollingFeatureGenerator(None)


def test_invalid_window_type():
    with pytest.raises(
        TypeError, match="Windows for column 'sales' must be a list of integers."
    ):
        RollingFeatureGenerator({"sales": 3})


def test_invalid_window_value():
    with pytest.raises(
        ValueError, match="Invalid window value '-1' for column 'sales'"
    ):
        RollingFeatureGenerator({"sales": [-1]})

    with pytest.raises(ValueError, match="Invalid window value '0' for column 'sales'"):
        RollingFeatureGenerator({"sales": [0]})


def test_empty_dataframe():
    generator = RollingFeatureGenerator({"sales": [3]})
    df = pd.DataFrame(columns=["sales"])
    with pytest.raises(ValueError, match="Input DataFrame is empty."):
        generator.generate(df)


def test_missing_columns(sample_data):
    generator = RollingFeatureGenerator({"sales": [3], "inventory": [3]})
    with pytest.raises(
        ValueError,
        match="Missing required columns for rolling feature generation: .*",
    ):
        generator.generate(sample_data)


def test_invalid_input_type():
    generator = RollingFeatureGenerator({"sales": [3]})
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame."):
        generator.generate([1, 2, 3])
