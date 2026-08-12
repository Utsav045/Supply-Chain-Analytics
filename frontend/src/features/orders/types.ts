export interface Order {
  id: number | string;
  productId: string;
  date: string;
  quantity: number;
  price: number;
  total: number;
}