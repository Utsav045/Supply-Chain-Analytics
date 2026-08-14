export interface DashboardSummary {
  total_products: number;
  total_sales_volume: number;
  total_revenue: number;
  total_inventory: number;
  total_forecast: number;
  total_anomalies: number;
  anomalies: {
    high: number;
    medium: number;
    low: number;
  };
}