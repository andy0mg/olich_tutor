import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./auth/AuthContext";
import { RequireAuth } from "./auth/RequireAuth";
import { LoginPage } from "./pages/LoginPage";
import { StudentLayout } from "./pages/student/StudentLayout";
import { ConversationsPage } from "./pages/student/ConversationsPage";
import { ChatPage } from "./pages/student/ChatPage";
import { ProgressPage } from "./pages/student/ProgressPage";
import { ParentLayout } from "./pages/parent/ParentLayout";
import { ChildrenPage } from "./pages/parent/ChildrenPage";
import { ChildActivityPage } from "./pages/parent/ChildActivityPage";
import { ChildProgressPage } from "./pages/parent/ChildProgressPage";
import { InvitePage } from "./pages/InvitePage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/invite/:code" element={<InvitePage />} />

            <Route element={<RequireAuth role="student" />}>
              <Route element={<StudentLayout />}>
                <Route path="/" element={<ConversationsPage />} />
                <Route path="/chat/:conversationId" element={<ChatPage />} />
                <Route path="/progress" element={<ProgressPage />} />
              </Route>
            </Route>

            <Route element={<RequireAuth role="parent" />}>
              <Route element={<ParentLayout />}>
                <Route path="/parent" element={<ChildrenPage />} />
                <Route
                  path="/parent/child/:studentId/activity"
                  element={<ChildActivityPage />}
                />
                <Route
                  path="/parent/child/:studentId/progress"
                  element={<ChildProgressPage />}
                />
              </Route>
            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
