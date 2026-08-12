import api from "../../api/axios";
import type { Order } from "./types";

export const getOrders = async (): Promise<Order[]> => {
  const response = await api.get("/orders");
  return response.data;
};