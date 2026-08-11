import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

// POST /api/admin/parse-pdf
// multipart/form-data: file (PDF), year, month, section, moduleNumber, timeLimit, testId (optional), isAnswerKey
export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== "admin") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const formData = await req.formData();
  const file = formData.get("file") as File | null;

  if (!file) {
    return NextResponse.json({ error: "No file provided" }, { status: 400 });
  }

  const arrayBuffer = await file.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);

  // Dynamic import to avoid issues with pdf-parse on edge
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const pdfParse = require("pdf-parse");
  const data = await pdfParse(buffer);
  const rawText = data.text;

  const isAnswerKey = formData.get("isAnswerKey") === "true";

  if (isAnswerKey) {
    // Parse answer key: lines like "1. A" or "1 A" or "1) A"
    const answers = parseAnswerKey(rawText);
    return NextResponse.json({ type: "answerKey", answers });
  }

  // Parse questions
  const questions = parseQuestions(rawText);
  return NextResponse.json({ type: "questions", questions, rawText: rawText.slice(0, 2000) });
}

function parseAnswerKey(text: string): { number: number; answer: string }[] {
  const results: { number: number; answer: string }[] = [];
  const lines = text.split("\n");
  for (const line of lines) {
    const match = line.trim().match(/^(\d+)[.):\s]+([ABCD])\b/i);
    if (match) {
      results.push({ number: parseInt(match[1]), answer: match[2].toUpperCase() });
    }
  }
  return results;
}

function parseQuestions(text: string): ParsedQuestion[] {
  const questions: ParsedQuestion[] = [];

  // Split by question number pattern: newline + number + period/dot
  const questionPattern = /\n(\d+)\.\s+/g;
  const parts = text.split(questionPattern);

  // parts: [prefix, num, text, num, text, ...]
  for (let i = 1; i < parts.length; i += 2) {
    const num = parseInt(parts[i]);
    const body = parts[i + 1] || "";

    // Try to extract choices A-D
    const choicePattern = new RegExp("\\n([A-D])[.)]\\s+(.+?)(?=\\n[A-D][.)]|\\n\\d+\\.|\\n*$)", "gs");
    const choices: Record<string, string> = {};
    let questionText = body;

    const choiceMatches = [...body.matchAll(choicePattern)];
    if (choiceMatches.length >= 2) {
      const firstChoiceIdx = body.search(/\n[A-D][.)]/);
      if (firstChoiceIdx > 0) {
        questionText = body.slice(0, firstChoiceIdx).trim();
      }
      for (const m of choiceMatches) {
        choices[m[1]] = m[2].trim().replace(/\n/g, " ");
      }
    }

    if (questionText.trim()) {
      questions.push({
        order: num,
        text: questionText.trim().replace(/\n/g, " "),
        choices:
          Object.keys(choices).length >= 2
            ? choices
            : { A: "", B: "", C: "", D: "" },
        correctAnswer: "",
      });
    }
  }

  return questions;
}

export interface ParsedQuestion {
  order: number;
  text: string;
  choices: Record<string, string>;
  correctAnswer: string;
}

// POST /api/admin/save-questions
// Save parsed (and reviewed) questions to DB
export async function PUT(req: NextRequest) {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== "admin") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const { moduleId, questions } = await req.json();

  const created = await prisma.$transaction(
    questions.map((q: { order: number; text: string; choices: Record<string, string>; correctAnswer: string; imageUrl?: string; explanation?: string }) =>
      prisma.question.create({
        data: {
          moduleId,
          order: q.order,
          text: q.text,
          imageUrl: q.imageUrl ?? null,
          choices: JSON.stringify(q.choices),
          correctAnswer: q.correctAnswer,
          explanation: q.explanation ?? null,
        },
      })
    )
  );

  return NextResponse.json({ saved: created.length });
}
