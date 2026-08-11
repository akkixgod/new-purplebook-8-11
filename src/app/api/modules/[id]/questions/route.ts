import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

// Module question payload is large; cache across warm serverless instances.
const CACHE_TTL_MS = 120_000;
type CacheEntry = { expiresAt: number; data: unknown };
const globalCache = globalThis as unknown as { __moduleQuestionsCache?: Map<string, CacheEntry> };
const moduleQuestionsCache =
  globalCache.__moduleQuestionsCache ?? new Map<string, CacheEntry>();
globalCache.__moduleQuestionsCache = moduleQuestionsCache;

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const { searchParams } = new URL(req.url);
  const offset = Math.max(0, parseInt(searchParams.get("offset") ?? "0", 10) || 0);
  const limitRaw = searchParams.get("limit");
  const limit = limitRaw ? Math.min(50, Math.max(1, parseInt(limitRaw, 10) || 27)) : null;
  const cacheKey = limit == null ? id : `${id}:o${offset}:l${limit}`;

  const now = Date.now();
  const cached = moduleQuestionsCache.get(cacheKey);
  if (cached && cached.expiresAt > now) {
    return NextResponse.json(cached.data, {
      headers: { "Cache-Control": "private, max-age=60" },
    });
  }

  const module_ = await prisma.module.findUnique({
    where: { id },
    select: {
      id: true,
      number: true,
      timeLimit: true,
      // Take-test payload: omit correctAnswer / explanation (graded only on submit).
      questions: {
        orderBy: { order: "asc" },
        ...(limit != null ? { skip: offset, take: limit } : {}),
        select: {
          id: true,
          order: true,
          stimulus: true,
          text: true,
          imageUrl: true,
          choices: true,
        },
      },
      test: { select: { title: true, section: true, year: true, month: true } },
      _count: { select: { questions: true } },
    },
  });

  if (!module_) {
    return NextResponse.json({ error: "Module not found" }, { status: 404 });
  }

  const payload = {
    id: module_.id,
    number: module_.number,
    timeLimit: module_.timeLimit,
    test: module_.test,
    questions: module_.questions,
    totalQuestions: module_._count.questions,
    offset,
    limit: limit ?? module_._count.questions,
  };

  moduleQuestionsCache.set(cacheKey, { expiresAt: now + CACHE_TTL_MS, data: payload });
  return NextResponse.json(payload, {
    headers: { "Cache-Control": "private, max-age=60" },
  });
}
