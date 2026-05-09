export type HealthResponse = {
  status: string;
  dependencies: Record<string, string>;
};

export type SessionCreateResponse = {
  session_id: string;
};

export type ChatResponse = {
  response: string;
  session_id: string;
  confidence?: number | null;
  handoff_trigger: boolean;
  intent?: string | null;
  metadata: Record<string, unknown>;
};

export type HistoryResponse = {
  session_id: string;
  messages: Array<{ role: string; content: string; timestamp?: string }>;
};

export type AnalyticsResponse = {
  total_sessions: number;
  total_messages: number;
  avg_session_sentiment: number | null;
  handoff_rate: number;
};

function apiBase(): string {
  return (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000").replace(/\/+$/, "");
}

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${apiBase()}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return (await res.json()) as T;
}

export const api = {
  health: () => jsonFetch<HealthResponse>("/health"),

  createSession: (userId: string) =>
    jsonFetch<SessionCreateResponse>("/session", {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }),

  chat: (payload: { user_id: string; session_id?: string; query: string }) =>
    jsonFetch<ChatResponse>("/chat", { method: "POST", body: JSON.stringify(payload) }),

  history: (sessionId: string) =>
    jsonFetch<HistoryResponse>(`/history?session_id=${encodeURIComponent(sessionId)}`),

  analytics: () => jsonFetch<AnalyticsResponse>("/analytics"),
};

