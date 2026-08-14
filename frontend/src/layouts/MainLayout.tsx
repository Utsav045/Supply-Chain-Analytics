import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

const MainLayout = () => {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-area">
        <Header />

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;