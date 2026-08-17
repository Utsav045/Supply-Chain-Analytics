import type { LogisticsRecord } from "./types";

interface LogisticsTableProps {
  records: LogisticsRecord[];
}

const LogisticsTable = ({ records }: LogisticsTableProps) => {
  if (records.length === 0) {
    return (
      <div className="inventory-message">
        No logistics records found.
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
          {records.map((record, index) => (
            <tr
              key={`${record.supplierId}-${record.productId}-${record.deliveryDate}-${index}`}
            >
              <td>{record.supplierId}</td>
              <td>{record.supplierName}</td>
              <td>{record.productId}</td>
              <td>{record.deliveryDate}</td>
              <td>{record.expectedDate}</td>

              <td>
                {record.delayDays === 0
                  ? "On Time"
                  : `${record.delayDays} day${
                      record.delayDays === 1 ? "" : "s"
                    }`}
              </td>

              <td>{record.supplierRating.toFixed(1)} / 5</td>

              <td>₹{record.transportationCost.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LogisticsTable;