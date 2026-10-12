import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

function Layout({ onLogout }) {
    return (
        <div className="app-layout">
            <Sidebar onLogout={onLogout} />

            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
}

export default Layout;