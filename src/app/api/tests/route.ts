import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requireSessionUserId, UnauthenticatedError } from "@/lib/require-session-user";

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

  let attemptMap: Record<string, { score: number; totalQuestions: number; id: string }> = {};

  try {
    const userId = await requireSessionUserId();
    const moduleIds = tests.flatMap((t) => t.modules.map((m) => m.id));
    const attempts = await prisma.attempt.findMany({
      where: {
        userId,
        finishedAt: { not: null },
        moduleId: { in: moduleIds },
      },
      orderBy: { finishedAt: "desc" },
      select: {
        id: true,
        moduleId: true,
        score: true,
        totalQuestions: true,
      },
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
  } catch (error) {
    if (!(error instanceof UnauthenticatedError)) {
      console.warn("[tests] skipped attemptMap — session resolve failed", error);
    }
  }

  return NextResponse.json(
    { tests, attemptMap },
    { headers: { "Cache-Control": "no-store, max-age=0" } }
  );
}
