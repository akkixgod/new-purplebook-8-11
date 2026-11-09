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
  let attemptMapError: string | null = null;
  let canonicalUserId: string | null = null;

  try {
    const userId = await requireSessionUserId();
    canonicalUserId = userId;
    const moduleIds = tests.flatMap((t: (typeof tests)[number]) =>
      t.modules.map((m: (typeof t.modules)[number]) => m.id)
    );
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
    if (error instanceof UnauthenticatedError) {
      // Guest catalog — empty attemptMap is expected.
    } else {
      console.warn("[tests] skipped attemptMap — session resolve failed", error);
      attemptMapError = "Failed to load practice history. Retrying may help.";
    }
  }

  return NextResponse.json(
    { tests, attemptMap, attemptMapError, canonicalUserId },
    { headers: { "Cache-Control": "no-store, max-age=0" } }
  );
}
