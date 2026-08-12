import { auth } from "@/lib/auth";
import { resolveSessionUserId } from "@/lib/resolve-session-user";

export class UnauthenticatedError extends Error {
  constructor(message = "Unauthorized") {
    super(message);
    this.name = "UnauthenticatedError";
  }
}

/** userId from the server session only — never from a request body. */
export async function requireSessionUserId(): Promise<string> {
  const session = await auth();
  if (!session?.user?.id) {
    throw new UnauthenticatedError();
  }
  return resolveSessionUserId({
    id: session.user.id,
    email: session.user.email,
    name: session.user.name,
    image: session.user.image,
  });
}
