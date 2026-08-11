"use client";

import { useEffect, useState, use } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useSession } from "next-auth/react";
import {
  TelegramCommunityCheckModal,
  isTelegramJoinedThisSession,
} from "@/components/TelegramCommunityCheckModal";

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

export default function ResultsPage({ params }: { params: Promise<{ moduleId: string }> }) {
  const { moduleId } = use(params);
  const router = useRouter();
  const { data: session } = useSession();
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("attemptId") ?? "";
  const [data, setData] = useState<AttemptData | null>(null);
  const [nextModuleId, setNextModuleId] = useState<string | null>(null);
  const [showTelegramModal, setShowTelegramModal] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(() =>
    attemptId ? null : "Missing attempt id. Return home and retake the module."
  );

  useEffect(() => {
    if (!attemptId) {
      return;
    }

    let cancelled = false;
    let didRetry = false;

    const load = async () => {
      try {
        const r = await fetch(`/api/attempts/${attemptId}`, { credentials: "include" });
        const json = (await r.json()) as AttemptData;
        if (!r.ok) {
          // Very small chance the submit transaction hasn't become visible yet.
          if (r.status === 404 && !didRetry) {
            didRetry = true;
            await new Promise((res) => setTimeout(res, 350));
            return load();
          }
          throw new Error(json.error || `Failed to load results (${r.status})`);
        }
        if (!json.module?.test) {
          throw new Error("Incomplete attempt data (missing module/test).");
        }
        if (!cancelled) setData(json);
      } catch (error: unknown) {
        console.error("Results page error:", error);
        if (!cancelled) {
          setLoadError(error instanceof Error ? error.message : "Failed to load results.");
        }
      }
    };

    void load();

    return () => {
      cancelled = true;
    };
  }, [attemptId]);

  useEffect(() => {
    let cancelled = false;
    const loadNext = async () => {
      try {
        const r = await fetch(`/api/modules/${moduleId}/next-module`, { credentials: "include" });
        const json = (await r.json()) as { nextModuleId: string | null };
        if (!cancelled) setNextModuleId(json.nextModuleId ?? null);
      } catch {
        if (!cancelled) setNextModuleId(null);
      }
    };
    void loadNext();
    return () => {
      cancelled = true;
    };
  }, [moduleId]);

  const startNextModule = async () => {
    if (!nextModuleId) return;
    if (!session) {
      router.push("/auth/signin");
      return;
    }

    const res = await fetch("/api/attempts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ moduleId: nextModuleId }),
    });

    if (!res.ok) return;
    const attempt = (await res.json()) as { id: string };
    router.push(`/test/${nextModuleId}?attemptId=${attempt.id}`);
  };

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

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const score = data.score ?? 0;
  const totalQuestions = data.totalQuestions ?? 0;
  const pct = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
  const incorrect = Math.max(0, totalQuestions - score);
  const mins = data.timeSpent != null ? Math.floor(data.timeSpent / 60) : null;
  const secs =
    data.timeSpent != null ? (data.timeSpent % 60).toString().padStart(2, "0") : null;
  const title = data.module?.test?.title ?? "Practice module";
  const moduleNumber = data.module?.number ?? 1;

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">{pct >= 80 ? "🎉" : pct >= 60 ? "👍" : "📚"}</div>
          <h1 className="text-2xl font-bold text-gray-900">Module Complete!</h1>
          <p className="text-gray-500 text-sm mt-1">
            {title} — Module {moduleNumber}
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-4">
          <div className="flex justify-around mb-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-[#7c3aed]">{score}</div>
              <div className="text-xs text-gray-500 mt-1">Correct</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900">{totalQuestions}</div>
              <div className="text-xs text-gray-500 mt-1">Total</div>
            </div>
            <div className="w-px bg-gray-200" />
            <div className="text-center">
              <div className="text-4xl font-bold text-red-500">{incorrect}</div>
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

        {nextModuleId && (
          <button
            type="button"
            onClick={() => {
              if (isTelegramJoinedThisSession()) {
                void startNextModule();
                return;
              }
              setShowTelegramModal(true);
            }}
            className="mt-4 w-full py-3 text-sm font-semibold rounded-xl bg-[#7c3aed] hover:bg-[#6d28d9] text-white transition-colors"
          >
            Next Module
          </button>
        )}
      </div>

      <TelegramCommunityCheckModal
        open={showTelegramModal}
        mode="inter-module"
        onClose={() => setShowTelegramModal(false)}
        onJoin={() => {
          setShowTelegramModal(false);
          void startNextModule();
        }}
        onAlreadyJoined={() => {
          setShowTelegramModal(false);
          void startNextModule();
        }}
      />
    </div>
  );
}
