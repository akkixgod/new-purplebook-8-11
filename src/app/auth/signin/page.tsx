"use client";

import { useEffect, useState } from "react";
import { signIn, getProviders } from "next-auth/react";
import Link from "next/link";

const inputClass =
  "w-full px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#7c3aed] focus:border-transparent text-sm transition-colors";

const AUTH_BACKUP_STORAGE_PREFIX = "purplebook_auth_backup_v1:";

function backupStorageKey(email: string) {
  return `${AUTH_BACKUP_STORAGE_PREFIX}${email.trim().toLowerCase()}`;
}

function readStoredBackup(email: string): string {
  try {
    return localStorage.getItem(backupStorageKey(email)) ?? "";
  } catch {
    return "";
  }
}

function writeStoredBackup(email: string, token: string) {
  try {
    localStorage.setItem(backupStorageKey(email), token);
  } catch {
    /* private mode / quota */
  }
}

export default function SignInPage() {
  const [mode, setMode] = useState<"signin" | "register">("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleEnabled, setGoogleEnabled] = useState(false);
  const [callbackUrl, setCallbackUrl] = useState("/");

  useEffect(() => {
    getProviders().then((providers) => {
      setGoogleEnabled(Boolean(providers?.google));
    }).catch(() => setGoogleEnabled(false));

    try {
      const params = new URLSearchParams(window.location.search);
      const next = params.get("callbackUrl");
      if (next && next.startsWith("/") && !next.startsWith("//")) {
        setCallbackUrl(next);
      }
    } catch {
      /* ignore */
    }
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const normalizedEmail = email.trim().toLowerCase();

      if (mode === "register") {
        if (password.length < 6) {
          setError("Password must be at least 6 characters");
          setLoading(false);
          return;
        }

        const res = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: name.trim(), email: normalizedEmail, password }),
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          setError(data.error ?? "Registration failed");
          setLoading(false);
          return;
        }
        if (typeof data.authBackup === "string" && data.authBackup) {
          writeStoredBackup(normalizedEmail, data.authBackup);
        }
      }

      const backup = readStoredBackup(normalizedEmail);
      const result = await signIn("credentials", {
        email: normalizedEmail,
        password,
        backup,
        redirect: false,
      });

      if (result?.error) {
        const code = (result as { code?: string }).code ?? "";
        if (mode === "register") {
          setError(
            "Account was saved, but automatic sign-in failed. Try signing in again with the same email and password."
          );
        } else if (code === "service_error" || result.error === "Configuration") {
          setError("Sign-in temporarily unavailable. Please try again in a moment.");
        } else if (code === "no_password") {
          setError(
            "This account has no password. Continue with Google if you used that before, or register a new account."
          );
        } else {
          setError("Invalid email or password");
        }
        setLoading(false);
        return;
      }

      // Refresh signed backup (httpOnly cookie + localStorage) so later logins
      // can rehydrate the User row on a new ephemeral SQLite isolate.
      try {
        const br = await fetch("/api/auth/issue-backup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: normalizedEmail, password }),
        });
        const bj = await br.json().catch(() => ({}));
        if (br.ok && typeof bj.authBackup === "string") {
          writeStoredBackup(normalizedEmail, bj.authBackup);
        }
      } catch {
        /* non-fatal */
      }

      // Full navigation so the session cookie is picked up reliably
      window.location.assign(callbackUrl || "/");
    } catch {
      setError("Something went wrong. Please try again.");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link href="/" className="text-3xl font-bold text-[#7c3aed]">
            PurpleBook.cc
          </Link>
          <p className="text-sm text-gray-500 mt-1">SAT Practice Platform</p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
          <div className="flex rounded-xl bg-gray-100 p-1 mb-6">
            {(["signin", "register"] as const).map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => {
                  setMode(m);
                  setError("");
                }}
                className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${
                  mode === m
                    ? "bg-white text-[#7c3aed] shadow-sm"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                {m === "signin" ? "Sign In" : "Register"}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                  className={inputClass}
                  autoComplete="name"
                />
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                className={inputClass}
                autoComplete="email"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 6 characters"
                required
                minLength={6}
                className={inputClass}
                autoComplete={mode === "register" ? "new-password" : "current-password"}
              />
            </div>

            {error && (
              <div className="px-3 py-2 rounded-lg bg-red-50 border border-red-200">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white font-medium text-sm transition-colors disabled:opacity-60 mt-2"
            >
              {loading ? "Please wait..." : mode === "signin" ? "Sign In" : "Create Account"}
            </button>
          </form>

          {googleEnabled && (
            <>
              <div className="relative my-5">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-200" />
                </div>
                <div className="relative flex justify-center text-xs">
                  <span className="bg-white px-3 text-gray-400">or</span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => signIn("google", { callbackUrl })}
                className="w-full py-2.5 rounded-lg border border-gray-200 bg-white text-gray-700 text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                </svg>
                Continue with Google
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
