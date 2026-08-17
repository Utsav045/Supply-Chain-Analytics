import type { ForecastPoint } from "./types";

interface ForecastTableProps {
  forecasts: ForecastPoint[];
}

const ForecastTable = ({ forecasts }: ForecastTableProps) => {
  if (forecasts.length === 0) {
    return (
      <div className="inventory-message">
        No forecast results available.
      </div>
    );
  }

  return (
    <div className="inventory-table-wrapper">
      <table className="inventory-table">
        <thead>
          <tr>
            <th>Forecast Date</th>
            <th>Predicted Demand</th>
            <th>Lower Bound</th>
            <th>Upper Bound</th>
          </tr>
        </thead>

        <tbody>
          {forecasts.map((forecast) => (
            <tr key={forecast.forecast_date}>
              <td>
                {new Date(
                  forecast.forecast_date,
                ).toLocaleDateString("en-IN")}
              </td>

              <td>
                {forecast.predicted_demand.toFixed(2)}
              </td>

              <td>
                {forecast.lower_bound !== null &&
                forecast.lower_bound !== undefined
                  ? forecast.lower_bound.toFixed(2)
                  : "-"}
              </td>

              <td>
                {forecast.upper_bound !== null &&
                forecast.upper_bound !== undefined
                  ? forecast.upper_bound.toFixed(2)
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ForecastTable;