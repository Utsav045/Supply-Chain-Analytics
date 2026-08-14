import axios from "axios";
import type { DashboardSummary } from "./types";

const API_BASE_URL = "http://localhost:8000/api/v1";

export const getDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await axios.get<DashboardSummary>(
    `${API_BASE_URL}/dashboard/summary`
  );

  return response.data;
};