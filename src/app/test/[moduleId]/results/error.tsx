"use client";

import { useEffect } from "react";
import Link from "next/link";

export default function ResultsError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Results page error:", error);
    if (process.env.NODE_ENV !== "production") {
      console.error(error.stack);
    }
  }, [error]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-4">
      <div className="max-w-md w-full text-center">
        <h1 className="text-xl font-bold text-gray-900 mb-2">Something went wrong</h1>
        <p className="text-sm text-gray-500 mb-6">
          We couldn’t show your module results. You can try again or return home.
        </p>
        {process.env.NODE_ENV !== "production" && (
          <pre className="mb-6 max-h-40 overflow-auto rounded-lg bg-gray-50 p-3 text-left text-xs text-red-600">
            {error.message}
            {"\n"}
            {error.stack}
          </pre>
        )}
        <div className="flex gap-3 justify-center">
          <button
            type="button"
            onClick={reset}
            className="px-4 py-2.5 text-sm font-semibold rounded-xl bg-[#7c3aed] text-white hover:bg-[#6d28d9]"
          >
            Try again
          </button>
          <Link
            href="/"
            className="px-4 py-2.5 text-sm font-semibold rounded-xl border border-gray-200 text-gray-800 hover:bg-gray-50"
          >
            Home
          </Link>
        </div>
      </div>
    </div>
  );
}
