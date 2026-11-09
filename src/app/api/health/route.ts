import { NextResponse } from "next/server";
import { getDbMode, prisma } from "@/lib/prisma";

/** GET /api/health — public liveness + db mode + round-trip probe (no secrets). */
export async function GET() {
  const dbMode = getDbMode();
  const onVercel = Boolean(process.env.VERCEL);
  const headers = { "Cache-Control": "no-store, max-age=0" };

  if (onVercel && dbMode === "ephemeral") {
    return NextResponse.json(
      {
        ok: false,
        dbMode,
        vercel: true,
        error: "Ephemeral /tmp SQLite is not allowed on Vercel.",
      },
      { status: 503, headers }
    );
  }

  try {
    await prisma.$queryRaw`SELECT 1`;
    return NextResponse.json(
      {
        ok: true,
        dbMode,
        vercel: onVercel,
      },
      { headers }
    );
  } catch (error) {
    console.error("[health] database probe failed", error);
    return NextResponse.json(
      {
        ok: false,
        dbMode,
        vercel: onVercel,
        error: "Database probe failed",
      },
      { status: 503, headers }
    );
  }
}
