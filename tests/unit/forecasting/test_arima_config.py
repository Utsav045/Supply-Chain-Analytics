"""Tests for ARIMA model configuration."""

import pytest

from src.forecasting.arima_config import (
    ARIMAConfig,
    generate_arima_configs,
)
from src.forecasting.model_validation import (
    ModelInputValidationError,
)


def test_default_arima_configuration() -> None:
    """Default configuration should represent ARIMA(1, 1, 1)."""
    configuration = ARIMAConfig()

    assert configuration.order == (1, 1, 1)
    assert configuration.model_name == "arima_1_1_1"
    assert configuration.minimum_observations >= 12


def test_custom_arima_configuration() -> None:
    """Custom order values should be retained."""
    configuration = ARIMAConfig(
        p=2,
        d=0,
        q=3,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    assert configuration.order == (2, 0, 3)
    assert configuration.model_name == "arima_2_0_3"
    assert configuration.enforce_stationarity is False
    assert configuration.enforce_invertibility is False


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("p", -1),
        ("d", -1),
        ("q", -1),
        ("p", 1.5),
        ("d", True),
        ("q", "1"),
    ],
)
def test_invalid_order_component_is_rejected(
    field_name: str,
    invalid_value: object,
) -> None:
    """ARIMA order values must be non-negative integers."""
    parameters: dict[str, object] = {
        "p": 1,
        "d": 1,
        "q": 1,
    }
    parameters[field_name] = invalid_value

    with pytest.raises(ModelInputValidationError):
        ARIMAConfig(**parameters)  # type: ignore[arg-type]


def test_generate_arima_configs_respects_maximum_order() -> None:
    """Generated configurations should respect complexity limits."""
    configurations = generate_arima_configs(
        p_values=(0, 1),
        d_values=(0, 1),
        q_values=(0, 1),
        maximum_total_order=2,
    )

    assert len(configurations) == 7

    assert all(sum(configuration.order) <= 2 for configuration in configurations)


def test_generated_configs_are_unique() -> None:
    """Duplicate candidate values should not duplicate models."""
    configurations = generate_arima_configs(
        p_values=(0, 1, 1),
        d_values=(0, 1),
        q_values=(0, 1, 1),
    )

    orders = [configuration.order for configuration in configurations]

    assert len(orders) == len(set(orders))


def test_generated_configs_are_ordered_by_complexity() -> None:
    """Simpler ARIMA candidates should be returned first."""
    configurations = generate_arima_configs(
        p_values=(0, 1, 2),
        d_values=(0, 1),
        q_values=(0, 1),
    )

    total_orders = [sum(configuration.order) for configuration in configurations]

    assert total_orders == sorted(total_orders)


@pytest.mark.parametrize(
    "invalid_candidates",
    [
        (),
        [],
        "012",
    ],
)
def test_invalid_candidate_collection_is_rejected(
    invalid_candidates: object,
) -> None:
    """Candidate collections must be non-empty integer sequences."""
    with pytest.raises(ModelInputValidationError):
        generate_arima_configs(
            p_values=invalid_candidates,  # type: ignore[arg-type]
        )


def test_impossible_constraints_are_rejected() -> None:
    """At least one candidate must satisfy the order constraint."""
    with pytest.raises(
        ModelInputValidationError,
        match="No ARIMA configurations",
    ):
        generate_arima_configs(
            p_values=(2,),
            d_values=(1,),
            q_values=(2,),
            maximum_total_order=3,
        )
