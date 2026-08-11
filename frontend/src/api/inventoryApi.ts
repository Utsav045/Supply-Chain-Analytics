import api from "./axios";
import type { InventoryItem } from "../features/inventory/types";

export const getInventory = async (): Promise<InventoryItem[]> => {
  const response = await api.get("/inventory");
  return response.data;
};