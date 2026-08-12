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
      {/* Mobile: brand + actions only (no duplicate center title) */}
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between gap-3 md:hidden">
        <Link
          href="/"
          className="text-sm font-semibold text-[#7c3aed] inline-flex items-baseline min-w-0"
        >
          PurpleBook
          <span className="relative inline-block">
            .win
            <BrandStar />
          </span>
        </Link>
        <div className="flex items-center gap-2 flex-shrink-0">
          {session ? (
            <>
              <Link
                href="/account"
                className="text-sm px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                Account
              </Link>
              <button
                onClick={() => signOut({ callbackUrl: "/" })}
                className="text-sm px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
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

      {/* Desktop: original 3-column header (unchanged) */}
      <div className="max-w-7xl mx-auto px-4 h-14 hidden md:grid grid-cols-3 items-center">
        <Link
          href="/"
          className="text-base font-semibold text-[#7c3aed] justify-self-start inline-flex items-baseline"
        >
          PurpleBook
          <span className="relative inline-block">
            .win
            <BrandStar />
          </span>
        </Link>

        <p className="text-lg font-bold text-gray-900 text-center truncate px-2">
          PurpleBook.win
        </p>

        <div className="flex items-center gap-2 justify-self-end">
          {session ? (
            <>
              {(session.user as { role?: string })?.role === "admin" && (
                <Link
                  href="/admin"
                  className="text-xs px-3 py-1.5 rounded-lg bg-[#7c3aed]/10 text-[#7c3aed] font-medium hover:bg-[#7c3aed]/20 transition-colors inline-flex"
                >
                  Admin
                </Link>
              )}
              <Link
                href="/account"
                className="text-sm text-gray-600 hover:text-[#7c3aed] max-w-[140px] truncate"
                title={session.user?.email ?? "My Account"}
              >
                {session.user?.name ?? session.user?.email ?? "My Account"}
              </Link>
              <button
                onClick={() => signOut({ callbackUrl: "/" })}
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
