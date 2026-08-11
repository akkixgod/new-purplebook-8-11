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
