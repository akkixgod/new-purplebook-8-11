import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

// POST /api/attempts/[id]/submit
// Body: { answers: { questionId: string, selected: string | null }[], timeSpent: number }
export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      console.warn("[attempts/submit] unauthorized — no session");
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { id } = await params;
    const body = await req.json().catch(() => null);
    const answers = body?.answers;
    const timeSpent = body?.timeSpent;

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
    } catch (error) {
      console.error("[attempts/submit] resolveSessionUserId failed", error);
      return NextResponse.json(
        { error: "Session expired. Sign in again, then retry submission." },
        { status: 401 }
      );
    }

    const attempt = await prisma.attempt.findUnique({
      where: { id },
      include: { module: { include: { questions: true } } },
    });

    if (!attempt || attempt.userId !== userId) {
      console.warn("[attempts/submit] not found or ownership mismatch", {
        attemptId: id,
        userId,
        owner: attempt?.userId ?? null,
      });
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    if (attempt.finishedAt) {
      return NextResponse.json(
        {
          error: "Already submitted",
          score: attempt.score,
          total: attempt.totalQuestions,
          persisted: true,
          userId: attempt.userId,
        },
        { status: 409 }
      );
    }

    if (!attempt.module) {
      console.error("[attempts/submit] attempt missing module", { attemptId: id });
      return NextResponse.json({ error: "Attempt module missing" }, { status: 500 });
    }

    const questions = attempt.module.questions ?? [];
    const questionMap = new Map(questions.map((q) => [q.id, q]));

    let score = 0;
    const answerData = (
      answers as { questionId: string; selected: string | null }[]
    ).map((a) => {
      const q = questionMap.get(a.questionId);
      const isCorrect = !!q && a.selected === q.correctAnswer;
      if (isCorrect) score++;
      return {
        attemptId: id,
        questionId: a.questionId,
        selected: a.selected,
        isCorrect,
      };
    });

    const total = questions.length;

    try {
      await prisma.$transaction([
        prisma.answer.createMany({ data: answerData }),
        prisma.attempt.update({
          where: { id },
          data: {
            finishedAt: new Date(),
            score,
            totalQuestions: total,
            timeSpent: typeof timeSpent === "number" ? timeSpent : null,
          },
        }),
      ]);
    } catch (dbError) {
      console.error("[attempts/submit] database write failed", {
        attemptId: id,
        userId,
        error: dbError instanceof Error ? dbError.message : dbError,
      });
      return NextResponse.json(
        { error: "Database could not save this attempt. Check server logs." },
        { status: 500 }
      );
    }

    console.info("[attempts/submit] persisted", { attemptId: id, userId, score, total });
    return NextResponse.json({ score, total, persisted: true, userId, attemptId: id });
  } catch (error) {
    console.error("[attempts/submit] unexpected error", error);
    return NextResponse.json({ error: "Failed to submit attempt" }, { status: 500 });
  }
}
