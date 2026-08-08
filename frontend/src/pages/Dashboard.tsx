import React from "react";

const Dashboard: React.FC = () => {
  const metrics = [
    {
      title: "Total Revenue",
      value: "₹12.5M",
      change: "+12.5%",
      status: "positive",
    },
    {
      title: "Units Sold",
      value: "24,680",
      change: "+8.2%",
      status: "positive",
    },
    {
      title: "Current Inventory",
      value: "8,420",
      change: "-3.4%",
      status: "negative",
    },
    {
      title: "Anomalies",
      value: "24",
      change: "-18.6%",
      status: "positive",
    },
  ];

  const warehouses = [
    { name: "Mumbai", stock: 2180, capacity: 82 },
    { name: "Bengaluru", stock: 1840, capacity: 76 },
    { name: "Delhi", stock: 1560, capacity: 68 },
    { name: "Kolkata", stock: 1240, capacity: 54 },
  ];

  const anomalies = [
    {
      product: "P002 - Phone",
      warehouse: "Mumbai",
      issue: "High Demand",
      severity: "High",
    },
    {
      product: "P004 - Rice",
      warehouse: "Delhi",
      issue: "Low Stock",
      severity: "Medium",
    },
    {
      product: "P007 - Laptop",
      warehouse: "Kolkata",
      issue: "Demand Spike",
      severity: "High",
    },
    {
      product: "P003 - Chair",
      warehouse: "Bengaluru",
      issue: "Stock Variation",
      severity: "Low",
    },
  ];

  const monthlySales = [
    42, 55, 48, 68, 60, 74, 69, 82, 76, 88, 81, 94,
  ];

  const forecast = [55, 68, 62, 78, 72, 88, 82];

  return (
    <div style={styles.page}>
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Supply Chain Dashboard</h1>

          <p style={styles.subtitle}>
            Monitor sales, inventory, demand forecasting and anomalies
          </p>
        </div>

        <div style={styles.headerActions}>
          <button style={styles.dateButton}>
            📅 Last 30 Days ▾
          </button>

          <button style={styles.refreshButton}>
            ↻ Refresh
          </button>
        </div>
      </div>

      {/* =====================================================
          KPI CARDS
      ====================================================== */}
      <div style={styles.metricsGrid}>
        {metrics.map((metric) => (
          <div style={styles.metricCard} key={metric.title}>
            <div style={styles.metricHeader}>
              <span style={styles.metricTitle}>
                {metric.title}
              </span>

              <div style={styles.metricIcon}>
                {metric.title === "Total Revenue" && "₹"}
                {metric.title === "Units Sold" && "↗"}
                {metric.title === "Current Inventory" && "▣"}
                {metric.title === "Anomalies" && "⚠"}
              </div>
            </div>

            <h2 style={styles.metricValue}>
              {metric.value}
            </h2>

            <div style={styles.metricChange}>
              <span
                style={{
                  ...styles.changeValue,
                  color:
                    metric.status === "positive"
                      ? "#16a34a"
                      : "#dc2626",
                }}
              >
                {metric.change}
              </span>

              <span style={styles.changeText}>
                vs last month
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* =====================================================
          MAIN SECTION
      ====================================================== */}
      <div style={styles.mainGrid}>
        {/* SALES CHART */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Sales & Demand Trend
              </h2>

              <p style={styles.cardSubtitle}>
                Actual sales compared with forecast
              </p>
            </div>

            <select style={styles.select}>
              <option>2024</option>
              <option>2025</option>
              <option>2026</option>
            </select>
          </div>

          <div style={styles.chartArea}>
            <div style={styles.chartYAxis}>
              <span>100K</span>
              <span>75K</span>
              <span>50K</span>
              <span>25K</span>
              <span>0</span>
            </div>

            <div style={styles.chartWrapper}>
              <div
                style={{
                  ...styles.horizontalLine,
                  top: "0%",
                }}
              />

              <div
                style={{
                  ...styles.horizontalLine,
                  top: "25%",
                }}
              />

              <div
                style={{
                  ...styles.horizontalLine,
                  top: "50%",
                }}
              />

              <div
                style={{
                  ...styles.horizontalLine,
                  top: "75%",
                }}
              />

              <div
                style={{
                  ...styles.horizontalLine,
                  top: "100%",
                }}
              />

              <svg
                viewBox="0 0 600 220"
                preserveAspectRatio="none"
                style={styles.chartSvg}
              >
                <polyline
                  points="
                    0,150
                    55,120
                    110,135
                    165,90
                    220,105
                    275,68
                    330,82
                    385,45
                    440,62
                    495,30
                    550,48
                    600,18
                  "
                  fill="none"
                  stroke="#2563eb"
                  strokeWidth="4"
                />

                <polyline
                  points="
                    0,172
                    55,153
                    110,162
                    165,134
                    220,142
                    275,118
                    330,128
                    385,95
                    440,112
                    495,84
                    550,97
                    600,70
                  "
                  fill="none"
                  stroke="#93c5fd"
                  strokeWidth="3"
                  strokeDasharray="7 5"
                />
              </svg>

              <div style={styles.monthLabels}>
                {[
                  "Jan",
                  "Feb",
                  "Mar",
                  "Apr",
                  "May",
                  "Jun",
                  "Jul",
                  "Aug",
                  "Sep",
                  "Oct",
                  "Nov",
                  "Dec",
                ].map((month) => (
                  <span key={month}>{month}</span>
                ))}
              </div>
            </div>
          </div>

          <div style={styles.legend}>
            <span>
              <span
                style={{
                  ...styles.legendDot,
                  background: "#2563eb",
                }}
              />
              Actual Sales
            </span>

            <span>
              <span
                style={{
                  ...styles.legendDot,
                  background: "#93c5fd",
                }}
              />
              Forecast
            </span>
          </div>
        </div>

        {/* INVENTORY */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Inventory by Warehouse
              </h2>

              <p style={styles.cardSubtitle}>
                Current stock availability
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
                  <span>{warehouse.name}</span>

                  <strong>
                    {warehouse.stock.toLocaleString()} units
                  </strong>
                </div>

                <div style={styles.progressBackground}>
                  <div
                    style={{
                      ...styles.progressBar,
                      width: `${warehouse.capacity}%`,
                    }}
                  />
                </div>

                <span style={styles.capacityText}>
                  {warehouse.capacity}% capacity
                </span>
              </div>
            ))}
          </div>

          <div style={styles.inventoryFooter}>
            <span>Total inventory</span>
            <strong>8,420 units</strong>
          </div>
        </div>
      </div>

      {/* =====================================================
          BOTTOM SECTION
      ====================================================== */}
      <div style={styles.bottomGrid}>
        {/* ANOMALIES */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Recent Anomalies
              </h2>

              <p style={styles.cardSubtitle}>
                Detected supply chain issues
              </p>
            </div>

            <button style={styles.viewButton}>
              View All →
            </button>
          </div>

          <div>
            {anomalies.map((anomaly) => (
              <div
                key={`${anomaly.product}-${anomaly.warehouse}`}
                style={styles.anomalyRow}
              >
                <div style={styles.warningIcon}>
                  ⚠
                </div>

                <div style={styles.anomalyInfo}>
                  <strong>{anomaly.product}</strong>

                  <span>
                    {anomaly.warehouse} • {anomaly.issue}
                  </span>
                </div>

                <span
                  style={{
                    ...styles.badge,
                    ...(anomaly.severity === "High"
                      ? styles.highBadge
                      : anomaly.severity === "Medium"
                        ? styles.mediumBadge
                        : styles.lowBadge),
                  }}
                >
                  {anomaly.severity}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* FORECAST */}
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <div>
              <h2 style={styles.cardTitle}>
                Demand Forecast
              </h2>

              <p style={styles.cardSubtitle}>
                Next 7 days prediction
              </p>
            </div>

            <span style={styles.accuracyBadge}>
              92.4% accuracy
            </span>
          </div>

          <div style={styles.forecastNumber}>
            18,450
            <span> units</span>
          </div>

          <p style={styles.forecastText}>
            Expected demand for the upcoming week
          </p>

          <div style={styles.forecastChart}>
            {forecast.map((value, index) => (
              <div
                key={index}
                style={styles.forecastColumn}
              >
                <div
                  style={{
                    ...styles.forecastBar,
                    height: `${value}%`,
                  }}
                />

                <span>
                  {
                    [
                      "Mon",
                      "Tue",
                      "Wed",
                      "Thu",
                      "Fri",
                      "Sat",
                      "Sun",
                    ][index]
                  }
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* =====================================================
          FOOTER
      ====================================================== */}
      <div style={styles.footer}>
        <span>
          Supply Chain Analytics
        </span>

        <span>
          Last updated: Today
        </span>
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
    background: "#f5f7fb",
    padding: "28px",
    boxSizing: "border-box",
    fontFamily:
      "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    color: "#172033",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    flexWrap: "wrap",
    marginBottom: "28px",
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

  headerActions: {
    display: "flex",
    gap: "10px",
  },

  dateButton: {
    padding: "10px 14px",
    border: "1px solid #dce1ea",
    background: "#ffffff",
    borderRadius: "8px",
    color: "#374151",
    cursor: "pointer",
  },

  refreshButton: {
    padding: "10px 16px",
    border: "none",
    background: "#2563eb",
    color: "#ffffff",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: 600,
  },

  metricsGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, minmax(0, 1fr))",
    gap: "18px",
    marginBottom: "20px",
  },

  metricCard: {
    background: "#ffffff",
    border: "1px solid #e6e9ef",
    borderRadius: "12px",
    padding: "20px",
    boxShadow:
      "0 2px 8px rgba(0, 0, 0, 0.03)",
  },

  metricHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  metricTitle: {
    color: "#6b7280",
    fontSize: "14px",
  },

  metricIcon: {
    width: "34px",
    height: "34px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: "8px",
    background: "#eff6ff",
    color: "#2563eb",
    fontWeight: 700,
  },

  metricValue: {
    margin: "13px 0 0",
    fontSize: "27px",
    fontWeight: 700,
  },

  metricChange: {
    display: "flex",
    gap: "7px",
    alignItems: "center",
    marginTop: "8px",
  },

  changeValue: {
    fontSize: "13px",
    fontWeight: 600,
  },

  changeText: {
    color: "#9ca3af",
    fontSize: "12px",
  },

  mainGrid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px",
    marginBottom: "20px",
  },

  bottomGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
  },

  card: {
    background: "#ffffff",
    border: "1px solid #e6e9ef",
    borderRadius: "12px",
    padding: "20px",
    boxShadow:
      "0 2px 8px rgba(0, 0, 0, 0.03)",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "10px",
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

  select: {
    padding: "7px 10px",
    border: "1px solid #dce1ea",
    background: "#ffffff",
    borderRadius: "7px",
  },

  chartArea: {
    display: "flex",
    height: "260px",
  },

  chartYAxis: {
    width: "48px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    color: "#9ca3af",
    fontSize: "10px",
    paddingBottom: "30px",
  },

  chartWrapper: {
    position: "relative",
    flex: 1,
    height: "230px",
  },

  horizontalLine: {
    position: "absolute",
    left: 0,
    right: 0,
    borderTop: "1px dashed #e5e7eb",
  },

  chartSvg: {
    position: "absolute",
    left: 0,
    top: 0,
    width: "100%",
    height: "200px",
  },

  monthLabels: {
    position: "absolute",
    left: 0,
    right: 0,
    bottom: 0,
    display: "flex",
    justifyContent: "space-between",
    color: "#9ca3af",
    fontSize: "10px",
  },

  legend: {
    display: "flex",
    gap: "20px",
    color: "#6b7280",
    fontSize: "12px",
  },

  legendDot: {
    display: "inline-block",
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    marginRight: "6px",
  },

  warehouseList: {
    display: "flex",
    flexDirection: "column",
    gap: "21px",
  },

  warehouseItem: {
    display: "flex",
    flexDirection: "column",
    gap: "7px",
  },

  warehouseHeader: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "13px",
  },

  progressBackground: {
    height: "8px",
    background: "#edf0f5",
    borderRadius: "10px",
    overflow: "hidden",
  },

  progressBar: {
    height: "100%",
    background: "#2563eb",
    borderRadius: "10px",
  },

  capacityText: {
    color: "#9ca3af",
    fontSize: "11px",
  },

  inventoryFooter: {
    display: "flex",
    justifyContent: "space-between",
    borderTop: "1px solid #eef0f4",
    marginTop: "25px",
    paddingTop: "15px",
    fontSize: "13px",
  },

  viewButton: {
    border: "none",
    background: "transparent",
    color: "#2563eb",
    cursor: "pointer",
    fontWeight: 600,
  },

  anomalyRow: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "13px 0",
    borderBottom: "1px solid #f0f1f4",
  },

  warningIcon: {
    width: "34px",
    height: "34px",
    flexShrink: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: "8px",
    background: "#fff7ed",
    color: "#ea580c",
  },

  anomalyInfo: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "3px",
    fontSize: "13px",
  },

  badge: {
    padding: "4px 9px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: 600,
  },

  highBadge: {
    background: "#fee2e2",
    color: "#b91c1c",
  },

  mediumBadge: {
    background: "#fef3c7",
    color: "#92400e",
  },

  lowBadge: {
    background: "#dcfce7",
    color: "#166534",
  },

  accuracyBadge: {
    background: "#ecfdf5",
    color: "#047857",
    padding: "5px 9px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: 600,
  },

  forecastNumber: {
    fontSize: "34px",
    fontWeight: 700,
  },

  forecastText: {
    margin: "5px 0 0",
    color: "#9ca3af",
    fontSize: "12px",
  },

  forecastChart: {
    height: "150px",
    display: "flex",
    alignItems: "flex-end",
    justifyContent: "space-between",
    gap: "10px",
    marginTop: "20px",
  },

  forecastColumn: {
    height: "100%",
    flex: 1,
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    alignItems: "center",
    gap: "7px",
    color: "#9ca3af",
    fontSize: "10px",
  },

  forecastBar: {
    width: "100%",
    maxWidth: "30px",
    minHeight: "15px",
    background: "#3b82f6",
    borderRadius: "5px 5px 2px 2px",
  },

  footer: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "25px",
    padding: "15px 5px",
    color: "#9ca3af",
    fontSize: "12px",
  },
};

export default Dashboard;