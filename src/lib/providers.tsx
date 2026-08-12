"use client";

import { useEffect, useRef } from "react";
import { SessionProvider, useSession } from "next-auth/react";
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
    if (ranForUser.current === userId) return;
    ranForUser.current = userId;
    void syncAccountAttempts().then((r) => {
      if (r.claimed || r.flushed) {
        console.info("[AccountAttemptSync]", r);
      }
    });
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
