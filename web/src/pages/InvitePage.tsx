import { useState, type FormEvent } from "react";
import { useParams, Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { ApiError } from "../api/client";

export function InvitePage() {
  const { code } = useParams<{ code: string }>();
  const { user, loading, acceptInvite } = useAuth();
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (loading) return null;
  if (user) {
    return <Navigate to={user.role === "parent" ? "/parent" : "/"} replace />;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!code) return;
    setError("");
    setSubmitting(true);
    try {
      await acceptInvite(code, displayName.trim());
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.body.message);
      } else {
        setError("Ошибка соединения");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-sm">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <h1 className="text-2xl font-semibold text-gray-900 text-center mb-2">
            Приглашение
          </h1>
          <p className="text-gray-500 text-center text-sm mb-6">
            Вас пригласили как родителя. Введите ваше имя для продолжения.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="Ваше имя"
              autoFocus
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />

            {error && (
              <p className="text-sm text-red-600 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={submitting || !displayName.trim()}
              className="w-full py-2.5 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {submitting ? "Подключение..." : "Принять приглашение"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
