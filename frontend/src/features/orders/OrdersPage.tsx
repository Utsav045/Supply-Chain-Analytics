import { useEffect, useMemo, useState } from "react";
import { getOrders } from "./ordersApi";
import type { Order } from "./types";
import OrdersTable from "./OrdersTable";

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

  const totalOrders = orders.length;

  const totalQuantity = orders.reduce(
    (total, order) => total + order.quantity,
    0,
  );

  const totalRevenue = orders.reduce(
    (total, order) => total + order.total,
    0,
  );

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Orders</h1>
          <p>Monitor sales orders and transaction details.</p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search orders..."
          className="inventory-search"
        />
      </div>

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Orders</span>
          <strong>{totalOrders}</strong>
        </div>

        <div className="inventory-card">
          <span>Total Quantity</span>
          <strong>{totalQuantity}</strong>
        </div>

        <div className="inventory-card">
          <span>Total Revenue</span>
          <strong>₹{totalRevenue.toFixed(2)}</strong>
        </div>
      </div>

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
        <OrdersTable orders={filteredOrders} />
      )}
    </section>
  );
};

export default OrdersPage;