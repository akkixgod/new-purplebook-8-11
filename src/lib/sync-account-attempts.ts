"use client";

import {
  clearClaimableAttempts,
  clearPendingSubmission,
  listAllPendingSubmissions,
  listClaimableAttempts,
  saveClaimableAttempt,
} from "@/lib/attempt-cache";

export type AccountSyncResult = {
  claimed: number;
  flushed: number;
};

/**
 * Bind guest completions + flush pending submits to the signed-in account.
 * Safe to call repeatedly; returns counts for UI/debug.
 */
export async function syncAccountAttempts(): Promise<AccountSyncResult> {
  let claimed = 0;
  let flushed = 0;

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
          bindToUser: true,
        }),
      });
      const json = (await res.json().catch(() => ({}))) as {
        attemptId?: string;
        id?: string;
        claimToken?: string;
        userId?: string | null;
        error?: string;
      };
      if (res.ok) {
        clearPendingSubmission(p.attemptId);
        flushed += 1;
        // Should be bound when authenticated; keep claim token only as fallback.
        if (typeof json.claimToken === "string" && (json.attemptId || json.id) && !json.userId) {
          saveClaimableAttempt(json.attemptId ?? json.id!, json.claimToken);
        }
      } else {
        console.warn("[syncAccountAttempts] flush pending failed", res.status, json.error);
      }
    } catch (error) {
      console.warn("[syncAccountAttempts] flush network error", error);
    }
  }

  // If flush created claimable rows while authenticated, claim them now.
  const leftover = listClaimableAttempts();
  if (leftover.length > 0) {
    try {
      const res = await fetch("/api/attempts/claim", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          claims: leftover.map((c) => ({
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
        claimed += typeof data.claimed === "number" ? data.claimed : 0;
        const ids = Array.isArray(data.attemptIds) ? data.attemptIds : [];
        clearClaimableAttempts(ids.length ? ids : undefined);
      }
    } catch {
      /* keep for next sync */
    }
  }

  return { claimed, flushed };
}
