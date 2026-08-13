import type { RouteObject } from "react-router-dom";

import DashboardPage from "../features/dashboard/DashboardPage";
import InventoryPage from "../features/inventory/InventoryPage";
import OrdersPage from "../features/orders/OrdersPage";
import SuppliersPage from "../features/suppliers/SuppliersPage";
import Reports from "../pages/Reports";

const routes: RouteObject[] = [
  {
    path: "/",
    element: <DashboardPage />,
  },
  {
    path: "/dashboard",
    element: <DashboardPage />,
  },
  {
    path: "/inventory",
    element: <InventoryPage />,
  },
  {
    path: "/orders",
    element: <OrdersPage />,
  },
  {
    path: "/suppliers",
    element: <SuppliersPage />,
  },
  {
    path: "/reports",
    element: <Reports />,
  },
];

export default routes;