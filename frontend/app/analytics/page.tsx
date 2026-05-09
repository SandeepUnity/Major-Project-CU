"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { api, AnalyticsResponse } from "@/lib/api";

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.analytics();
        if (!alive) return;
        setData(res);
      } catch (e) {
        if (!alive) return;
        setError(e instanceof Error ? e.message : "Failed to load analytics");
      } finally {
        if (alive) setLoading(false);
      }
    };
    run();
    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="min-h-screen">
      <header className="app-header">
        <div className="container-app py-4 flex items-center justify-between">
          <div className="text-base font-semibold">Analytics</div>
          <nav className="flex items-center gap-3 text-sm">
            <Link className="navlink" href="/">
              Chat
            </Link>
            <Link className="navlink" href="/history">
              History
            </Link>
          </nav>
        </div>
      </header>

      <main className="container-app py-6 grid gap-4">
        <section className="card p-5">
          {loading ? <div className="text-sm text-zinc-600">Loading...</div> : null}
          {error ? <div className="text-sm text-red-700">{error}</div> : null}

          {data ? (
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border bg-white/70 dark:bg-white/5 p-4">
                <div className="text-xs text-zinc-500">Total sessions</div>
                <div className="text-2xl font-semibold">{data.total_sessions}</div>
              </div>
              <div className="rounded-2xl border bg-white/70 dark:bg-white/5 p-4">
                <div className="text-xs text-zinc-500">Total messages</div>
                <div className="text-2xl font-semibold">{data.total_messages}</div>
              </div>
              <div className="rounded-2xl border bg-white/70 dark:bg-white/5 p-4">
                <div className="text-xs text-zinc-500">Avg session sentiment</div>
                <div className="text-2xl font-semibold">
                  {data.avg_session_sentiment === null ? "—" : data.avg_session_sentiment.toFixed(3)}
                </div>
              </div>
              <div className="rounded-2xl border bg-white/70 dark:bg-white/5 p-4">
                <div className="text-xs text-zinc-500">Handoff rate</div>
                <div className="text-2xl font-semibold">{(data.handoff_rate * 100).toFixed(1)}%</div>
              </div>

              <div className="md:col-span-2">
                <details className="text-xs text-zinc-600">
                  <summary className="cursor-pointer select-none">Raw JSON</summary>
                  <pre className="mt-2 overflow-auto rounded-xl bg-zinc-950 text-zinc-50 p-3 text-[11px] border border-white/10">
                    {JSON.stringify(data, null, 2)}
                  </pre>
                </details>
              </div>
            </div>
          ) : null}
        </section>
      </main>
    </div>
  );
}

