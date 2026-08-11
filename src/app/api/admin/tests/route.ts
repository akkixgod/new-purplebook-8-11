import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { auth } from "@/lib/auth";

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== "admin") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const { title, year, month, section, version, isFree, modules } = await req.json();

  const test = await prisma.test.create({
    data: {
      title,
      year: parseInt(year),
      month: parseInt(month),
      section: section.toUpperCase(),
      version: version ?? null,
      isFree: isFree ?? true,
      modules: {
        create: (modules as { number: number; timeLimit: number }[]).map((m) => ({
          number: m.number,
          timeLimit: m.timeLimit,
        })),
      },
    },
    include: { modules: true },
  });

  return NextResponse.json(test, { status: 201 });
}

export async function GET() {
  const session = await auth();
  if (!session?.user || (session.user as { role?: string }).role !== "admin") {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const tests = await prisma.test.findMany({
    include: {
      modules: {
        include: { _count: { select: { questions: true } } },
        orderBy: { number: "asc" },
      },
    },
    orderBy: [{ year: "desc" }, { month: "desc" }],
  });

  return NextResponse.json(tests);
}
