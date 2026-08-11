"use client";

import Link from "next/link";
import { useSession, signOut } from "next-auth/react";

export function Header() {
  const { data: session } = useSession();

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-[#7c3aed]">
          PurpleBook.cc
        </Link>

        <div className="flex items-center gap-3">
          {session ? (
            <div className="flex items-center gap-2">
              {(session.user as { role?: string })?.role === "admin" && (
                <Link
                  href="/admin"
                  className="text-xs px-3 py-1.5 rounded-lg bg-[#7c3aed]/10 text-[#7c3aed] font-medium hover:bg-[#7c3aed]/20 transition-colors"
                >
                  Admin
                </Link>
              )}
              <span className="text-sm text-gray-600 hidden sm:block">
                {session.user?.name ?? session.user?.email}
              </span>
              <button
                onClick={() => signOut()}
                className="text-sm px-3 py-1.5 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <Link
              href="/auth/signin"
              className="text-sm px-4 py-1.5 rounded-lg bg-[#7c3aed] hover:bg-[#6d28d9] text-white font-medium transition-colors"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
