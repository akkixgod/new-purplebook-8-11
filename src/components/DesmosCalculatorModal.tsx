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
  type DesmosAPI,
  type DesmosCalculatorInstance,
} from "@/lib/load-desmos";

const DEFAULT_W = 480;
const MIN_W = 340;
const MIN_H = 360;
const HEADER_H = 56; // below exam top bar
const BOTTOM_GAP = 56; // above bottom nav

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
  const desmosApiRef = useRef<DesmosAPI | null>(null);
  const dragRef = useRef<{ ox: number; oy: number; x: number; y: number } | null>(null);
  const resizeRef = useRef<{ ox: number; oy: number; w: number; h: number } | null>(null);

  const [mode, setMode] = useState<CalcMode>("graphing");
  const [pos, setPos] = useState({ x: 12, y: HEADER_H });
  const [size, setSize] = useState({ w: DEFAULT_W, h: 500 });
  const [readyGraph, setReadyGraph] = useState(false);
  const [readySci, setReadySci] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [placed, setPlaced] = useState(false);

  // Left-docked: ~480px wide, ~80% viewport height
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

  const ensureGraphing = useCallback(async (api: DesmosAPI) => {
    if (graphCalcRef.current || !graphHostRef.current) return;
    graphHostRef.current.innerHTML = "";
    graphCalcRef.current = api.GraphingCalculator(graphHostRef.current, { ...GRAPHING_OPTS });
    setReadyGraph(true);
  }, []);

  const ensureScientific = useCallback(async (api: DesmosAPI) => {
    if (sciCalcRef.current || !sciHostRef.current) return;
    sciHostRef.current.innerHTML = "";
    sciCalcRef.current = api.ScientificCalculator(sciHostRef.current, { ...SCIENTIFIC_OPTS });
    setReadySci(true);
  }, []);

  // Load API + init graphing (default). Keep both instances alive for the module.
  useEffect(() => {
    let cancelled = false;
    loadDesmos()
      .then(async (Desmos) => {
        if (cancelled) return;
        desmosApiRef.current = Desmos;
        await ensureGraphing(Desmos);
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message || "Failed to load calculator");
      });

    return () => {
      cancelled = true;
      graphCalcRef.current?.destroy();
      sciCalcRef.current?.destroy();
      graphCalcRef.current = null;
      sciCalcRef.current = null;
    };
  }, [ensureGraphing]);

  // Lazy-create scientific when first selected; never destroy on tab switch
  useEffect(() => {
    if (mode !== "scientific" || !desmosApiRef.current) return;
    ensureScientific(desmosApiRef.current).catch((e: Error) =>
      setError(e.message || "Failed to load scientific calculator")
    );
  }, [mode, ensureScientific]);

  const activeCalc = () =>
    mode === "graphing" ? graphCalcRef.current : sciCalcRef.current;

  // Resize active calculator when shown / sized / tabbed
  useEffect(() => {
    if (!open) return;
    const id = requestAnimationFrame(() => {
      activeCalc()?.resize();
      // Also resize the hidden one so it paints correctly when switched
      graphCalcRef.current?.resize();
      sciCalcRef.current?.resize();
    });
    return () => cancelAnimationFrame(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- active mode drives which instance is focused
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
    const dx = e.clientX - dragRef.current.ox;
    const dy = e.clientY - dragRef.current.oy;
    setPos(clampPos(dragRef.current.x + dx, dragRef.current.y + dy, size.w, size.h));
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
    const dw = e.clientX - resizeRef.current.ox;
    const dh = e.clientY - resizeRef.current.oy;
    const w = Math.min(Math.max(MIN_W, resizeRef.current.w + dw), window.innerWidth - 16);
    const h = Math.min(
      Math.max(MIN_H, resizeRef.current.h + dh),
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

  const switchMode = (next: CalcMode) => {
    if (next === mode) return;
    setMode(next);
  };

  const loading =
    (mode === "graphing" && !readyGraph && !error) ||
    (mode === "scientific" && !readySci && !error);

  return (
    <div
      ref={shellRef}
      role="dialog"
      aria-label="Calculator"
      aria-hidden={!open}
      className="fixed z-[120] flex flex-col overflow-hidden rounded-md border border-gray-400/40 bg-white shadow-[0_8px_32px_rgba(0,0,0,0.28)]"
      style={{
        left: pos.x,
        top: pos.y,
        width: size.w,
        height: size.h,
        visibility: open ? "visible" : "hidden",
        pointerEvents: open ? "auto" : "none",
      }}
    >
      {/* Dark Bluebook header with Graphing / Scientific tabs */}
      <div
        className="flex h-11 flex-shrink-0 cursor-grab items-center gap-2 bg-[#2d2d2d] px-2 active:cursor-grabbing select-none"
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
            onClick={() => switchMode("graphing")}
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
            onClick={() => switchMode("scientific")}
            className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-semibold transition-colors ${
              mode === "scientific"
                ? "bg-white text-gray-900"
                : "bg-transparent text-white/90 hover:bg-white/10"
            }`}
          >
            <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v3M9 7h6M8 12h2l2 5 2-8 2 3h2" />
            </svg>
            Scientific
          </button>
        </div>

        {/* Drag affordance (six-dot grip) */}
        <div className="ml-1 flex flex-col gap-0.5 opacity-50" aria-hidden>
          <span className="flex gap-0.5">
            <span className="h-1 w-1 rounded-full bg-white" />
            <span className="h-1 w-1 rounded-full bg-white" />
          </span>
          <span className="flex gap-0.5">
            <span className="h-1 w-1 rounded-full bg-white" />
            <span className="h-1 w-1 rounded-full bg-white" />
          </span>
          <span className="flex gap-0.5">
            <span className="h-1 w-1 rounded-full bg-white" />
            <span className="h-1 w-1 rounded-full bg-white" />
          </span>
        </div>

        <div className="flex-1" />

        <button
          type="button"
          onClick={onClose}
          aria-label="Close calculator"
          className="rounded p-1.5 text-white transition-colors hover:bg-white/15"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Calculator hosts — both kept mounted for state preservation */}
      <div className="relative min-h-0 flex-1 bg-white">
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
        {/* Keep both sized (not display:none) so Desmos layout persists */}
        <div
          ref={graphHostRef}
          className="absolute inset-0"
          style={{
            visibility: mode === "graphing" ? "visible" : "hidden",
            pointerEvents: mode === "graphing" ? "auto" : "none",
            zIndex: mode === "graphing" ? 1 : 0,
          }}
          aria-hidden={mode !== "graphing"}
        />
        <div
          ref={sciHostRef}
          className="absolute inset-0"
          style={{
            visibility: mode === "scientific" ? "visible" : "hidden",
            pointerEvents: mode === "scientific" ? "auto" : "none",
            zIndex: mode === "scientific" ? 1 : 0,
          }}
          aria-hidden={mode !== "scientific"}
        />
      </div>

      {/* Bluebook-style expand resize handle (bottom-right) */}
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
  );
}
