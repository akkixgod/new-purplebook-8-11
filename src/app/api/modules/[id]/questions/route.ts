import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

// Small in-memory cache: module question payload is large, and many users may start
// the same module around the same time. This avoids repeated Prisma query + JSON
// serialization during initial redirects.
const CACHE_TTL_MS = 30_000;
type CacheEntry = { expiresAt: number; data: unknown };
const globalCache = globalThis as unknown as { __moduleQuestionsCache?: Map<string, CacheEntry> };
const moduleQuestionsCache =
  globalCache.__moduleQuestionsCache ?? new Map<string, CacheEntry>();
globalCache.__moduleQuestionsCache = moduleQuestionsCache;

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;

  const now = Date.now();
  const cached = moduleQuestionsCache.get(id);
  if (cached && cached.expiresAt > now) {
    return NextResponse.json(cached.data);
  }

  const module_ = await prisma.module.findUnique({
    where: { id },
    include: {
      // Keep shape compatible with client expectations, but select only the fields we render.
      // This reduces payload size and speeds up JSON serialization.
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
        },
      },
      test: { select: { title: true, section: true, year: true, month: true } },
    },
  });

  if (!module_) {
    return NextResponse.json({ error: "Module not found" }, { status: 404 });
  }

  const payload = module_;
  moduleQuestionsCache.set(id, { expiresAt: now + CACHE_TTL_MS, data: payload });
  return NextResponse.json(payload);
}
