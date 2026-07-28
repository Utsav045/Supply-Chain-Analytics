# ruff: noqa: I001
import pandas as pd
import pytest

from backend.app.services.feature_engineering.calendar_features import (
    CalendarFeatureGenerator,
)


@pytest.fixture
def sample_data():
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    return pd.DataFrame({"value": range(365)}, index=dates)


def test_calendar_features_default(sample_data):
    generator = CalendarFeatureGenerator()
    result = generator.generate(sample_data)

    expected_cols = [
        "year",
        "quarter",
        "month",
        "week_of_year",
        "day_of_month",
        "day_of_week",
        "is_weekend",
        "is_month_start",
        "is_month_end",
        "is_quarter_start",
        "is_quarter_end",
        "is_year_start",
        "is_year_end",
    ]
    for col in expected_cols:
        assert col in result.columns

    assert result["year"].iloc[0] == 2023
    assert result["month"].iloc[0] == 1
    assert result["is_year_start"].iloc[0] == 1
    assert result["is_month_start"].iloc[0] == 1
    assert result["is_weekend"].iloc[0] == 1  # 2023-01-01 is a Sunday


def test_calendar_features_subset(sample_data):
    generator = CalendarFeatureGenerator(["year", "is_weekend"])
    result = generator.generate(sample_data)

    assert "year" in result.columns
    assert "is_weekend" in result.columns
    assert "month" not in result.columns


def test_invalid_features():
    with pytest.raises(ValueError, match="Invalid features requested"):
        CalendarFeatureGenerator(["invalid_feature"])


def test_empty_dataframe():
    generator = CalendarFeatureGenerator()
    df = pd.DataFrame(columns=["val"])
    with pytest.raises(ValueError, match="Input DataFrame is empty."):
        generator.generate(df)


def test_invalid_input_type():
    generator = CalendarFeatureGenerator()
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame."):
        generator.generate([1, 2, 3])


def test_invalid_index():
    generator = CalendarFeatureGenerator()
    df = pd.DataFrame({"val": [1, 2]}, index=["a", "b"])
    with pytest.raises(ValueError, match="DataFrame index must be a DatetimeIndex"):
        generator.generate(df)


def test_convertible_index():
    generator = CalendarFeatureGenerator()
    df = pd.DataFrame({"val": [1, 2]}, index=["2023-01-01", "2023-01-02"])
    result = generator.generate(df)
    assert "year" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result.index)
