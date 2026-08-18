import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch, RootState } from "../../store/store";
import { fetchDashboardData } from "./dashboardSlice";
import SalesTrendChart from "./SalesTrendChart";
import TopProductsChart from "./TopProductsChart";
import ServiceLevelChart from "./ServiceLevelChart";
import SupplyRiskAlerts from "./SupplyRiskAlerts";

const DashboardPage = () => {
  const dispatch = useDispatch<AppDispatch>();

  const { data, loading, error } = useSelector(
    (state: RootState) => state.dashboard,
  );

  useEffect(() => {
    void dispatch(fetchDashboardData());
  }, [dispatch]);

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
        maximumFractionDigits: 2,
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
      {/* Page Header */}
      <div className="dashboard-heading">
        <div>
          <h1>Executive Overview</h1>
          <p>Monitor your supply chain performance</p>
        </div>
      </div>

      {/* KPI Cards */}
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

      {/* Sales & Products Charts */}
      <div className="dashboard-charts-grid">
        <SalesTrendChart />
        <TopProductsChart />
      </div>

      {/* Executive Metrics */}
      <div className="dashboard-metrics-grid">
        {/* 1. Service Level */}
        <ServiceLevelChart value={data.service_level} />

        {/* 2. Top Performing Category */}
        <article className="dashboard-panel">
          <div className="panel-header">
            <div>
              <h2>Top Performing Category</h2>
              <span>Category with highest sales volume</span>
            </div>
          </div>

          <div className="metric-highlight">
            <strong>Electronics</strong>
            <span>Top category</span>
          </div>
        </article>

        {/* 3. Supply Risk Alerts */}
        <SupplyRiskAlerts count={data.anomalies.high} />
      </div>

      {/* Bottom Dashboard Panels */}
      <div className="dashboard-bottom-grid">
        {/* Anomaly Overview */}
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

        {/* Supply Chain Metrics */}
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