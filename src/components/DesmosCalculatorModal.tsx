"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from "react";
import {
  loadDesmos,
  waitForSize,
  type DesmosCalculatorInstance,
} from "@/lib/load-desmos";

const DEFAULT_W = 480;
const MIN_W = 360;
const MIN_H = 380;
const HEADER_H = 56;
const BOTTOM_GAP = 56;

type CalcMode = "graphing" | "scientific";

type Props = {
  open: boolean;
  onClose: () => void;
};

const GRAPHING_OPTS = {
  degreeMode: true,
  clearIntoDegreeMode: true,
  lockViewport: false,
  expressionsCollapsed: false,
  expressions: true,
  graphpaper: true,
  settingsMenu: true,
  zoomButtons: true,
  keypad: true,
  border: false,
  autosize: true,
} as const;

const SCIENTIFIC_OPTS = {
  degreeMode: true,
  clearIntoDegreeMode: true,
  settingsMenu: true,
  links: false,
} as const;

export function DesmosCalculatorModal({ open, onClose }: Props) {
  const shellRef = useRef<HTMLDivElement>(null);
  const graphHostRef = useRef<HTMLDivElement>(null);
  const sciHostRef = useRef<HTMLDivElement>(null);
  const graphCalcRef = useRef<DesmosCalculatorInstance | null>(null);
  const sciCalcRef = useRef<DesmosCalculatorInstance | null>(null);
  const graphInitingRef = useRef(false);
  const sciInitingRef = useRef(false);
  const dragRef = useRef<{ ox: number; oy: number; x: number; y: number } | null>(null);
  const resizeRef = useRef<{ ox: number; oy: number; w: number; h: number } | null>(null);

  const [mode, setMode] = useState<CalcMode>("graphing");
  const [pos, setPos] = useState({ x: 12, y: HEADER_H });
  const [size, setSize] = useState({ w: DEFAULT_W, h: 520 });
  const [readyGraph, setReadyGraph] = useState(false);
  const [readySci, setReadySci] = useState(false);
  const [graphFallback, setGraphFallback] = useState(false);
  const [sciFallback, setSciFallback] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [placed, setPlaced] = useState(false);

  // Left-docked Bluebook size
  useEffect(() => {
    if (placed || typeof window === "undefined") return;
    const w = Math.min(DEFAULT_W, Math.max(MIN_W, Math.floor(window.innerWidth * 0.42)));
    const h = Math.min(
      Math.floor(window.innerHeight * 0.8),
      window.innerHeight - HEADER_H - BOTTOM_GAP - 8
    );
    setSize({ w, h: Math.max(MIN_H, h) });
    setPos({ x: 12, y: HEADER_H });
    setPlaced(true);
  }, [placed]);

  // Init graphing once the modal is open and the host has real size
  useEffect(() => {
    if (!open) return;
    if (graphCalcRef.current || graphFallback) {
      graphCalcRef.current?.resize();
      return;
    }
    if (graphInitingRef.current) return;

    let cancelled = false;
    graphInitingRef.current = true;

    (async () => {
      let calc: DesmosCalculatorInstance | null = null;
      try {
        const host = graphHostRef.current;
        if (!host) throw new Error("Missing graph host");
        await waitForSize(host);
        if (cancelled) return;

        const Desmos = await loadDesmos();
        if (cancelled || !graphHostRef.current) return;

        graphHostRef.current.innerHTML = "";
        calc = Desmos.GraphingCalculator(graphHostRef.current, { ...GRAPHING_OPTS });
        if (cancelled) {
          calc.destroy();
          return;
        }
        graphCalcRef.current = calc;
        setReadyGraph(true);
        setError(null);
        requestAnimationFrame(() => calc?.resize());
      } catch (e) {
        console.error("Desmos graphing init failed, using embed fallback:", e);
        if (!cancelled) {
          setGraphFallback(true);
          setReadyGraph(true);
          setError(null);
        }
      } finally {
        graphInitingRef.current = false;
      }
    })();

    return () => {
      cancelled = true;
      graphInitingRef.current = false;
    };
  }, [open, graphFallback]);

  // Init scientific on first visit to that tab
  useEffect(() => {
    if (!open || mode !== "scientific") return;
    if (sciCalcRef.current || sciFallback) {
      sciCalcRef.current?.resize();
      return;
    }
    if (sciInitingRef.current) return;

    let cancelled = false;
    sciInitingRef.current = true;

    (async () => {
      let calc: DesmosCalculatorInstance | null = null;
      try {
        const host = sciHostRef.current;
        if (!host) throw new Error("Missing scientific host");
        await waitForSize(host);
        if (cancelled) return;

        const Desmos = await loadDesmos();
        if (!Desmos.ScientificCalculator) {
          throw new Error("ScientificCalculator not enabled for this API key");
        }
        if (cancelled || !sciHostRef.current) return;

        sciHostRef.current.innerHTML = "";
        calc = Desmos.ScientificCalculator(sciHostRef.current, { ...SCIENTIFIC_OPTS });
        if (cancelled) {
          calc.destroy();
          return;
        }
        sciCalcRef.current = calc;
        setReadySci(true);
        requestAnimationFrame(() => calc?.resize());
      } catch (e) {
        console.error("Desmos scientific init failed, using embed fallback:", e);
        if (!cancelled) {
          setSciFallback(true);
          setReadySci(true);
        }
      } finally {
        sciInitingRef.current = false;
      }
    })();

    return () => {
      cancelled = true;
      sciInitingRef.current = false;
    };
  }, [open, mode, sciFallback]);

  // Destroy on full unmount (leaving module)
  useEffect(() => {
    return () => {
      try {
        graphCalcRef.current?.destroy();
        sciCalcRef.current?.destroy();
      } catch {
        /* ignore */
      }
      graphCalcRef.current = null;
      sciCalcRef.current = null;
    };
  }, []);

  // Resize when shown / resized / tabbed
  useEffect(() => {
    if (!open) return;
    const id = window.setTimeout(() => {
      graphCalcRef.current?.resize();
      sciCalcRef.current?.resize();
    }, 50);
    return () => clearTimeout(id);
  }, [open, mode, size.w, size.h, readyGraph, readySci]);

  const clampPos = useCallback((x: number, y: number, w: number, h: number) => {
    const maxX = Math.max(0, window.innerWidth - 80);
    const maxY = Math.max(0, window.innerHeight - 48);
    return {
      x: Math.min(Math.max(-w + 80, x), maxX),
      y: Math.min(Math.max(0, y), maxY),
    };
  }, []);

  const onDragPointerDown = (e: ReactPointerEvent) => {
    if ((e.target as HTMLElement).closest("button")) return;
    e.preventDefault();
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    dragRef.current = { ox: e.clientX, oy: e.clientY, x: pos.x, y: pos.y };
  };

  const onDragPointerMove = (e: ReactPointerEvent) => {
    if (!dragRef.current) return;
    setPos(
      clampPos(
        dragRef.current.x + (e.clientX - dragRef.current.ox),
        dragRef.current.y + (e.clientY - dragRef.current.oy),
        size.w,
        size.h
      )
    );
  };

  const onDragPointerUp = (e: ReactPointerEvent) => {
    dragRef.current = null;
    try {
      (e.currentTarget as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      /* ignore */
    }
  };

  const onResizePointerDown = (e: ReactPointerEvent) => {
    e.preventDefault();
    e.stopPropagation();
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    resizeRef.current = { ox: e.clientX, oy: e.clientY, w: size.w, h: size.h };
  };

  const onResizePointerMove = (e: ReactPointerEvent) => {
    if (!resizeRef.current) return;
    const w = Math.min(
      Math.max(MIN_W, resizeRef.current.w + (e.clientX - resizeRef.current.ox)),
      window.innerWidth - 16
    );
    const h = Math.min(
      Math.max(MIN_H, resizeRef.current.h + (e.clientY - resizeRef.current.oy)),
      window.innerHeight - HEADER_H - 8
    );
    setSize({ w, h });
  };

  const onResizePointerUp = (e: ReactPointerEvent) => {
    resizeRef.current = null;
    try {
      (e.currentTarget as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      /* ignore */
    }
    graphCalcRef.current?.resize();
    sciCalcRef.current?.resize();
  };

  // Escape closes the calculator
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        onClose();
      }
    };
    window.addEventListener("keydown", onKey, true);
    return () => window.removeEventListener("keydown", onKey, true);
  }, [open, onClose]);

  const handleClose = useCallback(
    (e?: { preventDefault?: () => void; stopPropagation?: () => void }) => {
      e?.preventDefault?.();
      e?.stopPropagation?.();
      dragRef.current = null;
      resizeRef.current = null;
      onClose();
    },
    [onClose]
  );

  const loading =
    (mode === "graphing" && !readyGraph && !error) ||
    (mode === "scientific" && !readySci && !error);

  return (
    <>
      {/* Click-outside backdrop — only while open */}
      {open && (
        <div
          className="fixed inset-0 z-[119] bg-black/20"
          aria-hidden
          onClick={() => handleClose()}
          onPointerDown={(e) => {
            // Close on pointer down so Desmos cannot steal the gesture.
            if (e.button === 0) handleClose(e);
          }}
        />
      )}

      <div
        ref={shellRef}
        role="dialog"
        aria-label="Calculator"
        aria-modal={open}
        aria-hidden={!open}
        className="fixed z-[120] flex flex-col overflow-hidden rounded-md border border-gray-400/40 bg-white shadow-[0_8px_32px_rgba(0,0,0,0.28)]"
        style={{
          left: pos.x,
          top: pos.y,
          width: size.w,
          height: size.h,
          // Keep mounted when closed so calculator state persists
          visibility: open ? "visible" : "hidden",
          pointerEvents: open ? "auto" : "none",
        }}
        onPointerDown={(e) => e.stopPropagation()}
        onClick={(e) => e.stopPropagation()}
      >
        <div
          className="relative z-30 flex h-11 flex-shrink-0 cursor-grab items-center gap-2 bg-[#2d2d2d] px-2 active:cursor-grabbing select-none"
          onPointerDown={onDragPointerDown}
          onPointerMove={onDragPointerMove}
          onPointerUp={onDragPointerUp}
          onPointerCancel={onDragPointerUp}
        >
          <div className="flex items-center gap-1" role="tablist" aria-label="Calculator mode">
            <button
              type="button"
              role="tab"
              aria-selected={mode === "graphing"}
              onClick={() => setMode("graphing")}
              className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-semibold transition-colors ${
                mode === "graphing"
                  ? "bg-white text-gray-900"
                  : "bg-transparent text-white/90 hover:bg-white/10"
              }`}
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 17l6-6 4 4 7-8" />
                <path strokeLinecap="round" strokeWidth={2} d="M3 20h18" />
              </svg>
              Graphing
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={mode === "scientific"}
              onClick={() => setMode("scientific")}
              className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-semibold transition-colors ${
                mode === "scientific"
                  ? "bg-white text-gray-900"
                  : "bg-transparent text-white/90 hover:bg-white/10"
              }`}
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 20V10m4 10V4m4 16v-6m4 6V8m4 12V12"
                />
              </svg>
              Scientific
            </button>
          </div>

          <div className="ml-1 flex flex-col gap-0.5 opacity-50" aria-hidden>
            {[0, 1, 2].map((r) => (
              <span key={r} className="flex gap-0.5">
                <span className="h-1 w-1 rounded-full bg-white" />
                <span className="h-1 w-1 rounded-full bg-white" />
              </span>
            ))}
          </div>

          <div className="flex-1" />

          <button
            type="button"
            aria-label="Close calculator"
            title="Close calculator"
            className="relative z-40 flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-md text-white transition-colors hover:bg-white/20 active:bg-white/30"
            onPointerDown={(e) => {
              // Close on pointerdown so header drag / Desmos never swallows the click.
              e.stopPropagation();
              e.preventDefault();
              handleClose(e);
            }}
            onClick={(e) => {
              e.stopPropagation();
              e.preventDefault();
              handleClose(e);
            }}
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="relative z-10 min-h-0 flex-1 bg-white">
          {loading && (
            <div className="absolute inset-0 z-10 flex items-center justify-center bg-white text-sm text-gray-500">
              Loading calculator…
            </div>
          )}
          {error && (
            <div className="absolute inset-0 z-10 flex items-center justify-center bg-white px-4 text-center text-sm text-red-600">
              {error}
            </div>
          )}

          {/* Graphing pane */}
          <div
            className="absolute inset-0"
            style={{
              visibility: mode === "graphing" ? "visible" : "hidden",
              pointerEvents: mode === "graphing" ? "auto" : "none",
              zIndex: mode === "graphing" ? 1 : 0,
            }}
            aria-hidden={mode !== "graphing"}
          >
            {graphFallback ? (
              <iframe
                title="Desmos Graphing Calculator"
                src="https://www.desmos.com/calculator"
                className="h-full w-full border-0"
                allow="clipboard-write"
              />
            ) : (
              <div ref={graphHostRef} className="h-full w-full" />
            )}
          </div>

          {/* Scientific pane */}
          <div
            className="absolute inset-0"
            style={{
              visibility: mode === "scientific" ? "visible" : "hidden",
              pointerEvents: mode === "scientific" ? "auto" : "none",
              zIndex: mode === "scientific" ? 1 : 0,
            }}
            aria-hidden={mode !== "scientific"}
          >
            {sciFallback ? (
              <iframe
                title="Desmos Scientific Calculator"
                src="https://www.desmos.com/scientific"
                className="h-full w-full border-0"
                allow="clipboard-write"
              />
            ) : (
              <div ref={sciHostRef} className="h-full w-full" />
            )}
          </div>
        </div>

        <div
          className="absolute bottom-0 right-0 z-20 flex h-6 w-6 cursor-nwse-resize items-end justify-end p-1"
          onPointerDown={onResizePointerDown}
          onPointerMove={onResizePointerMove}
          onPointerUp={onResizePointerUp}
          onPointerCancel={onResizePointerUp}
          aria-label="Resize calculator"
          role="separator"
        >
          <svg className="h-3.5 w-3.5 text-gray-500" viewBox="0 0 16 16" aria-hidden>
            <path
              d="M6 14 L14 6 M10 14 L14 10 M14 14"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
              fill="none"
            />
          </svg>
        </div>
      </div>
    </>
  );
}
