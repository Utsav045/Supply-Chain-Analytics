import api from "./axios";

export interface ReportProduct {
  productId: string;
  productName: string;
  revenue: number;
}

export interface ReportsData {
  totalOrders: number;
  totalQuantity: number;
  totalRevenue: number;
  supplierCount: number;
  topProducts: ReportProduct[];
}

export const getReports = async (): Promise<ReportsData> => {
  const response = await api.get("/reports");
  return response.data;
};