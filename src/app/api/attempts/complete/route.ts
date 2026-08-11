import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

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

    const userId = await resolveSessionUserId({
      id: session.user.id,
      email: session.user.email,
      name: session.user.name,
      image: session.user.image,
    });

    const module = await prisma.module.findUnique({
      where: { id: moduleId },
      select: {
        id: true,
        number: true,
        test: { select: { title: true, section: true, year: true, month: true } },
        questions: {
          orderBy: { order: "asc" },
          select: {
            id: true,
            order: true,
            stimulus: true,
            text: true,
            imageUrl: true,
            choices: true,
            correctAnswer: true,
            explanation: true,
          },
        },
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
          userId,
          moduleId,
          finishedAt,
          score,
          totalQuestions: total,
          timeSpent: typeof timeSpent === "number" ? timeSpent : null,
        },
      });

      if (answerRows.length > 0) {
        await tx.answer.createMany({
          data: answerRows.map((row) => ({ ...row, attemptId: created.id })),
        });
      }

      return created;
    });

    const storedAnswers = answerRows.map((row, i) => ({
      id: `local-${i}`,
      attemptId: attempt.id,
      questionId: row.questionId,
      selected: row.selected,
      isCorrect: row.isCorrect,
    }));

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
    const message =
      error instanceof Error && /Unable to resolve session user/i.test(error.message)
        ? "Session expired. Sign in again, then retry submission."
        : "Failed to submit attempt";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
