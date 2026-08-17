import type { RouteObject } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import DashboardPage from "../features/dashboard/DashboardPage";
import InventoryPage from "../features/inventory/InventoryPage";
import OrdersPage from "../features/orders/OrdersPage";
import SuppliersPage from "../features/suppliers/SuppliersPage";
import Reports from "../pages/Reports";
import Settings from "../pages/Settings";

const routes: RouteObject[] = [
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "dashboard",
        element: <DashboardPage />,
      },
      {
        path: "inventory",
        element: <InventoryPage />,
      },
      {
        path: "orders",
        element: <OrdersPage />,
      },
      {
        path: "suppliers",
        element: <SuppliersPage />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
      {
        path: "settings",
        element: <Settings />,
      },
    ],
  },
];

export default routes;