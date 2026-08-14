import { useEffect, useState } from "react";
import { getDashboardSummary } from "./dashboardService";
import type { DashboardSummary } from "./types";

const DashboardPage = () => {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const result = await getDashboardSummary();
        setData(result);
      } catch (err) {
        console.error("Failed to load dashboard:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <section className="dashboard-page">
        <h1>Executive Overview</h1>
        <p>Loading dashboard data...</p>
      </section>
    );
  }

  if (error || !data) {
    return (
      <section className="dashboard-page">
        <h1>Executive Overview</h1>
        <p>{error || "No dashboard data available."}</p>
      </section>
    );
  }

  const kpiCards = [
    {
      title: "Total Products",
      value: data.total_products.toLocaleString(),
      period: "Products in catalog",
    },
    {
      title: "Total Sales Volume",
      value: data.total_sales_volume.toLocaleString(),
      period: "Units sold",
    },
    {
      title: "Total Revenue",
      value: `₹${data.total_revenue.toLocaleString("en-IN", {
        minimumFractionDigits: 2,
      })}`,
      period: "Total sales revenue",
    },
    {
      title: "Total Anomalies",
      value: data.total_anomalies.toLocaleString(),
      period: "Detected anomalies",
    },
  ];

  return (
    <section className="dashboard-page">
      <div className="dashboard-heading">
        <div>
          <h1>Executive Overview</h1>
          <p>Monitor your supply chain performance</p>
        </div>
      </div>

      <div className="kpi-grid">
        {kpiCards.map((card) => (
          <article className="kpi-card" key={card.title}>
            <div className="kpi-card-header">
              <span className="kpi-card-title">{card.title}</span>
            </div>

            <div className="kpi-value">{card.value}</div>

            <div className="kpi-change positive">
              <span>{card.period}</span>
            </div>
          </article>
        ))}
      </div>

      <div className="dashboard-bottom-grid">
        <article className="dashboard-panel">
          <div className="panel-header">
            <h2>Anomaly Overview</h2>
            <span>{data.total_anomalies} total</span>
          </div>

          <div className="anomaly-grid">
            <div>
              <strong>{data.anomalies.high}</strong>
              <span>High</span>
            </div>

            <div>
              <strong>{data.anomalies.medium}</strong>
              <span>Medium</span>
            </div>

            <div>
              <strong>{data.anomalies.low}</strong>
              <span>Low</span>
            </div>
          </div>
        </article>

        <article className="dashboard-panel">
          <div className="panel-header">
            <h2>Supply Chain Metrics</h2>
          </div>

          <div className="metric-row">
            <span>Total Inventory</span>
            <strong>{data.total_inventory.toLocaleString()}</strong>
          </div>

          <div className="metric-row">
            <span>Total Forecast</span>
            <strong>{data.total_forecast.toLocaleString()}</strong>
          </div>
        </article>
      </div>
    </section>
  );
};

export default DashboardPage;