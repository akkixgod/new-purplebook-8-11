import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  const module_ = await prisma.module.findUnique({
    where: { id },
    include: {
      questions: { orderBy: { order: "asc" } },
      test: { select: { title: true, section: true, year: true, month: true } },
    },
  });

  if (!module_) {
    return NextResponse.json({ error: "Module not found" }, { status: 404 });
  }

  return NextResponse.json(module_);
}
