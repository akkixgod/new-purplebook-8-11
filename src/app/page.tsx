"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/Header";
import { HeroPromoBanner } from "@/components/HeroPromoBanner";
import { TestCard } from "@/components/TestCard";
import { buildTestGroups, getTestGroup, sortTestsForDisplay } from "@/lib/test-groups";
import { syncAccountAttempts } from "@/lib/sync-account-attempts";

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

type Section = "MATH" | "ENGLISH";

function groupButtonClass(active: boolean, mobilePill: boolean) {
  if (mobilePill) {
    return active
      ? "whitespace-nowrap rounded-full bg-[#7c3aed] px-3.5 py-1.5 text-sm font-medium text-white"
      : "whitespace-nowrap rounded-full border border-gray-200 bg-white px-3.5 py-1.5 text-sm text-gray-600 hover:bg-gray-50";
  }
  return active
    ? "w-full text-left px-3 py-2 rounded-lg text-sm transition-colors bg-[#7c3aed]/10 text-[#7c3aed] font-medium"
    : "w-full text-left px-3 py-2 rounded-lg text-sm transition-colors text-gray-600 hover:bg-gray-100";
}

export default function HomePage() {
  const [section, setSection] = useState<Section>("MATH");
  const [tests, setTests] = useState<Test[]>([]);
  const [attemptMap, setAttemptMap] = useState<Record<string, AttemptInfo>>({});
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function fetchTests() {
    setLoading(true);
    try {
      await syncAccountAttempts();
    } catch {
      /* non-fatal — still load catalog */
    }
    const params = new URLSearchParams({ section });
    const res = await fetch(`/api/tests?${params}`, { credentials: "include" });
    const data = await res.json();
    setTests(data.tests ?? []);
    setAttemptMap(data.attemptMap ?? {});
    setSelectedGroup(null);
    setLoading(false);
  }

  useEffect(() => {
    fetchTests();
  }, [section]);

  const groupEntries = buildTestGroups(tests);

  const filteredTests = sortTestsForDisplay(
    selectedGroup ? tests.filter((t) => getTestGroup(t) === selectedGroup) : tests
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-7xl mx-auto px-4 pt-4">
        <HeroPromoBanner />
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
        <div className="flex flex-col gap-4 md:flex-row md:gap-6">
          {/* Mobile: horizontal scrollable group pills */}
          <aside className="md:hidden -mx-4 px-4">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
              Groups
            </p>
            <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
              <button
                type="button"
                onClick={() => setSelectedGroup(null)}
                className={groupButtonClass(!selectedGroup, true)}
              >
                All
              </button>
              {groupEntries.map((g) => (
                <button
                  key={g.key}
                  type="button"
                  onClick={() => setSelectedGroup(g.key)}
                  className={groupButtonClass(selectedGroup === g.key, true)}
                >
                  {g.label}
                  <span className="ml-1.5 text-xs opacity-70">{g.count}</span>
                </button>
              ))}
            </div>
          </aside>

          {/* Desktop: vertical group sidebar (unchanged) */}
          <aside className="hidden md:block w-44 flex-shrink-0">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
              Groups
            </p>
            <div className="space-y-1">
              <button
                type="button"
                onClick={() => setSelectedGroup(null)}
                className={groupButtonClass(!selectedGroup, false)}
              >
                All
              </button>
              {groupEntries.map((g) => (
                <button
                  key={g.key}
                  type="button"
                  onClick={() => setSelectedGroup(g.key)}
                  className={groupButtonClass(selectedGroup === g.key, false)}
                >
                  <span className="block truncate">{g.label}</span>
                  <span className="text-xs text-gray-400">
                    {g.count} {g.count === 1 ? "test" : "tests"}
                  </span>
                </button>
              ))}
            </div>
          </aside>

          {/* Test cards grid */}
          <main className="min-w-0 flex-1">
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-48 rounded-2xl bg-gray-100 animate-pulse" />
                ))}
              </div>
            ) : filteredTests.length === 0 ? (
              <div className="text-center py-20 text-gray-400">
                <svg
                  className="w-12 h-12 mx-auto mb-3 opacity-40"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <p className="text-sm">No tests available yet.</p>
                <p className="text-xs mt-1">
                  Check back soon or ask an admin to upload papers.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTests.map((test) => (
                  <TestCard key={test.id} {...test} attemptMap={attemptMap} />
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
