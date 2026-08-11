const TELEGRAM_URL = "https://t.me/purplebooksat";

function PromoGraphics() {
  return (
    <div className="flex items-center justify-center gap-3 md:gap-4" aria-hidden>
      {/* Geometric cursor / arrow */}
      <svg width="72" height="72" viewBox="0 0 72 72" fill="none" className="hidden sm:block shrink-0">
        <path
          d="M12 8 L58 36 L28 40 L24 62 Z"
          stroke="#7c3aed"
          strokeWidth="2.5"
          fill="white"
        />
        <path d="M28 40 L58 36 L44 28 Z" fill="#facc15" opacity="0.9" />
        <path d="M8 20 L18 24 L14 14 Z" fill="#7c3aed" />
      </svg>

      <svg width="36" height="16" viewBox="0 0 36 16" fill="none" className="shrink-0">
        <path d="M2 8 H28" stroke="#facc15" strokeWidth="2.5" strokeLinecap="round" />
        <path d="M24 4 L30 8 L24 12" stroke="#facc15" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>

      {/* Telegram paper plane */}
      <svg width="80" height="80" viewBox="0 0 80 80" fill="none" className="shrink-0">
        <circle cx="40" cy="40" r="38" stroke="#7c3aed" strokeWidth="2" fill="white" />
        <path
          d="M22 42 L58 26 L48 54 L38 46 L32 58 L34 44 Z"
          stroke="#7c3aed"
          strokeWidth="2"
          fill="white"
          strokeLinejoin="round"
        />
        <path d="M38 46 L48 54 L42 38 Z" fill="#facc15" />
        <path d="M22 42 L48 54 L38 46 Z" fill="#7c3aed" opacity="0.15" />
      </svg>
    </div>
  );
}

export function HeroPromoBanner() {
  return (
    <a
      href={TELEGRAM_URL}
      target="_blank"
      rel="noopener noreferrer"
      className="block border-2 border-black rounded-2xl p-6 my-6 bg-white hover:bg-gray-50/80 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[#7c3aed] focus-visible:ring-offset-2"
    >
      <div className="flex flex-col gap-8 md:grid md:grid-cols-3 md:items-center md:gap-6">
        {/* Left */}
        <div className="flex flex-col items-start gap-3 md:max-w-xs">
          <div>
            <p className="text-lg font-bold text-gray-900 leading-tight">Join our community</p>
            <p className="text-lg font-bold text-gray-900 leading-tight mt-0.5">
              on{" "}
              <span className="text-[#eab308] underline decoration-[#eab308] decoration-2 underline-offset-4">
                Telegram
              </span>
            </p>
          </div>
          <span
            className="inline-block border border-yellow-500 text-black rounded-lg px-4 py-2 text-sm font-medium hover:bg-yellow-50 transition-colors pointer-events-none"
            aria-hidden
          >
            Join Telegram Community
          </span>
        </div>

        {/* Center */}
        <div className="text-center md:px-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">PurpleBook.win</h1>
          <p className="text-sm sm:text-base text-gray-500 mt-2 leading-relaxed max-w-md mx-auto">
            Free SAT past papers with timed modules, instant scoring, and detailed answer review.
          </p>
        </div>

        {/* Right */}
        <div className="flex justify-center md:justify-end">
          <PromoGraphics />
        </div>
      </div>
    </a>
  );
}
