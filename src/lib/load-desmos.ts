/** Load the official Desmos API script once; resolves with the global Desmos object. */

/**
 * Documented Desmos development/demo API key from https://www.desmos.com/api docs.
 * Override with NEXT_PUBLIC_DESMOS_API_KEY for production (desmos.com/my-api).
 * Note: an older typo key (…dc6961159cdb094) returns HTTP 403 and must not be used.
 */
const DEMO_KEY = "dcb31709b452b1cf9dc26972add0fda6";

/** Prefer a pinned major that Desmos still serves; they 302 to a patch release. */
const API_VERSION = "v1.11";

function apiSrc(key: string = getApiKey()): string {
  return `https://www.desmos.com/api/${API_VERSION}/calculator.js?apiKey=${encodeURIComponent(key)}`;
}

function getApiKey(): string {
  const fromEnv =
    typeof process !== "undefined" ? process.env.NEXT_PUBLIC_DESMOS_API_KEY?.trim() : "";
  return fromEnv || DEMO_KEY;
}

/** Undocumented controller surface used for expression-list width (Bluebook-style splitter). */
export interface DesmosController {
  dispatch: (action: Record<string, unknown>) => void;
  getExpListWidth?: () => number;
}

export interface DesmosCalculatorInstance {
  resize: () => void;
  destroy: () => void;
  getState: () => unknown;
  setState: (state: unknown, opts?: { allowUndo?: boolean }) => void;
  setBlank: () => void;
  updateSettings: (settings: Record<string, unknown>) => void;
  /** Present on GraphingCalculator; not part of the public typed API. */
  controller?: DesmosController;
}

export interface DesmosAPI {
  GraphingCalculator: (
    element: HTMLElement,
    options?: Record<string, unknown>
  ) => DesmosCalculatorInstance;
  ScientificCalculator?: (
    element: HTMLElement,
    options?: Record<string, unknown>
  ) => DesmosCalculatorInstance;
}

declare global {
  interface Window {
    Desmos?: DesmosAPI;
  }
}

let loadPromise: Promise<DesmosAPI> | null = null;

function removeFailedScript(script: HTMLScriptElement | null) {
  try {
    script?.remove();
  } catch {
    /* ignore */
  }
}

export function loadDesmos(): Promise<DesmosAPI> {
  if (typeof window === "undefined") {
    return Promise.reject(new Error("Desmos can only load in the browser"));
  }
  if (window.Desmos?.GraphingCalculator) {
    return Promise.resolve(window.Desmos);
  }
  if (loadPromise) return loadPromise;

  loadPromise = new Promise<DesmosAPI>((resolve, reject) => {
    const src = apiSrc();

    const fail = (message: string, script?: HTMLScriptElement | null) => {
      loadPromise = null;
      removeFailedScript(script ?? null);
      // Plain string (not Error) avoids Next.js treating this as a redbox-worthy console error
      // when callers log the rejection during iframe fallback.
      reject(message);
    };

    const finish = (script?: HTMLScriptElement | null) => {
      if (window.Desmos?.GraphingCalculator) {
        resolve(window.Desmos);
        return;
      }
      fail("Desmos failed to initialize", script);
    };

    const existing = document.querySelector<HTMLScriptElement>(
      `script[data-desmos-api="1"]`
    );
    if (existing) {
      if (window.Desmos?.GraphingCalculator) {
        finish(existing);
        return;
      }
      // Stale failed tag from a previous attempt — replace it.
      if (existing.dataset.desmosFailed === "1") {
        removeFailedScript(existing);
      } else {
        existing.addEventListener("load", () => finish(existing));
        existing.addEventListener("error", () => {
          existing.dataset.desmosFailed = "1";
          fail("Desmos script failed to load", existing);
        });
        return;
      }
    }

    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.dataset.desmosApi = "1";
    script.onload = () => finish(script);
    script.onerror = () => {
      script.dataset.desmosFailed = "1";
      fail("Desmos script failed to load", script);
    };
    document.head.appendChild(script);
  });

  return loadPromise;
}

/** Wait until an element has a non-zero box (Desmos needs real dimensions). */
export function waitForSize(
  el: HTMLElement,
  timeoutMs = 2000
): Promise<{ width: number; height: number }> {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      const width = el.clientWidth;
      const height = el.clientHeight;
      if (width > 40 && height > 40) {
        resolve({ width, height });
        return;
      }
      if (Date.now() - start > timeoutMs) {
        reject(new Error("Calculator container never sized"));
        return;
      }
      requestAnimationFrame(check);
    };
    check();
  });
}
