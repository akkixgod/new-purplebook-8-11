import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

// POST /api/attempts/[id]/submit
// Body: { answers: { questionId: string, selected: string | null }[], timeSpent: number }
export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const { answers, timeSpent } = await req.json();

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

  const questionMap = new Map(attempt.module.questions.map((q) => [q.id, q]));

  let score = 0;
  const answerData = (answers as { questionId: string; selected: string | null }[]).map((a) => {
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

  await prisma.$transaction([
    prisma.answer.createMany({ data: answerData }),
    prisma.attempt.update({
      where: { id },
      data: {
        finishedAt: new Date(),
        score,
        totalQuestions: attempt.module.questions.length,
        timeSpent: timeSpent ?? null,
      },
    }),
  ]);

  return NextResponse.json({ score, total: attempt.module.questions.length });
}
