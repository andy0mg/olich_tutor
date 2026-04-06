import { Outlet } from "react-router-dom";
import { Navbar } from "../../components/Navbar";

const NAV_ITEMS = [
  { to: "/", label: "Занятия" },
  { to: "/progress", label: "Прогресс" },
];

export function StudentLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar items={NAV_ITEMS} />
      <Outlet />
    </div>
  );
}
