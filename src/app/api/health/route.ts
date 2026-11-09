import { NextResponse } from "next/server";
import { getDbMode } from "@/lib/prisma";

/** GET /api/health — public liveness + db mode (no secrets). */
export async function GET() {
  return NextResponse.json(
    {
      ok: true,
      dbMode: getDbMode(),
      vercel: Boolean(process.env.VERCEL),
    },
    { headers: { "Cache-Control": "no-store, max-age=0" } }
  );
}
