"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/Header";
import { syncAccountAttempts } from "@/lib/sync-account-attempts";

interface HistoryItem {
  id: string;
  testTitle: string;
  version: string | null;
  section: string;
  year: number;
  month: number;
  moduleNumber: number;
  finishedAt: string | null;
  correct: number;
  totalQuestions: number;
  percent: number;
}

const MONTHS = [
  "",
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

function formatDate(iso: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function AccountPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [attempts, setAttempts] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.replace("/auth/signin?callbackUrl=/account");
      return;
    }
    if (status !== "authenticated") return;

    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        // Claim guest / pending attempts before reading history so new scores appear immediately.
        await syncAccountAttempts();
        if (cancelled) return;

        const res = await fetch("/api/account/attempts", { credentials: "include" });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          if (!cancelled) setError(data.error ?? "Failed to load history");
          return;
        }
        if (!cancelled) setAttempts(Array.isArray(data.attempts) ? data.attempts : []);
      } catch {
        if (!cancelled) setError("Failed to load history");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [status, router]);

  async function deleteAttempt(id: string) {
    if (deletingId) return;
    const ok = window.confirm("Delete this practice attempt from your history?");
    if (!ok) return;
    setDeletingId(id);
    try {
      const res = await fetch(`/api/attempts/${id}`, {
        method: "DELETE",
        credentials: "include",
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.error ?? "Could not delete attempt");
        return;
      }
      setAttempts((prev) => prev.filter((a) => a.id !== id));
    } catch {
      setError("Could not delete attempt");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">My Account</h1>
          <p className="text-sm text-gray-500 mt-1">
            {session?.user?.email
              ? `Signed in as ${session.user.email}`
              : "Your completed practice history"}
          </p>
        </div>

        <section className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-900">Practice history</h2>
            <Link href="/" className="text-xs font-medium text-[#7c3aed] hover:underline">
              Back to tests
            </Link>
          </div>

          {loading || status === "loading" ? (
            <div className="p-10 flex justify-center">
              <div className="w-7 h-7 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
            </div>
          ) : error ? (
            <p className="p-5 text-sm text-red-600">{error}</p>
          ) : attempts.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-sm text-gray-600">No completed practice attempts yet.</p>
              <Link
                href="/"
                className="inline-block mt-3 text-sm font-medium text-[#7c3aed] hover:underline"
              >
                Start a practice test
              </Link>
            </div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {attempts.map((a) => (
                <li key={a.id} className="px-5 py-4 flex flex-col sm:flex-row sm:items-center gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold text-gray-900 truncate">
                      {a.testTitle}
                      {a.version ? (
                        <span className="font-normal text-gray-500"> · {a.version}</span>
                      ) : null}
                    </p>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {a.section} · Module {a.moduleNumber} · {MONTHS[a.month]} {a.year}
                    </p>
                    <p className="text-xs text-gray-500 mt-0.5">
                      Completed {formatDate(a.finishedAt)}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 flex-shrink-0">
                    <div className="text-right">
                      <p className="text-lg font-bold text-[#7c3aed] leading-none">
                        {a.percent}%
                      </p>
                      <p className="text-[11px] text-gray-400 mt-0.5">
                        {a.correct}/{a.totalQuestions} correct
                      </p>
                    </div>
                    <Link
                      href={`/review/${a.id}`}
                      className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-[#7c3aed] text-[#7c3aed] hover:bg-[#7c3aed] hover:text-white transition-colors"
                    >
                      Review
                    </Link>
                    <button
                      type="button"
                      onClick={() => deleteAttempt(a.id)}
                      disabled={deletingId === a.id}
                      className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-red-200 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
                    >
                      {deletingId === a.id ? "…" : "Delete"}
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}
