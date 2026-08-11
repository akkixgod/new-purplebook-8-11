"use client";

import { useEffect, useState, use } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { readAttemptCache } from "@/lib/attempt-cache";
import { scaleSectionScore } from "@/lib/sat-scale";

interface AttemptData {
  id: string;
  score: number | null;
  totalQuestions: number | null;
  timeSpent: number | null;
  module?: {
    number: number;
    test?: { title: string; section: string };
  } | null;
  error?: string;
}

async function loadAttempt(attemptId: string): Promise<AttemptData> {
  const cached = readAttemptCache(attemptId);
  if (cached?.module?.test) {
    return cached;
  }

  const r = await fetch(`/api/attempts/${attemptId}`, { credentials: "include" });
  const json = (await r.json()) as AttemptData;
  if (!r.ok) {
    const cachedAfterFail = readAttemptCache(attemptId);
    if (cachedAfterFail?.module?.test) return cachedAfterFail;
    throw new Error(json.error || `Failed to load results (${r.status})`);
  }
  if (!json.module?.test) {
    throw new Error("Incomplete attempt data (missing module/test).");
  }
  return json;
}

function ModuleBreakdown({
  label,
  correct,
  total,
}: {
  label: string;
  correct: number;
  total: number;
}) {
  const incorrect = Math.max(0, total - correct);
  return (
    <div className="rounded-xl border border-gray-100 bg-gray-50 px-4 py-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-gray-500">{label}</div>
      <div className="mt-2 flex justify-between text-sm">
        <span className="text-emerald-700 font-medium">{correct} correct</span>
        <span className="text-red-600 font-medium">{incorrect} incorrect</span>
        <span className="text-gray-500">{total} total</span>
      </div>
    </div>
  );
}

export default function ResultsPage({ params }: { params: Promise<{ moduleId: string }> }) {
  const { moduleId } = use(params);
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("attemptId") ?? "";
  const prevAttemptId = searchParams.get("prevAttemptId") ?? "";
  const combined = searchParams.get("combined") === "1";
  const solo = searchParams.get("solo") === "1";

  const [primary, setPrimary] = useState<AttemptData | null>(null);
  const [previous, setPrevious] = useState<AttemptData | null>(null);
  const [loadError, setLoadError] = useState<string | null>(() =>
    attemptId ? null : "Missing attempt id. Return home and retake the module."
  );

  useEffect(() => {
    if (!attemptId) return;

    let cancelled = false;
    let didRetry = false;

    const load = async () => {
      try {
        const main = await loadAttempt(attemptId);
        if (cancelled) return;
        setPrimary(main);

        if (combined && prevAttemptId) {
          try {
            const prev = await loadAttempt(prevAttemptId);
            if (!cancelled) setPrevious(prev);
          } catch {
            if (!cancelled) setPrevious(null);
          }
        }
      } catch (error: unknown) {
        const message = error instanceof Error ? error.message : "Failed to load results.";
        if (message.includes("404") && !didRetry) {
          didRetry = true;
          await new Promise((res) => setTimeout(res, 350));
          return load();
        }
        console.error("Results page error:", error);
        if (!cancelled) setLoadError(message);
      }
    };

    void load();
    return () => {
      cancelled = true;
    };
  }, [attemptId, prevAttemptId, combined]);

  if (loadError) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-12">
        <div className="w-full max-w-md text-center">
          <h1 className="text-xl font-bold text-gray-900 mb-2">Couldn’t load results</h1>
          <p className="text-sm text-gray-500 mb-6">{loadError}</p>
          <div className="flex gap-3 justify-center">
            <Link
              href={`/test/${moduleId}${attemptId ? `?attemptId=${attemptId}` : ""}`}
              className="px-4 py-2.5 text-sm font-semibold rounded-xl border border-gray-200 text-gray-800 hover:bg-gray-50"
            >
              Back to module
            </Link>
            <Link
              href="/"
              className="px-4 py-2.5 text-sm font-semibold rounded-xl bg-[#7c3aed] text-white hover:bg-[#6d28d9]"
            >
              Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!primary) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const isCombined = combined && previous;
  const m1 = isCombined
    ? previous
    : primary.module?.number === 1
      ? primary
      : null;
  const m2 = isCombined ? primary : null;

  const m1Correct = m1?.score ?? 0;
  const m1Total = m1?.totalQuestions ?? 0;
  const m2Correct = m2?.score ?? 0;
  const m2Total = m2?.totalQuestions ?? 0;

  const correct = isCombined ? m1Correct + m2Correct : (primary.score ?? 0);
  const total = isCombined ? m1Total + m2Total : (primary.totalQuestions ?? 0);
  const incorrect = Math.max(0, total - correct);
  const scaled = scaleSectionScore(correct, total);
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;

  const timeSpent = isCombined
    ? (m1?.timeSpent ?? 0) + (m2?.timeSpent ?? 0)
    : primary.timeSpent;
  const mins = timeSpent != null ? Math.floor(timeSpent / 60) : null;
  const secs =
    timeSpent != null ? (timeSpent % 60).toString().padStart(2, "0") : null;

  const title = primary.module?.test?.title ?? "Practice module";
  const section = primary.module?.test?.section === "MATH" ? "Math" : "Reading and Writing";
  const moduleNumber = primary.module?.number ?? 1;

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">{pct >= 80 ? "🎉" : pct >= 60 ? "👍" : "📚"}</div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isCombined
              ? "Section Complete!"
              : solo || moduleNumber === 1
                ? "Module 1 Complete!"
                : "Module Complete!"}
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            {title}
            {isCombined ? ` — Full ${section}` : ` — Module ${moduleNumber}`}
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
          <div className="text-center mb-6">
            <div className="text-5xl font-bold text-[#7c3aed]">{scaled}</div>
            <div className="text-xs text-gray-500 mt-1 uppercase tracking-wide">
              Scaled {section} score (200–800)
            </div>
          </div>

          <div className="flex justify-around mb-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{correct}</div>
              <div className="text-xs text-gray-500 mt-1">Correct</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{total}</div>
              <div className="text-xs text-gray-500 mt-1">Total</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-2xl font-bold text-red-500">{incorrect}</div>
              <div className="text-xs text-gray-500 mt-1">Incorrect</div>
            </div>
          </div>

          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#7c3aed] rounded-full transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
          <p className="text-center text-sm font-semibold text-[#7c3aed] mt-2">{pct}%</p>

          {mins !== null && (
            <p className="text-center text-xs text-gray-500 mt-2">
              Time: {mins}:{secs}
            </p>
          )}
        </div>

        {isCombined && (
          <div className="space-y-2 mb-4">
            <ModuleBreakdown label="Module 1" correct={m1Correct} total={m1Total} />
            <ModuleBreakdown label="Module 2" correct={m2Correct} total={m2Total} />
          </div>
        )}

        {!isCombined && (solo || moduleNumber === 1) && (
          <div className="mb-4">
            <ModuleBreakdown label="Module 1" correct={correct} total={total} />
          </div>
        )}

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

        {isCombined && prevAttemptId && (
          <Link
            href={`/review/${prevAttemptId}`}
            className="mt-3 block w-full py-3 text-sm font-semibold rounded-xl border border-gray-200 text-gray-800 text-center hover:bg-gray-50"
          >
            Review Module 1 Answers
          </Link>
        )}
      </div>
    </div>
  );
}
