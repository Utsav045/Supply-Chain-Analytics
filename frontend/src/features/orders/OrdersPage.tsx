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

import { getOrders } from "./ordersApi";
import type { Order } from "./types";
import OrdersTable from "./OrdersTable";

const formatCurrency = (value: number) => {
  return `₹${value.toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

const OrdersPage = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const loadOrders = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getOrders();
        setOrders(data);
      } catch (err) {
        console.error("Failed to load orders:", err);
        setError("Failed to load order data.");
      } finally {
        setLoading(false);
      }
    };

    void loadOrders();
  }, []);

  const filteredOrders = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return orders;
    }

    return orders.filter(
      (order) =>
        String(order.id).toLowerCase().includes(query) ||
        order.productId.toLowerCase().includes(query),
    );
  }, [orders, search]);

  /* =========================
     KPI CALCULATIONS
     ========================= */

  const totalOrders = orders.length;

  const totalQuantity = orders.reduce(
    (total, order) => total + order.quantity,
    0,
  );

  const totalRevenue = orders.reduce(
    (total, order) => total + order.total,
    0,
  );

  const averageOrderValue =
    totalOrders > 0 ? totalRevenue / totalOrders : 0;

  const averageQuantity =
    totalOrders > 0 ? totalQuantity / totalOrders : 0;

  const uniqueProducts = new Set(
    orders.map((order) => order.productId),
  ).size;

  /* =========================
     PRODUCT REVENUE CHART
     ========================= */

  const productRevenueData = useMemo(() => {
    const productMap = new Map<string, number>();

    orders.forEach((order) => {
      const currentRevenue =
        productMap.get(order.productId) ?? 0;

      productMap.set(
        order.productId,
        currentRevenue + order.total,
      );
    });

    return Array.from(productMap.entries())
      .map(([productId, revenue]) => ({
        productId,
        revenue: Number(revenue.toFixed(2)),
      }))
      .sort((a, b) => b.revenue - a.revenue)
      .slice(0, 6);
  }, [orders]);

  /* =========================
     RECENT ORDERS
     ========================= */

  const recentOrders = useMemo(() => {
    return [...orders]
      .sort(
        (a, b) =>
          new Date(b.date).getTime() -
          new Date(a.date).getTime(),
      )
      .slice(0, 5);
  }, [orders]);

  return (
    <section className="inventory-page">
      {/* =========================
          PAGE HEADER
          ========================= */}

      <div className="inventory-header">
        <div>
          <h1>Orders Management</h1>

          <p>
            Monitor sales orders, quantities, pricing, and
            transaction revenue.
          </p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search orders..."
          className="inventory-search"
        />
      </div>

      {/* =========================
          KPI CARDS
          ========================= */}

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Orders</span>

          <strong>{totalOrders}</strong>

          <small>
            Orders tracked
          </small>
        </div>

        <div className="inventory-card">
          <span>Total Quantity</span>

          <strong>
            {totalQuantity.toLocaleString("en-IN")}
          </strong>

          <small>
            Units ordered
          </small>
        </div>

        <div className="inventory-card">
          <span>Total Revenue</span>

          <strong>
            {formatCurrency(totalRevenue)}
          </strong>

          <small>
            Gross order value
          </small>
        </div>

        <div className="inventory-card">
          <span>Average Order Value</span>

          <strong>
            {formatCurrency(averageOrderValue)}
          </strong>

          <small>
            Revenue per order
          </small>
        </div>
      </div>

      {/* =========================
          LOADING / ERROR
          ========================= */}

      {loading && (
        <div className="inventory-message">
          Loading orders...
        </div>
      )}

      {error && (
        <div className="inventory-message inventory-message--error">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          {/* =========================
              ANALYTICS CARDS
              ========================= */}

          <div className="inventory-kpis">
            <div className="inventory-card">
              <span>Average Quantity / Order</span>

              <strong>
                {averageQuantity.toFixed(1)}
              </strong>

              <small>
                Units per order
              </small>
            </div>

            <div className="inventory-card">
              <span>Products Ordered</span>

              <strong>{uniqueProducts}</strong>

              <small>
                Unique products
              </small>
            </div>

            <div className="inventory-card">
              <span>Filtered Orders</span>

              <strong>
                {filteredOrders.length}
              </strong>

              <small>
                Matching search
              </small>
            </div>
          </div>

          {/* =========================
              REVENUE CHART
              ========================= */}

          {orders.length > 0 && (
            <div className="inventory-card">
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "16px",
                }}
              >
                <div>
                  <h2
                    style={{
                      margin: 0,
                      fontSize: "18px",
                    }}
                  >
                    Revenue by Product
                  </h2>

                  <p
                    style={{
                      margin: "4px 0 0",
                      color: "#64748b",
                      fontSize: "13px",
                    }}
                  >
                    Top products based on order revenue
                  </p>
                </div>
              </div>

              <div
                style={{
                  width: "100%",
                  height: "280px",
                }}
              >
                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >
                  <BarChart
                    data={productRevenueData}
                    margin={{
                      top: 10,
                      right: 10,
                      left: 0,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="productId"
                      tick={{ fontSize: 11 }}
                    />

                    <YAxis
                      tick={{ fontSize: 11 }}
                    />

                    <Tooltip
                      formatter={(value) =>
                        formatCurrency(Number(value))
                      }
                    />

                    <Bar
                      dataKey="revenue"
                      fill="#2563eb"
                      radius={[5, 5, 0, 0]}
                      barSize={32}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* =========================
              RECENT ORDERS
              ========================= */}

          {orders.length > 0 && (
            <div
              className="inventory-card"
              style={{ marginTop: "20px" }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "16px",
                }}
              >
                <div>
                  <h2
                    style={{
                      margin: 0,
                      fontSize: "18px",
                    }}
                  >
                    Recent Orders
                  </h2>

                  <p
                    style={{
                      margin: "4px 0 0",
                      color: "#64748b",
                      fontSize: "13px",
                    }}
                  >
                    Latest transactions from the orders
                    dataset
                  </p>
                </div>

                <strong>
                  {recentOrders.length} recent
                </strong>
              </div>

              <div className="inventory-table-wrapper">
                <table className="inventory-table">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Product ID</th>
                      <th>Date</th>
                      <th>Quantity</th>
                      <th>Total</th>
                    </tr>
                  </thead>

                  <tbody>
                    {recentOrders.map((order) => (
                      <tr key={order.id}>
                        <td>#{order.id}</td>

                        <td>
                          {order.productId}
                        </td>

                        <td>
                          {order.date}
                        </td>

                        <td>
                          {order.quantity}
                        </td>

                        <td>
                          {formatCurrency(order.total)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* =========================
              ALL ORDERS
              ========================= */}

          <div
            className="inventory-card"
            style={{ marginTop: "20px" }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "16px",
              }}
            >
              <div>
                <h2
                  style={{
                    margin: 0,
                    fontSize: "18px",
                  }}
                >
                  All Orders
                </h2>

                <p
                  style={{
                    margin: "4px 0 0",
                    color: "#64748b",
                    fontSize: "13px",
                  }}
                >
                  Detailed order and transaction records
                </p>
              </div>

              <strong>
                {filteredOrders.length} records
              </strong>
            </div>

            <OrdersTable orders={filteredOrders} />
          </div>
        </>
      )}
    </section>
  );
};

export default OrdersPage;