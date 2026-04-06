import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../../api/client";
import type { KnowledgeSnapshot } from "../../api/types";
import { PageShell } from "../../components/PageShell";
import { LevelBadge } from "../../components/LevelBadge";

export function ChildProgressPage() {
  const { studentId } = useParams<{ studentId: string }>();

  const { data, isLoading, error } = useQuery({
    queryKey: ["student-progress", studentId],
    queryFn: () =>
      apiFetch<KnowledgeSnapshot[]>(`/students/${studentId}/progress`),
    enabled: !!studentId,
  });

  return (
    <PageShell title="Прогресс ребёнка">
      <Link
        to="/parent"
        className="text-sm text-indigo-600 hover:underline mb-4 inline-block"
      >
        &larr; К списку детей
      </Link>

      {isLoading && <p className="text-gray-500">Загрузка...</p>}
      {error && <p className="text-red-600">Ошибка загрузки</p>}

      {data && data.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">Пока нет данных о прогрессе</p>
        </div>
      )}

      {data && data.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">
                  Тема
                </th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">
                  Уровень
                </th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">
                  Комментарий
                </th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">
                  Дата
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.map((snap) => (
                <tr key={snap.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {snap.topic}
                  </td>
                  <td className="px-4 py-3">
                    <LevelBadge level={snap.level} />
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {snap.comment || "—"}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {new Date(snap.recorded_at).toLocaleDateString("ru-RU")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </PageShell>
  );
}
