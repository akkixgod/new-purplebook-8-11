import { createHmac, timingSafeEqual } from "crypto";

export type AuthBackupPayload = {
  v: 1;
  id: string;
  email: string;
  passwordHash: string;
  exp: number;
};

const BACKUP_TTL_MS = 1000 * 60 * 60 * 24 * 180; // 180 days

function hmacSecrets(): string[] {
  const a = process.env.AUTH_SECRET?.trim();
  const b = process.env.NEXTAUTH_SECRET?.trim();
  const list: string[] = [];
  if (a) list.push(a);
  if (b && b !== a) list.push(b);
  return list;
}

function signingSecret(): string {
  const keys = hmacSecrets();
  if (!keys.length) {
    throw new Error("AUTH_SECRET / NEXTAUTH_SECRET is required for auth backup");
  }
  return keys[0];
}

function b64url(input: Buffer | string): string {
  const buf = Buffer.isBuffer(input) ? input : Buffer.from(input, "utf8");
  return buf
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/g, "");
}

function fromB64url(input: string): Buffer {
  const pad = input.length % 4 === 0 ? "" : "=".repeat(4 - (input.length % 4));
  const normalized = input.replace(/-/g, "+").replace(/_/g, "/") + pad;
  return Buffer.from(normalized, "base64");
}

function signatureMatches(body: string, sig: string, secret: string): boolean {
  const expected = createHmac("sha256", secret).update(body).digest();
  const got = fromB64url(sig);
  if (got.length !== expected.length) return false;
  return timingSafeEqual(got, expected);
}

export function createAuthBackup(user: {
  id: string;
  email: string;
  passwordHash: string;
}): string {
  const payload: AuthBackupPayload = {
    v: 1,
    id: user.id,
    email: user.email,
    passwordHash: user.passwordHash,
    exp: Date.now() + BACKUP_TTL_MS,
  };
  const body = b64url(JSON.stringify(payload));
  const sig = b64url(createHmac("sha256", signingSecret()).update(body).digest());
  return `${body}.${sig}`;
}

export function verifyAuthBackup(token: string): AuthBackupPayload | null {
  try {
    const [body, sig] = token.split(".");
    if (!body || !sig) return null;
    const keys = hmacSecrets();
    if (!keys.length || !keys.some((secret) => signatureMatches(body, sig, secret))) {
      return null;
    }
    const payload = JSON.parse(fromB64url(body).toString("utf8")) as AuthBackupPayload;
    if (payload.v !== 1 || !payload.id || !payload.email || !payload.passwordHash) return null;
    if (typeof payload.exp !== "number" || payload.exp < Date.now()) return null;
    return payload;
  } catch {
    return null;
  }
}
