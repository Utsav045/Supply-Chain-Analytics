"""Configuration utilities for ARIMA forecasting models."""

from collections.abc import Sequence
from dataclasses import dataclass

from src.forecasting.model_validation import (
    ModelInputValidationError,
)


def _validate_order_value(
    value: int,
    field_name: str,
) -> int:
    """
    Validate one component of an ARIMA order.

    Args:
        value: ARIMA order component.
        field_name: Name used in validation messages.

    Returns:
        Validated non-negative integer.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ModelInputValidationError(f"{field_name} must be an integer.")

    if value < 0:
        raise ModelInputValidationError(f"{field_name} cannot be negative.")

    return value


@dataclass(frozen=True, slots=True)
class ARIMAConfig:
    """Represent one non-seasonal ARIMA model configuration."""

    p: int = 1
    d: int = 1
    q: int = 1
    enforce_stationarity: bool = True
    enforce_invertibility: bool = True

    def __post_init__(self) -> None:
        """Validate the complete ARIMA configuration."""
        _validate_order_value(self.p, "p")
        _validate_order_value(self.d, "d")
        _validate_order_value(self.q, "q")

        if not isinstance(self.enforce_stationarity, bool):
            raise ModelInputValidationError("enforce_stationarity must be boolean.")

        if not isinstance(self.enforce_invertibility, bool):
            raise ModelInputValidationError("enforce_invertibility must be boolean.")

    @property
    def order(self) -> tuple[int, int, int]:
        """Return the statsmodels ARIMA order."""
        return self.p, self.d, self.q

    @property
    def model_name(self) -> str:
        """Return a unique model name for the configuration."""
        return f"arima_{self.p}_{self.d}_{self.q}"

    @property
    def minimum_observations(self) -> int:
        """
        Return a conservative minimum training-series length.

        More complex orders require additional historical observations.
        """
        return max(
            12,
            self.p + self.d + self.q + 8,
        )


def _validate_candidate_values(
    values: Sequence[int],
    field_name: str,
) -> tuple[int, ...]:
    """Validate candidate values used in ARIMA grid generation."""
    if isinstance(values, str) or not isinstance(values, Sequence):
        raise ModelInputValidationError(f"{field_name} candidates must be a sequence.")

    if not values:
        raise ModelInputValidationError(f"{field_name} candidates cannot be empty.")

    validated = {_validate_order_value(value, field_name) for value in values}

    return tuple(sorted(validated))


def generate_arima_configs(
    p_values: Sequence[int] = (0, 1, 2),
    d_values: Sequence[int] = (0, 1),
    q_values: Sequence[int] = (0, 1, 2),
    maximum_total_order: int = 5,
) -> list[ARIMAConfig]:
    """
    Generate validated ARIMA candidate configurations.

    Args:
        p_values: Candidate autoregressive orders.
        d_values: Candidate differencing orders.
        q_values: Candidate moving-average orders.
        maximum_total_order: Maximum permitted p + d + q.

    Returns:
        ARIMA configurations ordered by total complexity.
    """
    if not isinstance(maximum_total_order, int) or isinstance(
        maximum_total_order, bool
    ):
        raise ModelInputValidationError("maximum_total_order must be an integer.")

    if maximum_total_order < 0:
        raise ModelInputValidationError("maximum_total_order cannot be negative.")

    validated_p = _validate_candidate_values(
        p_values,
        "p",
    )
    validated_d = _validate_candidate_values(
        d_values,
        "d",
    )
    validated_q = _validate_candidate_values(
        q_values,
        "q",
    )

    configurations = [
        ARIMAConfig(p=p, d=d, q=q)
        for p in validated_p
        for d in validated_d
        for q in validated_q
        if p + d + q <= maximum_total_order
    ]

    if not configurations:
        raise ModelInputValidationError(
            "No ARIMA configurations satisfy the supplied constraints."
        )

    return sorted(
        configurations,
        key=lambda configuration: (
            sum(configuration.order),
            configuration.d,
            configuration.p,
            configuration.q,
        ),
    )
