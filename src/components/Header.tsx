"use client";

import Link from "next/link";
import { useSession, signOut } from "next-auth/react";

function BrandStar() {
  return (
    <svg
      className="inline-block w-3 h-3 text-[#7c3aed] -mt-3 ml-0.5"
      viewBox="0 0 12 12"
      fill="currentColor"
      aria-hidden
    >
      <path d="M6 0 L7.4 4.6 L12 6 L7.4 7.4 L6 12 L4.6 7.4 L0 6 L4.6 4.6 Z" />
    </svg>
  );
}

export function Header() {
  const { data: session } = useSession();

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 h-14 grid grid-cols-3 items-center">
        {/* Left brand */}
        <Link
          href="/"
          className="text-sm sm:text-base font-semibold text-[#7c3aed] justify-self-start inline-flex items-baseline"
        >
          PurpleBook
          <span className="relative inline-block">
            .win
            <BrandStar />
          </span>
        </Link>

        {/* Center title */}
        <p className="text-base sm:text-lg font-bold text-gray-900 text-center truncate px-2">
          PurpleBook.win
        </p>

        {/* Right actions */}
        <div className="flex items-center gap-2 justify-self-end">
          {session ? (
            <>
              {(session.user as { role?: string })?.role === "admin" && (
                <Link
                  href="/admin"
                  className="text-xs px-3 py-1.5 rounded-lg bg-[#7c3aed]/10 text-[#7c3aed] font-medium hover:bg-[#7c3aed]/20 transition-colors hidden sm:inline-flex"
                >
                  Admin
                </Link>
              )}
              <span className="text-sm text-gray-600 hidden lg:block max-w-[120px] truncate">
                {session.user?.name ?? session.user?.email}
              </span>
              <button
                onClick={() => signOut()}
                className="text-sm px-4 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                Sign Out
              </button>
            </>
          ) : (
            <Link
              href="/auth/signin"
              className="text-sm px-4 py-2 rounded-lg bg-black text-white font-medium hover:bg-gray-900 transition-colors"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
