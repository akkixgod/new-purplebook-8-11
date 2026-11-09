"use client";

import { useEffect, useRef } from "react";
import { SessionProvider, useSession } from "next-auth/react";
import { listAllPendingSubmissions } from "@/lib/attempt-cache";
import { syncAccountAttempts } from "@/lib/sync-account-attempts";

function AccountAttemptSync() {
  const { data: session, status } = useSession();
  const ranForUser = useRef<string | null>(null);
  const userId = session?.user?.id ?? null;

  useEffect(() => {
    if (status !== "authenticated" || !userId) {
      ranForUser.current = null;
      return;
    }

    const run = () => {
      void syncAccountAttempts().then((r) => {
        if (r.claimed || r.flushed) {
          console.info("[AccountAttemptSync]", r);
        }
      });
    };

    // Always sync once per signed-in user per tab mount.
    if (ranForUser.current !== userId) {
      ranForUser.current = userId;
      run();
    }

    // Keep flushing while pending submits remain (network recovery).
    const onVisible = () => {
      if (document.visibilityState !== "visible") return;
      if (listAllPendingSubmissions().length > 0) run();
    };
    const onOnline = () => {
      if (listAllPendingSubmissions().length > 0) run();
    };
    document.addEventListener("visibilitychange", onVisible);
    window.addEventListener("online", onOnline);

    const interval = window.setInterval(() => {
      if (listAllPendingSubmissions().length > 0) run();
    }, 20_000);

    return () => {
      document.removeEventListener("visibilitychange", onVisible);
      window.removeEventListener("online", onOnline);
      window.clearInterval(interval);
    };
  }, [status, userId]);

  return null;
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider refetchInterval={5 * 60} refetchOnWindowFocus>
      <AccountAttemptSync />
      {children}
    </SessionProvider>
  );
}
