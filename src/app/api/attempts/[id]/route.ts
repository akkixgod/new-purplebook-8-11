import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

// GET /api/attempts/[id] — get attempt details with answers for review page
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;

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

  if (!attempt || attempt.userId !== session.user.id) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(attempt);
}
