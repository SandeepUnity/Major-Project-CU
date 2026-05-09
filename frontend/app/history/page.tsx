"use client";

import Link from "next/link";
import { useState } from "react";

import { api, HistoryResponse } from "@/lib/api";

export default function HistoryPage() {
  const [sessionId, setSessionId] = useState("");
  const [data, setData] = useState<HistoryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    const sid = sessionId.trim();
    if (!sid) return;
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const res = await api.history(sid);
      setData(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load history");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen">
      <header className="app-header">
        <div className="container-app py-4 flex items-center justify-between">
          <div className="text-base font-semibold">Session History</div>
          <nav className="flex items-center gap-3 text-sm">
            <Link className="navlink" href="/">
              Chat
            </Link>
            <Link className="navlink" href="/analytics">
              Analytics
            </Link>
          </nav>
        </div>
      </header>

      <main className="container-app py-6 grid gap-4">
        <section className="card p-4 grid gap-3">
          <div className="text-sm text-zinc-600">
            Enter a session id (from the Chat page) to load stored messages.
          </div>
          <div className="flex gap-2">
            <input
              className="h-11 flex-1 rounded-xl border px-3 text-sm font-mono bg-white/70 dark:bg-white/5"
              placeholder="session_id"
              value={sessionId}
              onChange={(e) => setSessionId(e.target.value)}
            />
            <button
              className="btn btn-primary h-11 px-5 disabled:opacity-50"
              onClick={() => void load()}
              disabled={loading || !sessionId.trim()}
              type="button"
            >
              {loading ? "Loading..." : "Load"}
            </button>
          </div>
          {error ? <div className="text-sm text-red-700">{error}</div> : null}
        </section>

        {data ? (
          <section className="card overflow-hidden">
            <div className="border-b p-3 text-sm text-zinc-600">
              Session: <span className="font-mono">{data.session_id}</span>
            </div>
            <div className="p-5 space-y-4">
              {data.messages.map((m, idx) => (
                <div key={idx} className="grid gap-1">
                  <div className="text-xs text-zinc-500">
                    {m.role} {m.timestamp ? <span className="ml-2 font-mono">{m.timestamp}</span> : null}
                  </div>
                  <div className="rounded-2xl border bg-white/70 dark:bg-white/5 px-4 py-3 text-sm leading-6">
                    {m.content}
                  </div>
                </div>
              ))}
            </div>
            <div className="border-t p-3 flex gap-2">
              <button
                className="btn"
                onClick={() => navigator.clipboard.writeText(JSON.stringify(data, null, 2))}
                type="button"
              >
                Copy JSON
              </button>
            </div>
          </section>
        ) : null}
      </main>
    </div>
  );
}

