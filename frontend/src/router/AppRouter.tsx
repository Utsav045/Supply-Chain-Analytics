import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import OrdersPage from "../features/orders/OrdersPage";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/orders" replace />} />
        <Route path="/orders" element={<OrdersPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;