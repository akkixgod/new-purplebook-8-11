import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

// POST /api/attempts/[id]/submit
// Body: { answers: { questionId: string, selected: string | null }[], timeSpent: number }
export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { id } = await params;
    const body = await req.json().catch(() => null);
    const answers = body?.answers;
    const timeSpent = body?.timeSpent;

    if (!Array.isArray(answers)) {
      return NextResponse.json({ error: "Invalid answers payload" }, { status: 400 });
    }

    const attempt = await prisma.attempt.findUnique({
      where: { id },
      include: { module: { include: { questions: true } } },
    });

    if (!attempt || attempt.userId !== session.user.id) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    if (attempt.finishedAt) {
      return NextResponse.json({ error: "Already submitted" }, { status: 409 });
    }

    if (!attempt.module) {
      console.error("Results page error: submit attempt missing module", { attemptId: id });
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

    return NextResponse.json({ score, total });
  } catch (error) {
    console.error("Results page error:", error);
    return NextResponse.json({ error: "Failed to submit attempt" }, { status: 500 });
  }
}
