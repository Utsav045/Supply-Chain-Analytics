import axios from "axios";

import type {
  ForecastExecutionRequest,
  ForecastResponse,
} from "./types";

const forecastingApi = axios.create({
  baseURL: "http://localhost:8001/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getForecastingModels = async (): Promise<string[]> => {
  const response = await forecastingApi.get<string[]>(
    "/forecasting/models",
  );

  return response.data;
};

export const generateForecast = async (
  request: ForecastExecutionRequest,
): Promise<ForecastResponse> => {
  const response = await forecastingApi.post<ForecastResponse>(
    "/forecasting/forecast",
    request,
  );

  return response.data;
};