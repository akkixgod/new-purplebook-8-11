"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type MouseEvent } from "react";

interface ModuleInfo {
  id: string;
  number: number;
  timeLimit: number;
  _count: { questions: number };
}

interface AttemptInfo {
  id: string;
  score: number;
  totalQuestions: number;
}

interface Props {
  id: string;
  title: string;
  year: number;
  month: number;
  section: string;
  version?: string | null;
  isFree: boolean;
  modules: ModuleInfo[];
  attemptMap: Record<string, AttemptInfo>;
}

const MONTH_NAMES = [
  "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

export function TestCard({ title, year, month, section, version, isFree, modules, attemptMap }: Props) {
  const router = useRouter();
  const [startingModuleId, setStartingModuleId] = useState<string | null>(null);

  function startPractice(e: MouseEvent<HTMLButtonElement>, moduleId: string) {
    e.preventDefault();
    e.stopPropagation();
    if (startingModuleId) return;
    setStartingModuleId(moduleId);
    const attemptId = crypto.randomUUID();
    // Keep spinner until navigation unmounts the card — do not clear immediately.
    // Submitting requires sign-in so the Attempt row is bound to the account in the database.
    router.push(`/test/${moduleId}?attemptId=${attemptId}`);
  }

  const totalQuestions = modules.reduce((s, m) => s + m._count.questions, 0);
  const totalMinutes = Math.round(modules.reduce((s, m) => s + m.timeLimit, 0) / 60);
  const isStarting = startingModuleId !== null;

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 hover:border-[#7c3aed]/40 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2 min-w-0">
          <svg className="w-4 h-4 text-[#7c3aed] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <div className="min-w-0">
            <span className="font-semibold text-sm text-gray-900 block truncate">{title}</span>
            {version && (
              <span className="text-xs text-gray-500 block truncate">{version}</span>
            )}
          </div>
        </div>
        {isFree && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-600 font-medium flex-shrink-0">
            Free
          </span>
        )}
      </div>

      {/* Meta */}
      <div className="flex items-center gap-3 text-xs text-gray-500 mb-4">
        <span className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {totalMinutes} min
        </span>
        <span className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          {totalQuestions} questions
        </span>
        <span className="text-[#7c3aed] font-medium">
          {MONTH_NAMES[month]} {year}
        </span>
      </div>

      {/* Modules */}
      <div className="space-y-2">
        {modules.map((mod) => {
          const attempt = attemptMap[mod.id];
          const isDone = !!attempt;
          const thisStarting = startingModuleId === mod.id;

          return (
            <div
              key={mod.id}
              className="flex items-center justify-between py-2 border-t border-gray-100"
            >
              <div>
                <p className="text-sm font-medium text-gray-900">Module {mod.number}</p>
                {isDone && (
                  <p className="text-xs text-gray-500">
                    Score: {attempt.score}/{attempt.totalQuestions}
                  </p>
                )}
              </div>

              {isDone ? (
                <div className="flex items-center gap-2">
                  <Link
                    href={`/review/${attempt.id}`}
                    className="px-4 py-1.5 text-xs font-semibold rounded-lg border-2 border-[#7c3aed] text-[#7c3aed] hover:bg-[#7c3aed] hover:text-white transition-colors"
                  >
                    REVIEW
                  </Link>
                  <button
                    type="button"
                    onClick={(e) => startPractice(e, mod.id)}
                    disabled={isStarting || mod._count.questions === 0}
                    className="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors disabled:opacity-50"
                    title="Retake"
                  >
                    {thisStarting ? (
                      <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
                        <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
                      </svg>
                    ) : (
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    )}
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={(e) => startPractice(e, mod.id)}
                  disabled={isStarting || mod._count.questions === 0}
                  aria-busy={thisStarting}
                  className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {mod._count.questions === 0 ? (
                    "COMING SOON"
                  ) : thisStarting ? (
                    <span className="inline-flex items-center gap-2">
                      <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
                        <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
                      </svg>
                      Starting Test...
                    </span>
                  ) : (
                    "START PRACTICE"
                  )}
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
