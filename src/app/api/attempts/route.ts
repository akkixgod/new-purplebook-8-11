import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { isClientAttemptId } from "@/lib/attempt-id";
import { requireSessionUserId, UnauthenticatedError } from "@/lib/require-session-user";

// POST /api/attempts — start a new in-progress attempt (optional; complete can create on submit)
export async function POST(req: NextRequest) {
  try {
    const userId = await requireSessionUserId();
    const body = await req.json().catch(() => null);
    const moduleId = typeof body?.moduleId === "string" ? body.moduleId : "";
    const clientId = body?.attemptId;

    if (!moduleId) {
      return NextResponse.json({ error: "Missing moduleId" }, { status: 400 });
    }

    const module = await prisma.module.findUnique({ where: { id: moduleId }, select: { id: true } });
    if (!module) {
      return NextResponse.json({ error: "Module not found" }, { status: 404 });
    }

    if (isClientAttemptId(clientId)) {
      const existing = await prisma.attempt.findUnique({
        where: { id: clientId },
        select: { id: true, userId: true },
      });
      if (existing) {
        if (existing.userId && existing.userId !== userId) {
          return NextResponse.json({ error: "Not found" }, { status: 404 });
        }
        return NextResponse.json({ id: existing.id }, { status: 200 });
      }
      const attempt = await prisma.attempt.create({
        data: { id: clientId, userId, moduleId },
        select: { id: true },
      });
      return NextResponse.json(attempt, { status: 201 });
    }

    const attempt = await prisma.attempt.create({
      data: { userId, moduleId },
      select: { id: true },
    });
    return NextResponse.json(attempt, { status: 201 });
  } catch (error) {
    if (error instanceof UnauthenticatedError) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    console.error("[attempts] start failed", error);
    return NextResponse.json({ error: "Failed to start attempt" }, { status: 500 });
  }
}
