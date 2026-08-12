"use client";

import { useEffect, useRef } from "react";
import { SessionProvider, useSession } from "next-auth/react";
import {
  clearClaimableAttempts,
  clearPendingSubmission,
  listAllPendingSubmissions,
  listClaimableAttempts,
  saveClaimableAttempt,
} from "@/lib/attempt-cache";

async function syncAccountAttempts() {
  // 1) Bind guest completions that already landed in the DB.
  const claims = listClaimableAttempts();
  if (claims.length > 0) {
    try {
      const res = await fetch("/api/attempts/claim", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          claims: claims.map((c) => ({
            attemptId: c.attemptId,
            claimToken: c.claimToken,
          })),
        }),
      });
      if (res.ok) {
        const data = await res.json().catch(() => ({}));
        const claimed = Array.isArray(data.attemptIds) ? data.attemptIds : [];
        clearClaimableAttempts(claimed.length ? claimed : undefined);
      }
    } catch {
      /* non-fatal */
    }
  }

  // 2) Flush any pending submissions saved before / during auth loss.
  const pending = listAllPendingSubmissions();
  for (const p of pending) {
    try {
      const res = await fetch("/api/attempts/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          moduleId: p.moduleId,
          answers: p.answers,
          timeSpent: p.timeSpent,
        }),
      });
      const json = await res.json().catch(() => ({}));
      if (res.ok) {
        clearPendingSubmission(p.attemptId);
        if (typeof json.claimToken === "string" && json.attemptId) {
          saveClaimableAttempt(json.attemptId, json.claimToken);
        }
      }
    } catch {
      /* keep pending for next login */
    }
  }
}

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
    void syncAccountAttempts();
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
