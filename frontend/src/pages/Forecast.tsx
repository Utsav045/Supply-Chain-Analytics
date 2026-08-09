import React from "react";

const Forecast: React.FC = () => {
  const forecastData = [
    { day: "Mon", actual: 2350, forecast: 2420 },
    { day: "Tue", actual: 2680, forecast: 2610 },
    { day: "Wed", actual: 2410, forecast: 2490 },
    { day: "Thu", actual: 2940, forecast: 2860 },
    { day: "Fri", actual: 3180, forecast: 3090 },
    { day: "Sat", actual: 3560, forecast: 3480 },
    { day: "Sun", actual: 3290, forecast: 3370 },
  ];

  const productForecast = [
    {
      product: "P001",
      name: "Laptop",
      current: 320,
      forecast: 410,
      change: "+28.1%",
      status: "High",
    },
    {
      product: "P002",
      name: "Phone",
      current: 580,
      forecast: 720,
      change: "+24.1%",
      status: "High",
    },
    {
      product: "P003",
      name: "Chair",
      current: 420,
      forecast: 390,
      change: "-7.1%",
      status: "Normal",
    },
    {
      product: "P004",
      name: "Rice",
      current: 760,
      forecast: 690,
      change: "-9.2%",
      status: "Low",
    },
    {
      product: "P005",
      name: "Tablet",
      current: 280,
      forecast: 350,
      change: "+25.0%",
      status: "High",
    },
  ];

  const warehouses = [
    {
      name: "Mumbai",
      forecast: 4280,
      capacity: 82,
    },
    {
      name: "Bengaluru",
      forecast: 3650,
      capacity: 74,
    },
    {
      name: "Delhi",
      forecast: 3120,
      capacity: 66,
    },
    {
      name: "Kolkata",
      forecast: 2180,
      capacity: 53,
    },
  ];

  const maxValue = Math.max(
    ...forecastData.flatMap((item) => [
      item.actual,
      item.forecast,
    ])
  );

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Demand Forecast</h1>

          <p style={styles.subtitle}>
            Analyze historical demand and predicted future sales
          </p>
        </div>

        <div style={styles.actions}>
          <select style={styles.select}>
            <option>Next 7 Days</option>
            <option>Next 30 Days</option>
            <option>Next 90 Days</option>
          </select>

          <button style={styles.primaryButton}>
            Generate Forecast
          </button>
        </div>
      </div>

      {/* SUMMARY CARDS */}
      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon}>📈</div>

          <div>
            <p style={styles.summaryLabel}>
              Forecast Demand
            </p>

            <h2 style={styles.summaryValue}>
              18,450
            </h2>

            <span style={styles.positive}>
              +12.4% vs previous period
            </span>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon}>🎯</div>

          <div>
            <p style={styles.summaryLabel}>
              Forecast Accuracy
            </p>

            <h2 style={styles.summaryValue}>
              92.4%
            </h2>

            <span style={styles.positive}>
              +3.2% improvement
            </span>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon}>📊</div>

          <div>
            <p style={styles.summaryLabel}>
              MAPE
            </p>

            <h2 style={styles.summaryValue}>
              7.6%
            </h2>

            <span style={styles.positive}>
              Lower is better
            </span>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon}>⚠</div>

          <div>
            <p style={styles.summaryLabel}>
              High Demand Products
            </p>

            <h2 style={styles.summaryValue}>
              8
            </h2>

            <span style={styles.warning}>
              Requires attention
            </span>
          </div>
        </div>
      </div>

      {/* MAIN CHART */}
      <div style={styles.card}>
        <div style={styles.cardHeader}>
          <div>
            <h2 style={styles.cardTitle}>
              Actual vs Forecast Demand
            </h2>

            <p style={styles.cardSubtitle}>
              Daily demand comparison
            </p>
          </div>

          <div style={styles.legend}>
            <span>
              <i
                style={{
                  ...styles.legendDot,
                  background: "#2563eb",
                }}
              />
              Actual
            </span>

            <span>
              <i
                style={{
                  ...styles.legendDot,
                  background: "#93c5fd",
                }}
              />
              Forecast
            </span>
          </div>
        </div>

        <div style={styles.chart}>
          <div style={styles.yAxis}>
            <span>4K</span>
            <span>3K</span>
            <span>2K</span>
            <span>1K</span>
            <span>0</span>
          </div>

          <div style={styles.chartContent}>
            <div style={styles.gridLines}>
              <div />
              <div />
              <div />
              <div />
              <div />
            </div>

            <div style={styles.bars}>
              {forecastData.map((item) => (
                <div
                  key={item.day}
                  style={styles.barGroup}
                >
                  <div style={styles.barContainer}>
                    <div
                      style={{
                        ...styles.actualBar,
                        height: `${
                          (item.actual / maxValue) * 100
                        }%`,
                      }}
                      title={`Actual: ${item.actual}`}
                    />

                    <div
                      style={{
                        ...styles.forecastBar,
                        height: `${
                          (item.forecast / maxValue) * 100
                        }%`,
                      }}
                      title={`Forecast: ${item.forecast}`}
                    />
                  </div>

                  <span style={styles.dayLabel}>
                    {item.day}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* LOWER SECTION */}
      <div style={styles.twoColumn}>
        {/* PRODUCT FORECAST */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Product Forecast
              </h2>

              <p style={styles.cardSubtitle}>
                Expected demand by product
              </p>
            </div>
          </div>

          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Product</th>
                  <th style={styles.th}>Current</th>
                  <th style={styles.th}>Forecast</th>
                  <th style={styles.th}>Change</th>
                  <th style={styles.th}>Status</th>
                </tr>
              </thead>

              <tbody>
                {productForecast.map((product) => (
                  <tr key={product.product}>
                    <td style={styles.td}>
                      <strong>{product.product}</strong>
                      <span style={styles.productName}>
                        {product.name}
                      </span>
                    </td>

                    <td style={styles.td}>
                      {product.current}
                    </td>

                    <td style={styles.td}>
                      <strong>{product.forecast}</strong>
                    </td>

                    <td
                      style={{
                        ...styles.td,
                        color: product.change.startsWith("+")
                          ? "#16a34a"
                          : "#dc2626",
                        fontWeight: 600,
                      }}
                    >
                      {product.change}
                    </td>

                    <td style={styles.td}>
                      <span
                        style={{
                          ...styles.statusBadge,
                          ...(product.status === "High"
                            ? styles.highStatus
                            : product.status === "Low"
                              ? styles.lowStatus
                              : styles.normalStatus),
                        }}
                      >
                        {product.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* WAREHOUSE FORECAST */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Warehouse Demand
              </h2>

              <p style={styles.cardSubtitle}>
                Forecast demand by warehouse
              </p>
            </div>
          </div>

          <div style={styles.warehouseList}>
            {warehouses.map((warehouse) => (
              <div
                key={warehouse.name}
                style={styles.warehouseItem}
              >
                <div style={styles.warehouseHeader}>
                  <strong>{warehouse.name}</strong>

                  <span>
                    {warehouse.forecast.toLocaleString()} units
                  </span>
                </div>

                <div style={styles.progressBackground}>
                  <div
                    style={{
                      ...styles.progressBar,
                      width: `${warehouse.capacity}%`,
                    }}
                  />
                </div>

                <div style={styles.capacityRow}>
                  <span>
                    Expected capacity usage
                  </span>

                  <strong>
                    {warehouse.capacity}%
                  </strong>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* MODEL INFORMATION */}
      <div style={styles.modelCard}>
        <div>
          <h2 style={styles.modelTitle}>
            Forecast Model
          </h2>

          <p style={styles.modelText}>
            The demand forecasting pipeline uses historical
            sales data, calendar features and lag/rolling
            features to estimate future demand.
          </p>
        </div>

        <div style={styles.modelStats}>
          <div>
            <span>Model</span>
            <strong>Time Series</strong>
          </div>

          <div>
            <span>Training Data</span>
            <strong>2024–2026</strong>
          </div>

          <div>
            <span>Accuracy</span>
            <strong>92.4%</strong>
          </div>
        </div>
      </div>
    </div>
  );
};

/* ============================================================
   STYLES
============================================================ */

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    padding: "28px",
    background: "#f5f7fb",
    color: "#172033",
    fontFamily:
      "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    boxSizing: "border-box",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    flexWrap: "wrap",
    marginBottom: "25px",
  },

  title: {
    margin: 0,
    fontSize: "28px",
    fontWeight: 700,
  },

  subtitle: {
    margin: "7px 0 0",
    color: "#6b7280",
    fontSize: "14px",
  },

  actions: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },

  select: {
    padding: "10px 13px",
    border: "1px solid #dce1ea",
    background: "#ffffff",
    borderRadius: "8px",
    color: "#374151",
  },

  primaryButton: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "8px",
    background: "#2563eb",
    color: "#ffffff",
    fontWeight: 600,
    cursor: "pointer",
  },

  summaryGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, minmax(0, 1fr))",
    gap: "18px",
    marginBottom: "20px",
  },

  summaryCard: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
    background: "#ffffff",
    border: "1px solid #e6e9ef",
    borderRadius: "12px",
    padding: "19px",
    boxShadow:
      "0 2px 8px rgba(0, 0, 0, 0.03)",
  },

  summaryIcon: {
    width: "42px",
    height: "42px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    borderRadius: "10px",
    background: "#eff6ff",
    color: "#2563eb",
    fontSize: "19px",
  },

  summaryLabel: {
    margin: 0,
    color: "#6b7280",
    fontSize: "12px",
  },

  summaryValue: {
    margin: "4px 0",
    fontSize: "24px",
  },

  positive: {
    color: "#16a34a",
    fontSize: "11px",
    fontWeight: 600,
  },

  warning: {
    color: "#d97706",
    fontSize: "11px",
    fontWeight: 600,
  },

  card: {
    background: "#ffffff",
    border: "1px solid #e6e9ef",
    borderRadius: "12px",
    padding: "20px",
    boxShadow:
      "0 2px 8px rgba(0, 0, 0, 0.03)",
    marginBottom: "20px",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "15px",
    marginBottom: "20px",
  },

  cardTitle: {
    margin: 0,
    fontSize: "17px",
    fontWeight: 650,
  },

  cardSubtitle: {
    margin: "5px 0 0",
    color: "#9ca3af",
    fontSize: "12px",
  },

  legend: {
    display: "flex",
    gap: "18px",
    color: "#6b7280",
    fontSize: "12px",
  },

  legendDot: {
    display: "inline-block",
    width: "8px",
    height: "8px",
    marginRight: "6px",
    borderRadius: "50%",
  },

  chart: {
    display: "flex",
    height: "310px",
  },

  yAxis: {
    width: "45px",
    paddingBottom: "30px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    color: "#9ca3af",
    fontSize: "10px",
  },

  chartContent: {
    position: "relative",
    flex: 1,
    height: "270px",
  },

  gridLines: {
    position: "absolute",
    inset: 0,
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
  },

  bars: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    height: "250px",
    display: "flex",
    justifyContent: "space-around",
    gap: "15px",
  },

  barGroup: {
    flex: 1,
    height: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "flex-end",
  },

  barContainer: {
    width: "100%",
    height: "230px",
    display: "flex",
    alignItems: "flex-end",
    justifyContent: "center",
    gap: "4px",
  },

  actualBar: {
    width: "25%",
    minWidth: "12px",
    maxWidth: "28px",
    background: "#2563eb",
    borderRadius: "5px 5px 0 0",
    transition: "height 0.3s ease",
  },

  forecastBar: {
    width: "25%",
    minWidth: "12px",
    maxWidth: "28px",
    background: "#93c5fd",
    borderRadius: "5px 5px 0 0",
    transition: "height 0.3s ease",
  },

  dayLabel: {
    marginTop: "8px",
    color: "#9ca3af",
    fontSize: "11px",
  },

  twoColumn: {
    display: "grid",
    gridTemplateColumns: "1.5fr 1fr",
    gap: "20px",
  },

  tableWrapper: {
    overflowX: "auto",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "12px",
  },

  th: {
    padding: "10px",
    textAlign: "left",
    color: "#9ca3af",
    fontWeight: 600,
    borderBottom: "1px solid #eef0f4",
  },

  td: {
    padding: "13px 10px",
    borderBottom: "1px solid #f0f1f4",
    color: "#4b5563",
  },

  productName: {
    display: "block",
    marginTop: "3px",
    color: "#9ca3af",
    fontSize: "10px",
  },

  statusBadge: {
    display: "inline-block",
    padding: "4px 9px",
    borderRadius: "20px",
    fontSize: "10px",
    fontWeight: 600,
  },

  highStatus: {
    background: "#fee2e2",
    color: "#b91c1c",
  },

  lowStatus: {
    background: "#fef3c7",
    color: "#92400e",
  },

  normalStatus: {
    background: "#dcfce7",
    color: "#166534",
  },

  warehouseList: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },

  warehouseItem: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },

  warehouseHeader: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "13px",
  },

  progressBackground: {
    height: "9px",
    background: "#edf0f5",
    borderRadius: "10px",
    overflow: "hidden",
  },

  progressBar: {
    height: "100%",
    background: "#2563eb",
    borderRadius: "10px",
  },

  capacityRow: {
    display: "flex",
    justifyContent: "space-between",
    color: "#9ca3af",
    fontSize: "10px",
  },

  modelCard: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "25px",
    flexWrap: "wrap",
    padding: "20px",
    borderRadius: "12px",
    background: "#172033",
    color: "#ffffff",
  },

  modelTitle: {
    margin: "0 0 7px",
    fontSize: "16px",
  },

  modelText: {
    maxWidth: "650px",
    margin: 0,
    color: "#cbd5e1",
    fontSize: "12px",
    lineHeight: 1.6,
  },

  modelStats: {
    display: "flex",
    gap: "30px",
  },

  modelStatsItem: {
    display: "flex",
    flexDirection: "column",
  },

  footer: {
    marginTop: "20px",
  },
};

export default Forecast;