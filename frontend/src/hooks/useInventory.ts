import { useEffect, useState } from "react";
import { getInventory } from "../api/inventoryApi";
import type { InventoryItem } from "../features/inventory/types";

interface UseInventoryResult {
  items: InventoryItem[];
  loading: boolean;
  error: string | null;
}

export const useInventory = (): UseInventoryResult => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadInventory = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getInventory();
        setItems(data);
      } catch (err) {
        console.error("Failed to load inventory:", err);
        setError("Failed to load inventory data.");
      } finally {
        setLoading(false);
      }
    };

    void loadInventory();
  }, []);

  return {
    items,
    loading,
    error,
  };
};