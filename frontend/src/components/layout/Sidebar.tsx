import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    label: "Executive",
    path: "/dashboard",
    icon: "▣",
  },
  {
    label: "Forecasting",
    path: "/forecast",
    icon: "⌁",
  },
  {
    label: "Inventory",
    path: "/inventory",
    icon: "▤",
  },
  {
    label: "Logistics",
    path: "/logistics",
    icon: "⇢",
  },
  {
    label: "Suppliers",
    path: "/suppliers",
    icon: "♙",
  },
  {
    label: "Orders",
    path: "/orders",
    icon: "▦",
  },
  {
    label: "Settings",
    path: "/settings",
    icon: "⚙",
  },
];

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">◆</div>

        <span className="brand-name">Supply Analytics</span>
      </div>

      <nav className="sidebar-navigation">
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
          >
            <span className="sidebar-link-icon">{item.icon}</span>

            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button type="button" className="logout-button">
          <span>⇥</span>
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;