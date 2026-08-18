import { useState } from "react";

import ForecastForm from "./ForecastForm";
import ForecastTable from "./ForecastTable";
import { generateForecast } from "./forecastApi";

import type {
  DemandObservation,
  ForecastRequest,
  ForecastResponse,
} from "./types";

const FORECAST_MODELS = [
  "auto",
  "arima_1_0_0",
  "arima_1_1_1",
  "moving_average_3",
  "moving_average_7",
];

const ForecastPage = () => {
  const [forecast, setForecast] =
    useState<ForecastResponse | null>(null);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const handleGenerateForecast = async (
    forecastRequest: ForecastRequest,
    _observations: DemandObservation[],
  ) => {
    try {
      setSubmitting(true);
      setError(null);
      setForecast(null);

      const result = await generateForecast(
        forecastRequest,
      );

      setForecast(result);
    } catch (err) {
      console.error(
        "Failed to generate forecast:",
        err,
      );

      setError(
        "Failed to generate forecast. Please check the entered data and API connection.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Forecast</h1>

          <p>
            Generate demand forecasts using historical
            supply chain data.
          </p>
        </div>
      </div>

      {error && (
        <div className="inventory-message inventory-message--error">
          {error}
        </div>
      )}

      <ForecastForm
        models={FORECAST_MODELS}
        loadingModels={false}
        onSubmit={handleGenerateForecast}
        submitting={submitting}
      />

      {forecast && (
        <>
          <div className="inventory-kpis">
            <div className="inventory-card">
              <span>SKU</span>

              <strong>
                {forecast.sku_id}
              </strong>
            </div>

            <div className="inventory-card">
              <span>Model</span>

              <strong>
                {forecast.model_name}
              </strong>
            </div>

            <div className="inventory-card">
              <span>Forecast Horizon</span>

              <strong>
                {forecast.forecast_horizon} days
              </strong>
            </div>
          </div>

          <div className="settings-card">
            <div className="settings-card-header">
              <h2>Forecast Results</h2>

              <p>
                Generated at{" "}
                {new Date(
                  forecast.generated_at,
                ).toLocaleString("en-IN")}
              </p>
            </div>

            <ForecastTable
              forecasts={forecast.forecasts}
            />
          </div>

          {forecast.metrics && (
            <div className="settings-card">
              <div className="settings-card-header">
                <h2>Forecast Metrics</h2>

                <p>
                  Evaluation metrics returned by the
                  forecasting model.
                </p>
              </div>

              <div className="inventory-kpis">
                <div className="inventory-card">
                  <span>MAE</span>

                  <strong>
                    {forecast.metrics.mae.toFixed(2)}
                  </strong>
                </div>

                <div className="inventory-card">
                  <span>MAPE</span>

                  <strong>
                    {forecast.metrics.mape !== null
                      ? `${forecast.metrics.mape.toFixed(2)}%`
                      : "-"}
                  </strong>
                </div>

                <div className="inventory-card">
                  <span>RMSE</span>

                  <strong>
                    {forecast.metrics.rmse.toFixed(2)}
                  </strong>
                </div>

                <div className="inventory-card">
                  <span>R²</span>

                  <strong>
                    {forecast.metrics.r2 !== null
                      ? forecast.metrics.r2.toFixed(2)
                      : "-"}
                  </strong>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </section>
  );
};

export default ForecastPage;