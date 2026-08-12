import { NextRequest, NextResponse } from "next/server";
import { Prisma } from "@prisma/client";
import { prisma } from "@/lib/prisma";
import { isClientAttemptId } from "@/lib/attempt-id";
import { requireSessionUserId, UnauthenticatedError } from "@/lib/require-session-user";

type AnswerIn = { questionId: string; selected: string | null };

function jsonError(error: string, status: number, extra?: Record<string, unknown>) {
  return NextResponse.json({ error, ...extra }, { status });
}

/**
 * POST /api/attempts/complete
 * Idempotent finish: client UUID is Attempt.id. userId comes only from the session.
 */
export async function POST(req: NextRequest) {
  try {
    let userId: string;
    try {
      userId = await requireSessionUserId();
    } catch (error) {
      if (error instanceof UnauthenticatedError) {
        console.warn("[attempts/complete] rejected unauthenticated submit");
        return jsonError("Sign in required to save your practice attempt.", 401);
      }
      console.error("[attempts/complete] resolveSessionUserId failed", error);
      return jsonError("Session expired. Sign in again, then retry submission.", 401);
    }

    const body = await req.json().catch(() => null);
    const moduleId = typeof body?.moduleId === "string" ? body.moduleId : undefined;
    const attemptId = body?.attemptId;
    const answers = body?.answers;
    const timeSpent = body?.timeSpent;

    // Ignore any client-supplied userId.
    if (!isClientAttemptId(attemptId)) {
      return jsonError("Missing or invalid attemptId.", 400);
    }
    if (!moduleId) {
      return jsonError("Missing moduleId", 400);
    }
    if (!Array.isArray(answers)) {
      return jsonError("Invalid answers payload", 400);
    }

    console.info("[attempts/complete] authenticated submit", {
      userId,
      attemptId,
      moduleId,
      answerCount: answers.length,
    });

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
      return jsonError("Module not found", 404);
    }

    const questions = module.questions ?? [];
    const questionMap = new Map(questions.map((q) => [q.id, q]));
    const unknownIds = (answers as AnswerIn[])
      .map((a) => a.questionId)
      .filter((id) => typeof id === "string" && id && !questionMap.has(id));

    if (unknownIds.length > 0) {
      console.error("[attempts/complete] unknown questionIds", {
        moduleId,
        sample: unknownIds.slice(0, 5),
        unknownCount: unknownIds.length,
      });
      return jsonError("Answer payload does not match this module’s questions. Reload and retry.", 400);
    }

    const lastByQuestion = new Map<string, AnswerIn>();
    for (const a of answers as AnswerIn[]) {
      if (typeof a?.questionId === "string" && a.questionId) {
        lastByQuestion.set(a.questionId, a);
      }
    }

    let score = 0;
    const answerRows = [...lastByQuestion.values()].map((a) => {
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
    const timeSpentVal = typeof timeSpent === "number" ? timeSpent : null;

    type PersistResult = {
      id: string;
      userId: string | null;
      startedAt: Date;
      finishedAt: Date | null;
      timeSpent: number | null;
      idempotent: boolean;
    };

    let persisted: PersistResult;
    try {
      persisted = await prisma.$transaction(async (tx) => {
        const existing = await tx.attempt.findUnique({
          where: { id: attemptId },
          select: { id: true, userId: true, moduleId: true, finishedAt: true, startedAt: true, timeSpent: true },
        });

        if (existing) {
          if (existing.userId && existing.userId !== userId) {
            throw new Error("ATTEMPT_OWNED_BY_OTHER");
          }
          if (existing.moduleId !== moduleId) {
            throw new Error("ATTEMPT_MODULE_MISMATCH");
          }

          if (existing.finishedAt) {
            return {
              id: existing.id,
              userId: existing.userId,
              startedAt: existing.startedAt,
              finishedAt: existing.finishedAt,
              timeSpent: existing.timeSpent,
              idempotent: true,
            };
          }

          await tx.answer.deleteMany({ where: { attemptId } });
          const updated = await tx.attempt.update({
            where: { id: attemptId },
            data: {
              userId,
              claimToken: null,
              finishedAt,
              score,
              totalQuestions: total,
              timeSpent: timeSpentVal,
            },
          });
          if (answerRows.length > 0) {
            await tx.answer.createMany({
              data: answerRows.map((row) => ({ ...row, attemptId })),
            });
          }
          return {
            id: updated.id,
            userId: updated.userId,
            startedAt: updated.startedAt,
            finishedAt: updated.finishedAt,
            timeSpent: updated.timeSpent,
            idempotent: false,
          };
        }

        const created = await tx.attempt.create({
          data: {
            id: attemptId,
            userId,
            moduleId,
            claimToken: null,
            finishedAt,
            score,
            totalQuestions: total,
            timeSpent: timeSpentVal,
          },
        });
        if (answerRows.length > 0) {
          await tx.answer.createMany({
            data: answerRows.map((row) => ({ ...row, attemptId: created.id })),
          });
        }
        return {
          id: created.id,
          userId: created.userId,
          startedAt: created.startedAt,
          finishedAt: created.finishedAt,
          timeSpent: created.timeSpent,
          idempotent: false,
        };
      });
    } catch (dbError) {
      if (dbError instanceof Error && dbError.message === "ATTEMPT_OWNED_BY_OTHER") {
        return jsonError("Not found", 404);
      }
      if (dbError instanceof Error && dbError.message === "ATTEMPT_MODULE_MISMATCH") {
        return jsonError("This attempt belongs to a different module.", 409);
      }
      if (dbError instanceof Prisma.PrismaClientKnownRequestError && dbError.code === "P2002") {
        // Race: another request inserted the same attemptId. Re-read and treat as idempotent if owned.
        const raced = await prisma.attempt.findUnique({
          where: { id: attemptId },
          select: { id: true, userId: true, finishedAt: true, startedAt: true, timeSpent: true, score: true, totalQuestions: true },
        });
        if (raced?.userId === userId && raced.finishedAt) {
          persisted = {
            id: raced.id,
            userId: raced.userId,
            startedAt: raced.startedAt,
            finishedAt: raced.finishedAt,
            timeSpent: raced.timeSpent,
            idempotent: true,
          };
        } else {
          console.error("[attempts/complete] unique race without owned row", { attemptId, userId });
          return jsonError("Could not save this attempt. Please retry.", 409);
        }
      } else {
        console.error("[attempts/complete] database write failed", {
          moduleId,
          attemptId,
          userId,
          error: dbError instanceof Error ? dbError.message : dbError,
        });
        return jsonError(
          "Database could not save this attempt (schema or foreign-key error). Check server logs.",
          500
        );
      }
    }

    const verified = await prisma.attempt.findUnique({
      where: { id: persisted.id },
      select: { id: true, userId: true, finishedAt: true, score: true, totalQuestions: true },
    });

    if (!verified?.finishedAt || verified.userId !== userId) {
      console.error("[attempts/complete] verification failed", {
        attemptId: persisted.id,
        expectedUserId: userId,
        verified,
      });
      return jsonError("Attempt did not persist to your account. Please retry submission.", 500);
    }

    console.info("[attempts/complete] persisted", {
      attemptId: verified.id,
      userId: verified.userId,
      score: verified.score,
      total: verified.totalQuestions,
      idempotent: persisted.idempotent,
    });

    const storedAnswers = answerRows.map((row, i) => ({
      id: `ans-${i}`,
      attemptId: verified.id,
      questionId: row.questionId,
      selected: row.selected,
      isCorrect: row.isCorrect,
    }));

    return NextResponse.json({
      id: verified.id,
      attemptId: verified.id,
      userId: verified.userId,
      persisted: true,
      idempotent: persisted.idempotent,
      score: verified.score ?? score,
      totalQuestions: verified.totalQuestions ?? total,
      timeSpent: persisted.timeSpent,
      startedAt: persisted.startedAt.toISOString(),
      finishedAt: persisted.finishedAt?.toISOString() ?? null,
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
    return jsonError(message, 500);
  }
}
