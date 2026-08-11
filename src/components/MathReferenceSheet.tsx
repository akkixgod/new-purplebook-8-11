"use client";

type Props = {
  open: boolean;
  onClose: () => void;
};

/** Digital SAT Math reference sheet (Bluebook-style formulas). */
export function MathReferenceSheet({ open, onClose }: Props) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[110] flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
    >
      <div
        className="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-5 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label="Reference"
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900">Reference</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close reference"
            className="rounded p-1.5 text-gray-600 hover:bg-gray-100"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-4 text-sm text-gray-800">
          <section>
            <h3 className="mb-1.5 font-semibold text-gray-900">Area & volume</h3>
            <ul className="space-y-1 text-gray-700">
              <li>A<sub>rectangle</sub> = ℓw</li>
              <li>A<sub>triangle</sub> = ½bh</li>
              <li>A<sub>circle</sub> = πr²</li>
              <li>C<sub>circle</sub> = 2πr</li>
              <li>V<sub>rectangular prism</sub> = ℓwh</li>
              <li>V<sub>cylinder</sub> = πr²h</li>
              <li>V<sub>sphere</sub> = ⁴⁄₃πr³</li>
              <li>V<sub>cone</sub> = ⅓πr²h</li>
              <li>V<sub>pyramid</sub> = ⅓ℓwh</li>
            </ul>
          </section>

          <section>
            <h3 className="mb-1.5 font-semibold text-gray-900">Triangles</h3>
            <ul className="space-y-1 text-gray-700">
              <li>a² + b² = c² (right triangle)</li>
              <li>Special right: 30°–60°–90° → x : x√3 : 2x</li>
              <li>Special right: 45°–45°–90° → x : x : x√2</li>
            </ul>
          </section>

          <section>
            <h3 className="mb-1.5 font-semibold text-gray-900">Trigonometry</h3>
            <ul className="space-y-1 text-gray-700">
              <li>sin θ = opposite / hypotenuse</li>
              <li>cos θ = adjacent / hypotenuse</li>
              <li>tan θ = opposite / adjacent</li>
            </ul>
          </section>

          <section>
            <h3 className="mb-1.5 font-semibold text-gray-900">Circles & lines</h3>
            <ul className="space-y-1 text-gray-700">
              <li>Number of degrees in a circle = 360°</li>
              <li>Number of radians in a circle = 2π</li>
              <li>Slope: m = (y₂ − y₁) / (x₂ − x₁)</li>
              <li>Slope-intercept: y = mx + b</li>
            </ul>
          </section>

          <p className="text-xs text-gray-500 pt-1">
            The number π is approximately 3.14159.
          </p>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="mt-5 w-full rounded-lg bg-[#7c3aed] px-4 py-2 text-sm font-medium text-white hover:bg-[#6d28d9]"
        >
          Close
        </button>
      </div>
    </div>
  );
}
