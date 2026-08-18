import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getLogistics } from "./logisticsApi";
import type { LogisticsRecord } from "./types";
import LogisticsTable from "./LogisticsTable";
import ActiveShipmentsMap from "./ActiveShipmentsMap";

const LogisticsPage = () => {
  const [records, setRecords] = useState<LogisticsRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const loadLogistics = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getLogistics();
        setRecords(data);
      } catch (err) {
        console.error("Failed to load logistics:", err);
        setError("Failed to load logistics data.");
      } finally {
        setLoading(false);
      }
    };

    void loadLogistics();
  }, []);

  /* =========================
     SEARCH
     ========================= */

  const filteredRecords = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return records;
    }

    return records.filter(
      (record) =>
        record.supplierId.toLowerCase().includes(query) ||
        record.supplierName.toLowerCase().includes(query) ||
        record.productId.toLowerCase().includes(query),
    );
  }, [records, search]);

  /* =========================
     KPI CALCULATIONS
     ========================= */

  const totalRecords = records.length;

  const onTimeDeliveries = records.filter(
    (record) => record.delayDays === 0,
  ).length;

  const delayedDeliveries = records.filter(
    (record) => record.delayDays > 0,
  ).length;

  const onTimeRate =
    totalRecords > 0
      ? (onTimeDeliveries / totalRecords) * 100
      : 0;

  const averageDelay =
    totalRecords > 0
      ? records.reduce(
          (total, record) => total + record.delayDays,
          0,
        ) / totalRecords
      : 0;

  /* =========================
     SHIPMENT STATUS
     ========================= */

  /*
   * Backend currently provides delayDays,
   * but does not provide separate delivered/
   * exception fields.
   *
   * Therefore these are UI-level representations
   * based on the available dataset.
   */

  const deliveredShipments = onTimeDeliveries;
  const exceptionShipments = 0;

  const shipmentStatus = [
    {
      label: "On Time",
      value: onTimeDeliveries,
      className:
        "logistics-status logistics-status--ontime",
    },
    {
      label: "Delayed",
      value: delayedDeliveries,
      className:
        "logistics-status logistics-status--delayed",
    },
    {
      label: "Delivered",
      value: deliveredShipments,
      className:
        "logistics-status logistics-status--delivered",
    },
    {
      label: "Exception",
      value: exceptionShipments,
      className:
        "logistics-status logistics-status--exception",
    },
  ];

  /* =========================
     FREIGHT CHART
     ========================= */

  /*
   * These are presentation/reference values only.
   * No backend/API data is changed.
   */

  const freightData = [
    {
      mode: "Road",
      cost: 2.6,
    },
    {
      mode: "Air",
      cost: 1.8,
    },
    {
      mode: "Sea",
      cost: 1.2,
    },
    {
      mode: "Rail",
      cost: 0.6,
    },
  ];

  /* =========================
     COST PER MILE
     ========================= */

  /*
   * Carrier information is not currently available
   * in LogisticsRecord, so these are UI reference
   * values only.
   */

  const carrierData = [
    {
      name: "DHL Logistics",
      cost: "$2.45",
      width: "85%",
    },
    {
      name: "Blue Dart",
      cost: "$1.98",
      width: "70%",
    },
    {
      name: "XPO Logistics",
      cost: "$1.55",
      width: "55%",
    },
    {
      name: "Delhivery",
      cost: "$1.20",
      width: "40%",
    },
  ];

  return (
    <section className="logistics-page">
      {/* =========================
          PAGE HEADER
          ========================= */}

      <div className="logistics-header">
        <div>
          <h1>Logistics &amp; Shipments Tracking</h1>

          <p>
            Track active shipments, delivery performance,
            and freight logistics costs.
          </p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search logistics..."
          className="logistics-search"
        />
      </div>

      {/* =========================
          KPI CARDS
          ========================= */}

      <div className="logistics-kpis">
        <div className="logistics-kpi-card">
          <span>On-Time Delivery Rate</span>

          <strong>{onTimeRate.toFixed(1)}%</strong>

          <small className="logistics-positive">
            Delivery performance
          </small>
        </div>

        <div className="logistics-kpi-card">
          <span>Active Shipments</span>

          <strong>{totalRecords}</strong>

          <small className="logistics-info">
            Records tracked
          </small>
        </div>

        <div className="logistics-kpi-card">
          <span>Avg Transit Delay</span>

          <strong>
            {averageDelay.toFixed(1)} Days
          </strong>

          <small>
            Based on delivery records
          </small>
        </div>

        <div className="logistics-kpi-card">
          <span>Delayed Shipments</span>

          <strong>{delayedDeliveries}</strong>

          <small className="logistics-warning">
            Requires attention
          </small>
        </div>
      </div>

      {/* =========================
          MAP + SHIPMENT STATUS
          ========================= */}

      <div className="logistics-middle-grid">
        {/* ACTIVE SHIPMENTS MAP */}

        <div className="logistics-panel logistics-map-panel">
          <div className="logistics-panel-header">
            <div>
              <h2>Active Shipments Map</h2>

              <p>
                Geographic distribution of active supply
                transit
              </p>
            </div>
          </div>

          <ActiveShipmentsMap />
        </div>

        {/* SHIPMENT STATUS */}

        <div className="logistics-panel">
          <div className="logistics-panel-header">
            <div>
              <h2>Shipment Status</h2>

              <p>
                Current shipment distribution
              </p>
            </div>
          </div>

          <div className="logistics-status-list">
            {shipmentStatus.map((status) => (
              <div
                key={status.label}
                className={status.className}
              >
                <span className="logistics-status-label">
                  <span className="logistics-status-dot" />

                  {status.label}
                </span>

                <strong>{status.value}</strong>
              </div>
            ))}
          </div>

          <div className="logistics-status-total">
            <span>Total Records</span>

            <strong>{totalRecords}</strong>
          </div>
        </div>
      </div>

      {/* =========================
          FREIGHT + COST PER MILE
          ========================= */}

      <div className="logistics-bottom-grid">
        {/* FREIGHT COST */}

        <div className="logistics-panel">
          <div className="logistics-panel-header">
            <div>
              <h2>Freight Cost Breakdown</h2>

              <p>
                Transportation expenditure by mode
              </p>
            </div>
          </div>

          <div
            className="logistics-chart"
            style={{ height: 220 }}
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <BarChart
                data={freightData}
                margin={{
                  top: 10,
                  right: 10,
                  left: -20,
                  bottom: 0,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="mode"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  tick={{ fontSize: 11 }}
                />

                <Tooltip
                  formatter={(value) => [
                    `$${Number(value).toFixed(1)}K`,
                    "Cost",
                  ]}
                />

                <Bar
                  dataKey="cost"
                  fill="#2563eb"
                  radius={[4, 4, 0, 0]}
                  barSize={36}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* COST PER MILE */}

        <div className="logistics-panel">
          <div className="logistics-panel-header">
            <div>
              <h2>
                Cost Per Mile (By Carrier)
              </h2>

              <p>
                Carrier efficiency comparison
              </p>
            </div>
          </div>

          <div className="logistics-performance">
            {carrierData.map((carrier) => (
              <div
                key={carrier.name}
                className="logistics-performance-row"
              >
                <span
                  style={{
                    width: "105px",
                    flexShrink: 0,
                  }}
                >
                  {carrier.name}
                </span>

                <div
                  style={{
                    flex: 1,
                    height: "8px",
                    background: "#f1f5f9",
                    borderRadius: "999px",
                    margin: "0 12px",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      height: "100%",
                      width: carrier.width,
                      background: "#2563eb",
                      borderRadius: "999px",
                    }}
                  />
                </div>

                <strong
                  style={{
                    minWidth: "45px",
                    textAlign: "right",
                  }}
                >
                  {carrier.cost}
                </strong>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* =========================
          LOGISTICS RECORDS
          ========================= */}

      <div className="logistics-records-section">
        <div className="logistics-records-header">
          <div>
            <h2>Logistics Records</h2>

            <p>
              Detailed delivery and transportation records
            </p>
          </div>

          <span>
            {filteredRecords.length} records
          </span>
        </div>

        {loading && (
          <div className="inventory-message">
            Loading logistics...
          </div>
        )}

        {error && (
          <div className="inventory-message inventory-message--error">
            {error}
          </div>
        )}

        {!loading && !error && (
          <LogisticsTable
            records={filteredRecords}
          />
        )}
      </div>
    </section>
  );
};

export default LogisticsPage;