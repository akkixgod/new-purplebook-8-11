import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

async function ownedAttemptUserId(sessionUser: {
  id: string;
  email?: string | null;
  name?: string | null;
  image?: string | null;
}) {
  return resolveSessionUserId({
    id: sessionUser.id,
    email: sessionUser.email,
    name: sessionUser.name,
    image: sessionUser.image,
  });
}

// GET /api/attempts/[id] — get attempt details with answers for review page
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { id } = await params;
    if (!id) {
      return NextResponse.json({ error: "Missing attempt id" }, { status: 400 });
    }

    const userId = await ownedAttemptUserId(session.user);

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
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    if (!attempt.module) {
      console.error("Results page error: attempt missing module relation", { attemptId: id });
      return NextResponse.json({ error: "Attempt module missing" }, { status: 500 });
    }

    if (!attempt.module.test) {
      console.error("Results page error: module missing test relation", {
        attemptId: id,
        moduleId: attempt.moduleId,
      });
      return NextResponse.json({ error: "Attempt test missing" }, { status: 500 });
    }

    const questions = attempt.module.questions ?? [];
    const answers = attempt.answers ?? [];
    const totalQuestions =
      attempt.totalQuestions != null && attempt.totalQuestions > 0
        ? attempt.totalQuestions
        : questions.length;
    const score = attempt.score ?? 0;

    return NextResponse.json({
      ...attempt,
      score,
      totalQuestions,
      answers,
      module: {
        ...attempt.module,
        questions,
        test: attempt.module.test,
      },
    });
  } catch (error) {
    console.error("Results page error:", error);
    return NextResponse.json(
      { error: "Failed to load attempt" },
      { status: 500 }
    );
  }
}

/** DELETE /api/attempts/[id] — remove a completed attempt from the user's history */
export async function DELETE(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { id } = await params;
    if (!id) {
      return NextResponse.json({ error: "Missing attempt id" }, { status: 400 });
    }

    const userId = await ownedAttemptUserId(session.user);
    const existing = await prisma.attempt.findUnique({
      where: { id },
      select: { id: true, userId: true },
    });

    if (!existing || existing.userId !== userId) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    await prisma.attempt.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Delete attempt error:", error);
    return NextResponse.json({ error: "Failed to delete attempt" }, { status: 500 });
  }
}
