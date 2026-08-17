import api from "../../api/axios";
import type { LogisticsRecord } from "./types";

export const getLogistics = async (): Promise<LogisticsRecord[]> => {
  const response = await api.get("/suppliers");
  return response.data;
};