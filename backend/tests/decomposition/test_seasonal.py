# ruff: noqa: I001
import numpy as np
import pandas as pd
import pytest

from backend.app.services.decomposition.seasonal import SeasonalDecomposer


@pytest.fixture
def sample_additive_data():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    np.random.seed(42)
    # create trend + seasonality + noise
    trend = np.linspace(10, 50, 100)
    seasonality = 10 * np.sin(2 * np.pi * np.arange(100) / 7)  # period = 7
    noise = np.random.normal(0, 1, 100)
    values = trend + seasonality + noise
    return pd.DataFrame({"value": values}, index=dates)


@pytest.fixture
def sample_multiplicative_data():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    np.random.seed(42)
    trend = np.linspace(10, 50, 100)
    seasonality = 1 + 0.2 * np.sin(2 * np.pi * np.arange(100) / 7)  # period = 7
    noise = np.random.normal(1, 0.05, 100)
    values = trend * seasonality * noise
    return pd.DataFrame({"value": values}, index=dates)


def test_init_valid():
    decomposer = SeasonalDecomposer(value_column="val", model="additive", period=7)
    assert decomposer.value_column == "val"
    assert decomposer.model == "additive"
    assert decomposer.period == 7


def test_init_invalid_model():
    with pytest.raises(
        ValueError, match="Model must be either 'additive' or 'multiplicative'."
    ):
        SeasonalDecomposer(value_column="val", model="invalid_model")


def test_validate_input_not_df():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(TypeError, match="Input must be a pandas DataFrame."):
        decomposer._validate_input([1, 2, 3])


def test_validate_input_empty_df():
    decomposer = SeasonalDecomposer(value_column="value")
    df = pd.DataFrame(columns=["value"])
    with pytest.raises(ValueError, match="Input DataFrame is empty."):
        decomposer._validate_input(df)


def test_validate_input_missing_column():
    decomposer = SeasonalDecomposer(value_column="value")
    df = pd.DataFrame(
        {"other_col": [1, 2, 3]}, index=pd.date_range("2023-01-01", periods=3)
    )
    with pytest.raises(
        ValueError, match="Value column 'value' not found in DataFrame."
    ):
        decomposer._validate_input(df)


def test_validate_input_invalid_index():
    decomposer = SeasonalDecomposer(value_column="value")
    df = pd.DataFrame({"value": [1, 2, 3]}, index=["a", "b", "c"])
    with pytest.raises(
        ValueError,
        match="DataFrame index must be a DatetimeIndex or convertible to one.",
    ):
        decomposer._validate_input(df)


def test_validate_input_convertible_index():
    decomposer = SeasonalDecomposer(value_column="value")
    df = pd.DataFrame(
        {"value": [1, 2, 3]}, index=["2023-01-01", "2023-01-02", "2023-01-03"]
    )
    validated = decomposer._validate_input(df)
    assert pd.api.types.is_datetime64_any_dtype(validated.index)


def test_handle_missing_values():
    decomposer = SeasonalDecomposer(value_column="value")
    dates = pd.date_range(start="2023-01-01", periods=5, freq="D")
    series = pd.Series([1.0, np.nan, 3.0, np.nan, np.nan], index=dates)
    filled = decomposer._handle_missing_values(series)
    assert not filled.isna().any()
    assert filled.iloc[1] == 2.0  # Interpolated


def test_handle_missing_values_edge_nans():
    decomposer = SeasonalDecomposer(value_column="value")
    dates = pd.date_range(start="2023-01-01", periods=5, freq="D")
    series = pd.Series([np.nan, np.nan, 3.0, 4.0, np.nan], index=dates)
    filled = decomposer._handle_missing_values(series)
    assert not filled.isna().any()
    assert filled.iloc[0] == 3.0
    assert filled.iloc[4] == 4.0


def test_decompose_series_additive(sample_additive_data):
    decomposer = SeasonalDecomposer(value_column="value", model="additive", period=7)
    result = decomposer.decompose_series(sample_additive_data)
    assert "observed" in result
    assert "trend" in result
    assert "seasonal" in result
    assert "resid" in result
    assert len(result["trend"]) == len(sample_additive_data)


def test_decompose_series_multiplicative(sample_multiplicative_data):
    decomposer = SeasonalDecomposer(
        value_column="value", model="multiplicative", period=7
    )
    result = decomposer.decompose_series(sample_multiplicative_data)
    assert "observed" in result
    assert "trend" in result
    assert "seasonal" in result
    assert "resid" in result


def test_decompose_series_insufficient_observations():
    decomposer = SeasonalDecomposer(value_column="value", period=10)
    df = pd.DataFrame(
        {"value": [1] * 15}, index=pd.date_range("2023-01-01", periods=15)
    )
    with pytest.raises(ValueError, match="Insufficient observations"):
        decomposer.decompose_series(df)


def test_decompose_series_multiplicative_negative_values():
    decomposer = SeasonalDecomposer(
        value_column="value", model="multiplicative", period=7
    )
    df = pd.DataFrame(
        {"value": [-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
        index=pd.date_range("2023-01-01", periods=15),
    )
    with pytest.raises(
        ValueError,
        match="Multiplicative decomposition requires strictly positive values.",
    ):
        decomposer.decompose_series(df)


def test_get_trend_before_decompose():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(RuntimeError, match="Must call decompose_series first."):
        decomposer.get_trend()


def test_get_seasonality_before_decompose():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(RuntimeError, match="Must call decompose_series first."):
        decomposer.get_seasonality()


def test_get_residuals_before_decompose():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(RuntimeError, match="Must call decompose_series first."):
        decomposer.get_residuals()


def test_reconstruct_series_before_decompose():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(RuntimeError, match="Must call decompose_series first."):
        decomposer.reconstruct_series()


def test_reconstruct_series_additive(sample_additive_data):
    decomposer = SeasonalDecomposer(value_column="value", model="additive", period=7)
    decomposer.decompose_series(sample_additive_data)
    reconstructed = decomposer.reconstruct_series()
    # Allowing a small tolerance for floating point errors
    pd.testing.assert_series_equal(
        reconstructed, sample_additive_data["value"], check_names=False, rtol=1e-5
    )


def test_reconstruct_series_multiplicative(sample_multiplicative_data):
    decomposer = SeasonalDecomposer(
        value_column="value", model="multiplicative", period=7
    )
    decomposer.decompose_series(sample_multiplicative_data)
    reconstructed = decomposer.reconstruct_series()
    pd.testing.assert_series_equal(
        reconstructed, sample_multiplicative_data["value"], check_names=False, rtol=1e-5
    )


def test_plot_components(sample_additive_data):
    decomposer = SeasonalDecomposer(value_column="value", model="additive", period=7)
    decomposer.decompose_series(sample_additive_data)
    fig = decomposer.plot_components()
    assert fig is not None
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_plot_components_before_decompose():
    decomposer = SeasonalDecomposer(value_column="value")
    with pytest.raises(RuntimeError, match="Must call decompose_series first."):
        decomposer.plot_components()


def test_automatic_period_detection_with_freq():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    values = np.random.normal(0, 1, 100)
    df = pd.DataFrame({"value": values}, index=dates)

    decomposer = SeasonalDecomposer(value_column="value")
    # Should not raise an error, freq is 'D' which gives period=7
    # typically, but here we don't set it explicitly
    result = decomposer.decompose_series(df)
    assert result is not None


def test_automatic_period_detection_without_freq():
    # If no freq is set, we might get a fallback to period=1
    # or similar if we don't handle it
    dates = pd.DatetimeIndex(
        [
            "2023-01-01",
            "2023-01-02",
            "2023-01-05",
            "2023-01-07",
            "2023-01-10",
            "2023-01-12",
            "2023-01-15",
        ]
    )
    # Need sufficient values for fallback period=1 (at least 2)
    values = np.arange(7)
    df = pd.DataFrame({"value": values}, index=dates)
    decomposer = SeasonalDecomposer(value_column="value")

    result = decomposer.decompose_series(df)
    assert result is not None
