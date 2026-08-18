import { useEffect, useMemo, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getSuppliers } from "./suppliersApi";
import type { Supplier } from "./types";
import SuppliersTable from "./SuppliersTable";

interface SupplierPerformance {
  supplierId: string;
  supplierName: string;
  shipments: number;
  averageDelay: number;
  averageRating: number;
  totalCost: number;
  performanceScore: number;
  deliverySpeed: number;
  ratingScore: number;
  costEfficiency: number;
  lowDelay: number;
  reliability: number;
}

const isValidSupplier = (supplier: Supplier) => {
  const supplierId = supplier.supplierId?.trim();
  const supplierName = supplier.supplierName?.trim();

  return (
    Boolean(supplierId) &&
    Boolean(supplierName) &&
    supplierId.toLowerCase() !== "unknown" &&
    supplierName.toLowerCase() !== "unknown"
  );
};

const SuppliersPage = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const loadSuppliers = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getSuppliers();

        // Remove invalid / unknown supplier records.
        setSuppliers(data.filter(isValidSupplier));
      } catch (err) {
        console.error("Failed to load suppliers:", err);
        setError("Failed to load supplier data.");
      } finally {
        setLoading(false);
      }
    };

    void loadSuppliers();
  }, []);

  const filteredSuppliers = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return suppliers;
    }

    return suppliers.filter(
      (supplier) =>
        supplier.supplierId.toLowerCase().includes(query) ||
        supplier.supplierName.toLowerCase().includes(query) ||
        supplier.productId.toLowerCase().includes(query),
    );
  }, [suppliers, search]);

  const supplierPerformance = useMemo<SupplierPerformance[]>(() => {
    const grouped = new Map<string, Supplier[]>();

    suppliers.forEach((supplier) => {
      const existing = grouped.get(supplier.supplierId) ?? [];
      existing.push(supplier);
      grouped.set(supplier.supplierId, existing);
    });

    const summary = Array.from(grouped.entries()).map(
      ([supplierId, records]) => {
        const shipments = records.length;

        const averageDelay =
          records.reduce(
            (sum, record) => sum + Number(record.delayDays || 0),
            0,
          ) / shipments;

        const averageRating =
          records.reduce(
            (sum, record) =>
              sum + Number(record.supplierRating || 0),
            0,
          ) / shipments;

        const totalCost = records.reduce(
          (sum, record) =>
            sum + Number(record.transportationCost || 0),
          0,
        );

        return {
          supplierId,
          supplierName: records[0].supplierName,
          shipments,
          averageDelay,
          averageRating,
          totalCost,
        };
      },
    );

    if (summary.length === 0) {
      return [];
    }

    const costValues = summary.map(
      (supplier) => supplier.totalCost / supplier.shipments,
    );

    const minCost = Math.min(...costValues);
    const maxCost = Math.max(...costValues);

    return summary
      .map((supplier) => {
        const deliverySpeed = Math.max(
          0,
          Math.min(100, 100 - supplier.averageDelay * 10),
        );

        const ratingScore = Math.max(
          0,
          Math.min(100, (supplier.averageRating / 5) * 100),
        );

        const lowDelay = Math.max(
          0,
          Math.min(100, 100 - supplier.averageDelay * 12),
        );

        const reliability = Math.max(
          0,
          Math.min(100, 100 - supplier.averageDelay * 8),
        );

        const currentCost =
          supplier.totalCost / supplier.shipments;

        let costEfficiency = 100;

        if (maxCost !== minCost) {
          costEfficiency =
            ((maxCost - currentCost) /
              (maxCost - minCost)) *
            100;
        }

        const performanceScore =
          ratingScore * 0.3 +
          deliverySpeed * 0.2 +
          costEfficiency * 0.2 +
          lowDelay * 0.15 +
          reliability * 0.15;

        return {
          ...supplier,
          deliverySpeed,
          ratingScore,
          costEfficiency,
          lowDelay,
          reliability,
          performanceScore,
        };
      })
      .sort(
        (a, b) => b.performanceScore - a.performanceScore,
      );
  }, [suppliers]);

  const totalShipments = suppliers.length;
  const uniqueSuppliers = supplierPerformance.length;

  const averageRating =
    suppliers.length > 0
      ? suppliers.reduce(
          (total, supplier) =>
            total + Number(supplier.supplierRating || 0),
          0,
        ) / suppliers.length
      : 0;

  const averageDelay =
    suppliers.length > 0
      ? suppliers.reduce(
          (total, supplier) =>
            total + Number(supplier.delayDays || 0),
          0,
        ) / suppliers.length
      : 0;

  const topSupplier = supplierPerformance[0];

  const lowestDelaySupplier = useMemo(() => {
    return [...supplierPerformance].sort(
      (a, b) => a.averageDelay - b.averageDelay,
    )[0];
  }, [supplierPerformance]);

  const bestRatedSupplier = useMemo(() => {
    return [...supplierPerformance].sort(
      (a, b) => b.averageRating - a.averageRating,
    )[0];
  }, [supplierPerformance]);

  /*
   * IMPORTANT:
   * Radar axes are performance dimensions,
   * NOT supplier IDs.
   */
  const radarData = useMemo(() => {
    return [
      {
        metric: "Delivery Speed",
        ...Object.fromEntries(
          supplierPerformance.map((supplier) => [
            supplier.supplierId,
            Number(supplier.deliverySpeed.toFixed(1)),
          ]),
        ),
      },
      {
        metric: "Rating Score",
        ...Object.fromEntries(
          supplierPerformance.map((supplier) => [
            supplier.supplierId,
            Number(supplier.ratingScore.toFixed(1)),
          ]),
        ),
      },
      {
        metric: "Cost Efficiency",
        ...Object.fromEntries(
          supplierPerformance.map((supplier) => [
            supplier.supplierId,
            Number(supplier.costEfficiency.toFixed(1)),
          ]),
        ),
      },
      {
        metric: "Low Delay",
        ...Object.fromEntries(
          supplierPerformance.map((supplier) => [
            supplier.supplierId,
            Number(supplier.lowDelay.toFixed(1)),
          ]),
        ),
      },
      {
        metric: "Reliability",
        ...Object.fromEntries(
          supplierPerformance.map((supplier) => [
            supplier.supplierId,
            Number(supplier.reliability.toFixed(1)),
          ]),
        ),
      },
    ];
  }, [supplierPerformance]);

  /*
   * Clean comparison chart:
   * Left axis  = Performance Score
   * Right axis = Average Delay
   */
  const lineData = useMemo(() => {
    return supplierPerformance.map((supplier) => ({
      supplierId: supplier.supplierId,
      performanceScore: Number(
        supplier.performanceScore.toFixed(1),
      ),
      avgDelay: Number(supplier.averageDelay.toFixed(1)),
    }));
  }, [supplierPerformance]);

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Supplier Performance Scorecard</h1>
          <p>
            Monitor supplier reliability, delivery speed,
            ratings, and transportation performance.
          </p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search suppliers..."
          className="inventory-search"
        />
      </div>

      {loading && (
        <div className="inventory-message">
          Loading suppliers...
        </div>
      )}

      {error && (
        <div className="inventory-message inventory-message--error">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="inventory-kpis">
            <div className="inventory-card">
              <span>Total Shipments</span>
              <strong>{totalShipments}</strong>
            </div>

            <div className="inventory-card">
              <span>Average Delay</span>
              <strong>{averageDelay.toFixed(1)} days</strong>
            </div>

            <div className="inventory-card">
              <span>Average Supplier Rating</span>
              <strong>{averageRating.toFixed(2)} / 5</strong>
            </div>

            <div className="inventory-card">
              <span>Top Performing Supplier</span>
              <strong>
                {topSupplier?.supplierId ?? "N/A"}
              </strong>
            </div>
          </div>

          <div className="inventory-kpis">
            <div className="inventory-card">
              <span>Unique Suppliers</span>
              <strong>{uniqueSuppliers}</strong>
            </div>

            <div className="inventory-card">
              <span>Best Performance Score</span>
              <strong>
                {topSupplier
                  ? `${topSupplier.performanceScore.toFixed(1)} / 100`
                  : "N/A"}
              </strong>
            </div>

            <div className="inventory-card">
              <span>Best Rated Supplier</span>
              <strong>
                {bestRatedSupplier?.supplierId ?? "N/A"}
              </strong>
            </div>

            <div className="inventory-card">
              <span>Lowest Delay Supplier</span>
              <strong>
                {lowestDelaySupplier?.supplierId ?? "N/A"}
              </strong>
            </div>
          </div>

          <div className="inventory-table-wrapper">
            <table className="inventory-table">
              <thead>
                <tr>
                  <th>Supplier</th>
                  <th>Shipments</th>
                  <th>Avg Delay</th>
                  <th>Avg Rating</th>
                  <th>Total Cost</th>
                  <th>Performance Score</th>
                </tr>
              </thead>

              <tbody>
                {supplierPerformance
                  .filter((supplier) => {
                    const query = search.trim().toLowerCase();

                    if (!query) {
                      return true;
                    }

                    return (
                      supplier.supplierId
                        .toLowerCase()
                        .includes(query) ||
                      supplier.supplierName
                        .toLowerCase()
                        .includes(query)
                    );
                  })
                  .map((supplier) => (
                    <tr key={supplier.supplierId}>
                      <td>
                        <strong>{supplier.supplierId}</strong>
                        <br />
                        <small>{supplier.supplierName}</small>
                      </td>

                      <td>{supplier.shipments}</td>

                      <td>
                        {supplier.averageDelay.toFixed(1)} days
                      </td>

                      <td>
                        {supplier.averageRating.toFixed(2)} / 5
                      </td>

                      <td>
                        ₹{supplier.totalCost.toFixed(2)}
                      </td>

                      <td>
                        <strong>
                          {supplier.performanceScore.toFixed(1)}
                          /100
                        </strong>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(420px, 1fr))",
              gap: "20px",
              marginTop: "24px",
            }}
          >
            {/* RADAR */}
            <div className="inventory-table-wrapper">
              <div style={{ padding: "20px 20px 0" }}>
                <h2>Supplier Performance Radar</h2>
                <p>
                  Comparison across delivery speed, rating,
                  cost efficiency, low delay, and reliability.
                </p>
              </div>

              <div
                style={{
                  width: "100%",
                  height: 420,
                }}
              >
                <ResponsiveContainer>
                  <RadarChart data={radarData}>
                    <PolarGrid />

                    <PolarAngleAxis dataKey="metric" />

                    <PolarRadiusAxis
                      domain={[0, 100]}
                      tickCount={6}
                    />

                    {supplierPerformance.map(
                      (supplier) => (
                        <Radar
                          key={supplier.supplierId}
                          name={supplier.supplierId}
                          dataKey={supplier.supplierId}
                          fill="currentColor"
                          fillOpacity={0.08}
                          stroke="currentColor"
                        />
                      ),
                    )}

                    <Tooltip />
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* LINE */}
            <div className="inventory-table-wrapper">
              <div style={{ padding: "20px 20px 0" }}>
                <h2>Performance Comparison</h2>
                <p>
                  Supplier performance score versus average
                  delivery delay.
                </p>
              </div>

              <div
                style={{
                  width: "100%",
                  height: 420,
                }}
              >
                <ResponsiveContainer>
                  <LineChart
                    data={lineData}
                    margin={{
                      top: 20,
                      right: 30,
                      left: 10,
                      bottom: 10,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="supplierId" />

                    <YAxis
                      yAxisId="left"
                      domain={[0, 100]}
                    />

                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      domain={[0, "auto"]}
                    />

                    <Tooltip />
                    <Legend />

                    <Line
                      yAxisId="left"
                      type="monotone"
                      dataKey="performanceScore"
                      name="Performance Score"
                      stroke="currentColor"
                      strokeWidth={3}
                      dot
                    />

                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="avgDelay"
                      name="Avg Delay (Days)"
                      stroke="currentColor"
                      strokeWidth={2}
                      dot
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div style={{ marginTop: "30px" }}>
            <h2>Shipment-Level Supplier Details</h2>
            <p>
              Detailed delivery and transportation records.
            </p>

            <SuppliersTable suppliers={filteredSuppliers} />
          </div>
        </>
      )}
    </section>
  );
};

export default SuppliersPage;