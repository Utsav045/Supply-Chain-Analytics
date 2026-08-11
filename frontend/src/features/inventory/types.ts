export interface InventoryItem {
  id: number | string;
  productName: string;
  category: string;
  supplier: string;
  stock: number;
  reorderLevel: number;
  status: "In Stock" | "Low Stock" | "Out of Stock";
}

export interface InventoryState {
  items: InventoryItem[];
  loading: boolean;
  error: string | null;
}