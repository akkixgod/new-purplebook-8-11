"use client";

import { useEffect, useRef } from "react";
import { SessionProvider, useSession } from "next-auth/react";
import { syncAccountAttempts } from "@/lib/sync-account-attempts";

function AccountAttemptSync() {
  const { status } = useSession();
  const ranForSession = useRef(false);

  useEffect(() => {
    if (status !== "authenticated") {
      ranForSession.current = false;
      return;
    }
    if (ranForSession.current) return;
    ranForSession.current = true;
    void syncAccountAttempts().then((r) => {
      if (r.claimed || r.flushed) {
        console.info("[AccountAttemptSync]", r);
      }
    });
  }, [status]);

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
