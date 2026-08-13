import { useEffect, useState } from "react";
import {
  getReports,
  type ReportsData,
} from "../api/reportsApi";

const Reports = () => {
  const [reports, setReports] = useState<ReportsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadReports = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getReports();
        setReports(data);
      } catch (err) {
        console.error("Failed to load reports:", err);
        setError("Failed to load report data.");
      } finally {
        setLoading(false);
      }
    };

    void loadReports();
  }, []);

  if (loading) {
    return (
      <section className="inventory-page">
        <div className="inventory-message">
          Loading reports...
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="inventory-page">
        <div className="inventory-message inventory-message--error">
          {error}
        </div>
      </section>
    );
  }

  if (!reports) {
    return (
      <section className="inventory-page">
        <div className="inventory-message">
          No report data available.
        </div>
      </section>
    );
  }

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Reports</h1>
          <p>
            View sales performance, revenue and supplier summary.
          </p>
        </div>
      </div>

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Orders</span>
          <strong>
            {reports.totalOrders.toLocaleString()}
          </strong>
        </div>

        <div className="inventory-card">
          <span>Total Quantity</span>
          <strong>
            {reports.totalQuantity.toLocaleString()}
          </strong>
        </div>

        <div className="inventory-card">
          <span>Total Revenue</span>
          <strong>
            ₹{reports.totalRevenue.toLocaleString("en-IN")}
          </strong>
        </div>

        <div className="inventory-card">
          <span>Total Suppliers</span>
          <strong>
            {reports.supplierCount}
          </strong>
        </div>
      </div>

      <div className="inventory-table-wrapper">
        <h2>Top Products by Revenue</h2>

        <table className="inventory-table">
          <thead>
            <tr>
              <th>Product ID</th>
              <th>Product Name</th>
              <th>Revenue</th>
            </tr>
          </thead>

          <tbody>
            {reports.topProducts.map((product) => (
              <tr
                key={`${product.productId}-${product.productName}`}
              >
                <td>{product.productId}</td>
                <td>{product.productName}</td>
                <td>
                  ₹{product.revenue.toLocaleString("en-IN")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default Reports;