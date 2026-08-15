"use client";

import { useEffect, useState, useCallback, use, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { DesmosCalculatorModal } from "@/components/DesmosCalculatorModal";
import { MathReferenceSheet } from "@/components/MathReferenceSheet";
import { Module1PathModal } from "@/components/Module1PathModal";
import { ModuleReviewModal } from "@/components/ModuleReviewModal";
import { QuestionNavGrid } from "@/components/QuestionNavGrid";
import {
  TelegramCommunityCheckModal,
  isTelegramJoinedThisSession,
} from "@/components/TelegramCommunityCheckModal";
import { cacheAttempt, savePendingSubmission, clearPendingSubmission, type CachedAttempt } from "@/lib/attempt-cache";
import { saveModule1Journey, readModule1Journey } from "@/lib/test-journey";
import { textToHtml } from "@/lib/text-to-html";
import { applyTextHighlight } from "@/lib/text-highlight";
import { useSession } from "next-auth/react";

interface Question {
  id: string;
  order: number;
  stimulus: string | null;
  text: string;
  imageUrl: string | null;
  choices: string;
}

interface ModuleData {
  id: string;
  testId?: string;
  number: number;
  timeLimit: number;
  test: { title: string; section: string; year: number; month: number };
  questions: Question[];
}

const STORAGE_KEY = (id: string) => `purplebook_answers_${id}`;
const STORAGE_TIME_KEY = (id: string) => `purplebook_time_${id}`;
const STORAGE_MARKS_KEY = (id: string) => `purplebook_marks_${id}`;
const STORAGE_CROSSED_KEY = (id: string) => `purplebook_crossed_${id}`;
const STORAGE_HIDE_TIMER_KEY = (id: string) => `purplebook_hide_timer_${id}`;

const FIVE_MINUTES_SEC = 300;

type ChoiceLetter = "A" | "B" | "C" | "D";
type CrossedMap = Record<string, ChoiceLetter[]>;

export default function TestPage({ params }: { params: Promise<{ moduleId: string }> }) {
  const { moduleId } = use(params);
  const router = useRouter();
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("attemptId") ?? "";
  const { status: authStatus } = useSession();

  const [moduleData, setModuleData] = useState<ModuleData | null>(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | null>>({});
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [paused, setPaused] = useState(false);
  const [hideTimer, setHideTimer] = useState(false);
  const [timerHideLocked, setTimerHideLocked] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "error">("idle");
  const [loading, setLoading] = useState(true);
  const [markedForReview, setMarkedForReview] = useState<Set<string>>(new Set());
  const [highlightMode, setHighlightMode] = useState(false);
  const [crossedOut, setCrossedOut] = useState<CrossedMap>({});
  const [highlights, setHighlights] = useState<Record<string, string>>({});
  const [showDesmos, setShowDesmos] = useState(false);
  const [desmosMounted, setDesmosMounted] = useState(false);
  const [showReference, setShowReference] = useState(false);
  const [showDirections, setShowDirections] = useState(false);
  const [showQuestionGrid, setShowQuestionGrid] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [showModule1PathModal, setShowModule1PathModal] = useState(false);
  const [showTelegramModal, setShowTelegramModal] = useState(false);
  const [pendingResultsUrl, setPendingResultsUrl] = useState<string | null>(null);
  const [submittedAttemptId, setSubmittedAttemptId] = useState<string | null>(null);
  const [nextModuleId, setNextModuleId] = useState<string | null>(null);
  const passageRef = useRef<HTMLDivElement>(null);
  const handleSubmitRef = useRef<() => void>(() => {});
  const currentQuestionIdRef = useRef<string>("");

  const openCalculator = useCallback(() => {
    setDesmosMounted(true);
    setShowDesmos(true);
  }, []);

  const closeCalculator = useCallback(() => {
    setShowDesmos(false);
  }, []);

  const toggleCalculator = useCallback(() => {
    setDesmosMounted(true);
    setShowDesmos((v) => !v);
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
        const remaining = Math.max(0, data.timeLimit - elapsed);
        setTimeLeft(remaining);
        if (!savedTime) localStorage.setItem(STORAGE_TIME_KEY(attemptId), String(Date.now()));

        // Restore hide-timer preference unless already in the final 5 minutes.
        if (remaining <= FIVE_MINUTES_SEC) {
          setHideTimer(false);
          setTimerHideLocked(true);
        } else {
          const savedHide = localStorage.getItem(STORAGE_HIDE_TIMER_KEY(attemptId));
          setHideTimer(savedHide === "1");
          setTimerHideLocked(false);
        }
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

    if (authStatus !== "authenticated") {
      setSaveStatus("error");
      setSubmitError("Sign in required to save your practice attempt to your account.");
      return;
    }

    setSubmitting(true);
    setSaveStatus("saving");

    const startTime = parseInt(localStorage.getItem(STORAGE_TIME_KEY(attemptId)) ?? "0");
    const timeSpent = startTime ? Math.floor((Date.now() - startTime) / 1000) : null;
    const answerPayload = moduleData.questions.map((q) => ({
      questionId: q.id,
      selected: answers[q.id] ?? null,
    }));

    // Draft / retry buffer only — history is always read from the database after a successful write.
    savePendingSubmission({
      moduleId,
      attemptId,
      answers: answerPayload,
      timeSpent,
      savedAt: Date.now(),
    });
    localStorage.setItem(STORAGE_KEY(attemptId), JSON.stringify(answers));

    const maxAttempts = 3;
    let lastError = "Couldn't save your attempt.";

    for (let i = 0; i < maxAttempts; i++) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 25000);
        const r = await fetch("/api/attempts/complete", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          signal: controller.signal,
          body: JSON.stringify({
            attemptId,
            moduleId,
            answers: answerPayload,
            timeSpent,
          }),
        });
        clearTimeout(timeout);

        const json = (await r.json().catch(() => null)) as
          | (CachedAttempt & {
              attemptId?: string;
              userId?: string | null;
              persisted?: boolean;
              error?: string;
            })
          | null;

        if (!r.ok) {
          lastError = json?.error ?? `Submit failed (${r.status})`;
          if (r.status === 401) {
            setSaveStatus("error");
            setSubmitError(
              json?.error ?? "Sign in required to save your practice attempt to your account."
            );
            setSubmitting(false);
            return;
          }
          if (i < maxAttempts - 1) {
            await new Promise((res) => setTimeout(res, 400 * 2 ** i));
            continue;
          }
          break;
        }

        const serverAttemptId = json?.attemptId ?? json?.id ?? attemptId;

        if (!json?.persisted || !json?.userId || serverAttemptId !== attemptId) {
          lastError =
            "Your score was not saved to your account. Sign in again, then retry saving.";
          if (i < maxAttempts - 1) {
            await new Promise((res) => setTimeout(res, 400 * 2 ** i));
            continue;
          }
          break;
        }

        if (json?.module?.test) {
          cacheAttempt({ ...json, id: serverAttemptId });
        }
        clearPendingSubmission(attemptId);
        localStorage.removeItem(STORAGE_KEY(attemptId));
        localStorage.removeItem(STORAGE_TIME_KEY(attemptId));
        localStorage.removeItem(STORAGE_MARKS_KEY(attemptId));
        localStorage.removeItem(STORAGE_CROSSED_KEY(attemptId));
        localStorage.removeItem(STORAGE_HIDE_TIMER_KEY(attemptId));
        setShowReviewModal(false);
        setSubmittedAttemptId(serverAttemptId);
        setSaveStatus("saved");

        // Module 1: choose finish vs continue (no Telegram until Finish is chosen).
        if (moduleData.number === 1) {
          const journeyTestId =
            moduleData.testId ||
            `${moduleData.test.section}-${moduleData.test.year}-${moduleData.test.month}-${moduleData.test.title}`;
          saveModule1Journey({
            testId: journeyTestId,
            module1AttemptId: serverAttemptId,
            module1ModuleId: moduleId,
          });
          // Stash under moduleId too so Module 2 can find it if testId is missing from cache.
          saveModule1Journey({
            testId: moduleId,
            module1AttemptId: serverAttemptId,
            module1ModuleId: moduleId,
          });
          let siblingId: string | null = null;
          try {
            const nr = await fetch(`/api/modules/${moduleId}/next-module`, {
              credentials: "include",
            });
            const nj = (await nr.json()) as { nextModuleId: string | null };
            siblingId = nj.nextModuleId ?? null;
          } catch {
            siblingId = null;
          }
          setNextModuleId(siblingId);
          setShowModule1PathModal(true);
          setSubmitting(false);
          return;
        }

        // Module 2: Telegram then combined results.
        const journeyKeys = [
          moduleData.testId,
          `${moduleData.test.section}-${moduleData.test.year}-${moduleData.test.month}-${moduleData.test.title}`,
        ].filter(Boolean) as string[];
        let m1Id: string | undefined;
        for (const key of journeyKeys) {
          const j = readModule1Journey(key);
          if (j?.module1AttemptId) {
            m1Id = j.module1AttemptId;
            break;
          }
        }
        // Also check journeys saved under sibling module 1 id via next-module reverse lookup.
        if (!m1Id) {
          try {
            const nr = await fetch(`/api/modules/${moduleId}/next-module`, {
              credentials: "include",
            });
            const nj = (await nr.json()) as { nextModuleId: string | null };
            if (nj.nextModuleId) {
              m1Id = readModule1Journey(nj.nextModuleId)?.module1AttemptId;
            }
          } catch {
            /* ignore */
          }
        }
        const resultsUrl = m1Id
          ? `/test/${moduleId}/results?attemptId=${serverAttemptId}&prevAttemptId=${m1Id}&combined=1`
          : `/test/${moduleId}/results?attemptId=${serverAttemptId}`;

        if (isTelegramJoinedThisSession()) {
          router.push(resultsUrl);
          return;
        }

        setPendingResultsUrl(resultsUrl);
        setShowTelegramModal(true);
        setSubmitting(false);
        return;
      } catch (err) {
        lastError =
          err instanceof DOMException && err.name === "AbortError"
            ? "Save timed out. Your answers are still on this device — retry saving."
            : "Network error. Your answers are still on this device — retry saving.";
        if (i < maxAttempts - 1) {
          await new Promise((res) => setTimeout(res, 400 * 2 ** i));
        }
      }
    }

    setSaveStatus("error");
    setSubmitError(lastError);
    setSubmitting(false);
  }, [submitting, moduleData, attemptId, answers, moduleId, router, authStatus]);

  useEffect(() => { handleSubmitRef.current = handleSubmit; }, [handleSubmit]);

  useEffect(() => {
    if (saveStatus !== "error" && saveStatus !== "saving") return;
    const onBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = "";
    };
    window.addEventListener("beforeunload", onBeforeUnload);
    return () => window.removeEventListener("beforeunload", onBeforeUnload);
  }, [saveStatus]);

  useEffect(() => {
    if (timeLeft === null || paused) return;
    if (timeLeft <= 0) { handleSubmitRef.current(); return; }
    const t = setTimeout(() => setTimeLeft((p) => (p !== null ? p - 1 : null)), 1000);
    return () => clearTimeout(t);
  }, [timeLeft, paused]);

  // Bluebook-style rule: at 5:00 remaining, force the timer visible and lock Hide Timer.
  useEffect(() => {
    if (timeLeft === null) return;
    if (timeLeft <= FIVE_MINUTES_SEC) {
      setHideTimer(false);
      setTimerHideLocked(true);
      if (attemptId) localStorage.setItem(STORAGE_HIDE_TIMER_KEY(attemptId), "0");
    }
  }, [timeLeft, attemptId]);

  useEffect(() => {
    if (!attemptId || timerHideLocked) return;
    localStorage.setItem(STORAGE_HIDE_TIMER_KEY(attemptId), hideTimer ? "1" : "0");
  }, [hideTimer, attemptId, timerHideLocked]);

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

  // Cross-out is controlled via the right-edge badge (click / right-click only).

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

  // Highlight: wrap selected text (supports overlapping / nested double-highlights)
  const handleMouseUp = useCallback(() => {
    if (!highlightMode) return;
    const root = passageRef.current;
    if (!root) return;

    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed) return;

    const range = selection.getRangeAt(0);
    const ancestor = range.commonAncestorContainer;
    if (ancestor !== root && !root.contains(ancestor)) return;

    const applied = applyTextHighlight(root, range);
    selection.removeAllRanges();

    if (applied) {
      const qId = root.dataset.qid;
      if (qId) setHighlights((prev) => ({ ...prev, [qId]: root.innerHTML }));
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
  const showTimerDigits = !hideTimer || timerHideLocked;

  const togglePause = () => setPaused((p) => !p);
  const toggleHideTimer = () => {
    if (timerHideLocked) return;
    setHideTimer((h) => !h);
  };

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

          {/* Center: timer + hide + pause */}
          <div className="flex items-center gap-2 flex-shrink-0">
            <span
              className={`text-lg font-mono font-bold tabular-nums min-w-[4.5rem] text-center ${
                showTimerDigits
                  ? isLow
                    ? "text-red-500"
                    : "text-gray-900"
                  : "text-gray-400"
              }`}
              aria-live="polite"
              aria-label={showTimerDigits ? `Time remaining ${mins} minutes ${secs} seconds` : "Timer hidden"}
            >
              {showTimerDigits ? `${mins}:${secs}` : "--:--"}
            </span>

            <button
              type="button"
              onClick={toggleHideTimer}
              disabled={timerHideLocked}
              title={
                timerHideLocked
                  ? "Timer stays visible in the last 5 minutes"
                  : hideTimer
                    ? "Show timer"
                    : "Hide timer"
              }
              aria-pressed={hideTimer && !timerHideLocked}
              className="flex items-center gap-1 px-2.5 py-0.5 text-xs border border-gray-300 rounded-full hover:bg-gray-100 text-gray-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent"
            >
              {hideTimer && !timerHideLocked ? (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <span className="hidden sm:inline">Show Timer</span>
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <span className="hidden sm:inline">Hide Timer</span>
                </>
              )}
            </button>

            <button
              type="button"
              onClick={togglePause}
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
                  return !p;
                });
              }}
              title={
                highlightMode
                  ? "Exit highlight mode"
                  : "Highlight text (select text; select again to double-highlight)"
              }
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

            {/* Cross-out button intentionally removed:
                elimination is handled by the right-edge badge (click / right-click). */}

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
                  onClick={() => (showDesmos ? closeCalculator() : openCalculator())}
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
              {saveStatus === "saving" ? "Saving…" : submitting ? "Submitting…" : "Submit"}
            </button>
          </div>
        </div>
        {saveStatus === "saving" && (
          <div className="border-t border-violet-100 bg-violet-50 px-4 py-2 text-center">
            <p className="text-xs font-medium text-[#7c3aed]">Saving to your account...</p>
          </div>
        )}
        {saveStatus === "saved" && (
          <div className="border-t border-emerald-100 bg-emerald-50 px-4 py-2 text-center">
            <p className="text-xs font-medium text-emerald-700">✓ Saved to Account</p>
          </div>
        )}
        {(saveStatus === "error" || submitError) && (
          <div className="border-t border-red-200 bg-red-50 px-4 py-2.5 flex flex-wrap items-center justify-center gap-3">
            <p className="text-sm font-semibold text-red-800">
              ⚠ Couldn&apos;t save your attempt{submitError ? ` — ${submitError}` : ""}
            </p>
            {authStatus !== "authenticated" ? (
              <a
                href={`/auth/signin?callbackUrl=${encodeURIComponent(`/test/${moduleId}?attemptId=${attemptId}`)}`}
                className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-[#7c3aed] text-white hover:bg-[#6d28d9]"
              >
                Sign In to Save
              </a>
            ) : (
              <button
                type="button"
                onClick={() => void handleSubmit()}
                disabled={submitting}
                className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-60"
              >
                Retry Saving
              </button>
            )}
          </div>
        )}

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

                    {/* Right-edge Cross-Out badge — click only (no hover toggle) */}
                    <button
                      type="button"
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        handleEliminateClick(q.id, letter);
                      }}
                      onMouseDown={(e) => {
                        // Keep focus/selection on the badge; never bubble into choice selection.
                        e.preventDefault();
                        e.stopPropagation();
                      }}
                      title={eliminated ? `Restore ${letter}` : `Cross out ${letter}`}
                      aria-label={
                        eliminated
                          ? `Cross-out badge ${letter}, active`
                          : `Cross-out badge ${letter}`
                      }
                      aria-pressed={eliminated}
                      className="flex-shrink-0 ml-1.5 min-w-11 w-11 self-stretch flex items-center justify-center rounded-lg hover:bg-gray-100 active:bg-gray-200 transition-colors"
                    >
                      <span
                        className={`relative w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold leading-none transition-colors pointer-events-none ${
                          eliminated
                            ? "border-gray-700 bg-gray-100 text-gray-800"
                            : "border-gray-400 text-gray-700"
                        }`}
                        aria-hidden
                      >
                        {letter}
                        {eliminated && (
                          <span className="absolute inset-0 flex items-center justify-center">
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
        submitError={submitError}
        moduleNumber={moduleData.number}
        questions={questions}
        answers={answers}
        markedForReview={markedForReview}
        onNavigate={setCurrent}
      />

      <Module1PathModal
        open={showModule1PathModal}
        submitting={submitting}
        onBack={() => setShowModule1PathModal(false)}
        onFinishTest={() => {
          if (!submittedAttemptId) return;
          const resultsUrl = `/test/${moduleId}/results?attemptId=${submittedAttemptId}&solo=1`;
          setShowModule1PathModal(false);
          if (isTelegramJoinedThisSession()) {
            router.push(resultsUrl);
            return;
          }
          setPendingResultsUrl(resultsUrl);
          setShowTelegramModal(true);
        }}
        onContinueModule2={() => {
          if (!nextModuleId) {
            setShowModule1PathModal(false);
            setSubmitError("Module 2 is not available for this test.");
            return;
          }
          setShowModule1PathModal(false);
          const nextAttemptId = crypto.randomUUID();
          router.push(`/test/${nextModuleId}?attemptId=${nextAttemptId}`);
        }}
      />

      <TelegramCommunityCheckModal
        open={showTelegramModal}
        mode="post-test"
        onClose={() => setShowTelegramModal(false)}
        onJoin={() => {
          setShowTelegramModal(false);
          const url = pendingResultsUrl;
          setPendingResultsUrl(null);
          if (url) router.push(url);
        }}
        onAlreadyJoined={() => {
          setShowTelegramModal(false);
          const url = pendingResultsUrl;
          setPendingResultsUrl(null);
          if (url) router.push(url);
        }}
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
        <DesmosCalculatorModal open={showDesmos} onClose={closeCalculator} />
      )}
    </div>
  );
}
