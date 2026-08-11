"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";

interface AnswerRow {
  id: string;
  questionId: string;
  selected: string | null;
  isCorrect: boolean;
}

interface QuestionRow {
  id: string;
  order: number;
  text: string;
  imageUrl: string | null;
  choices: string;
  correctAnswer: string;
  explanation: string | null;
}

interface AttemptDetail {
  id: string;
  score: number;
  totalQuestions: number;
  timeSpent: number | null;
  startedAt: string;
  finishedAt: string | null;
  module: {
    number: number;
    test: { title: string; section: string; year: number; month: number };
    questions: QuestionRow[];
  };
  answers: AnswerRow[];
}

export default function ReviewPage({ params }: { params: Promise<{ attemptId: string }> }) {
  const { attemptId } = use(params);
  const [data, setData] = useState<AttemptDetail | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/attempts/${attemptId}`)
      .then(async (r) => {
        const json = await r.json();
        if (!r.ok) throw new Error(json.error || `Failed to load review (${r.status})`);
        if (!json.module?.test || !Array.isArray(json.module?.questions)) {
          throw new Error("Incomplete attempt data");
        }
        return json as AttemptDetail;
      })
      .then(setData)
      .catch((error: unknown) => {
        console.error("Results page error:", error);
        setData(null);
      });
  }, [attemptId]);

  if (!data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-white px-4">
        <div className="w-8 h-8 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-sm text-gray-500">Loading review…</p>
        <Link href="/" className="mt-4 text-sm text-[#7c3aed] hover:underline">
          Back to Home
        </Link>
      </div>
    );
  }

  const answers = data.answers ?? [];
  const questions = data.module?.questions ?? [];
  const score = data.score ?? 0;
  const totalQuestions = data.totalQuestions ?? questions.length;
  const answerByQuestion = new Map(answers.map((a) => [a.questionId, a]));
  const incorrect = Math.max(0, totalQuestions - score);
  const wrongNums = questions
    .filter((q) => {
      const a = answerByQuestion.get(q.id);
      return a && !a.isCorrect;
    })
    .map((q) => q.order)
    .join(", ");

  const mins = data.timeSpent ? Math.floor(data.timeSpent / 60) : null;
  const secs = data.timeSpent ? (data.timeSpent % 60).toString().padStart(2, "0") : null;

  const finishedDate = data.finishedAt
    ? new Date(data.finishedAt).toLocaleString()
    : "—";

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Back link */}
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-[#7c3aed] mb-6 transition-colors">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </Link>

        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Score Details</h1>

          <div className="mt-3 space-y-1 text-sm text-gray-600">
            <p className="flex items-center gap-2">
              <svg className="w-4 h-4 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {data.module?.test?.title ?? "Practice"} Module {data.module?.number ?? 1}
            </p>
            <p className="flex items-center gap-2">
              <svg className="w-4 h-4 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              {data.module?.test?.section === "MATH" ? "Math" : "Reading and Writing"}
            </p>
            {finishedDate && (
              <p className="flex items-center gap-2">
                <svg className="w-4 h-4 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {finishedDate}
              </p>
            )}
            {mins !== null && (
              <p className="flex items-center gap-2">
                <svg className="w-4 h-4 text-[#7c3aed]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {mins}:{secs}
              </p>
            )}
            {wrongNums && (
              <p className="flex items-center gap-2">
                <svg className="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Wrong: {wrongNums}
              </p>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[
            { label: "Total Questions", value: totalQuestions, color: "text-gray-900" },
            { label: "Correct Answers", value: score, color: "text-[#7c3aed]" },
            { label: "Incorrect Answers", value: incorrect, color: "text-red-500" },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl border border-gray-200 p-4 text-center">
              <div className={`text-3xl font-bold ${s.color}`}>{s.value}</div>
              <div className="text-xs text-gray-500 mt-1">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Questions table */}
        <div className="space-y-3">
          {questions.map((q, i) => {
            const answer = answerByQuestion.get(q.id);
            const isCorrect = answer?.isCorrect ?? false;
            const choices: Record<string, string> = JSON.parse(q.choices);
            const isExpanded = expanded === q.id;

            return (
              <div
                key={q.id}
                className="bg-white rounded-xl border border-gray-200 overflow-hidden"
              >
                {/* Row */}
                <div className="flex items-start gap-4 p-4">
                  {/* Number */}
                  <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-full text-sm font-bold bg-gray-100 text-gray-900">
                    {i + 1}
                  </div>

                  {/* Question text */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900 leading-relaxed line-clamp-2">
                      {q.text}
                    </p>
                  </div>

                  {/* Correct answer */}
                  <div className="text-center w-20 flex-shrink-0">
                    <p className="text-xs text-gray-400 mb-0.5">Correct</p>
                    <p className="text-sm font-semibold text-gray-900">
                      {q.correctAnswer}
                      {choices[q.correctAnswer] && (
                        <span className="block text-xs font-normal text-gray-500 truncate max-w-[80px]">
                          {choices[q.correctAnswer].slice(0, 20)}
                        </span>
                      )}
                    </p>
                  </div>

                  {/* Your answer */}
                  <div className="text-center w-20 flex-shrink-0">
                    <p className="text-xs text-gray-400 mb-0.5">Yours</p>
                    <p className={`text-sm font-semibold ${isCorrect ? "text-[#7c3aed]" : "text-red-500"}`}>
                      {answer?.selected ?? "—"}
                      {answer?.selected && choices[answer.selected] && (
                        <span className="block text-xs font-normal truncate max-w-[80px]">
                          {choices[answer.selected].slice(0, 20)}
                        </span>
                      )}
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center ${isCorrect ? "bg-green-100" : "bg-red-100"}`}>
                      {isCorrect ? (
                        <svg className="w-3 h-3 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      ) : (
                        <svg className="w-3 h-3 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      )}
                    </span>
                    <button
                      onClick={() => setExpanded(isExpanded ? null : q.id)}
                      className="px-3 py-1 text-xs font-medium rounded-lg border border-gray-200 hover:border-[#7c3aed] hover:text-[#7c3aed] transition-colors"
                    >
                      Review
                    </button>
                  </div>
                </div>

                {/* Expanded detail */}
                {isExpanded && (
                  <div className="border-t border-gray-100 p-4 bg-gray-50/50">
                    <p className="text-sm font-medium text-gray-900 mb-3">{q.text}</p>
                    {q.imageUrl && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={q.imageUrl} alt="" className="mb-3 rounded-lg max-w-full border border-gray-200" />
                    )}
                    <div className="space-y-2">
                      {choices.gridIn ? (
                        <div className="text-sm text-gray-700">
                          <span className="font-medium">Correct answer:</span> {q.correctAnswer}
                          {answer?.selected != null && answer.selected !== q.correctAnswer && (
                            <span className="ml-3 text-red-600">Your answer: {answer.selected}</span>
                          )}
                        </div>
                      ) : (
                        (["A", "B", "C", "D"] as const).map((letter) => {
                          if (!(letter in choices)) return null;
                          const isRight = letter === q.correctAnswer;
                          const isSelected = letter === answer?.selected;
                          return (
                            <div
                              key={letter}
                              className={`flex items-start gap-2 px-3 py-2 rounded-lg text-sm ${
                                isRight
                                  ? "bg-[#7c3aed]/10 border border-[#7c3aed]/30 text-[#7c3aed]"
                                  : isSelected && !isRight
                                  ? "bg-red-50 border border-red-200 text-red-600"
                                  : "border border-transparent text-gray-600"
                              }`}
                            >
                              <span className="font-bold w-4">{letter}.</span>
                              <span>{choices[letter]}</span>
                            </div>
                          );
                        })
                      )}
                    </div>
                    {q.explanation && (
                      <div className="mt-3 p-3 rounded-lg bg-blue-50 border border-blue-100">
                        <p className="text-xs font-semibold text-blue-600 mb-1">Explanation</p>
                        <p className="text-xs text-gray-600">{q.explanation}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
