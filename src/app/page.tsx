"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/Header";
import { TestCard } from "@/components/TestCard";

interface ModuleInfo {
  id: string;
  number: number;
  timeLimit: number;
  _count: { questions: number };
}

interface Test {
  id: string;
  title: string;
  year: number;
  month: number;
  section: string;
  version: string | null;
  isFree: boolean;
  modules: ModuleInfo[];
}

interface AttemptInfo {
  id: string;
  score: number;
  totalQuestions: number;
}

const MONTH_NAMES = [
  "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

type Section = "MATH" | "ENGLISH";

interface DateEntry {
  year: number;
  month: number;
  label: string;
}

export default function HomePage() {
  const [section, setSection] = useState<Section>("MATH");
  const [tests, setTests] = useState<Test[]>([]);
  const [attemptMap, setAttemptMap] = useState<Record<string, AttemptInfo>>({});
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function fetchTests() {
    setLoading(true);
    const params = new URLSearchParams({ section });
    const res = await fetch(`/api/tests?${params}`);
    const data = await res.json();
    setTests(data.tests ?? []);
    setAttemptMap(data.attemptMap ?? {});
    setSelectedDate(null);
    setLoading(false);
  }

  useEffect(() => { fetchTests(); }, [section]);

  // Build unique dates from tests
  const dateEntries: DateEntry[] = Array.from(
    new Map(
      tests.map((t) => [`${t.year}-${t.month}`, { year: t.year, month: t.month, label: `${String(t.month).padStart(2, "0")}.${String(t.year).slice(2)}` }])
    ).values()
  );

  const filteredTests = selectedDate
    ? tests.filter((t) => `${t.year}-${t.month}` === selectedDate)
    : tests;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      {/* Hero */}
      <div className="max-w-7xl mx-auto px-4 pt-10 pb-6 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">PurpleBook.cc</h1>
        <p className="text-gray-500 text-base max-w-md mx-auto leading-relaxed">
          Free SAT past papers with timed modules, instant scoring, and detailed answer review.
        </p>
        <a
          href="https://t.me/purplebook_cc"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-4 px-6 py-2 rounded-lg border-2 border-[#7c3aed] text-[#7c3aed] font-medium text-sm hover:bg-[#7c3aed] hover:text-white transition-colors"
        >
          Join Community
        </a>
      </div>

      {/* Section tabs */}
      <div className="max-w-7xl mx-auto px-4 mb-6">
        <div className="flex items-center justify-center gap-8 border-b border-gray-200">
          {(["MATH", "ENGLISH"] as Section[]).map((s) => (
            <button
              key={s}
              onClick={() => setSection(s)}
              className={`pb-3 text-sm font-medium capitalize border-b-2 transition-colors ${
                section === s
                  ? "border-[#7c3aed] text-[#7c3aed]"
                  : "border-transparent text-gray-500 hover:text-gray-900"
              }`}
            >
              {s.toLowerCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Content area */}
      <div className="max-w-7xl mx-auto px-4 pb-12">
        <div className="flex gap-6">
          {/* Date Sidebar */}
          <aside className="w-36 flex-shrink-0">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Dates</p>
            <div className="space-y-1">
              <button
                onClick={() => setSelectedDate(null)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                  !selectedDate
                    ? "bg-[#7c3aed]/10 text-[#7c3aed] font-medium"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                All
              </button>
              {dateEntries.map((d) => {
                const key = `${d.year}-${d.month}`;
                return (
                  <button
                    key={key}
                    onClick={() => setSelectedDate(key)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                      selectedDate === key
                        ? "bg-[#7c3aed]/10 text-[#7c3aed] font-medium"
                        : "text-gray-600 hover:bg-gray-100"
                    }`}
                  >
                    {d.label}
                  </button>
                );
              })}
            </div>
          </aside>

          {/* Test cards grid */}
          <main className="flex-1">
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-48 rounded-2xl bg-gray-100 animate-pulse" />
                ))}
              </div>
            ) : filteredTests.length === 0 ? (
              <div className="text-center py-20 text-gray-400">
                <svg className="w-12 h-12 mx-auto mb-3 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-sm">No tests available yet.</p>
                <p className="text-xs mt-1">Check back soon or ask an admin to upload papers.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTests.map((test) => (
                  <TestCard
                    key={test.id}
                    {...test}
                    attemptMap={attemptMap}
                  />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
