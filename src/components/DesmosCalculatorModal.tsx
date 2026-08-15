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

/**
 * Desmos clamps expression-list width to [320, containerWidth - 200].
 * Below ~520px container width the native splitter has no movable range —
 * that is why a ~480px modal felt "static". Keep the shell wide enough.
 */
const DEFAULT_W = 640;
const MIN_W = 520;
const MIN_H = 380;
const HEADER_H = 56;
const BOTTOM_GAP = 56;

/** Soft UX bounds (further clamped by Desmos's 320 / width-200 rules). */
const EXP_FRAC_MIN = 0.2;
const EXP_FRAC_MAX = 0.8;
const DESMOS_EXP_MIN_PX = 320;
const DESMOS_GRAPH_MIN_PX = 200;

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

type DragState = { ox: number; oy: number; x: number; y: number };
type ResizeState = { ox: number; oy: number; w: number; h: number; edge: "se" | "e" | "s" };
type SplitState = { startX: number; startW: number; hostW: number };

function clampExpListWidth(desired: number, hostW: number): number {
  const softMin = Math.max(DESMOS_EXP_MIN_PX, Math.floor(hostW * EXP_FRAC_MIN));
  const softMax = Math.min(
    hostW - DESMOS_GRAPH_MIN_PX,
    Math.floor(hostW * EXP_FRAC_MAX)
  );
  // When the shell is too narrow for any range, keep Desmos's floor.
  if (softMax < DESMOS_EXP_MIN_PX) return DESMOS_EXP_MIN_PX;
  const lo = Math.min(softMin, softMax);
  const hi = Math.max(softMin, softMax);
  return Math.min(Math.max(desired, lo), hi);
}

export function DesmosCalculatorModal({ open, onClose }: Props) {
  const shellRef = useRef<HTMLDivElement>(null);
  const graphHostRef = useRef<HTMLDivElement>(null);
  const sciHostRef = useRef<HTMLDivElement>(null);
  const graphCalcRef = useRef<DesmosCalculatorInstance | null>(null);
  const sciCalcRef = useRef<DesmosCalculatorInstance | null>(null);
  const graphInitingRef = useRef(false);
  const sciInitingRef = useRef(false);
  const dragRef = useRef<DragState | null>(null);
  const resizeRef = useRef<ResizeState | null>(null);
  const splitRef = useRef<SplitState | null>(null);

  const [mode, setMode] = useState<CalcMode>("graphing");
  const [pos, setPos] = useState({ x: 12, y: HEADER_H });
  const [size, setSize] = useState({ w: DEFAULT_W, h: 520 });
  const [readyGraph, setReadyGraph] = useState(false);
  const [readySci, setReadySci] = useState(false);
  const [graphFallback, setGraphFallback] = useState(false);
  const [sciFallback, setSciFallback] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [placed, setPlaced] = useState(false);
  const [expListWidth, setExpListWidth] = useState(DESMOS_EXP_MIN_PX);
  const [splitting, setSplitting] = useState(false);

  // Left-docked Bluebook-ish size — wide enough for Desmos's splitter range
  useEffect(() => {
    if (placed || typeof window === "undefined") return;
    const w = Math.min(
      DEFAULT_W,
      Math.max(MIN_W, Math.floor(window.innerWidth * 0.48))
    );
    const h = Math.min(
      Math.floor(window.innerHeight * 0.8),
      window.innerHeight - HEADER_H - BOTTOM_GAP - 8
    );
    setSize({ w, h: Math.max(MIN_H, h) });
    setPos({ x: 12, y: HEADER_H });
    setPlaced(true);
  }, [placed]);

  const readExpListWidth = useCallback((): number => {
    const fromCtrl = graphCalcRef.current?.controller?.getExpListWidth?.();
    if (typeof fromCtrl === "number" && fromCtrl > 0) return fromCtrl;
    const panel = graphHostRef.current?.querySelector(
      ".dcg-exppanel-outer"
    ) as HTMLElement | null;
    if (panel) {
      const w = panel.getBoundingClientRect().width;
      if (w > 0) return w;
    }
    return expListWidth;
  }, [expListWidth]);

  const applyExpListWidth = useCallback((desired: number, hostW: number) => {
    const next = clampExpListWidth(desired, hostW);
    setExpListWidth(next);
    const ctrl = graphCalcRef.current?.controller;
    if (ctrl?.dispatch) {
      ctrl.dispatch({ type: "resize-exp-list", expListWidth: next });
    } else {
      const panel = graphHostRef.current?.querySelector(
        ".dcg-exppanel-outer"
      ) as HTMLElement | null;
      if (panel) panel.style.width = `${next}px`;
      graphCalcRef.current?.resize();
    }
  }, []);

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
        requestAnimationFrame(() => {
          calc?.resize();
          // Prefer our custom splitter; disable Desmos's invisible native hit-target.
          const native = graphHostRef.current?.querySelector(
            ".dcg-exp-list-resizer"
          ) as HTMLElement | null;
          if (native) {
            native.style.pointerEvents = "none";
            native.setAttribute("aria-hidden", "true");
          }
          const hostW = graphHostRef.current?.clientWidth ?? DEFAULT_W;
          // Start closer to a balanced Bluebook split when the shell is wide enough.
          const target = clampExpListWidth(Math.floor(hostW * 0.42), hostW);
          calc?.controller?.dispatch?.({
            type: "resize-exp-list",
            expListWidth: target,
          });
          const w = calc?.controller?.getExpListWidth?.() ?? target;
          setExpListWidth(w);
        });
      } catch (e) {
        // Soft log — avoid console.error(Error) which triggers the Next.js redbox in dev.
        console.warn(
          "Desmos graphing API unavailable, using embed fallback:",
          e instanceof Error ? e.message : e
        );
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
        console.warn(
          "Desmos scientific API unavailable, using embed fallback:",
          e instanceof Error ? e.message : e
        );
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

  // Resize when shown / resized / tabbed; re-clamp expression width to the new host
  useEffect(() => {
    if (!open) return;
    const id = window.setTimeout(() => {
      graphCalcRef.current?.resize();
      sciCalcRef.current?.resize();
      if (mode === "graphing" && graphCalcRef.current && !graphFallback) {
        const hostW = graphHostRef.current?.clientWidth ?? size.w;
        const current =
          graphCalcRef.current.controller?.getExpListWidth?.() ?? expListWidth;
        applyExpListWidth(current, hostW);
      }
    }, 50);
    return () => clearTimeout(id);
    // Intentionally omit expListWidth / applyExpListWidth to avoid feedback loops while dragging.
    // eslint-disable-next-line react-hooks/exhaustive-deps -- size/mode/open drive this sync
  }, [open, mode, size.w, size.h, readyGraph, readySci, graphFallback]);

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

  // Stable window listeners (same function identity for add/remove)
  const onWindowResizeMove = useRef((e: PointerEvent) => {
    const st = resizeRef.current;
    if (!st) return;
    let w = st.w;
    let h = st.h;
    if (st.edge === "se" || st.edge === "e") {
      w = Math.min(
        Math.max(MIN_W, st.w + (e.clientX - st.ox)),
        window.innerWidth - 16
      );
    }
    if (st.edge === "se" || st.edge === "s") {
      h = Math.min(
        Math.max(MIN_H, st.h + (e.clientY - st.oy)),
        window.innerHeight - HEADER_H - 8
      );
    }
    setSize({ w, h });
  }).current;

  const endWindowResize = useRef(() => {
    resizeRef.current = null;
    window.removeEventListener("pointermove", onWindowResizeMove);
    window.removeEventListener("pointerup", endWindowResize);
    window.removeEventListener("pointercancel", endWindowResize);
    graphCalcRef.current?.resize();
    sciCalcRef.current?.resize();
  }).current;

  const startWindowResize = (edge: ResizeState["edge"]) => (e: ReactPointerEvent) => {
    e.preventDefault();
    e.stopPropagation();
    resizeRef.current = {
      ox: e.clientX,
      oy: e.clientY,
      w: size.w,
      h: size.h,
      edge,
    };
    window.addEventListener("pointermove", onWindowResizeMove);
    window.addEventListener("pointerup", endWindowResize);
    window.addEventListener("pointercancel", endWindowResize);
    try {
      (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      /* inactive pointer — window listeners still handle the gesture */
    }
  };

  // Re-bind applyExpListWidth into split move via ref so the stable listener stays fresh
  const applyExpListWidthRef = useRef(applyExpListWidth);
  applyExpListWidthRef.current = applyExpListWidth;

  const onSplitMoveLive = useRef((e: PointerEvent) => {
    const st = splitRef.current;
    if (!st) return;
    applyExpListWidthRef.current(st.startW + (e.clientX - st.startX), st.hostW);
  }).current;

  const endSplitDrag = useRef(() => {
    splitRef.current = null;
    setSplitting(false);
    window.removeEventListener("pointermove", onSplitMoveLive);
    window.removeEventListener("pointerup", endSplitDrag);
    window.removeEventListener("pointercancel", endSplitDrag);
    graphCalcRef.current?.resize();
  }).current;

  useEffect(() => {
    return () => {
      window.removeEventListener("pointermove", onWindowResizeMove);
      window.removeEventListener("pointerup", endWindowResize);
      window.removeEventListener("pointercancel", endWindowResize);
      window.removeEventListener("pointermove", onSplitMoveLive);
      window.removeEventListener("pointerup", endSplitDrag);
      window.removeEventListener("pointercancel", endSplitDrag);
    };
  }, [onWindowResizeMove, endWindowResize, onSplitMoveLive, endSplitDrag]);

  const onSplitPointerDown = (e: ReactPointerEvent) => {
    if (graphFallback || mode !== "graphing") return;
    e.preventDefault();
    e.stopPropagation();
    const host = graphHostRef.current;
    if (!host) return;
    const hostW = host.clientWidth;
    // Too narrow for any Desmos splitter range — ignore.
    if (hostW < DESMOS_EXP_MIN_PX + DESMOS_GRAPH_MIN_PX) return;

    splitRef.current = {
      startX: e.clientX,
      startW: readExpListWidth(),
      hostW,
    };
    setSplitting(true);
    window.addEventListener("pointermove", onSplitMoveLive);
    window.addEventListener("pointerup", endSplitDrag);
    window.addEventListener("pointercancel", endSplitDrag);
    try {
      (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      /* Synthetic or inactive pointers — window listeners still drive the drag. */
    }
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
      splitRef.current = null;
      setSplitting(false);
      onClose();
    },
    [onClose]
  );

  const loading =
    (mode === "graphing" && !readyGraph && !error) ||
    (mode === "scientific" && !readySci && !error);

  // Pane visibility must NOT force `visible` while the shell is closed.
  // Descendants with visibility:visible override an ancestor's visibility:hidden,
  // which left the Desmos iframe painted on screen after dismiss.
  const graphPaneOpen = open && mode === "graphing";
  const sciPaneOpen = open && mode === "scientific";
  const showSplitter =
    graphPaneOpen && readyGraph && !graphFallback && !loading && !error;
  const splitterEnabled =
    showSplitter && size.w >= DESMOS_EXP_MIN_PX + DESMOS_GRAPH_MIN_PX;

  return (
    <>
      {/* Click-outside backdrop — only while open */}
      {open && (
        <div
          className="fixed inset-0 z-[119] bg-black/20"
          aria-hidden
          onPointerDown={(e) => {
            // Close on pointer down (not click) so nothing under the overlay steals the gesture.
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
        // Keep mounted when closed so calculator state persists; display:none
        // reliably hides iframes (visibility:hidden alone does not when children
        // set visibility:visible).
        // Do NOT stopPropagation on the shell — Desmos touch-tracking listens on
        // document during bubble, and blocking it freezes the native resizer.
        className={`fixed z-[120] flex flex-col overflow-hidden rounded-md border border-gray-400/40 bg-white shadow-[0_8px_32px_rgba(0,0,0,0.28)] ${
          open ? "" : "hidden"
        }`}
        style={{
          left: pos.x,
          top: pos.y,
          width: size.w,
          height: size.h,
          pointerEvents: open ? "auto" : "none",
        }}
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
              visibility: graphPaneOpen ? "visible" : "hidden",
              pointerEvents: graphPaneOpen ? "auto" : "none",
              zIndex: graphPaneOpen ? 1 : 0,
            }}
            aria-hidden={!graphPaneOpen}
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

            {/* Custom expression/graph splitter — drives Desmos via controller.dispatch */}
            {showSplitter && (
              <div
                role="separator"
                aria-orientation="vertical"
                aria-label="Resize expression list"
                aria-valuenow={Math.round(expListWidth)}
                aria-disabled={!splitterEnabled}
                title={
                  splitterEnabled
                    ? "Drag to resize expression list"
                    : "Widen the calculator to resize panes"
                }
                className={`absolute top-0 bottom-0 z-30 -ml-1.5 flex w-3 touch-none items-stretch justify-center ${
                  splitterEnabled
                    ? "cursor-ew-resize"
                    : "cursor-not-allowed opacity-40"
                } ${splitting ? "bg-blue-500/10" : ""}`}
                style={{ left: expListWidth }}
                onPointerDown={onSplitPointerDown}
              >
                <span
                  className={`w-0.5 self-stretch ${
                    splitting ? "bg-blue-500" : "bg-gray-400/80"
                  }`}
                  aria-hidden
                />
              </div>
            )}
          </div>

          {/* Scientific pane */}
          <div
            className="absolute inset-0"
            style={{
              visibility: sciPaneOpen ? "visible" : "hidden",
              pointerEvents: sciPaneOpen ? "auto" : "none",
              zIndex: sciPaneOpen ? 1 : 0,
            }}
            aria-hidden={!sciPaneOpen}
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

        {/* East edge resize */}
        <div
          className="absolute top-11 bottom-3 right-0 z-20 w-2 cursor-ew-resize"
          onPointerDown={startWindowResize("e")}
          aria-hidden
        />
        {/* South edge resize */}
        <div
          className="absolute bottom-0 left-0 right-3 z-20 h-2 cursor-ns-resize"
          onPointerDown={startWindowResize("s")}
          aria-hidden
        />
        {/* SE corner resize */}
        <div
          className="absolute bottom-0 right-0 z-30 flex h-7 w-7 cursor-nwse-resize items-end justify-end p-1"
          onPointerDown={startWindowResize("se")}
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
