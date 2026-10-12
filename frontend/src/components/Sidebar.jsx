import { useState } from "react";
import { NavLink } from "react-router-dom";
import styles from "../styles/Sidebar.module.css";
import {
  LayoutDashboard,
  Package,
  PackagePlus,
  ShoppingCart,
  History,
  Truck,
  Users,
  Settings,
  LogOut,
} from "lucide-react";

const SIDEBAR_ITEMS = [
  {
    id: "general",
    label: "GENERAL",
    type: "section",
  },
  {
    id: "dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
    type: "page",
  },
  {
    id: "gestion",
    label: "GESTION",
    type: "section",
  },
  {
    id: "inventario",
    label: "Inventario",
    icon: Package,
    type: "page",
  },
  {
    id: "cargar-stock",
    label: "Cargar Stock",
    icon: PackagePlus,
    type: "page",
    path: "/cargar-stock",
  },
  {
    id: "ventas",
    label: "Ventas",
    icon: ShoppingCart,
    type: "page",
  },
  {
    id: "historial",
    label: "Historial",
    icon: History,
    type: "page",
  },
  {
    id: "proveedores",
    label: "Proveedores",
    icon: Truck,
    type: "page",
    path: "/proveedores",
  },
  {
    id: "administracion",
    label: "ADMINISTRACION",
    type: "section",
  },
  {
    id: "usuarios",
    label: "Usuarios",
    icon: Users,
    type: "page",
  },
  {
    id: "ajustes",
    label: "Ajustes",
    icon: Settings,
    type: "page",
  },
];

export const Sidebar = ({ onLogout }) => {
  const [activeItem, setActiveItem] = useState("dashboard");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handlePageClick = (id) => {
    setActiveItem(id);
    setMobileMenuOpen(false);
  };

  
  return (
    <section
      className={`${styles.page} ${styles["sidebar-12-page"]} color-de-fondo`}
    >
      <aside
        className={`${styles["sidebar-12"]} ${
          mobileMenuOpen ? styles["sidebar-12--open"] : ""
        }`}
      >
        <header>
          <span>Stock</span>
          <button
            type="button"
            className={styles["mobile-toggle"]}
            aria-expanded={mobileMenuOpen}
            aria-controls="sidebar-navigation"
            onClick={() => setMobileMenuOpen((isOpen) => !isOpen)}
          >
            {mobileMenuOpen ? "Cerrar" : "Menú"}
          </button>
        </header>
        <ul id="sidebar-navigation">
          {SIDEBAR_ITEMS.map((item) =>
            item.type === "section" ? (
              <li key={item.id}>
                <p
                  style={{
                    margin: "16px 16px 4px",
                    color: "rgb(255 255 255 / 60%)",
                    fontSize: "12px",
                    fontWeight: 600,
                  }}
                >
                  {item.label}
                </p>
              </li>
            ) : item.path ? (
              <li key={item.id}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) => (isActive ? styles.active : "")}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <item.icon size={20} strokeWidth={2} aria-hidden="true" />
                  <p>{item.label}</p>
                </NavLink>
              </li>
            ) : (
              <li key={item.id}>
                <button
                  className={activeItem === item.id ? styles.active : ""}
                  onClick={() => handlePageClick(item.id)}
                >
                  <item.icon size={20} strokeWidth={2} aria-hidden="true" />
                  <p>{item.label}</p>
                </button>
              </li>
            ),
          )}
        </ul>
        <button
          type="button"
          className={styles["logout-button"]}
          onClick={onLogout}
        >
          <LogOut size={20} strokeWidth={2} aria-hidden="true" />
          <p>Cerrar Sesión</p>
        </button>
      </aside>
    </section>
  );
};

export default Sidebar;