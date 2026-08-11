"use client";

import { FormEvent, Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

const inputClass =
  "w-full px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#7c3aed] focus:border-transparent text-sm transition-colors";

function passwordStrength(password: string): { score: number; label: string; color: string } {
  let score = 0;
  if (password.length >= 6) score += 1;
  if (password.length >= 10) score += 1;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;

  if (!password) return { score: 0, label: "", color: "bg-gray-200" };
  if (score <= 2) return { score: 1, label: "Weak", color: "bg-red-400" };
  if (score <= 3) return { score: 2, label: "Fair", color: "bg-amber-400" };
  if (score <= 4) return { score: 3, label: "Good", color: "bg-lime-500" };
  return { score: 4, label: "Strong", color: "bg-emerald-500" };
}

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token")?.trim() ?? "";

  const [checking, setChecking] = useState(true);
  const [valid, setValid] = useState(false);
  const [emailHint, setEmailHint] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const strength = useMemo(() => passwordStrength(password), [password]);

  useEffect(() => {
    let cancelled = false;

    async function validate() {
      if (!token) {
        setChecking(false);
        setValid(false);
        setError("Missing reset token. Use the link from your email.");
        return;
      }

      try {
        const res = await fetch(
          `/api/auth/reset-password?token=${encodeURIComponent(token)}`
        );
        const data = await res.json().catch(() => ({}));
        if (cancelled) return;

        if (!res.ok || !data.valid) {
          setValid(false);
          setError(data.error ?? "Invalid or expired reset link");
        } else {
          setValid(true);
          setEmailHint(typeof data.email === "string" ? data.email : "");
        }
      } catch {
        if (!cancelled) {
          setValid(false);
          setError("Could not validate reset link");
        }
      } finally {
        if (!cancelled) setChecking(false);
      }
    }

    validate();
    return () => {
      cancelled = true;
    };
  }, [token]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password, confirmPassword }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setError(data.error ?? "Could not reset password");
        setLoading(false);
        return;
      }

      setSuccess(data.message ?? "Password updated.");
      setTimeout(() => router.push("/auth/signin"), 1500);
    } catch {
      setError("Something went wrong. Please try again.");
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
      <h1 className="text-xl font-semibold text-gray-900 mb-1">Set a new password</h1>
      <p className="text-sm text-gray-500 mb-6">
        {emailHint ? `Account: ${emailHint}` : "Choose a new password for your account."}
      </p>

      {checking ? (
        <p className="text-sm text-gray-500">Validating reset link…</p>
      ) : !valid ? (
        <div className="space-y-4">
          <div className="px-3 py-2 rounded-lg bg-red-50 border border-red-200">
            <p className="text-red-600 text-sm">{error || "Invalid or expired reset link"}</p>
          </div>
          <Link
            href="/auth/signin"
            className="inline-flex text-sm font-medium text-[#7c3aed] hover:underline"
          >
            Back to sign in
          </Link>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">New password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 6 characters"
              required
              minLength={6}
              className={inputClass}
              autoComplete="new-password"
            />
            {password && (
              <div className="mt-2">
                <div className="flex gap-1 mb-1">
                  {[1, 2, 3, 4].map((n) => (
                    <div
                      key={n}
                      className={`h-1.5 flex-1 rounded-full ${
                        n <= strength.score ? strength.color : "bg-gray-200"
                      }`}
                    />
                  ))}
                </div>
                <p className="text-xs text-gray-500">
                  Strength: {strength.label}. Use 10+ characters with mixed case, numbers, or symbols for a stronger password.
                </p>
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Confirm password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter password"
              required
              minLength={6}
              className={inputClass}
              autoComplete="new-password"
            />
          </div>

          {error && (
            <div className="px-3 py-2 rounded-lg bg-red-50 border border-red-200">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}
          {success && (
            <div className="px-3 py-2 rounded-lg bg-emerald-50 border border-emerald-200">
              <p className="text-emerald-700 text-sm">{success}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || Boolean(success)}
            className="w-full py-2.5 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white font-medium text-sm transition-colors disabled:opacity-60 mt-2"
          >
            {loading ? "Updating…" : success ? "Redirecting…" : "Update password"}
          </button>
        </form>
      )}
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link href="/" className="text-3xl font-bold text-[#7c3aed]">
            PurpleBook.cc
          </Link>
          <p className="text-sm text-gray-500 mt-1">SAT Practice Platform</p>
        </div>
        <Suspense
          fallback={
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
              <p className="text-sm text-gray-500">Loading…</p>
            </div>
          }
        >
          <ResetPasswordForm />
        </Suspense>
      </div>
    </div>
  );
}
