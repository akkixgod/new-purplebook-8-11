"use client";

import { useEffect, useState, use } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";

interface AttemptData {
  id: string;
  score: number;
  totalQuestions: number;
  timeSpent: number | null;
  module: {
    number: number;
    test: { title: string; section: string };
  };
}

export default function ResultsPage({ params }: { params: Promise<{ moduleId: string }> }) {
  use(params); // consume params (not needed directly)
  const searchParams = useSearchParams();
  const router = useRouter();
  const attemptId = searchParams.get("attemptId") ?? "";
  const [data, setData] = useState<AttemptData | null>(null);

  useEffect(() => {
    if (!attemptId) return;
    fetch(`/api/attempts/${attemptId}`)
      .then((r) => r.json())
      .then(setData);
  }, [attemptId]);

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const pct = data.totalQuestions > 0 ? Math.round((data.score / data.totalQuestions) * 100) : 0;
  const incorrect = data.totalQuestions - data.score;
  const mins = data.timeSpent ? Math.floor(data.timeSpent / 60) : null;
  const secs = data.timeSpent ? (data.timeSpent % 60).toString().padStart(2, "0") : null;

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Celebration header */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">{pct >= 80 ? "🎉" : pct >= 60 ? "👍" : "📚"}</div>
          <h1 className="text-2xl font-bold text-gray-900">Module Complete!</h1>
          <p className="text-gray-500 text-sm mt-1">
            {data.module.test.title} — Module {data.module.number}
          </p>
        </div>

        {/* Score card */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
          {/* Big score */}
          <div className="flex justify-around mb-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-[#7c3aed]">{data.score}</div>
              <div className="text-xs text-gray-500 mt-1">Correct</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900">{data.totalQuestions}</div>
              <div className="text-xs text-gray-500 mt-1">Total</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-4xl font-bold text-red-500">{incorrect}</div>
              <div className="text-xs text-gray-500 mt-1">Incorrect</div>
            </div>
          </div>

          {/* Progress bar */}
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#7c3aed] rounded-full transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
          <p className="text-center text-sm font-semibold text-[#7c3aed] mt-2">{pct}%</p>

          {mins !== null && (
            <p className="text-center text-xs text-gray-500 mt-2">Time: {mins}:{secs}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <Link
            href={`/review/${attemptId}`}
            className="flex-1 py-3 text-sm font-semibold rounded-xl bg-[#7c3aed] hover:bg-[#6d28d9] text-white text-center transition-colors"
          >
            Review Answers
          </Link>
          <Link
            href="/"
            className="flex-1 py-3 text-sm font-semibold rounded-xl border-2 border-gray-200 text-gray-900 text-center hover:bg-gray-50 transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
