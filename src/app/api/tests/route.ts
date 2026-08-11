import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const section = searchParams.get("section");
  const year = searchParams.get("year");
  const month = searchParams.get("month");

  const tests = await prisma.test.findMany({
    where: {
      ...(section ? { section: section.toUpperCase() } : {}),
      ...(year ? { year: parseInt(year) } : {}),
      ...(month ? { month: parseInt(month) } : {}),
    },
    include: {
      modules: {
        select: { id: true, number: true, timeLimit: true, _count: { select: { questions: true } } },
        orderBy: { number: "asc" },
      },
    },
    orderBy: [{ year: "desc" }, { month: "desc" }],
  });

  // Get user attempts if logged in
  const session = await auth();
  let attemptMap: Record<string, { score: number; totalQuestions: number; id: string }> = {};

  if (session?.user?.id) {
    const attempts = await prisma.attempt.findMany({
      where: {
        userId: session.user.id,
        finishedAt: { not: null },
        moduleId: { in: tests.flatMap((t) => t.modules.map((m) => m.id)) },
      },
      orderBy: { finishedAt: "desc" },
    });

    for (const a of attempts) {
      if (!attemptMap[a.moduleId]) {
        attemptMap[a.moduleId] = {
          id: a.id,
          score: a.score ?? 0,
          totalQuestions: a.totalQuestions ?? 0,
        };
      }
    }
  }

  return NextResponse.json({ tests, attemptMap });
}
