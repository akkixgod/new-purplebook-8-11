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

/** Server attemptMap wins; local fills modules the server forgot (ephemeral isolate miss). */
export function mergeAttemptMapWithLocal(
  userId: string | null,
  serverMap: Record<string, { id: string; score: number; totalQuestions: number }>
): Record<string, { id: string; score: number; totalQuestions: number }> {
  if (!userId) return serverMap;
  const local = readLocalHistory(userId);
  const out = { ...serverMap };
  for (const [moduleId, entry] of Object.entries(local)) {
    if (!out[moduleId] && entry?.id) {
      out[moduleId] = {
        id: entry.id,
        score: entry.score,
        totalQuestions: entry.totalQuestions,
      };
    }
  }
  return out;
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

