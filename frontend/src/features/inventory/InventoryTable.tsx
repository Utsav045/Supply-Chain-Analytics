import type { InventoryItem } from "./types";

interface InventoryTableProps {
  items: InventoryItem[];
}

const InventoryTable = ({ items }: InventoryTableProps) => {
  if (items.length === 0) {
    return (
      <div className="inventory-empty">
        No inventory records found.
      </div>
    );
  }

  return (
    <div className="inventory-table-wrapper">
      <table className="inventory-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Supplier</th>
            <th>Stock</th>
            <th>Reorder Level</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.productName}</td>
              <td>{item.category}</td>
              <td>{item.supplier}</td>
              <td>{item.stock}</td>
              <td>{item.reorderLevel}</td>
              <td>
                <span
                  className={`inventory-status inventory-status--${item.status
                    .toLowerCase()
                    .replace(/\s+/g, "-")}`}
                >
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryTable;