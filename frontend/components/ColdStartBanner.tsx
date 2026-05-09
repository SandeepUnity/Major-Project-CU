"use client";

import { useCallback, useSyncExternalStore } from "react";

const STORAGE_KEY = "empowertech_hide_cold_start_banner";

const listeners = new Set<() => void>();

function subscribe(onStoreChange: () => void) {
  listeners.add(onStoreChange);
  return () => listeners.delete(onStoreChange);
}

function emitChange() {
  listeners.forEach((l) => l());
}

function hostingShowsColdStartDelay(): boolean {
  if (process.env.NEXT_PUBLIC_HIDE_COLD_START_HINT === "true") return false;
  const base = (process.env.NEXT_PUBLIC_API_BASE_URL || "").toLowerCase();
  return base.includes("onrender.com") || base.includes("render.com");
}

function readDismissedFromStorage(): boolean {
  try {
    return sessionStorage.getItem(STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

/** Visible when hosting looks like free Render and banner not dismissed. */
function getClientSnapshotVisible(): boolean {
  if (!hostingShowsColdStartDelay()) return false;
  return !readDismissedFromStorage();
}

/**
 * Server / first paint: mirror “likely visible” without session (assume not dismissed).
 * Avoid flash-off then on for Render URLs; dismissal only applies after client read.
 */
function getServerSnapshotVisible(): boolean {
  return hostingShowsColdStartDelay();
}

export function ColdStartBanner() {
  const visible = useSyncExternalStore(
    subscribe,
    getClientSnapshotVisible,
    getServerSnapshotVisible,
  );

  const dismiss = useCallback(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, "1");
    } catch {
      /* ignore */
    }
    emitChange();
  }, []);

  if (!visible) return null;

  return (
    <div
      className="border-b border-amber-200/90 bg-amber-50 text-amber-950 dark:border-amber-800/80 dark:bg-amber-950/50 dark:text-amber-100"
      role="region"
      aria-label="Hosting notice"
    >
      <div className="container-app flex flex-col gap-2 py-2.5 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
        <p className="text-sm leading-snug">
          <span className="font-medium">Demo hosting note:</span> this API may <strong>spin down</strong> after idle
          periods. The first request after a break can take about <strong>30–60 seconds</strong> — please wait; it is
          normal for a free tier.
        </p>
        <button
          type="button"
          onClick={dismiss}
          className="shrink-0 rounded-lg border border-amber-300/80 bg-white/80 px-3 py-1 text-xs font-medium text-amber-950 shadow-sm hover:bg-amber-100 dark:border-amber-700 dark:bg-zinc-900/80 dark:text-amber-50 dark:hover:bg-zinc-800"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}
