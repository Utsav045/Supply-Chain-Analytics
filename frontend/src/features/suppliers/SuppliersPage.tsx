import { useEffect, useMemo, useState } from "react";
import { getSuppliers } from "./suppliersApi";
import type { Supplier } from "./types";
import SuppliersTable from "./SuppliersTable";

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
        setSuppliers(data);
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

  const totalRecords = suppliers.length;

  const uniqueSuppliers = new Set(
    suppliers.map((supplier) => supplier.supplierId),
  ).size;

  const averageRating =
    suppliers.length > 0
      ? suppliers.reduce(
          (total, supplier) => total + supplier.supplierRating,
          0,
        ) / suppliers.length
      : 0;

  const averageDelay =
    suppliers.length > 0
      ? suppliers.reduce(
          (total, supplier) => total + supplier.delayDays,
          0,
        ) / suppliers.length
      : 0;

  return (
    <section className="inventory-page">
      <div className="inventory-header">
        <div>
          <h1>Suppliers</h1>
          <p>Monitor supplier performance and delivery information.</p>
        </div>

        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search suppliers..."
          className="inventory-search"
        />
      </div>

      <div className="inventory-kpis">
        <div className="inventory-card">
          <span>Total Records</span>
          <strong>{totalRecords}</strong>
        </div>

        <div className="inventory-card">
          <span>Unique Suppliers</span>
          <strong>{uniqueSuppliers}</strong>
        </div>

        <div className="inventory-card">
          <span>Average Rating</span>
          <strong>{averageRating.toFixed(1)} / 5</strong>
        </div>

        <div className="inventory-card">
          <span>Average Delay</span>
          <strong>{averageDelay.toFixed(1)} days</strong>
        </div>
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
        <SuppliersTable suppliers={filteredSuppliers} />
      )}
    </section>
  );
};

export default SuppliersPage;