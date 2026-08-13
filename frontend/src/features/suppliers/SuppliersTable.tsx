import type { Supplier } from "./types";

interface SuppliersTableProps {
  suppliers: Supplier[];
}

const SuppliersTable = ({ suppliers }: SuppliersTableProps) => {
  if (suppliers.length === 0) {
    return (
      <div className="inventory-message">
        No suppliers found.
      </div>
    );
  }

  return (
    <div className="inventory-table-wrapper">
      <table className="inventory-table">
        <thead>
          <tr>
            <th>Supplier ID</th>
            <th>Supplier Name</th>
            <th>Product ID</th>
            <th>Delivery Date</th>
            <th>Expected Date</th>
            <th>Delay</th>
            <th>Rating</th>
            <th>Transportation Cost</th>
          </tr>
        </thead>

        <tbody>
          {suppliers.map((supplier, index) => (
            <tr
              key={`${supplier.supplierId}-${supplier.productId}-${supplier.deliveryDate}-${index}`}
            >
              <td>{supplier.supplierId}</td>
              <td>{supplier.supplierName}</td>
              <td>{supplier.productId}</td>
              <td>{supplier.deliveryDate}</td>
              <td>{supplier.expectedDate}</td>

              <td>
                {supplier.delayDays === 0
                  ? "On Time"
                  : `${supplier.delayDays} day${
                      supplier.delayDays === 1 ? "" : "s"
                    }`}
              </td>

              <td>
                {supplier.supplierRating.toFixed(1)} / 5
              </td>

              <td>
                ₹{supplier.transportationCost.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SuppliersTable;