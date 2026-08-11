"use client";

import { useEffect } from "react";

type QuestionItem = {
  id: string;
  order: number;
};

type Props = {
  open: boolean;
  onClose: () => void;
  onConfirmSubmit: () => void;
  submitting: boolean;
  moduleNumber: number;
  questions: QuestionItem[];
  answers: Record<string, string | null>;
  markedForReview: Set<string>;
  onNavigate: (index: number) => void;
};

function isAnswered(value: string | null | undefined): boolean {
  return value != null && String(value).trim() !== "";
}

export function ModuleReviewModal({
  open,
  onClose,
  onConfirmSubmit,
  submitting,
  moduleNumber,
  questions,
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

  const unanswered = questions
    .map((q, i) => ({ q, i }))
    .filter(({ q }) => !isAnswered(answers[q.id]));
  const flagged = questions
    .map((q, i) => ({ q, i }))
    .filter(({ q }) => markedForReview.has(q.id));
  const answeredCount = questions.length - unanswered.length;

  const jumpTo = (index: number) => {
    onNavigate(index);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-[110] flex items-end justify-center bg-black/50 p-4 sm:items-center"
      role="presentation"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="module-review-title"
        className="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="border-b border-gray-100 px-5 py-4">
          <h2 id="module-review-title" className="text-lg font-bold text-gray-900">
            Check Your Work — Module {moduleNumber}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Review flagged and unanswered questions before you submit.
          </p>
          <div className="mt-3 flex flex-wrap gap-3 text-xs text-gray-600">
            <span>
              <span className="font-semibold text-gray-900">{answeredCount}</span> answered
            </span>
            <span>
              <span className="font-semibold text-gray-900">{unanswered.length}</span> unanswered
            </span>
            <span className="inline-flex items-center gap-1">
              <svg className="h-3.5 w-3.5 text-orange-500" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              <span className="font-semibold text-orange-600">{flagged.length}</span> flagged
            </span>
          </div>
        </div>

        <div className="space-y-5 px-5 py-4">
          <section aria-label="Flagged for review">
            <h3 className="mb-2 flex items-center gap-1.5 text-sm font-semibold text-gray-900">
              <svg className="h-4 w-4 text-orange-500" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              Flagged for review
            </h3>
            {flagged.length === 0 ? (
              <p className="text-sm text-gray-500">No questions flagged.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {flagged.map(({ q, i }) => (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => jumpTo(i)}
                    className="relative inline-flex h-9 min-w-9 items-center justify-center rounded-lg border border-orange-200 bg-orange-50 px-2.5 text-sm font-semibold text-orange-800 hover:bg-orange-100"
                    aria-label={`Go to flagged question ${q.order || i + 1}`}
                  >
                    {q.order || i + 1}
                    <span className="absolute -right-1 -top-1" aria-hidden>
                      <svg className="h-3 w-3 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                      </svg>
                    </span>
                  </button>
                ))}
              </div>
            )}
          </section>

          <section aria-label="Unanswered questions">
            <h3 className="mb-2 text-sm font-semibold text-gray-900">Unanswered</h3>
            {unanswered.length === 0 ? (
              <p className="text-sm text-gray-500">All questions have an answer.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {unanswered.map(({ q, i }) => (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => jumpTo(i)}
                    className="inline-flex h-9 min-w-9 items-center justify-center rounded-lg border border-gray-300 bg-white px-2.5 text-sm font-semibold text-gray-700 hover:bg-gray-50"
                    aria-label={`Go to unanswered question ${q.order || i + 1}`}
                  >
                    {q.order || i + 1}
                  </button>
                ))}
              </div>
            )}
          </section>
        </div>

        <div className="flex flex-col-reverse gap-2 border-t border-gray-100 px-5 py-4 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-gray-200 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Back to questions
          </button>
          <button
            type="button"
            onClick={onConfirmSubmit}
            disabled={submitting}
            className="rounded-lg bg-green-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-green-700 disabled:opacity-60"
          >
            {submitting ? "Submitting…" : "Submit module"}
          </button>
        </div>
      </div>
    </div>
  );
}
