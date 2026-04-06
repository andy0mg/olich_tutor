import { Navigate, Outlet } from "react-router-dom";
import type { UserRole } from "../api/types";
import { useAuth } from "./AuthContext";

export function RequireAuth({ role }: { role: UserRole }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role !== role) {
    const redirect = user.role === "parent" ? "/parent" : "/";
    return <Navigate to={redirect} replace />;
  }

  return <Outlet />;
}
