import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { apiFetch } from "../../api/client";
import type { GuardianChild } from "../../api/types";
import { PageShell } from "../../components/PageShell";

export function ChildrenPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["children"],
    queryFn: () => apiFetch<GuardianChild[]>("/guardian-links/children"),
  });

  return (
    <PageShell title="Мои дети">
      {isLoading && <p className="text-gray-500">Загрузка...</p>}
      {error && <p className="text-red-600">Ошибка загрузки</p>}
      {data && data.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">Нет привязанных детей</p>
          <p className="text-sm text-gray-400 mt-1">
            Попросите ученика отправить вам ссылку-приглашение из бота
          </p>
        </div>
      )}
      {data && data.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2">
          {data.map((child) => (
            <div
              key={child.student_id}
              className="bg-white rounded-lg border border-gray-200 p-5"
            >
              <h3 className="text-lg font-medium text-gray-900 mb-1">
                {child.display_name}
              </h3>
              {child.grade_or_age_band && (
                <p className="text-sm text-gray-500 mb-3">
                  {child.grade_or_age_band}
                </p>
              )}
              <div className="flex gap-2">
                <Link
                  to={`/parent/child/${child.student_id}/activity`}
                  className="text-sm px-3 py-1.5 rounded-md bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition-colors"
                >
                  Активность
                </Link>
                <Link
                  to={`/parent/child/${child.student_id}/progress`}
                  className="text-sm px-3 py-1.5 rounded-md bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition-colors"
                >
                  Прогресс
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </PageShell>
  );
}
