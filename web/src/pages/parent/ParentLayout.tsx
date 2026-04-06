import { Outlet } from "react-router-dom";
import { Navbar } from "../../components/Navbar";

const NAV_ITEMS = [{ to: "/parent", label: "Мои дети" }];

export function ParentLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar items={NAV_ITEMS} />
      <Outlet />
    </div>
  );
}
