export interface Supplier {
  supplierId: string;
  supplierName: string;
  productId: string;
  deliveryDate: string;
  expectedDate: string;
  delayDays: number;
  supplierRating: number;
  transportationCost: number;
}