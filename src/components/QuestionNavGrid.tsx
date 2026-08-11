"use client";

import { useEffect } from "react";

type QuestionNavItem = {
  id: string;
  order: number;
};

type Props = {
  open: boolean;
  onClose: () => void;
  moduleNumber: number;
  questions: QuestionNavItem[];
  currentIndex: number;
  answers: Record<string, string | null>;
  markedForReview: Set<string>;
  onNavigate: (index: number) => void;
};

function isAnswered(value: string | null | undefined): boolean {
  return value != null && String(value).trim() !== "";
}

export function QuestionNavGrid({
  open,
  onClose,
  moduleNumber,
  questions,
  currentIndex,
  answers,
  markedForReview,
  onNavigate,
}: Props) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  const answeredCount = questions.filter((q) => isAnswered(answers[q.id])).length;
  const flaggedCount = questions.filter((q) => markedForReview.has(q.id)).length;
  const unansweredCount = questions.length - answeredCount;

  return (
    <div
      className="fixed inset-0 z-[90]"
      role="presentation"
      onClick={onClose}
    >
      {/* Dim backdrop above content, leave bottom bar readable */}
      <div className="absolute inset-0 bottom-14 bg-black/25" aria-hidden />

      <div
        role="dialog"
        aria-modal="true"
        aria-label={`Module ${moduleNumber} question menu`}
        className="absolute bottom-14 left-1/2 z-[91] w-[min(420px,calc(100vw-1.5rem))] -translate-x-1/2 rounded-xl border border-gray-200 bg-white shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3 border-b border-gray-100 px-4 py-3">
          <div>
            <h2 className="text-sm font-bold text-gray-900">
              Module {moduleNumber} Review
            </h2>
            <p className="mt-1 text-xs text-gray-500">
              <span className="font-medium text-gray-700">{answeredCount}</span> answered
              <span className="mx-1.5 text-gray-300">·</span>
              <span className="font-medium text-gray-700">{unansweredCount}</span> unanswered
              <span className="mx-1.5 text-gray-300">·</span>
              <span className="font-medium text-orange-600">{flaggedCount}</span> flagged
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-2.5 py-1 text-xs font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900"
            aria-label="Close question menu"
          >
            Close
          </button>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-x-4 gap-y-1.5 border-b border-gray-100 px-4 py-2 text-[11px] text-gray-500">
          <span className="inline-flex items-center gap-1.5">
            <span className="h-3.5 w-3.5 rounded border-2 border-[#7c3aed] bg-white" />
            Current
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-3.5 w-3.5 rounded bg-[#7c3aed]" />
            Answered
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-3.5 w-3.5 rounded border border-gray-300 bg-white" />
            Unanswered
          </span>
          <span className="inline-flex items-center gap-1.5">
            <svg className="h-3 w-3 text-orange-500" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            Flagged
          </span>
        </div>

        <div
          className="grid max-h-[min(50vh,320px)] grid-cols-6 gap-2 overflow-y-auto p-4 sm:grid-cols-7"
          role="listbox"
          aria-label={`Questions in module ${moduleNumber}`}
        >
          {questions.map((qq, i) => {
            const answered = isAnswered(answers[qq.id]);
            const flagged = markedForReview.has(qq.id);
            const isCurrent = i === currentIndex;
            const label = qq.order || i + 1;

            return (
              <button
                key={qq.id}
                type="button"
                role="option"
                aria-selected={isCurrent}
                aria-label={`Question ${label}${answered ? ", answered" : ", unanswered"}${flagged ? ", flagged for review" : ""}${isCurrent ? ", current" : ""}`}
                onClick={() => {
                  onNavigate(i);
                  onClose();
                }}
                className={`relative flex h-10 w-full items-center justify-center rounded-lg text-sm font-semibold transition-colors ${
                  isCurrent
                    ? answered
                      ? "bg-[#7c3aed] text-white ring-2 ring-[#7c3aed] ring-offset-2"
                      : "border-2 border-[#7c3aed] bg-white text-[#7c3aed] ring-2 ring-[#7c3aed]/30"
                    : answered
                    ? "bg-[#7c3aed] text-white hover:bg-[#6d28d9]"
                    : "border border-gray-300 bg-white text-gray-700 hover:border-gray-400 hover:bg-gray-50"
                }`}
              >
                {label}
                {flagged && (
                  <span
                    className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-white shadow-sm"
                    aria-hidden
                  >
                    <svg className="h-3 w-3 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
