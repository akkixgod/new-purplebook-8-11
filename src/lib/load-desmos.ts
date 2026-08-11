/** Load the official Desmos API script once; resolves with the global Desmos object. */

// Documented Desmos demo key (docs); override with NEXT_PUBLIC_DESMOS_API_KEY in production.
const DEMO_KEY = "dcb31709b452b1cf9dc6961159cdb094";

function apiSrc(): string {
  const key =
    (typeof process !== "undefined" && process.env.NEXT_PUBLIC_DESMOS_API_KEY) || DEMO_KEY;
  return `https://www.desmos.com/api/v1.10/calculator.js?apiKey=${encodeURIComponent(key)}`;
}

export interface DesmosCalculatorInstance {
  resize: () => void;
  destroy: () => void;
  getState: () => unknown;
  setState: (state: unknown, opts?: { allowUndo?: boolean }) => void;
  setBlank: () => void;
  updateSettings: (settings: Record<string, unknown>) => void;
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
    const finish = () => {
      if (window.Desmos?.GraphingCalculator) resolve(window.Desmos);
      else {
        loadPromise = null;
        reject(new Error("Desmos failed to initialize"));
      }
    };

    const existing = document.querySelector<HTMLScriptElement>(
      `script[data-desmos-api="1"]`
    );
    if (existing) {
      if (window.Desmos?.GraphingCalculator) {
        finish();
        return;
      }
      existing.addEventListener("load", finish);
      existing.addEventListener("error", () => {
        loadPromise = null;
        reject(new Error("Desmos script failed to load"));
      });
      return;
    }

    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.dataset.desmosApi = "1";
    script.onload = finish;
    script.onerror = () => {
      loadPromise = null;
      reject(new Error("Desmos script failed to load"));
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
