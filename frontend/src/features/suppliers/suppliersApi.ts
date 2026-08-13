import api from "../../api/axios";
import type { Supplier } from "./types";

export const getSuppliers = async (): Promise<Supplier[]> => {
  const response = await api.get("/suppliers");
  return response.data;
};