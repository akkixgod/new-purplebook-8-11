"use client";

import React from "react";

const TELEGRAM_URL = "https://t.me/purplebooksat";
const JOINED_SESSION_KEY = "purplebook_telegram_joined_session_v1";

export type TelegramModalMode = "post-test" | "inter-module";

type Props =
  | {
      open: boolean;
      mode: "post-test";
      onClose: () => void;
      onJoin: () => void;
    }
  | {
      open: boolean;
      mode: "inter-module";
      onClose: () => void;
      onJoin: () => void;
      onAlreadyJoined: () => void;
    };

export function TelegramCommunityCheckModal(props: Props) {
  if (!props.open) return null;

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 p-4"
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        className="w-full max-w-md rounded-2xl bg-white shadow-2xl border border-gray-100 p-6"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl font-bold text-gray-900">Did you join our SAT community on Telegram?</h2>
        <p className="mt-2 text-sm text-gray-600 leading-relaxed">
          Join other students for practice updates, community tips, and faster help when you get stuck.
        </p>

        <div className="mt-6 flex flex-col sm:flex-row gap-3 sm:justify-end">
          {props.mode === "post-test" ? (
            <button
              type="button"
              onClick={() => {
                sessionStorage.setItem(JOINED_SESSION_KEY, "1");
                window.open(TELEGRAM_URL, "_blank", "noopener,noreferrer");
                props.onJoin();
              }}
              className="w-full sm:w-auto rounded-xl bg-[#7c3aed] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#6d28d9]"
            >
              Join
            </button>
          ) : (
            <>
              <button
                type="button"
                onClick={() => {
                  sessionStorage.setItem(JOINED_SESSION_KEY, "1");
                  window.open(TELEGRAM_URL, "_blank", "noopener,noreferrer");
                  props.onJoin();
                }}
                className="w-full sm:w-auto rounded-xl bg-[#7c3aed] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#6d28d9]"
              >
                Join
              </button>
              <button
                type="button"
                onClick={() => {
                  sessionStorage.setItem(JOINED_SESSION_KEY, "1");
                  props.onAlreadyJoined();
                }}
                className="w-full sm:w-auto rounded-xl border border-gray-200 px-4 py-2.5 text-sm font-semibold text-gray-900 hover:bg-gray-50"
              >
                Already Joined
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export function isTelegramJoinedThisSession() {
  try {
    return sessionStorage.getItem(JOINED_SESSION_KEY) === "1";
  } catch {
    return false;
  }
}

