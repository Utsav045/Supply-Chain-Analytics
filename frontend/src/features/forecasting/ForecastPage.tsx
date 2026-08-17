import { useEffect, useState } from "react";

import ForecastForm from "./ForecastForm";
import ForecastTable from "./ForecastTable";
import {
  generateForecast,
  getForecastingModels,
} from "./forecastApi";
import type {
  DemandObservation,
  ForecastRequest,
  ForecastResponse,
} from "./types";

const ForecastPage = () => {
  const [models, setModels] = useState<string[]>([]);
  const [loadingModels, setLoadingModels] = useState(true);

  const [forecast, setForecast] =
    useState<ForecastResponse | null>(null);

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadModels = async () => {
      try {
        setLoadingModels(true);
        setError(null);

        const availableModels =
          await getForecastingModels();

        setModels(availableModels);
      } catch (err) {
        console.error(
          "Failed to load forecasting models:",
          err,
        );

        setError(
          "Failed to load forecasting models.",
        );
      } finally {
        setLoadingModels(false);
      }
    };

    void loadModels();
  }, []);

  const handleGenerateForecast = async (
    forecastRequest: ForecastRequest,
    observations: DemandObservation[],
  ) => {
    try {
      setSubmitting(true);
      setError(null);
      setForecast(null);

      const result = await generateForecast({
        forecast: forecastRequest,
        observations,
        persist_model: false,
      });

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
        models={models}
        loadingModels={loadingModels}
        onSubmit={handleGenerateForecast}
        submitting={submitting}
      />

      {forecast && (
        <>
          <div className="inventory-kpis">
            <div className="inventory-card">
              <span>SKU</span>
              <strong>{forecast.sku_id}</strong>
            </div>

            <div className="inventory-card">
              <span>Model</span>
              <strong>{forecast.model_name}</strong>
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