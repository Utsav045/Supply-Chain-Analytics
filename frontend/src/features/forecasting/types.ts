export interface DemandObservation {
  date: string;
  sku_id: string;
  demand: number;
  inventory_level?: number | null;
  price?: number | null;
  promotion?: boolean | null;
  holiday?: boolean | null;
  category?: string | null;
  location_id?: string | null;
}

export interface ForecastRequest {
  sku_id: string;
  location_id?: string | null;
  forecast_horizon: number;
  model_name: string;
  confidence_level: number;
}

export interface ForecastExecutionRequest {
  forecast: ForecastRequest;
  observations: DemandObservation[];
  persist_model: boolean;
}

export interface ForecastPoint {
  forecast_date: string;
  predicted_demand: number;
  lower_bound?: number | null;
  upper_bound?: number | null;
}

export interface ForecastMetrics {
  mae: number;
  mape: number | null;
  mse: number;
  rmse: number;
  r2: number | null;
}

export interface ForecastResponse {
  sku_id: string;
  location_id: string | null;
  model_name: string;
  forecast_horizon: number;
  generated_at: string;
  metrics: ForecastMetrics | null;
  forecasts: ForecastPoint[];
  model_artifact_id: string | null;
}