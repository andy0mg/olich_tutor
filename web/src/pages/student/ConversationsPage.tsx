import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { apiFetch } from "../../api/client";
import type { Conversation } from "../../api/types";
import { PageShell } from "../../components/PageShell";

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function ConversationsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["conversations"],
    queryFn: () => apiFetch<Conversation[]>("/conversations"),
  });

  return (
    <PageShell title="Занятия">
      {isLoading && (
        <p className="text-gray-500">Загрузка...</p>
      )}
      {error && (
        <p className="text-red-600">Ошибка загрузки</p>
      )}
      {data && data.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-2">Пока нет занятий</p>
          <p className="text-sm text-gray-400">
            Начните диалог с репетитором в Telegram-боте или здесь
          </p>
        </div>
      )}
      {data && data.length > 0 && (
        <div className="space-y-2">
          {data.map((conv) => (
            <Link
              key={conv.id}
              to={`/chat/${conv.id}`}
              className="block bg-white rounded-lg border border-gray-200 p-4 hover:border-indigo-300 hover:shadow-sm transition"
            >
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">
                  {conv.topic || "Без темы"}
                </span>
                <span className="text-sm text-gray-400">
                  {formatDate(conv.updated_at)}
                </span>
              </div>
              <span className="text-sm text-gray-500 mt-1 block">
                {conv.channel === "telegram" ? "Telegram" : "Веб"}
              </span>
            </Link>
          ))}
        </div>
      )}
    </PageShell>
  );
}
