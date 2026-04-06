import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import type { AuthUser, AuthTokens, UserRole } from "../api/types";
import { apiFetch, setTokens, clearTokens } from "../api/client";

interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  login: (code: string) => Promise<void>;
  acceptInvite: (code: string, displayName: string) => Promise<void>;
  logout: () => void;
}

const AuthCtx = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    apiFetch<AuthUser>("/auth/me")
      .then(setUser)
      .catch(() => {
        clearTokens();
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (code: string) => {
    const data = await apiFetch<AuthTokens>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ code }),
    });
    setTokens(data.access_token, data.refresh_token);
    setUser(data.user);
  }, []);

  const acceptInvite = useCallback(
    async (code: string, displayName: string) => {
      const data = await apiFetch<AuthTokens>("/auth/accept-invite", {
        method: "POST",
        body: JSON.stringify({ code, display_name: displayName }),
      });
      setTokens(data.access_token, data.refresh_token);
      setUser(data.user);
    },
    [],
  );

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
  }, []);

  return (
    <AuthCtx.Provider value={{ user, loading, login, acceptInvite, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthCtx);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}

export function useRequireRole(role: UserRole): AuthUser {
  const { user } = useAuth();
  if (!user || user.role !== role) {
    throw new Error(`Requires role ${role}`);
  }
  return user;
}
