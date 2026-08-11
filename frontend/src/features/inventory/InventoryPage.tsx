import { useMemo, useState } from "react";
import InventoryTable from "./InventoryTable";
import { useInventory } from "../../hooks/useInventory";

const InventoryPage = () => {
  const { items, loading, error } = useInventory();

  const [search, setSearch] = useState("");

  const filteredItems = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return items;
    }

    return items.filter(
      (item) =>
        item.productName.toLowerCase().includes(query) ||
        item.category.toLowerCase().includes(query) ||
        item.supplier.toLowerCase().includes(query)
    );
  }, [items, search]);

  const totalProducts = items.length;

  const totalStock = items.reduce(
    (total, item) => total + item.stock,
    0
  );

  const lowStock = items.filter(
    (item) => item.status === "Low Stock"
  ).length;

  const outOfStock = items.filter(
    (item) => item.status === "Out of Stock"
  ).length;

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Inventory</h1>
          <p>Monitor stock levels and inventory availability.</p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search inventory..."
          className="inventory-search"
        />
      </div>

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Products</span>
          <strong>{totalProducts}</strong>
        </div>

        <div className="inventory-card">
          <span>Total Stock</span>
          <strong>{totalStock}</strong>
        </div>

        <div className="inventory-card">
          <span>Low Stock</span>
          <strong>{lowStock}</strong>
        </div>

        <div className="inventory-card">
          <span>Out of Stock</span>
          <strong>{outOfStock}</strong>
        </div>
      </div>

      {loading && (
        <div className="inventory-message">
          Loading inventory...
        </div>
      )}

      {error && (
        <div className="inventory-message inventory-message--error">
          {error}
        </div>
      )}

      {!loading && !error && (
        <InventoryTable items={filteredItems} />
      )}
    </section>
  );
};

export default InventoryPage;