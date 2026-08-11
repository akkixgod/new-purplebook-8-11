import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

// POST /api/attempts/complete — create + grade + finish in one request (serverless-safe)
export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const body = await req.json().catch(() => null);
    const moduleId = body?.moduleId as string | undefined;
    const answers = body?.answers;
    const timeSpent = body?.timeSpent;

    if (!moduleId) {
      return NextResponse.json({ error: "Missing moduleId" }, { status: 400 });
    }
    if (!Array.isArray(answers)) {
      return NextResponse.json({ error: "Invalid answers payload" }, { status: 400 });
    }

    const module = await prisma.module.findUnique({
      where: { id: moduleId },
      include: {
        test: { select: { title: true, section: true, year: true, month: true } },
        questions: { orderBy: { order: "asc" } },
      },
    });

    if (!module?.test) {
      return NextResponse.json({ error: "Module not found" }, { status: 404 });
    }

    const questions = module.questions ?? [];
    const questionMap = new Map(questions.map((q) => [q.id, q]));

    let score = 0;
    const answerRows = (
      answers as { questionId: string; selected: string | null }[]
    ).map((a) => {
      const q = questionMap.get(a.questionId);
      const isCorrect = !!q && a.selected === q.correctAnswer;
      if (isCorrect) score++;
      return {
        questionId: a.questionId,
        selected: a.selected,
        isCorrect,
      };
    });

    const total = questions.length;
    const finishedAt = new Date();

    const attempt = await prisma.$transaction(async (tx) => {
      const created = await tx.attempt.create({
        data: {
          userId: session.user.id,
          moduleId,
          finishedAt,
          score,
          totalQuestions: total,
          timeSpent: typeof timeSpent === "number" ? timeSpent : null,
        },
      });

      await tx.answer.createMany({
        data: answerRows.map((row) => ({ ...row, attemptId: created.id })),
      });

      return created;
    });

    const storedAnswers = await prisma.answer.findMany({
      where: { attemptId: attempt.id },
    });

    return NextResponse.json({
      id: attempt.id,
      attemptId: attempt.id,
      score,
      totalQuestions: total,
      timeSpent: attempt.timeSpent,
      startedAt: attempt.startedAt.toISOString(),
      finishedAt: attempt.finishedAt?.toISOString() ?? null,
      module: {
        number: module.number,
        test: module.test,
        questions,
      },
      answers: storedAnswers,
    });
  } catch (error) {
    console.error("Complete attempt error:", error);
    return NextResponse.json({ error: "Failed to submit attempt" }, { status: 500 });
  }
}
