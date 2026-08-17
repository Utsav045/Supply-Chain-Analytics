"""Tests for forecasting model persistence."""

import pandas as pd
import pytest

from src.forecasting.moving_average import (
    MovingAverageForecaster,
)
from src.forecasting.persistence import (
    ModelPersistenceError,
    ModelStore,
)


@pytest.fixture
def fitted_model() -> MovingAverageForecaster:
    """Return a fitted Moving Average model."""
    series = pd.Series(
        data=[
            10.0,
            12.0,
            14.0,
            16.0,
            18.0,
            20.0,
        ],
        index=pd.date_range(
            start="2026-01-01",
            periods=6,
            freq="D",
        ),
        name="demand",
    )

    model = MovingAverageForecaster(window=3)
    model.fit(series)

    return model


def test_fitted_model_can_be_saved(
    tmp_path,
    fitted_model: MovingAverageForecaster,
) -> None:
    """Saving should create model and metadata files."""
    store = ModelStore(tmp_path)

    artifact = store.save(
        fitted_model,
        sku_id="SKU-001",
        location_id="LAGOS-01",
    )

    assert artifact.model_path.is_file()
    assert artifact.metadata_path.is_file()
    assert len(artifact.sha256) == 64


def test_saved_model_can_be_loaded(
    tmp_path,
    fitted_model: MovingAverageForecaster,
) -> None:
    """A valid persisted model should retain its behaviour."""
    store = ModelStore(tmp_path)

    artifact = store.save(
        fitted_model,
        sku_id="SKU-001",
    )

    loaded_model = store.load(artifact.artifact_id)

    original_forecast = fitted_model.predict(horizon=2)
    loaded_forecast = loaded_model.predict(horizon=2)

    assert loaded_model.model_name == (fitted_model.model_name)

    assert loaded_forecast.equals(original_forecast)


def test_metadata_can_be_read(
    tmp_path,
    fitted_model: MovingAverageForecaster,
) -> None:
    """Artifact metadata should describe the model."""
    store = ModelStore(tmp_path)

    artifact = store.save(
        fitted_model,
        sku_id="SKU-001",
        location_id="ABUJA-01",
    )

    metadata = store.get_metadata(artifact.artifact_id)

    assert metadata["sku_id"] == "SKU-001"
    assert metadata["location_id"] == "ABUJA-01"
    assert metadata["model_name"] == "moving_average_3"


def test_unfitted_model_is_rejected(
    tmp_path,
) -> None:
    """Only trained models should be persisted."""
    store = ModelStore(tmp_path)
    model = MovingAverageForecaster(window=3)

    with pytest.raises(
        ModelPersistenceError,
        match="must be fitted",
    ):
        store.save(
            model,
            sku_id="SKU-001",
        )


def test_modified_artifact_fails_checksum(
    tmp_path,
    fitted_model: MovingAverageForecaster,
) -> None:
    """Unexpected file changes should be detected."""
    store = ModelStore(tmp_path)

    artifact = store.save(
        fitted_model,
        sku_id="SKU-001",
    )

    with artifact.model_path.open("ab") as model_file:
        model_file.write(b"tampered")

    with pytest.raises(
        ModelPersistenceError,
        match="checksum",
    ):
        store.load(artifact.artifact_id)


def test_path_traversal_identifier_is_rejected(
    tmp_path,
) -> None:
    """Artifact identifiers cannot escape the model directory."""
    store = ModelStore(tmp_path)

    with pytest.raises(
        ModelPersistenceError,
        match="Invalid model artifact",
    ):
        store.load("../../unauthorized")
