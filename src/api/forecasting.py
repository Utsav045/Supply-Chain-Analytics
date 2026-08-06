"""FastAPI routes for demand forecasting."""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Annotated

import pandas as pd
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.forecasting.arima import ARIMAModelError
from src.forecasting.model_validation import (
    ModelInputValidationError,
)
from src.forecasting.persistence import (
    ModelPersistenceError,
    ModelStore,
)
from src.forecasting.response_mapper import (
    build_forecast_response,
)
from src.forecasting.schemas import (
    ForecastExecutionRequest,
    ForecastResponse,
)
from src.forecasting.validation import (
    ForecastingDataValidationError,
)
from src.services.forecasting_service import (
    ForecastingService,
)

LOGGER = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/forecasting",
    tags=["forecasting"],
)


@lru_cache(maxsize=1)
def get_forecasting_service() -> ForecastingService:
    """Return the application forecasting service."""
    return ForecastingService(model_store=ModelStore(Path("models") / "forecasting"))


ForecastingServiceDependency = Annotated[
    ForecastingService,
    Depends(get_forecasting_service),
]


@router.get(
    "/models",
    response_model=list[str],
)
def list_forecasting_models(
    service: ForecastingServiceDependency,
) -> list[str]:
    """Return forecasting models supported by the API."""
    return list(service.available_models)


@router.post(
    "/forecast",
    response_model=ForecastResponse,
    status_code=status.HTTP_200_OK,
)
def generate_forecast(
    payload: ForecastExecutionRequest,
    service: ForecastingServiceDependency,
) -> ForecastResponse:
    """Generate a demand forecast from historical observations."""
    dataframe = pd.DataFrame(
        [observation.model_dump(mode="python") for observation in payload.observations]
    )

    try:
        result = service.forecast(
            dataframe=dataframe,
            request=payload.forecast,
            persist_model=payload.persist_model,
        )

        return build_forecast_response(result)

    except (
        ForecastingDataValidationError,
        ModelInputValidationError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except (
        ARIMAModelError,
        ModelPersistenceError,
        RuntimeError,
    ) as exc:
        LOGGER.exception("Forecast generation failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Forecast generation failed.",
        ) from exc
