/** Session-scoped cache so results/review work after serverless submit on a fresh DB instance. */

export interface CachedAnswer {
  id?: string;
  questionId: string;
  selected: string | null;
  isCorrect: boolean;
}

export interface CachedQuestion {
  id: string;
  order: number;
  stimulus?: string | null;
  text: string;
  imageUrl: string | null;
  choices: string;
  correctAnswer: string;
  explanation?: string | null;
}

export interface CachedAttempt {
  id: string;
  score: number;
  totalQuestions: number;
  timeSpent: number | null;
  startedAt?: string;
  finishedAt?: string | null;
  module: {
    number: number;
    test: { title: string; section: string; year?: number; month?: number };
    questions: CachedQuestion[];
  };
  answers: CachedAnswer[];
}

const key = (attemptId: string) => `purplebook_attempt_cache_${attemptId}`;

export function cacheAttempt(data: CachedAttempt): void {
  try {
    sessionStorage.setItem(key(data.id), JSON.stringify(data));
  } catch {
    /* quota / private mode */
  }
}

export function readAttemptCache(attemptId: string): CachedAttempt | null {
  try {
    const raw = sessionStorage.getItem(key(attemptId));
    if (!raw) return null;
    return JSON.parse(raw) as CachedAttempt;
  } catch {
    return null;
  }
}

/** Durable per-browser index of completed modules (survives refresh; not a substitute for Turso). */
export type LocalHistoryEntry = {
  id: string;
  score: number;
  totalQuestions: number;
  moduleId: string;
  savedAt: number;
};

const historyKey = (userId: string) => `purplebook_local_history_v1_${userId}`;

export function rememberLocalAttempt(
  userId: string,
  entry: LocalHistoryEntry
): void {
  if (!userId || !entry.moduleId) return;
  try {
    const prev = readLocalHistory(userId);
    prev[entry.moduleId] = entry;
    localStorage.setItem(historyKey(userId), JSON.stringify(prev));
  } catch {
    /* quota / private mode */
  }
}

export function readLocalHistory(
  userId: string
): Record<string, LocalHistoryEntry> {
  if (!userId) return {};
  try {
    const raw = localStorage.getItem(historyKey(userId));
    if (!raw) return {};
    const parsed = JSON.parse(raw) as Record<string, LocalHistoryEntry>;
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

/**
 * With Turso, server attemptMap is the only source of REVIEW truth.
 * Keep local history only as a write-side cache; prune it to match the server.
 */
export function pruneLocalHistoryToServer(
  userId: string | null,
  serverMap: Record<string, { id: string; score: number; totalQuestions: number }>
): void {
  if (!userId) return;
  try {
    const next: Record<string, LocalHistoryEntry> = {};
    for (const [moduleId, server] of Object.entries(serverMap)) {
      next[moduleId] = {
        id: server.id,
        score: server.score,
        totalQuestions: server.totalQuestions,
        moduleId,
        savedAt: Date.now(),
      };
    }
    localStorage.setItem(historyKey(userId), JSON.stringify(next));
  } catch {
    /* quota / private mode */
  }
}

export function forgetLocalAttempt(
  userId: string | null,
  opts: { moduleId?: string; attemptId?: string }
): void {
  if (!userId) return;
  try {
    const prev = readLocalHistory(userId);
    let changed = false;
    for (const [moduleId, entry] of Object.entries(prev)) {
      if (
        (opts.moduleId && moduleId === opts.moduleId) ||
        (opts.attemptId && entry.id === opts.attemptId)
      ) {
        delete prev[moduleId];
        changed = true;
      }
    }
    if (changed) localStorage.setItem(historyKey(userId), JSON.stringify(prev));
  } catch {
    /* ignore */
  }
}

/** @deprecated Prefer server attemptMap only — kept for type compatibility during cleanup. */
export function mergeAttemptMapWithLocal(
  _userId: string | null,
  serverMap: Record<string, { id: string; score: number; totalQuestions: number }>
): Record<string, { id: string; score: number; totalQuestions: number }> {
  return serverMap;
}

export interface PendingSubmission {
  moduleId: string;
  attemptId: string;
  answers: { questionId: string; selected: string | null }[];
  timeSpent: number | null;
  savedAt: number;
}

const pendingKey = (attemptId: string) => `purplebook_pending_submit_${attemptId}`;

export function savePendingSubmission(data: PendingSubmission): void {
  try {
    localStorage.setItem(pendingKey(data.attemptId), JSON.stringify(data));
  } catch {
    /* quota / private mode */
  }
}

export function readPendingSubmission(attemptId: string): PendingSubmission | null {
  try {
    const raw = localStorage.getItem(pendingKey(attemptId));
    if (!raw) return null;
    return JSON.parse(raw) as PendingSubmission;
  } catch {
    return null;
  }
}

export function clearPendingSubmission(attemptId: string): void {
  try {
    localStorage.removeItem(pendingKey(attemptId));
  } catch {
    /* ignore */
  }
}

/** Guest / pre-login completed attempts waiting to be bound to an account. */
export interface ClaimableAttempt {
  attemptId: string;
  claimToken: string;
  savedAt: number;
}

const CLAIMABLE_KEY = "purplebook_claimable_attempts_v1";

export function listClaimableAttempts(): ClaimableAttempt[] {
  try {
    const raw = localStorage.getItem(CLAIMABLE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as ClaimableAttempt[];
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(
      (c) =>
        typeof c?.attemptId === "string" &&
        typeof c?.claimToken === "string" &&
        c.attemptId &&
        c.claimToken
    );
  } catch {
    return [];
  }
}

export function saveClaimableAttempt(attemptId: string, claimToken: string): void {
  try {
    const next = listClaimableAttempts().filter((c) => c.attemptId !== attemptId);
    next.push({ attemptId, claimToken, savedAt: Date.now() });
    localStorage.setItem(CLAIMABLE_KEY, JSON.stringify(next.slice(-40)));
  } catch {
    /* ignore */
  }
}

export function clearClaimableAttempts(attemptIds?: string[]): void {
  try {
    if (!attemptIds?.length) {
      localStorage.removeItem(CLAIMABLE_KEY);
      return;
    }
    const keep = listClaimableAttempts().filter((c) => !attemptIds.includes(c.attemptId));
    if (keep.length === 0) localStorage.removeItem(CLAIMABLE_KEY);
    else localStorage.setItem(CLAIMABLE_KEY, JSON.stringify(keep));
  } catch {
    /* ignore */
  }
}

export function listAllPendingSubmissions(): PendingSubmission[] {
  try {
    const out: PendingSubmission[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k?.startsWith("purplebook_pending_submit_")) continue;
      const raw = localStorage.getItem(k);
      if (!raw) continue;
      const parsed = JSON.parse(raw) as PendingSubmission;
      if (parsed?.moduleId && Array.isArray(parsed.answers)) out.push(parsed);
    }
    return out;
  } catch {
    return [];
  }
}

