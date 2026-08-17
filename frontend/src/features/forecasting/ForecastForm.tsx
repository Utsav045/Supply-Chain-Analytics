import { useState } from "react";

import type {
  DemandObservation,
  ForecastRequest,
} from "./types";

interface ForecastFormProps {
  models: string[];
  loadingModels: boolean;
  onSubmit: (
    forecast: ForecastRequest,
    observations: DemandObservation[],
  ) => void;
  submitting: boolean;
}

const ForecastForm = ({
  models,
  loadingModels,
  onSubmit,
  submitting,
}: ForecastFormProps) => {
  const [skuId, setSkuId] = useState("");
  const [locationId, setLocationId] = useState("");
  const [forecastHorizon, setForecastHorizon] = useState(30);
  const [modelName, setModelName] = useState("auto");
  const [confidenceLevel, setConfidenceLevel] = useState(0.95);

  const [observations, setObservations] = useState<
    DemandObservation[]
  >([
    {
      date: "",
      sku_id: "",
      demand: 0,
      inventory_level: null,
      price: null,
      promotion: false,
      holiday: false,
      location_id: null,
    },
    {
      date: "",
      sku_id: "",
      demand: 0,
      inventory_level: null,
      price: null,
      promotion: false,
      holiday: false,
      location_id: null,
    },
    {
      date: "",
      sku_id: "",
      demand: 0,
      inventory_level: null,
      price: null,
      promotion: false,
      holiday: false,
      location_id: null,
    },
    {
      date: "",
      sku_id: "",
      demand: 0,
      inventory_level: null,
      price: null,
      promotion: false,
      holiday: false,
      location_id: null,
    },
  ]);

  const updateObservation = (
    index: number,
    field: keyof DemandObservation,
    value: string | number | boolean | null,
  ) => {
    setObservations((current) =>
      current.map((observation, observationIndex) =>
        observationIndex === index
          ? {
              ...observation,
              [field]: value,
              ...(field === "date" && {
                date: String(value),
              }),
              ...(field === "demand" && {
                demand: Number(value),
              }),
            }
          : observation,
      ),
    );
  };

  const handleSubmit = (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    const preparedObservations = observations.map(
      (observation) => ({
        ...observation,
        sku_id: skuId.trim(),
        location_id: locationId.trim() || null,
      }),
    );

    onSubmit(
      {
        sku_id: skuId.trim(),
        location_id: locationId.trim() || null,
        forecast_horizon: forecastHorizon,
        model_name: modelName,
        confidence_level: confidenceLevel,
      },
      preparedObservations,
    );
  };

  return (
    <form
      className="settings-card"
      onSubmit={handleSubmit}
    >
      <div className="settings-card-header">
        <h2>Forecast Configuration</h2>
        <p>
          Configure the demand forecast using historical
          observations.
        </p>
      </div>

      <div className="settings-form-grid">
        <div className="settings-field">
          <label htmlFor="forecast-sku">
            SKU ID
          </label>

          <p className="settings-field-description">
            SKU for which the forecast should be generated.
          </p>

          <input
            id="forecast-sku"
            type="text"
            value={skuId}
            onChange={(event) =>
              setSkuId(event.target.value)
            }
            className="settings-input"
            placeholder="Enter SKU ID"
            required
          />
        </div>

        <div className="settings-field">
          <label htmlFor="forecast-location">
            Location ID
          </label>

          <p className="settings-field-description">
            Optional location identifier.
          </p>

          <input
            id="forecast-location"
            type="text"
            value={locationId}
            onChange={(event) =>
              setLocationId(event.target.value)
            }
            className="settings-input"
            placeholder="Optional"
          />
        </div>

        <div className="settings-field">
          <label htmlFor="forecast-horizon">
            Forecast Horizon
          </label>

          <p className="settings-field-description">
            Number of future days to forecast.
          </p>

          <input
            id="forecast-horizon"
            type="number"
            min={1}
            max={365}
            value={forecastHorizon}
            onChange={(event) =>
              setForecastHorizon(
                Number(event.target.value),
              )
            }
            className="settings-input"
            required
          />
        </div>

        <div className="settings-field">
          <label htmlFor="forecast-model">
            Forecast Model
          </label>

          <p className="settings-field-description">
            Select the forecasting model.
          </p>

          <select
            id="forecast-model"
            value={modelName}
            onChange={(event) =>
              setModelName(event.target.value)
            }
            className="settings-select"
            disabled={loadingModels}
          >
            {models.length === 0 ? (
              <option value="auto">
                auto
              </option>
            ) : (
              models.map((model) => (
                <option
                  key={model}
                  value={model}
                >
                  {model}
                </option>
              ))
            )}
          </select>
        </div>

        <div className="settings-field">
          <label htmlFor="forecast-confidence">
            Confidence Level
          </label>

          <p className="settings-field-description">
            Statistical confidence level.
          </p>

          <select
            id="forecast-confidence"
            value={confidenceLevel}
            onChange={(event) =>
              setConfidenceLevel(
                Number(event.target.value),
              )
            }
            className="settings-select"
          >
            <option value={0.9}>90%</option>
            <option value={0.95}>95%</option>
            <option value={0.99}>99%</option>
          </select>
        </div>
      </div>

      <div className="settings-card-header" style={{ marginTop: "24px" }}>
        <h2>Historical Observations</h2>
        <p>
          Enter at least 4 historical observations required
          by the forecasting API.
        </p>
      </div>

      <div className="inventory-table-wrapper">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Demand</th>
              <th>Inventory</th>
              <th>Price</th>
              <th>Promotion</th>
              <th>Holiday</th>
            </tr>
          </thead>

          <tbody>
            {observations.map(
              (observation, index) => (
                <tr key={index}>
                  <td>
                    <input
                      type="datetime-local"
                      value={observation.date}
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "date",
                          event.target.value,
                        )
                      }
                      required
                    />
                  </td>

                  <td>
                    <input
                      type="number"
                      min={0}
                      value={observation.demand}
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "demand",
                          event.target.value,
                        )
                      }
                      required
                    />
                  </td>

                  <td>
                    <input
                      type="number"
                      min={0}
                      value={
                        observation.inventory_level ?? ""
                      }
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "inventory_level",
                          event.target.value === ""
                            ? null
                            : Number(
                                event.target.value,
                              ),
                        )
                      }
                    />
                  </td>

                  <td>
                    <input
                      type="number"
                      min={0}
                      value={
                        observation.price ?? ""
                      }
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "price",
                          event.target.value === ""
                            ? null
                            : Number(
                                event.target.value,
                              ),
                        )
                      }
                    />
                  </td>

                  <td>
                    <input
                      type="checkbox"
                      checked={
                        observation.promotion ?? false
                      }
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "promotion",
                          event.target.checked,
                        )
                      }
                    />
                  </td>

                  <td>
                    <input
                      type="checkbox"
                      checked={
                        observation.holiday ?? false
                      }
                      onChange={(event) =>
                        updateObservation(
                          index,
                          "holiday",
                          event.target.checked,
                        )
                      }
                    />
                  </td>
                </tr>
              ),
            )}
          </tbody>
        </table>
      </div>

      <div className="settings-save-area">
        <button
          type="submit"
          className="settings-save-button"
          disabled={submitting}
        >
          {submitting
            ? "Generating..."
            : "Generate Forecast"}
        </button>
      </div>
    </form>
  );
};

export default ForecastForm;