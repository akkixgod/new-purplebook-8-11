"use client";

import { useEffect, useState, useCallback, use, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { DesmosCalculatorModal } from "@/components/DesmosCalculatorModal";
import { MathReferenceSheet } from "@/components/MathReferenceSheet";
import { ModuleReviewModal } from "@/components/ModuleReviewModal";
import { QuestionNavGrid } from "@/components/QuestionNavGrid";

interface Question {
  id: string;
  order: number;
  stimulus: string | null;
  text: string;
  imageUrl: string | null;
  choices: string;
  correctAnswer: string;
}

interface ModuleData {
  id: string;
  number: number;
  timeLimit: number;
  test: { title: string; section: string; year: number; month: number };
  questions: Question[];
}

const STORAGE_KEY = (id: string) => `purplebook_answers_${id}`;
const STORAGE_TIME_KEY = (id: string) => `purplebook_time_${id}`;
const STORAGE_MARKS_KEY = (id: string) => `purplebook_marks_${id}`;
const STORAGE_CROSSED_KEY = (id: string) => `purplebook_crossed_${id}`;

type ChoiceLetter = "A" | "B" | "C" | "D";
type CrossedMap = Record<string, ChoiceLetter[]>;

function textToHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br/>");
}

export default function TestPage({ params }: { params: Promise<{ moduleId: string }> }) {
  const { moduleId } = use(params);
  const router = useRouter();
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("attemptId") ?? "";

  const [moduleData, setModuleData] = useState<ModuleData | null>(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | null>>({});
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [paused, setPaused] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [markedForReview, setMarkedForReview] = useState<Set<string>>(new Set());
  const [highlightMode, setHighlightMode] = useState(false);
  const [crossOutMode, setCrossOutMode] = useState(false);
  const [crossedOut, setCrossedOut] = useState<CrossedMap>({});
  const [highlights, setHighlights] = useState<Record<string, string>>({});
  const [showDesmos, setShowDesmos] = useState(false);
  const [desmosMounted, setDesmosMounted] = useState(false);
  const [showReference, setShowReference] = useState(false);
  const [showDirections, setShowDirections] = useState(false);
  const [showQuestionGrid, setShowQuestionGrid] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const passageRef = useRef<HTMLDivElement>(null);
  const handleSubmitRef = useRef<() => void>(() => {});
  const currentQuestionIdRef = useRef<string>("");
  const lastCrossHoverRef = useRef<string>("");

  const openCalculator = useCallback(() => {
    setDesmosMounted(true);
    setShowDesmos(true);
  }, []);

  const toggleCalculator = useCallback(() => {
    setDesmosMounted(true);
    setShowDesmos((v) => !v);
  }, []);

  const toggleCrossOutMode = useCallback(() => {
    setCrossOutMode((v) => {
      if (!v) setHighlightMode(false);
      return !v;
    });
  }, []);

  useEffect(() => {
    fetch(`/api/modules/${moduleId}/questions`)
      .then((r) => r.json())
      .then((data: ModuleData) => {
        setModuleData(data);
        const saved = localStorage.getItem(STORAGE_KEY(attemptId));
        if (saved) setAnswers(JSON.parse(saved));
        const savedMarks = localStorage.getItem(STORAGE_MARKS_KEY(attemptId));
        if (savedMarks) setMarkedForReview(new Set(JSON.parse(savedMarks)));
        const savedCrossed = localStorage.getItem(STORAGE_CROSSED_KEY(attemptId));
        if (savedCrossed) setCrossedOut(JSON.parse(savedCrossed));
        const savedTime = localStorage.getItem(STORAGE_TIME_KEY(attemptId));
        const elapsed = savedTime ? Math.floor((Date.now() - parseInt(savedTime)) / 1000) : 0;
        setTimeLeft(Math.max(0, data.timeLimit - elapsed));
        if (!savedTime) localStorage.setItem(STORAGE_TIME_KEY(attemptId), String(Date.now()));
        setLoading(false);
      });
  }, [moduleId, attemptId]);

  // Keep an up-to-date ref for keyboard handlers (Alt+K) without writing to refs during render.
  useEffect(() => {
    if (!moduleData) return;
    const q = moduleData.questions[current];
    if (q) currentQuestionIdRef.current = q.id;
  }, [moduleData, current]);

  useEffect(() => {
    if (attemptId) localStorage.setItem(STORAGE_KEY(attemptId), JSON.stringify(answers));
  }, [answers, attemptId]);

  useEffect(() => {
    if (attemptId) localStorage.setItem(STORAGE_MARKS_KEY(attemptId), JSON.stringify([...markedForReview]));
  }, [markedForReview, attemptId]);

  useEffect(() => {
    if (attemptId) localStorage.setItem(STORAGE_CROSSED_KEY(attemptId), JSON.stringify(crossedOut));
  }, [crossedOut, attemptId]);

  const handleSubmit = useCallback(async () => {
    if (submitting || !moduleData || !attemptId) return;
    setSubmitError(null);
    setSubmitting(true);
    const startTime = parseInt(localStorage.getItem(STORAGE_TIME_KEY(attemptId)) ?? "0");
    const timeSpent = startTime ? Math.floor((Date.now() - startTime) / 1000) : null;
    const answerPayload = moduleData.questions.map((q) => ({
      questionId: q.id,
      selected: answers[q.id] ?? null,
    }));
    const r = await fetch(`/api/attempts/${attemptId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ answers: answerPayload, timeSpent }),
    });
    if (!r.ok) {
      const json = (await r.json().catch(() => null)) as { error?: string } | null;
      setSubmitError(json?.error ?? `Submit failed (${r.status})`);
      setSubmitting(false);
      return;
    }
    localStorage.removeItem(STORAGE_KEY(attemptId));
    localStorage.removeItem(STORAGE_TIME_KEY(attemptId));
    localStorage.removeItem(STORAGE_MARKS_KEY(attemptId));
    localStorage.removeItem(STORAGE_CROSSED_KEY(attemptId));
    router.push(`/test/${moduleId}/results?attemptId=${attemptId}`);
  }, [submitting, moduleData, attemptId, answers, moduleId, router]);

  useEffect(() => { handleSubmitRef.current = handleSubmit; }, [handleSubmit]);

  useEffect(() => {
    if (timeLeft === null || paused) return;
    if (timeLeft <= 0) { handleSubmitRef.current(); return; }
    const t = setTimeout(() => setTimeLeft((p) => (p !== null ? p - 1 : null)), 1000);
    return () => clearTimeout(t);
  }, [timeLeft, paused]);

  // Alt+C / Option+C — toggle Desmos (Math only)
  useEffect(() => {
    if (!moduleData || moduleData.test.section !== "MATH") return;
    const onKey = (e: KeyboardEvent) => {
      if (!e.altKey) return;
      if (e.key !== "c" && e.key !== "C") return;
      e.preventDefault();
      toggleCalculator();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [moduleData, toggleCalculator]);

  // Alt+X / Option+X — toggle option eliminator
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!e.altKey) return;
      if (e.key !== "x" && e.key !== "X") return;
      e.preventDefault();
      toggleCrossOutMode();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [toggleCrossOutMode]);

  const toggleMark = useCallback((qId: string) => {
    setMarkedForReview((prev) => {
      const next = new Set(prev);
      if (next.has(qId)) next.delete(qId);
      else next.add(qId);
      return next;
    });
  }, []);

  // Alt+K / Option+K — toggle Mark for Review on current question
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!e.altKey) return;
      if (e.key !== "k" && e.key !== "K") return;
      const qId = currentQuestionIdRef.current;
      if (!qId) return;
      e.preventDefault();
      toggleMark(qId);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [toggleMark]);

  // Highlight: wrap selected text in <mark> on mouseup
  const handleMouseUp = useCallback(() => {
    if (!highlightMode) return;
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed) return;
    if (!passageRef.current?.contains(selection.getRangeAt(0).commonAncestorContainer)) return;
    try {
      const range = selection.getRangeAt(0);
      const mark = document.createElement("mark");
      mark.style.backgroundColor = "#fef08a";
      mark.style.borderRadius = "2px";
      mark.style.padding = "0 1px";
      range.surroundContents(mark);
      selection.removeAllRanges();
    } catch {
      // selection spans multiple nodes — skip
    }
    if (passageRef.current) {
      const qId = passageRef.current.dataset.qid;
      if (qId) setHighlights((prev) => ({ ...prev, [qId]: passageRef.current!.innerHTML }));
    }
  }, [highlightMode]);

  const toggleCrossedLetter = useCallback((qId: string, letter: ChoiceLetter) => {
    setCrossedOut((prev) => {
      const current = prev[qId] ?? [];
      const nextList = current.includes(letter)
        ? current.filter((l) => l !== letter)
        : [...current, letter];
      return { ...prev, [qId]: nextList };
    });
  }, []);

  /** Select an answer (does NOT restore cross-out; badge exclusively handles elimination). */
  const handleChoiceClick = useCallback((qId: string, letter: ChoiceLetter) => {
    // Bluebook behavior: selection and cross-out are separate controls.
    // If the choice is already eliminated, clicking the main choice box should NOT restore or select it.
    const isEliminated = (crossedOut[qId] ?? []).includes(letter);
    if (isEliminated) return;
    setAnswers((prev) => ({ ...prev, [qId]: letter }));
  }, [crossedOut]);

  /** Eliminate / restore a choice via the right-side control (Bluebook). */
  const handleEliminateClick = useCallback(
    (qId: string, letter: ChoiceLetter) => {
      const wasCrossed = (crossedOut[qId] ?? []).includes(letter);
      toggleCrossedLetter(qId, letter);
      // Eliminating the selected answer clears the selection
      if (!wasCrossed) {
        setAnswers((prev) => (prev[qId] === letter ? { ...prev, [qId]: null } : prev));
      }
    },
    [crossedOut, toggleCrossedLetter]
  );

  if (loading || !moduleData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const questions = moduleData.questions;
  const q = questions[current];
  const isFlagged = markedForReview.has(q.id);
  const choices: Record<string, string | boolean> = JSON.parse(q.choices);
  const isMath = moduleData.test.section === "MATH";
  const mins = Math.floor((timeLeft ?? 0) / 60);
  const secs = ((timeLeft ?? 0) % 60).toString().padStart(2, "0");
  const isLow = (timeLeft ?? 0) < 120;

  // Left: passage/stimulus, or figure, or question text
  // Right: question prompt when stimulus/figure exists; always choices
  const hasFigure = Boolean(q.imageUrl);
  const hasStimulus = Boolean(q.stimulus);
  const leftHTML =
    highlights[q.id] ??
    textToHtml(
      hasStimulus ? (q.stimulus as string) : hasFigure ? "" : q.text
    );
  const rightQuestionText = hasStimulus || hasFigure ? q.text : null;

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-white">
      {/* ── Header ── */}
      <header className="flex-shrink-0 bg-white border-b border-gray-200 z-50">
        <div className="flex items-center h-12 px-4 gap-3">
          {/* Left: title + directions */}
          <div className="flex items-center gap-3 flex-1 min-w-0">
            <div className="min-w-0">
              <p className="text-sm font-semibold text-gray-900 truncate leading-tight">
                {moduleData.test.title} — Module {moduleData.number}
              </p>
            </div>
            <button
              onClick={() => setShowDirections(true)}
              className="flex items-center gap-0.5 text-xs text-gray-500 hover:text-gray-800 whitespace-nowrap transition-colors"
            >
              Directions
              <svg className="w-3 h-3 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          {/* Center: timer + pause */}
          <div className="flex items-center gap-2.5 flex-shrink-0">
            <span className={`text-lg font-mono font-bold tabular-nums ${isLow ? "text-red-500" : "text-gray-900"}`}>
              {mins}:{secs}
            </span>
            <button
              onClick={() => setPaused((p) => !p)}
              className="px-3 py-0.5 text-xs border border-gray-300 rounded-full hover:bg-gray-100 text-gray-700 transition-colors"
            >
              {paused ? "Resume" : "Pause"}
            </button>
          </div>

          {/* Right: tools */}
          <div className="flex items-center gap-1.5 flex-1 justify-end">
            {/* Highlight */}
            <button
              type="button"
              onClick={() => {
                setHighlightMode((p) => {
                  if (!p) setCrossOutMode(false);
                  return !p;
                });
              }}
              title={highlightMode ? "Exit highlight mode" : "Highlight text (select text to highlight)"}
              aria-pressed={highlightMode}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                highlightMode
                  ? "bg-yellow-200 text-yellow-800 border border-yellow-400"
                  : "border border-gray-300 text-gray-600 hover:bg-gray-100"
              }`}
            >
              <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              <span className="hidden sm:inline">Highlight</span>
            </button>

            {/* Option eliminator (Cross-Out) */}
            <button
              type="button"
              onClick={toggleCrossOutMode}
              title={crossOutMode ? "Hide cross-out buttons (Alt+X)" : "Show cross-out buttons (Alt+X)"}
              aria-pressed={crossOutMode}
              aria-label="Cross-Out tool"
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                crossOutMode
                  ? "bg-gray-900 text-white border border-gray-900"
                  : "border border-gray-300 text-gray-600 hover:bg-gray-100"
              }`}
            >
              <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
                <circle cx="12" cy="12" r="9" strokeWidth={2} />
                <path strokeLinecap="round" strokeWidth={2} d="M7 7l10 10" />
              </svg>
              <span className="hidden sm:inline">Cross-Out</span>
            </button>

            {/* Reference + Calculator — Math only (Bluebook tools) */}
            {isMath && (
              <>
                <button
                  type="button"
                  onClick={() => setShowReference(true)}
                  title="Reference sheet"
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium border border-gray-300 text-gray-600 hover:bg-gray-100 transition-colors"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="hidden sm:inline">Reference</span>
                </button>
                <button
                  type="button"
                  onClick={() => (showDesmos ? setShowDesmos(false) : openCalculator())}
                  title="Graphing Calculator (Alt+C)"
                  className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium border transition-colors ${
                    showDesmos
                      ? "border-[#7c3aed] bg-[#7c3aed]/10 text-[#7c3aed]"
                      : "border-gray-300 text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 19h16a2 2 0 002-2V7a2 2 0 00-2-2H4a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span className="hidden sm:inline">Calculator</span>
                </button>
              </>
            )}

            <button
              onClick={() => {
                setShowQuestionGrid(false);
                setShowReviewModal(true);
              }}
              disabled={submitting}
              className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white transition-colors disabled:opacity-60"
            >
              Submit
            </button>
            {submitError && (
              <p className="mt-2 text-xs text-red-600 text-center w-full">{submitError}</p>
            )}
          </div>
        </div>

        {/* Segmented progress bar */}
        <div className="flex h-1.5 w-full gap-px bg-gray-200">
          {questions.map((qq, i) => {
            const answered = !!answers[qq.id];
            const marked = markedForReview.has(qq.id);
            let bg = "bg-gray-200";
            if (i === current) bg = "bg-[#7c3aed]";
            else if (marked && answered) bg = "bg-orange-400";
            else if (marked) bg = "bg-orange-300";
            else if (answered) bg = "bg-[#7c3aed]/50";
            return <div key={qq.id} className={`flex-1 ${bg} transition-colors`} />;
          })}
        </div>
      </header>

      {/* ── Body: split panel ── */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left panel */}
        <div className="w-1/2 overflow-y-auto border-r border-gray-200 p-6 lg:p-10">
          {leftHTML && (
            <div
              ref={passageRef}
              data-qid={q.id}
              onMouseUp={handleMouseUp}
              className={`text-gray-800 text-sm leading-7 select-text ${highlightMode ? "cursor-text" : ""}`}
              dangerouslySetInnerHTML={{ __html: leftHTML }}
            />
          )}
          {q.imageUrl && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={q.imageUrl}
              alt="Figure"
              className={`${leftHTML ? "mt-4" : ""} rounded-lg max-w-full border border-gray-200`}
            />
          )}
        </div>

        {/* Right panel */}
        <div className="w-1/2 overflow-y-auto p-6 lg:p-10">
          {/* Question number + mark for review */}
          <div className="flex items-center gap-2 mb-5">
            <span className="w-8 h-8 rounded flex items-center justify-center bg-gray-900 text-white text-sm font-bold flex-shrink-0">
              {current + 1}
            </span>
            <button
              type="button"
              onClick={() => toggleMark(q.id)}
              aria-pressed={isFlagged}
              title={isFlagged ? "Remove mark for review (Alt+K)" : "Mark for review (Alt+K)"}
              className={`flex items-center gap-1.5 rounded-lg border px-2.5 py-1.5 text-xs font-medium transition-colors ${
                isFlagged
                  ? "border-orange-400 bg-orange-50 text-orange-700 shadow-sm"
                  : "border-transparent text-gray-500 hover:border-gray-200 hover:bg-gray-50 hover:text-gray-800"
              }`}
            >
              <svg
                className="w-4 h-4"
                fill={isFlagged ? "currentColor" : "none"}
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={isFlagged ? 1.5 : 2}
                aria-hidden
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              Mark for Review
            </button>
          </div>

          {/* Question prompt */}
          {rightQuestionText && (
            <p className="mb-5 text-sm text-gray-800 leading-relaxed">{rightQuestionText}</p>
          )}

          {/* Choices / grid-in */}
          {choices.gridIn ? (
            <div className="space-y-2">
              <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide">
                Enter answer
              </label>
              <input
                type="text"
                inputMode="decimal"
                value={answers[q.id] ?? ""}
                onChange={(e) =>
                  setAnswers((prev) => ({
                    ...prev,
                    [q.id]: e.target.value.trim() === "" ? null : e.target.value.trim(),
                  }))
                }
                placeholder="Type your answer"
                className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-[#7c3aed] focus:outline-none text-sm font-medium text-gray-900"
              />
            </div>
          ) : (
            <div
              className="space-y-2.5"
              role="listbox"
              aria-label="Answer choices"
              aria-orientation="vertical"
            >
              {(["A", "B", "C", "D"] as const).map((letter) => {
                if (!choices[letter] && choices[letter] !== "") return null;
                if (!(letter in choices)) return null;
                const selected = answers[q.id] === letter;
                const eliminated = (crossedOut[q.id] ?? []).includes(letter);
                const choiceLabel =
                  typeof choices[letter] === "boolean"
                    ? choices[letter]
                      ? "True"
                      : "False"
                    : String(choices[letter] ?? "");
                return (
                  <div
                    key={letter}
                    role="none"
                    className="w-full flex items-stretch"
                    onContextMenu={(e) => {
                      e.preventDefault();
                      handleEliminateClick(q.id, letter);
                    }}
                  >
                    {/* Main answer choice (selection only) */}
                    <button
                      type="button"
                      role="option"
                      aria-selected={selected}
                      aria-label={
                        eliminated
                          ? `Choice ${letter}, crossed out`
                          : `Choice ${letter}`
                      }
                      data-eliminated={eliminated ? "true" : "false"}
                      onClick={() => {
                        // If eliminated, the badge exclusively handles cross-out.
                        if (eliminated) return;
                        handleChoiceClick(q.id, letter);
                      }}
                      className={`flex-1 min-w-0 text-left px-4 py-3 rounded-xl border-2 transition-all flex items-start gap-3 ${
                        eliminated
                          ? "opacity-50 border-gray-200 bg-gray-50"
                          : selected
                            ? "border-[#7c3aed] bg-[#7c3aed]/5"
                            : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <span
                        className={`relative w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold border-2 mt-0.5 transition-colors ${
                          eliminated
                            ? "border-gray-400 text-gray-500"
                            : selected
                              ? "border-[#7c3aed] bg-[#7c3aed] text-white"
                              : "border-gray-300 text-gray-600"
                        }`}
                      >
                        {letter}
                        {eliminated && (
                          <span
                            className="pointer-events-none absolute inset-0 flex items-center justify-center"
                            aria-hidden
                          >
                            <span className="block w-[130%] h-0.5 bg-gray-500 rotate-[-45deg] rounded-full" />
                          </span>
                        )}
                      </span>
                      <span
                        className={`text-sm leading-relaxed ${
                          eliminated
                            ? "text-gray-500 line-through decoration-gray-500"
                            : selected
                              ? "text-[#7c3aed] font-medium"
                              : "text-gray-900"
                        }`}
                      >
                        {choiceLabel}
                      </span>
                    </button>

                    {/* Right-edge Cross-Out badge (always visible; hover toggle only in tool mode). */}
                    <button
                      type="button"
                      onClick={() => handleEliminateClick(q.id, letter)}
                      onMouseEnter={() => {
                        if (!crossOutMode) return;
                        const key = `${q.id}:${letter}`;
                        // Toggle only once per hover entry to prevent rapid double toggles.
                        if (lastCrossHoverRef.current === key) return;
                        lastCrossHoverRef.current = key;
                        handleEliminateClick(q.id, letter);
                      }}
                      onMouseLeave={() => {
                        // allow re-toggle next time user hovers
                        lastCrossHoverRef.current = "";
                      }}
                      title={crossOutMode ? (eliminated ? `Restore ${letter}` : `Cross out ${letter}`) : `Cross out ${letter}`}
                      aria-label={
                        eliminated
                          ? `Cross-out badge ${letter}, active`
                          : `Cross-out badge ${letter}`
                      }
                      aria-pressed={eliminated}
                      className="flex-shrink-0 ml-2 w-10 flex items-center justify-end"
                    >
                      <span
                        className={`relative w-7 h-7 rounded-full border-2 flex items-center justify-center text-xs font-bold leading-none transition-colors ${
                          eliminated
                            ? "border-gray-700 bg-gray-100 text-gray-800"
                            : "border-gray-400 text-gray-700"
                        }`}
                        aria-hidden
                      >
                        {letter}
                        {eliminated && (
                          <span className="pointer-events-none absolute inset-0 flex items-center justify-center">
                            <span className="w-[70%] h-[2px] bg-current rounded-full" />
                          </span>
                        )}
                      </span>
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* ── Bottom nav ── */}
      <div className="relative flex-shrink-0 border-t border-gray-200 bg-white px-4 py-2 flex items-center justify-between gap-3 z-[95]">
        <button
          type="button"
          onClick={() => setCurrent((p) => Math.max(0, p - 1))}
          disabled={current === 0}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors disabled:opacity-30 flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>

        {/* Question menu trigger (Bluebook overview) */}
        <button
          type="button"
          onClick={() => setShowQuestionGrid((v) => !v)}
          aria-expanded={showQuestionGrid}
          aria-haspopup="dialog"
          aria-controls="question-nav-grid"
          title="Open question menu"
          className={`flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg border font-medium transition-colors flex-shrink-0 ${
            showQuestionGrid
              ? "border-[#7c3aed] bg-[#7c3aed]/10 text-[#7c3aed]"
              : "border-gray-200 text-gray-800 hover:bg-gray-50"
          }`}
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h4v4H4V6zm6 0h4v4h-4V6zm6 0h4v4h-4V6zM4 12h4v4H4v-4zm6 0h4v4h-4v-4zm6 0h4v4h-4v-4zM4 18h4v4H4v-4zm6 0h4v4h-4v-4zm6 0h4v4h-4v-4z" />
          </svg>
          <span>
            Question {current + 1} of {questions.length}
          </span>
          <svg
            className={`w-3.5 h-3.5 text-gray-400 transition-transform ${showQuestionGrid ? "rotate-180" : ""}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 15l7-7 7 7" />
          </svg>
        </button>

        {current < questions.length - 1 ? (
          <button
            type="button"
            onClick={() => setCurrent((p) => Math.min(questions.length - 1, p + 1))}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg bg-[#7c3aed] text-white hover:bg-[#6d28d9] transition-colors flex-shrink-0"
          >
            Next
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        ) : (
          <button
            type="button"
            onClick={() => {
              setShowQuestionGrid(false);
              setShowReviewModal(true);
            }}
            disabled={submitting}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg bg-green-600 text-white hover:bg-green-700 transition-colors disabled:opacity-60 flex-shrink-0"
          >
            Finish
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </button>
        )}
      </div>

      <div id="question-nav-grid">
        <QuestionNavGrid
          open={showQuestionGrid}
          onClose={() => setShowQuestionGrid(false)}
          moduleNumber={moduleData.number}
          questions={questions}
          currentIndex={current}
          answers={answers}
          markedForReview={markedForReview}
          onNavigate={setCurrent}
        />
      </div>

      <ModuleReviewModal
        open={showReviewModal}
        onClose={() => setShowReviewModal(false)}
        onConfirmSubmit={handleSubmit}
        submitting={submitting}
        moduleNumber={moduleData.number}
        questions={questions}
        answers={answers}
        markedForReview={markedForReview}
        onNavigate={setCurrent}
      />

      {/* ── Pause overlay ── */}
      {paused && (
        <div className="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center">
          <div className="bg-white rounded-2xl p-8 text-center max-w-sm mx-4 shadow-2xl">
            <svg className="w-12 h-12 text-[#7c3aed] mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10 9v6m4-6v6" />
              <circle cx="12" cy="12" r="9" strokeWidth={1.5} />
            </svg>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Timer Paused</h2>
            <p className="text-sm text-gray-500 mb-6">Your progress is saved.</p>
            <button
              onClick={() => setPaused(false)}
              className="px-6 py-2.5 rounded-lg bg-[#7c3aed] text-white font-medium hover:bg-[#6d28d9] transition-colors"
            >
              Resume
            </button>
          </div>
        </div>
      )}

      {/* ── Directions modal ── */}
      {showDirections && (
        <div
          className="fixed inset-0 z-[100] bg-black/60 flex items-center justify-center"
          onClick={() => setShowDirections(false)}
        >
          <div
            className="bg-white rounded-2xl p-6 max-w-md mx-4 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-bold text-gray-900 mb-3">Directions</h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              {isMath
                ? "The questions in this section address a number of important math skills. Use of a calculator is permitted for all questions. A reference sheet, calculator, and these directions can be accessed throughout the test. For multiple-choice questions, solve each problem and choose the correct answer from the choices provided."
                : "The questions in this section address a number of important reading and writing skills. Each question includes one or more passages, which may include a table or graph. Read each passage and question carefully, and then choose the best answer to the question based on the passage(s). All questions in this section are multiple-choice with four answer choices."}
            </p>
            <button
              onClick={() => setShowDirections(false)}
              className="mt-5 px-4 py-2 rounded-lg bg-[#7c3aed] text-white text-sm font-medium hover:bg-[#6d28d9] transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* ── Math Reference Sheet ── */}
      {isMath && (
        <MathReferenceSheet open={showReference} onClose={() => setShowReference(false)} />
      )}

      {/* ── Desmos Graphing Calculator (kept mounted for state persistence) ── */}
      {isMath && desmosMounted && (
        <DesmosCalculatorModal open={showDesmos} onClose={() => setShowDesmos(false)} />
      )}
    </div>
  );
}
