import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requireSessionUserId, UnauthenticatedError } from "@/lib/require-session-user";

function jsonError(error: string, status: number) {
  return NextResponse.json({ error }, { status });
}

async function sessionUserId() {
  try {
    return await requireSessionUserId();
  } catch (error) {
    if (error instanceof UnauthenticatedError) {
      return null;
    }
    throw error;
  }
}

// GET /api/attempts/[id] — get attempt details with answers for review page
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const userId = await sessionUserId();
    if (!userId) {
      return jsonError("Unauthorized", 401);
    }

    const { id } = await params;
    if (!id) {
      return jsonError("Missing attempt id", 400);
    }

    const attempt = await prisma.attempt.findUnique({
      where: { id },
      include: {
        module: {
          include: {
            test: { select: { title: true, section: true, year: true, month: true } },
            questions: { orderBy: { order: "asc" } },
          },
        },
        answers: true,
      },
    });

    if (!attempt || attempt.userId !== userId) {
      return jsonError("Not found", 404);
    }

    if (!attempt.module) {
      console.error("Results page error: attempt missing module relation", { attemptId: id });
      return jsonError("Attempt module missing", 500);
    }

    if (!attempt.module.test) {
      console.error("Results page error: module missing test relation", {
        attemptId: id,
        moduleId: attempt.moduleId,
      });
      return jsonError("Attempt test missing", 500);
    }

    const questions = attempt.module.questions ?? [];
    const answers = attempt.answers ?? [];
    const totalQuestions =
      attempt.totalQuestions != null && attempt.totalQuestions > 0
        ? attempt.totalQuestions
        : questions.length;
    const score = attempt.score ?? 0;

    return NextResponse.json(
      {
        ...attempt,
        score,
        totalQuestions,
        answers,
        module: {
          ...attempt.module,
          questions,
          test: attempt.module.test,
        },
      },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  } catch (error) {
    console.error("Results page error:", error);
    return jsonError("Failed to load attempt", 500);
  }
}

/** DELETE /api/attempts/[id] — remove a completed attempt from the user's history */
export async function DELETE(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const userId = await sessionUserId();
    if (!userId) {
      return jsonError("Unauthorized", 401);
    }

    const { id } = await params;
    if (!id) {
      return jsonError("Missing attempt id", 400);
    }

    const existing = await prisma.attempt.findUnique({
      where: { id },
      select: { id: true, userId: true },
    });

    if (!existing || existing.userId !== userId) {
      return jsonError("Not found", 404);
    }

    await prisma.attempt.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Delete attempt error:", error);
    return jsonError("Failed to delete attempt", 500);
  }
}
