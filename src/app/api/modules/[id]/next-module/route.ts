import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

// GET /api/modules/[id]/next-module
// Returns the sibling module within the same test (module 1 <-> module 2) for that test.
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  const current = await prisma.module.findUnique({
    where: { id },
    select: { id: true, number: true, testId: true },
  });

  if (!current) return NextResponse.json({ nextModuleId: null }, { status: 200 });

  const nextNumber = current.number === 1 ? 2 : 1;
  const next = await prisma.module.findFirst({
    where: { testId: current.testId, number: nextNumber },
    select: { id: true },
  });

  return NextResponse.json({ nextModuleId: next?.id ?? null }, { status: 200 });
}

