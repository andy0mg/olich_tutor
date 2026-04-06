import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../../api/client";
import type { StudentActivity } from "../../api/types";
import { PageShell } from "../../components/PageShell";

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function ChildActivityPage() {
  const { studentId } = useParams<{ studentId: string }>();

  const { data, isLoading, error } = useQuery({
    queryKey: ["student-activity", studentId],
    queryFn: () =>
      apiFetch<StudentActivity>(`/students/${studentId}/activity`),
    enabled: !!studentId,
  });

  return (
    <PageShell title={data ? `Активность: ${data.display_name}` : "Активность"}>
      <Link
        to="/parent"
        className="text-sm text-indigo-600 hover:underline mb-4 inline-block"
      >
        &larr; К списку детей
      </Link>

      {isLoading && <p className="text-gray-500">Загрузка...</p>}
      {error && <p className="text-red-600">Ошибка загрузки</p>}

      {data && (
        <>
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
              <p className="text-2xl font-semibold text-gray-900">
                {data.total_conversations}
              </p>
              <p className="text-sm text-gray-500">Занятий</p>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
              <p className="text-2xl font-semibold text-gray-900">
                {data.total_messages}
              </p>
              <p className="text-sm text-gray-500">Сообщений</p>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
              <p className="text-2xl font-semibold text-gray-900">
                {data.last_activity ? formatDate(data.last_activity) : "—"}
              </p>
              <p className="text-sm text-gray-500">Последняя активность</p>
            </div>
          </div>

          <h2 className="text-lg font-medium text-gray-900 mb-3">
            Последние занятия
          </h2>
          {data.recent_conversations.length === 0 ? (
            <p className="text-gray-500">Занятий пока нет</p>
          ) : (
            <div className="space-y-2">
              {data.recent_conversations.map((conv) => (
                <div
                  key={conv.id}
                  className="bg-white rounded-lg border border-gray-200 p-4"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900">
                      {conv.topic || "Без темы"}
                    </span>
                    <span className="text-sm text-gray-400">
                      {formatDate(conv.updated_at)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </PageShell>
  );
}
