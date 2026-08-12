import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

/**
 * POST /api/attempts/complete — create + grade + finish in one request.
 * userId is taken only from the server session — never from the client body.
 */
export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      console.warn("[attempts/complete] rejected unauthenticated submit");
      return NextResponse.json(
        { error: "Sign in required to save your practice attempt." },
        { status: 401 }
      );
    }

    // Ignore any client-supplied userId / claimToken — session is the only source of truth.
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

    let userId: string;
    try {
      userId = await resolveSessionUserId({
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
        image: session.user.image,
      });
      console.info("[attempts/complete] authenticated submit", {
        sessionUserId: session.user.id,
        resolvedUserId: userId,
        moduleId,
        answerCount: answers.length,
      });
    } catch (error) {
      console.error("[attempts/complete] resolveSessionUserId failed", error);
      return NextResponse.json(
        { error: "Session expired. Sign in again, then retry submission." },
        { status: 401 }
      );
    }

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
      console.error("[attempts/complete] module not found", { moduleId });
      return NextResponse.json({ error: "Module not found" }, { status: 404 });
    }

    const questions = module.questions ?? [];
    const questionMap = new Map(questions.map((q) => [q.id, q]));
    const unknownIds = (
      answers as { questionId: string; selected: string | null }[]
    )
      .map((a) => a.questionId)
      .filter((id) => typeof id === "string" && id && !questionMap.has(id));

    if (unknownIds.length > 0) {
      console.error("[attempts/complete] unknown questionIds", {
        moduleId,
        sample: unknownIds.slice(0, 5),
        unknownCount: unknownIds.length,
      });
      return NextResponse.json(
        {
          error: "Answer payload does not match this module’s questions. Reload and retry.",
        },
        { status: 400 }
      );
    }

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

    let attempt;
    try {
      attempt = await prisma.$transaction(async (tx) => {
        const created = await tx.attempt.create({
          data: {
            userId,
            moduleId,
            claimToken: null,
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
    } catch (dbError) {
      console.error("[attempts/complete] database write failed", {
        moduleId,
        userId,
        error: dbError instanceof Error ? dbError.message : dbError,
      });
      return NextResponse.json(
        {
          error:
            "Database could not save this attempt (schema or foreign-key error). Check server logs.",
        },
        { status: 500 }
      );
    }

    const verified = await prisma.attempt.findUnique({
      where: { id: attempt.id },
      select: { id: true, userId: true, finishedAt: true, score: true, totalQuestions: true },
    });

    if (!verified?.finishedAt || verified.userId !== userId) {
      console.error("[attempts/complete] verification failed", {
        attemptId: attempt.id,
        expectedUserId: userId,
        verified,
      });
      return NextResponse.json(
        { error: "Attempt did not persist to your account. Please retry submission." },
        { status: 500 }
      );
    }

    console.info("[attempts/complete] persisted", {
      attemptId: attempt.id,
      userId: verified.userId,
      score,
      total,
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
      userId: verified.userId,
      persisted: true,
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
    console.error("[attempts/complete] unexpected error", error);
    const message =
      error instanceof Error && /Unable to resolve session user/i.test(error.message)
        ? "Session expired. Sign in again, then retry submission."
        : "Failed to submit attempt";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
