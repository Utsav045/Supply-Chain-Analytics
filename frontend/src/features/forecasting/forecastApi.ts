import axios from "axios";

import type {
  ForecastRequest,
  ForecastResponse,
} from "./types";

const forecastingApi = axios.create({
  baseURL: "http://localhost:8001/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export const generateForecast = async (
  request: ForecastRequest,
): Promise<ForecastResponse> => {
  const response = await forecastingApi.post<ForecastResponse>(
    "/forecast",
    request,
  );

  return response.data;
};