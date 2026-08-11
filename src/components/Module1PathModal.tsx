"use client";

import { useEffect } from "react";

type Props = {
  open: boolean;
  submitting: boolean;
  onFinishTest: () => void;
  onContinueModule2: () => void;
  onBack: () => void;
};

export function Module1PathModal({
  open,
  submitting,
  onFinishTest,
  onContinueModule2,
  onBack,
}: Props) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !submitting) {
        e.preventDefault();
        onBack();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, submitting, onBack]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[120] flex items-end justify-center bg-black/50 p-4 sm:items-center"
      role="presentation"
      onClick={() => {
        if (!submitting) onBack();
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="module1-path-title"
        className="w-full max-w-lg rounded-2xl bg-white shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="border-b border-gray-100 px-5 py-4">
          <h2 id="module1-path-title" className="text-lg font-bold text-gray-900">
            Module 1 submitted
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Finish now for your Module 1 score, or continue straight into Module 2.
          </p>
        </div>

        <div className="space-y-3 px-5 py-5">
          <button
            type="button"
            disabled={submitting}
            onClick={onFinishTest}
            className="w-full rounded-xl border border-gray-200 bg-white px-4 py-3.5 text-left hover:border-[#7c3aed]/50 hover:bg-violet-50/40 disabled:opacity-60 transition-colors"
          >
            <div className="text-sm font-semibold text-gray-900">Finish Test (Get Module 1 Score)</div>
            <div className="mt-0.5 text-xs text-gray-500">
              See a scaled Reading/Writing or Math score (200–800) for Module 1 only.
            </div>
          </button>

          <button
            type="button"
            disabled={submitting}
            onClick={onContinueModule2}
            className="w-full rounded-xl bg-[#7c3aed] px-4 py-3.5 text-left text-white hover:bg-[#6d28d9] disabled:opacity-60 transition-colors"
          >
            <div className="text-sm font-semibold">Move to Module 2</div>
            <div className="mt-0.5 text-xs text-violet-100">
              Continue immediately — no ads or community prompts.
            </div>
          </button>
        </div>

        <div className="border-t border-gray-100 px-5 py-3">
          <button
            type="button"
            disabled={submitting}
            onClick={onBack}
            className="text-sm font-medium text-gray-500 hover:text-gray-800 disabled:opacity-60"
          >
            Back
          </button>
        </div>
      </div>
    </div>
  );
}
