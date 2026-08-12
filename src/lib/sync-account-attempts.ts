"use client";

import {
  clearClaimableAttempts,
  clearPendingSubmission,
  listAllPendingSubmissions,
  listClaimableAttempts,
} from "@/lib/attempt-cache";

export type AccountSyncResult = {
  claimed: number;
  flushed: number;
};

/**
 * Flush locally buffered failed submits + claim any legacy guest rows onto the signed-in account.
 * Practice history itself is always read from the database — never from localStorage.
 */
export async function syncAccountAttempts(): Promise<AccountSyncResult> {
  let claimed = 0;
  let flushed = 0;

  // Legacy guest completions (from older builds) still sitting in localStorage.
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
        const data = (await res.json().catch(() => ({}))) as {
          claimed?: number;
          attemptIds?: string[];
        };
        claimed = typeof data.claimed === "number" ? data.claimed : 0;
        const ids = Array.isArray(data.attemptIds) ? data.attemptIds : [];
        clearClaimableAttempts(ids.length ? ids : undefined);
      } else {
        console.warn("[syncAccountAttempts] claim failed", res.status);
      }
    } catch (error) {
      console.warn("[syncAccountAttempts] claim network error", error);
    }
  }

  // Retry submits that failed mid-flight (answers buffered locally until the DB write succeeds).
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
      const json = (await res.json().catch(() => ({}))) as {
        attemptId?: string;
        userId?: string | null;
        persisted?: boolean;
        error?: string;
      };
      if (res.ok && json.persisted && json.userId) {
        clearPendingSubmission(p.attemptId);
        flushed += 1;
      } else {
        console.warn("[syncAccountAttempts] flush pending failed", res.status, json.error);
      }
    } catch (error) {
      console.warn("[syncAccountAttempts] flush network error", error);
    }
  }

  return { claimed, flushed };
}
