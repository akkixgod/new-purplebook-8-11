import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

// POST /api/attempts — start a new attempt
export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { moduleId } = await req.json();

  const attempt = await prisma.attempt.create({
    data: {
      userId: session.user.id,
      moduleId,
    },
    select: { id: true },
  });

  return NextResponse.json(attempt, { status: 201 });
}
