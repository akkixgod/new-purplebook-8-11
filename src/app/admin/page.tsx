"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";

interface ParsedQuestion {
  order: number;
  text: string;
  choices: Record<string, string>;
  correctAnswer: string;
}

interface TestModule {
  id: string;
  number: number;
  _count: { questions: number };
}

interface Test {
  id: string;
  title: string;
  year: number;
  month: number;
  section: string;
  modules: TestModule[];
}

const MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];

export default function AdminPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  const [tests, setTests] = useState<Test[]>([]);
  const [tab, setTab] = useState<"tests" | "upload">("tests");

  // New test form
  const [title, setTitle] = useState("");
  const [year, setYear] = useState(new Date().getFullYear().toString());
  const [month, setMonth] = useState("1");
  const [section, setSection] = useState("MATH");
  const [version, setVersion] = useState("");
  const [creating, setCreating] = useState(false);

  // Upload form
  const [selectedTest, setSelectedTest] = useState("");
  const [selectedModule, setSelectedModule] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isAnswerKey, setIsAnswerKey] = useState(false);
  const [parsing, setParsing] = useState(false);
  const [parsed, setParsed] = useState<ParsedQuestion[] | null>(null);
  const [answerKey, setAnswerKey] = useState<Record<number, string>>({});
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState("");

  useEffect(() => {
    if (status === "unauthenticated") router.push("/auth/signin");
    if (status === "authenticated" && (session?.user as { role?: string })?.role !== "admin") {
      router.push("/");
    }
  }, [status, session, router]);

  useEffect(() => {
    fetch("/api/admin/tests").then((r) => r.json()).then(setTests).catch(() => {});
  }, []);

  async function createTest(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    const res = await fetch("/api/admin/tests", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        year: parseInt(year),
        month: parseInt(month),
        section,
        version: version || null,
        isFree: true,
        modules: [
          { number: 1, timeLimit: section === "MATH" ? 2100 : 1920 },
          { number: 2, timeLimit: section === "MATH" ? 2100 : 1920 },
        ],
      }),
    });
    const data = await res.json();
    setTests((prev) => [data, ...prev]);
    setTitle(""); setVersion("");
    setCreating(false);
  }

  async function parsePDF() {
    if (!file) return;
    setParsing(true);
    setParsed(null);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("isAnswerKey", String(isAnswerKey));

    const res = await fetch("/api/admin/parse-pdf", { method: "POST", body: fd });
    const data = await res.json();
    setParsing(false);

    if (data.type === "answerKey") {
      const map: Record<number, string> = {};
      for (const a of data.answers) map[a.number] = a.answer;
      setAnswerKey(map);
      setSaveMsg(`Loaded ${data.answers.length} answers from key.`);
    } else {
      // Merge answer key if available
      const qs = (data.questions as ParsedQuestion[]).map((q) => ({
        ...q,
        correctAnswer: answerKey[q.order] ?? "",
      }));
      setParsed(qs);
    }
  }

  async function saveQuestions() {
    if (!parsed || !selectedModule) return;
    setSaving(true);
    const res = await fetch("/api/admin/parse-pdf", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ moduleId: selectedModule, questions: parsed }),
    });
    const data = await res.json();
    setSaving(false);
    setSaveMsg(`Saved ${data.saved} questions.`);
    setParsed(null);
    // Refresh tests
    fetch("/api/admin/tests").then((r) => r.json()).then(setTests).catch(() => {});
  }

  const selectedTestModules = tests.find((t) => t.id === selectedTest)?.modules ?? [];

  if (status === "loading") {
    return <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
    </div>;
  }

  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-md">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="text-[#7c3aed] font-bold">PurpleBook.cc</Link>
            <span className="text-gray-400">/</span>
            <span className="text-sm font-medium text-gray-900">Admin</span>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-gray-100 rounded-xl p-1 w-fit">
          {(["tests", "upload"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
                tab === t ? "bg-white text-[#7c3aed] shadow" : "text-gray-500"
              }`}
            >
              {t === "tests" ? "Tests" : "Upload PDF"}
            </button>
          ))}
        </div>

        {tab === "tests" && (
          <div className="space-y-6">
            {/* Create test form */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6">
              <h2 className="text-base font-semibold text-gray-900 mb-4">Create New Test</h2>
              <form onSubmit={createTest} className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Title</label>
                  <input
                    value={title} onChange={(e) => setTitle(e.target.value)} required
                    placeholder="e.g. August 2024 US Form B"
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Year</label>
                  <input
                    value={year} onChange={(e) => setYear(e.target.value)} type="number" required
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Month</label>
                  <select
                    value={month} onChange={(e) => setMonth(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                  >
                    {MONTH_NAMES.slice(1).map((m, i) => (
                      <option key={i + 1} value={i + 1}>{m}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Section</label>
                  <select
                    value={section} onChange={(e) => setSection(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                  >
                    <option value="MATH">Math</option>
                    <option value="ENGLISH">English (Reading &amp; Writing)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Version (optional)</label>
                  <input
                    value={version} onChange={(e) => setVersion(e.target.value)}
                    placeholder="e.g. US Form B"
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                  />
                </div>
                <div className="col-span-2">
                  <button
                    type="submit" disabled={creating}
                    className="px-5 py-2 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white text-sm font-medium transition-colors disabled:opacity-60"
                  >
                    {creating ? "Creating..." : "Create Test (auto-creates Module 1 & 2)"}
                  </button>
                </div>
              </form>
            </div>

            {/* Test list */}
            <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100">
                <h2 className="text-base font-semibold text-gray-900">All Tests ({tests.length})</h2>
              </div>
              {tests.length === 0 ? (
                <p className="text-sm text-gray-400 text-center py-8">No tests yet.</p>
              ) : (
                <div className="divide-y divide-gray-100">
                  {tests.map((t) => (
                    <div key={t.id} className="px-6 py-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{t.title}</p>
                        <p className="text-xs text-gray-500">{t.section} · {MONTH_NAMES[t.month]} {t.year}</p>
                      </div>
                      <div className="flex gap-2">
                        {t.modules.map((m) => (
                          <span key={m.id} className="text-xs px-2 py-1 rounded-md bg-gray-100 text-gray-600">
                            M{m.number}: {m._count.questions}q
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {tab === "upload" && (
          <div className="bg-white rounded-2xl border border-gray-200 p-6 space-y-5">
            <h2 className="text-base font-semibold text-gray-900">Upload & Parse PDF</h2>

            {/* Select test + module */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Select Test</label>
                <select
                  value={selectedTest} onChange={(e) => { setSelectedTest(e.target.value); setSelectedModule(""); }}
                  className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
                >
                  <option value="">— choose test —</option>
                  {tests.map((t) => (
                    <option key={t.id} value={t.id}>{t.title}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Module</label>
                <select
                  value={selectedModule} onChange={(e) => setSelectedModule(e.target.value)}
                  disabled={!selectedTest}
                  className="w-full px-3 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-[#7c3aed] disabled:opacity-50"
                >
                  <option value="">— choose module —</option>
                  {selectedTestModules.map((m) => (
                    <option key={m.id} value={m.id}>Module {m.number} ({m._count.questions} questions)</option>
                  ))}
                </select>
              </div>
            </div>

            {/* File upload */}
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">PDF File</label>
              <input
                type="file" accept=".pdf"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className="block w-full text-sm text-gray-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:bg-[#7c3aed]/10 file:text-[#7c3aed] file:font-medium hover:file:bg-[#7c3aed]/20 transition-colors cursor-pointer"
              />
            </div>

            {/* Type toggle */}
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-2 text-sm text-gray-900 cursor-pointer">
                <input
                  type="checkbox" checked={isAnswerKey} onChange={(e) => setIsAnswerKey(e.target.checked)}
                  className="w-4 h-4 accent-[#7c3aed]"
                />
                This is an Answer Key PDF
              </label>
            </div>

            <button
              onClick={parsePDF}
              disabled={!file || parsing}
              className="px-5 py-2 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white text-sm font-medium transition-colors disabled:opacity-60"
            >
              {parsing ? "Parsing..." : "Parse PDF"}
            </button>

            {saveMsg && (
              <div className="px-4 py-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">
                {saveMsg}
              </div>
            )}

            {/* Parsed questions review */}
            {parsed && (
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-semibold text-gray-900">
                    Parsed {parsed.length} questions — review & edit before saving
                  </h3>
                  <button
                    onClick={saveQuestions}
                    disabled={saving || !selectedModule}
                    className="px-4 py-1.5 rounded-lg bg-green-600 hover:bg-green-700 text-white text-xs font-semibold transition-colors disabled:opacity-60"
                  >
                    {saving ? "Saving..." : "Save to DB"}
                  </button>
                </div>

                <div className="space-y-4 max-h-[600px] overflow-y-auto pr-1">
                  {parsed.map((q, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-xl p-4 space-y-3">
                      <div className="flex items-start gap-2">
                        <span className="text-xs font-bold text-[#7c3aed] w-6 flex-shrink-0 mt-0.5">#{q.order}</span>
                        <textarea
                          value={q.text}
                          onChange={(e) => {
                            const updated = [...parsed];
                            updated[idx] = { ...q, text: e.target.value };
                            setParsed(updated);
                          }}
                          rows={2}
                          className="flex-1 text-sm px-2 py-1 rounded-lg border border-gray-200 bg-transparent focus:outline-none focus:ring-1 focus:ring-[#7c3aed] resize-none"
                        />
                      </div>

                      {/* Choices */}
                      <div className="grid grid-cols-2 gap-2">
                        {(["A", "B", "C", "D"] as const).map((letter) => (
                          <div key={letter} className="flex items-center gap-2">
                            <span className="text-xs font-bold text-gray-400 w-4">{letter}</span>
                            <input
                              value={q.choices[letter] ?? ""}
                              onChange={(e) => {
                                const updated = [...parsed];
                                updated[idx] = { ...q, choices: { ...q.choices, [letter]: e.target.value } };
                                setParsed(updated);
                              }}
                              className="flex-1 text-xs px-2 py-1 rounded border border-gray-200 bg-transparent focus:outline-none focus:ring-1 focus:ring-[#7c3aed]"
                              placeholder={`Choice ${letter}`}
                            />
                          </div>
                        ))}
                      </div>

                      {/* Correct answer */}
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-500">Correct answer:</span>
                        <div className="flex gap-1">
                          {(["A", "B", "C", "D"] as const).map((letter) => (
                            <button
                              key={letter}
                              onClick={() => {
                                const updated = [...parsed];
                                updated[idx] = { ...q, correctAnswer: letter };
                                setParsed(updated);
                              }}
                              className={`w-7 h-7 text-xs font-bold rounded-md transition-colors ${
                                q.correctAnswer === letter
                                  ? "bg-[#7c3aed] text-white"
                                  : "bg-gray-100 text-gray-500 hover:bg-[#7c3aed]/20"
                              }`}
                            >
                              {letter}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
