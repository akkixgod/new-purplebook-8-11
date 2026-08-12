import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";
/** GET /api/account/attempts — completed practice history for the signed-in user */
export async function GET() {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const userId = await resolveSessionUserId({
      id: session.user.id,
      email: session.user.email,
      name: session.user.name,
      image: session.user.image,
    });

    const attempts = await prisma.attempt.findMany({
      where: {
        userId,
        finishedAt: { not: null },
      },
      orderBy: { finishedAt: "desc" },
      select: {
        id: true,
        score: true,
        totalQuestions: true,
        finishedAt: true,
        timeSpent: true,
        module: {
          select: {
            id: true,
            number: true,
            test: {
              select: {
                id: true,
                title: true,
                section: true,
                year: true,
                month: true,
                version: true,
              },
            },
          },
        },
      },
    });

    const items = attempts.map((a) => {
      const correct = a.score ?? 0;
      const total = a.totalQuestions ?? 0;
      const percent = total > 0 ? Math.round((correct / total) * 100) : 0;
      return {
        id: a.id,
        testTitle: a.module.test.title,
        version: a.module.test.version,
        section: a.module.test.section,
        year: a.module.test.year,
        month: a.module.test.month,
        moduleNumber: a.module.number,
        moduleId: a.module.id,
        finishedAt: a.finishedAt?.toISOString() ?? null,
        timeSpent: a.timeSpent,
        correct,
        totalQuestions: total,
        // Per-module history uses raw accuracy only; 200–800 is for full M1+M2 results.
        percent,
      };
    });

    console.info("[account/attempts] loaded", {
      userId,
      count: items.length,
    });

    return NextResponse.json({
      user: {
        id: userId,
        email: session.user.email ?? null,
        name: session.user.name ?? null,
      },
      attempts: items,
    });
  } catch (error) {
    console.error("[account/attempts] unexpected error", error);
    return NextResponse.json({ error: "Failed to load history" }, { status: 500 });
  }
}
