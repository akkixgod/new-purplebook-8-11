import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { requireSessionUserId, UnauthenticatedError } from "@/lib/require-session-user";

type ClaimItem = { attemptId?: string; claimToken?: string };

/**
 * POST /api/attempts/claim
 * Bind guest (userId=null) completed attempts to the signed-in user.
 * Body: { claims: { attemptId, claimToken }[] }
 */
export async function POST(req: NextRequest) {
  try {
    let userId: string;
    try {
      userId = await requireSessionUserId();
    } catch (error) {
      if (error instanceof UnauthenticatedError) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
      }
      throw error;
    }

    const body = await req.json().catch(() => null);
    const claims = Array.isArray(body?.claims) ? (body.claims as ClaimItem[]) : [];
    if (claims.length === 0) {
      return NextResponse.json({ claimed: 0, attemptIds: [] });
    }

    const claimed: string[] = [];
    for (const item of claims.slice(0, 40)) {
      const attemptId = typeof item.attemptId === "string" ? item.attemptId : "";
      const claimToken = typeof item.claimToken === "string" ? item.claimToken : "";
      if (!attemptId || !claimToken) continue;

      const result = await prisma.attempt.updateMany({
        where: {
          id: attemptId,
          claimToken,
          userId: null,
        },
        data: {
          userId,
          claimToken: null,
        },
      });
      if (result.count > 0) claimed.push(attemptId);
    }

    console.info("[attempts/claim] bound attempts", {
      userId,
      claimed: claimed.length,
      attemptIds: claimed,
    });

    return NextResponse.json({ claimed: claimed.length, attemptIds: claimed });
  } catch (error) {
    console.error("[attempts/claim] unexpected error", error);
    return NextResponse.json({ error: "Failed to claim attempts" }, { status: 500 });
  }
}
