export type Channel = "telegram" | "web";
export type KnowledgeLevel = "needs_work" | "developing" | "proficient" | "mastered";
export type MessageRole = "user" | "assistant" | "system";
export type SnapshotSource = "homework" | "self_report" | "tutor";
export type UserRole = "student" | "parent";
export type LinkStatus = "pending" | "active" | "rejected" | "revoked" | "expired";

export interface Conversation {
  id: string;
  channel: Channel;
  external_user_id: string;
  topic: string | null;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: MessageRole;
  content: string;
  sequence: number;
  created_at: string;
  metadata: Record<string, unknown> | null;
}

export interface ConversationWithMessages {
  conversation: Conversation;
  messages: Message[];
  next_cursor: string | null;
}

export interface MessageTurnResponse {
  user_message: Message;
  assistant_message: Message;
  conversation: Conversation;
}

export interface KnowledgeSnapshot {
  id: string;
  channel: Channel;
  external_user_id: string;
  topic: string;
  level: KnowledgeLevel;
  comment: string | null;
  enrollment_id: string | null;
  learning_stream_id: string | null;
  source: SnapshotSource;
  recorded_at: string;
}

export interface AuthUser {
  user_id: number;
  role: UserRole;
  display_name: string;
  student_id: number | null;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  user: AuthUser;
}

export interface GuardianChild {
  student_id: number;
  display_name: string;
  grade_or_age_band: string | null;
  link_status: LinkStatus;
}

export interface StudentActivity {
  student_id: number;
  display_name: string;
  total_conversations: number;
  total_messages: number;
  last_activity: string | null;
  recent_conversations: Conversation[];
}

export interface ErrorResponse {
  error: string;
  message: string;
  details: Record<string, unknown> | null;
}
