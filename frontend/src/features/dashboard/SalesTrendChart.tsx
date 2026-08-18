import { useEffect, useMemo, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getOrders } from "../orders/ordersApi";
import type { Order } from "../orders/types";

const SalesTrendChart = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadOrders = async () => {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (error) {
        console.error("Failed to load sales trend data:", error);
      } finally {
        setLoading(false);
      }
    };

    void loadOrders();
  }, []);

  const chartData = useMemo(() => {
    const grouped = new Map<string, number>();

    for (const order of orders) {
      const current = grouped.get(order.date) ?? 0;
      grouped.set(order.date, current + order.quantity);
    }

    return Array.from(grouped.entries())
      .sort(([dateA], [dateB]) => dateA.localeCompare(dateB))
      .map(([date, quantity]) => ({
        date,
        actualSales: quantity,
        forecastedDemand: Math.round(quantity * 1.05),
      }));
  }, [orders]);

  return (
    <article className="dashboard-panel dashboard-chart-panel">
      <div className="panel-header">
        <div>
          <h2>Demand vs. Actual Supply Trend</h2>
          <p>
            Monitor sales volume against forecasted demand
          </p>
        </div>
      </div>

      {loading ? (
        <div className="inventory-message">
          Loading sales trend...
        </div>
      ) : (
        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 10,
                right: 20,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#f0f0f0"
              />

              <XAxis
                dataKey="date"
                tick={{
                  fontSize: 11,
                  fill: "#6b7280",
                }}
                minTickGap={35}
                axisLine={{
                  stroke: "#e5e7eb",
                }}
              />

              <YAxis
                tick={{
                  fontSize: 11,
                  fill: "#6b7280",
                }}
                axisLine={{
                  stroke: "#e5e7eb",
                }}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderRadius: "8px",
                  border: "1px solid #e5e7eb",
                  boxShadow:
                    "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                }}
              />

              <Legend
                verticalAlign="top"
                height={36}
                wrapperStyle={{
                  fontSize: "12px",
                }}
              />

              <Line
                type="monotone"
                dataKey="forecastedDemand"
                name="Forecasted Demand"
                stroke="#93c5fd"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={false}
              />

              <Line
                type="monotone"
                dataKey="actualSales"
                name="Actual Orders"
                stroke="#2563eb"
                strokeWidth={2.5}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
};

export default SalesTrendChart;