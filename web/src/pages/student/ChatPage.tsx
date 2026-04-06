import { useState, useRef, useEffect, type FormEvent } from "react";
import { useParams } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../../api/client";
import type { ConversationWithMessages, MessageTurnResponse } from "../../api/types";

export function ChatPage() {
  const { conversationId } = useParams<{ conversationId: string }>();
  const queryClient = useQueryClient();
  const bottomRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["conversation", conversationId],
    queryFn: () =>
      apiFetch<ConversationWithMessages>(
        `/conversations/${conversationId}?limit=100`,
      ),
    enabled: !!conversationId,
  });

  const sendMutation = useMutation({
    mutationFn: (content: string) =>
      apiFetch<MessageTurnResponse>(
        `/conversations/${conversationId}/messages`,
        { method: "POST", body: JSON.stringify({ content }) },
      ),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["conversation", conversationId],
      });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [data?.messages.length, sendMutation.isPending]);

  function handleSend(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sendMutation.isPending) return;
    setInput("");
    sendMutation.mutate(text);
  }

  const topic = data?.conversation.topic;

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {topic && (
        <div className="border-b border-gray-200 bg-white px-4 py-2">
          <span className="text-sm text-gray-600">Тема: {topic}</span>
        </div>
      )}

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
        {isLoading && <p className="text-gray-400 text-center">Загрузка...</p>}
        {data?.messages.map((msg) => (
          <div
            key={msg.id}
            className={`max-w-[80%] ${msg.role === "user" ? "ml-auto" : "mr-auto"}`}
          >
            <div
              className={`rounded-2xl px-4 py-2.5 ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-white border border-gray-200 text-gray-900"
              }`}
            >
              <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
            </div>
            <p
              className={`text-xs mt-1 ${msg.role === "user" ? "text-right text-gray-400" : "text-gray-400"}`}
            >
              {new Date(msg.created_at).toLocaleTimeString("ru-RU", {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
        ))}

        {sendMutation.isPending && (
          <div className="mr-auto max-w-[80%]">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <form
        onSubmit={handleSend}
        className="border-t border-gray-200 bg-white p-4 flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Введите сообщение..."
          className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          disabled={sendMutation.isPending}
        />
        <button
          type="submit"
          disabled={!input.trim() || sendMutation.isPending}
          className="px-6 py-2.5 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Отправить
        </button>
      </form>
    </div>
  );
}
