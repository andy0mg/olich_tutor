import type { KnowledgeLevel } from "../api/types";

const LEVEL_CONFIG: Record<KnowledgeLevel, { label: string; cls: string }> = {
  needs_work: { label: "Нужна работа", cls: "bg-red-100 text-red-800" },
  developing: { label: "В процессе", cls: "bg-yellow-100 text-yellow-800" },
  proficient: { label: "Хорошо", cls: "bg-blue-100 text-blue-800" },
  mastered: { label: "Освоено", cls: "bg-green-100 text-green-800" },
};

export function LevelBadge({ level }: { level: KnowledgeLevel }) {
  const { label, cls } = LEVEL_CONFIG[level];
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>
      {label}
    </span>
  );
}
