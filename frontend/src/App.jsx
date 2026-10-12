import { useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import CargarProductos from "./components/CargarProductos";
import CargarProveedores from "./pages/CargarProveedor";
import LoginForm from "./pages/Login";

function App() {
  const [token, setToken] = useState(() =>
    localStorage.getItem("access_token"),
  );

  function handleLogin(accessToken) {
    localStorage.setItem("access_token", accessToken);
    setToken(accessToken);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setToken(null);
  }

  if (!token) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <Routes>
      <Route element={<Layout onLogout={handleLogout} />}>
        <Route index element={<Navigate to="/cargar-stock" replace />} />
        <Route
          path="cargar-stock"
          element={<CargarProductos token={token} />}
        />
        <Route
          path="proveedores"
          element={<CargarProveedores token={token} />}
        />
        <Route
          path="*"
          element={<Navigate to="/cargar-stock" replace />}
        />
      </Route>
    </Routes>
  );
}

export default App;
