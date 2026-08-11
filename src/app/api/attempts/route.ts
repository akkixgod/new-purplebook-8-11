import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

// POST /api/attempts — start a new attempt
export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { moduleId } = await req.json();
  if (!moduleId || typeof moduleId !== "string") {
    return NextResponse.json({ error: "Missing moduleId" }, { status: 400 });
  }

  const userId = await resolveSessionUserId({
    id: session.user.id,
    email: session.user.email,
    name: session.user.name,
    image: session.user.image,
  });

  const attempt = await prisma.attempt.create({
    data: {
      userId,
      moduleId,
    },
    select: { id: true },
  });

  return NextResponse.json(attempt, { status: 201 });
}
