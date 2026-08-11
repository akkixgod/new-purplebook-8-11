/** Load the official Desmos API script once; resolves with the global Desmos object. */

const DESMOS_API_SRC =
  "https://www.desmos.com/api/v1.11/calculator.js?apiKey=dcb31709b452b1cf9dc6961159cdb094";

export interface DesmosCalculatorInstance {
  resize: () => void;
  destroy: () => void;
  getState: () => unknown;
  setState: (state: unknown) => void;
  setBlank: () => void;
  updateSettings: (settings: Record<string, unknown>) => void;
}

/** @deprecated Use DesmosCalculatorInstance */
export type DesmosGraphingCalculator = DesmosCalculatorInstance;

export interface DesmosAPI {
  GraphingCalculator: (
    element: HTMLElement,
    options?: Record<string, unknown>
  ) => DesmosCalculatorInstance;
  ScientificCalculator: (
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
  if (window.Desmos) return Promise.resolve(window.Desmos);
  if (loadPromise) return loadPromise;

  loadPromise = new Promise<DesmosAPI>((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(
      `script[src^="https://www.desmos.com/api/"]`
    );
    if (existing) {
      existing.addEventListener("load", () => {
        if (window.Desmos) resolve(window.Desmos);
        else reject(new Error("Desmos failed to initialize"));
      });
      existing.addEventListener("error", () => reject(new Error("Desmos script failed to load")));
      if (window.Desmos) resolve(window.Desmos);
      return;
    }

    const script = document.createElement("script");
    script.src = DESMOS_API_SRC;
    script.async = true;
    script.onload = () => {
      if (window.Desmos) resolve(window.Desmos);
      else reject(new Error("Desmos failed to initialize"));
    };
    script.onerror = () => {
      loadPromise = null;
      reject(new Error("Desmos script failed to load"));
    };
    document.head.appendChild(script);
  });

  return loadPromise;
}
