import { useEffect, useMemo, useState } from "react";
import { getLogistics } from "./logisticsApi";
import type { LogisticsRecord } from "./types";
import LogisticsTable from "./LogisticsTable";

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

  const totalRecords = records.length;

  const onTimeDeliveries = records.filter(
    (record) => record.delayDays === 0,
  ).length;

  const delayedDeliveries = records.filter(
    (record) => record.delayDays > 0,
  ).length;

  const averageDelay =
    records.length > 0
      ? records.reduce(
          (total, record) => total + record.delayDays,
          0,
        ) / records.length
      : 0;

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Logistics</h1>
          <p>Monitor deliveries, delays, and transportation performance.</p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search logistics..."
          className="inventory-search"
        />
      </div>

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Deliveries</span>
          <strong>{totalRecords}</strong>
        </div>

        <div className="inventory-card">
          <span>On Time</span>
          <strong>{onTimeDeliveries}</strong>
        </div>

        <div className="inventory-card">
          <span>Delayed</span>
          <strong>{delayedDeliveries}</strong>
        </div>

        <div className="inventory-card">
          <span>Average Delay</span>
          <strong>{averageDelay.toFixed(1)} days</strong>
        </div>
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
        <LogisticsTable records={filteredRecords} />
      )}
    </section>
  );
};

export default LogisticsPage;