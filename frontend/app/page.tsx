"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";

import { api, ChatResponse, HealthResponse } from "@/lib/api";

type UiMessage = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
  details?: ChatResponse;
};

function nowIso() {
  return new Date().toISOString();
}

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [userId, setUserId] = useState("user_web");
  const [sessionId, setSessionId] = useState<string | null>(null);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<UiMessage[]>([]);
  const listRef = useRef<HTMLDivElement | null>(null);

  const canSend = useMemo(() => input.trim().length > 0 && !loading, [input, loading]);

  useEffect(() => {
    const stored = localStorage.getItem("empowertech_session_id");
    if (stored) setSessionId(stored);
  }, []);

  useEffect(() => {
    if (sessionId) localStorage.setItem("empowertech_session_id", sessionId);
  }, [sessionId]);

  useEffect(() => {
    let alive = true;
    const tick = async () => {
      try {
        const h = await api.health();
        if (!alive) return;
        setHealth(h);
        setHealthError(null);
      } catch (e) {
        if (!alive) return;
        setHealth(null);
        setHealthError(e instanceof Error ? e.message : "Health check failed");
      }
    };
    tick();
    const t = setInterval(tick, 5000);
    return () => {
      alive = false;
      clearInterval(t);
    };
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages.length]);

  async function ensureSession() {
    if (sessionId) return sessionId;
    const s = await api.createSession(userId);
    setSessionId(s.session_id);
    return s.session_id;
  }

  async function send() {
    const q = input.trim();
    if (!q) return;
    setInput("");
    setLoading(true);

    const msgId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: msgId, role: "user", content: q, timestamp: nowIso() },
    ]);

    try {
      const sid = await ensureSession();
      const res = await api.chat({ user_id: userId, session_id: sid, query: q });
      setSessionId(res.session_id);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: res.response,
          timestamp: nowIso(),
          details: res,
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "system",
          content: e instanceof Error ? e.message : "Request failed",
          timestamp: nowIso(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function newSession() {
    setSessionId(null);
    localStorage.removeItem("empowertech_session_id");
    setMessages([]);
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="app-header">
        <div className="container-app py-4 flex items-center justify-between gap-4">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-xl border bg-gradient-to-br from-blue-600 to-indigo-600 shadow-sm" />
              <div className="min-w-0">
                <div className="text-base font-semibold leading-5 truncate">EmpowerTech Support</div>
                <div className="text-xs text-zinc-500 truncate">
                  RAG Chatbot • Customer support assistant
                </div>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2">
              <span className="badge">
                <span
                  className={[
                    "h-2 w-2 rounded-full",
                    health ? "bg-emerald-500" : healthError ? "bg-red-500" : "bg-zinc-300",
                  ].join(" ")}
                />
                <span className="text-zinc-700 dark:text-zinc-200">
                  {health ? "API healthy" : healthError ? "API offline" : "Checking API"}
                </span>
              </span>
              {health?.dependencies ? (
                <span className="badge text-zinc-600 dark:text-zinc-300">
                  postgres: {health.dependencies.postgres} • openai: {health.dependencies.openai} • pinecone:{" "}
                  {health.dependencies.pinecone}
                </span>
              ) : null}
            </div>

            <nav className="flex items-center gap-4">
            <Link className="navlink" href="/">
              Chat
            </Link>
            <Link className="navlink" href="/history">
              History
            </Link>
            <Link className="navlink" href="/analytics">
              Analytics
            </Link>
          </nav>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <div className="container-app py-6 grid gap-4">
          <section className="card p-4">
            <div className="flex flex-col md:flex-row md:items-end gap-3 justify-between">
              <div className="grid gap-2">
                <label className="text-xs font-medium text-zinc-600">User ID</label>
                <input
                  className="h-10 w-full md:w-72 rounded-xl border px-3 text-sm bg-white/70 dark:bg-white/5"
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                />
              </div>
              <div className="flex items-center gap-2">
                <div className="text-xs text-zinc-500">
                  Session: <span className="font-mono">{sessionId || "(none)"}</span>
                </div>
                <button
                  className="btn"
                  onClick={newSession}
                  type="button"
                >
                  New session
                </button>
              </div>
            </div>
          </section>

          <section className="card overflow-hidden">
            <div ref={listRef} className="h-[58vh] overflow-auto p-5 space-y-4">
              {messages.length === 0 ? (
                <div className="text-sm text-zinc-600">
                  Try: <span className="font-medium">“What payment methods are supported?”</span> or{" "}
                  <span className="font-medium">“How do I enroll in a course?”</span>
                </div>
              ) : null}
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={[
                    "grid gap-1",
                    m.role === "user" ? "justify-items-end" : "justify-items-start",
                  ].join(" ")}
                >
                  <div
                    className={[
                      "max-w-[90%] md:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-6 border shadow-sm",
                      m.role === "user"
                        ? "bg-gradient-to-br from-blue-600 to-indigo-600 text-white border-transparent"
                        : m.role === "assistant"
                          ? "bg-white/70 dark:bg-white/5 border-zinc-200/70 dark:border-white/10"
                          : "bg-zinc-50 border-zinc-200 text-zinc-700",
                    ].join(" ")}
                  >
                    {m.content}
                  </div>
                  <div className="text-[11px] text-zinc-500">
                    {m.role}
                    {m.timestamp ? <span className="ml-2 font-mono">{m.timestamp}</span> : null}
                  </div>
                  {m.details ? (
                    <details className="text-xs text-zinc-600 w-full max-w-[90%] md:max-w-[75%]">
                      <summary className="cursor-pointer select-none hover:text-zinc-900 dark:hover:text-white">
                        Details
                      </summary>
                      <pre className="mt-2 overflow-auto rounded-xl bg-zinc-950 text-zinc-50 p-3 text-[11px] border border-white/10">
                        {JSON.stringify(
                          {
                            session_id: m.details.session_id,
                            confidence: m.details.confidence,
                            intent: m.details.intent,
                            handoff_trigger: m.details.handoff_trigger,
                            metadata: m.details.metadata,
                          },
                          null,
                          2,
                        )}
                      </pre>
                    </details>
                  ) : null}
                </div>
              ))}
            </div>
            <div className="border-t p-3 flex gap-2 bg-white/60 dark:bg-white/5">
              <input
                className="h-11 flex-1 rounded-xl border px-3 text-sm bg-white/70 dark:bg-white/5"
                placeholder={loading ? "Waiting for response..." : "Type your question..."}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    if (canSend) void send();
                  }
                }}
                disabled={loading}
              />
              <button
                className="btn btn-primary h-11 px-5 disabled:opacity-50"
                disabled={!canSend}
                onClick={() => void send()}
                type="button"
              >
                Send
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
