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

import { getOrders } from "../orders/ordersApi";
import type { Order } from "../orders/types";

interface ProductSummary {
  productId: string;
  quantity: number;
  revenue: number;
}

const TopProductsChart = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadOrders = async () => {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (error) {
        console.error("Failed to load top products:", error);
      } finally {
        setLoading(false);
      }
    };

    void loadOrders();
  }, []);

  const topProducts = useMemo<ProductSummary[]>(() => {
    const productMap = new Map<
      string,
      { quantity: number; revenue: number }
    >();

    for (const order of orders) {
      const current = productMap.get(order.productId) ?? {
        quantity: 0,
        revenue: 0,
      };

      productMap.set(order.productId, {
        quantity: current.quantity + order.quantity,
        revenue: current.revenue + order.total,
      });
    }

    return Array.from(productMap.entries())
      .map(([productId, values]) => ({
        productId,
        quantity: values.quantity,
        revenue: values.revenue,
      }))
      .sort((a, b) => b.quantity - a.quantity)
      .slice(0, 5);
  }, [orders]);

  return (
    <article className="dashboard-panel dashboard-chart-panel">
      <div className="panel-header">
        <div>
          <h2>Top Performing Products</h2>
          <p>Products with the highest sales volume</p>
        </div>
      </div>

      {loading ? (
        <div className="inventory-message">
          Loading product performance...
        </div>
      ) : topProducts.length === 0 ? (
        <div className="inventory-message">
          No product sales data available.
        </div>
      ) : (
        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={topProducts}
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
                dataKey="productId"
                tick={{
                  fontSize: 11,
                  fill: "#6b7280",
                }}
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
                formatter={(value, name) => {
                  if (name === "quantity") {
                    return [
                      Number(value).toLocaleString(),
                      "Units Sold",
                    ];
                  }

                  return [
                    `₹${Number(value).toLocaleString("en-IN")}`,
                    "Revenue",
                  ];
                }}
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderRadius: "8px",
                  border: "1px solid #e5e7eb",
                  boxShadow:
                    "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                }}
              />

              <Bar
                dataKey="quantity"
                name="Units Sold"
                fill="#2563eb"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
};

export default TopProductsChart;