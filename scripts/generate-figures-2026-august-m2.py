#!/usr/bin/env python3
"""Clean SAT-style SVGs for 2026 August Module 2 (R&W methane flux graph)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-august-m2/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def methane_flux_graph() -> str:
    """Q11 — Methane Emission Flux Across Soil Temperatures."""
    W, H = 620, 460
    pad_l, pad_r, pad_t, pad_b = 78, 28, 58, 88
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 100
    temps = [0, 5, 10, 15, 20]
    # Approximate values read from the Bluebook screenshot (thermokarst >90 at 20°C).
    thermo = [5, 12, 28, 62, 93]
    intact = [2, 3, 5, 8, 13]

    def sx(i: int) -> float:
        return pad_l + (i / (len(temps) - 1)) * plot_w

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / ymax) * plot_h

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W / 2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700">'
        "Methane Emission Flux Across Soil Temperatures</text>",
    ]

    for v in range(0, 101, 20):
        y = sy(v)
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l + plot_w}" y2="{y:.1f}" '
            f'stroke="#d1d5db" stroke-width="1" stroke-dasharray="3 3"/>'
        )
        parts.append(
            f'<text x="{pad_l - 10}" y="{y + 4:.1f}" text-anchor="end" '
            f'font-family="{ARIAL}" font-size="12">{v}</text>'
        )

    # Intact mineral (dashed + triangles)
    pts_i = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(intact))
    parts.append(
        f'<polyline points="{pts_i}" fill="none" stroke="#6b7280" stroke-width="2" stroke-dasharray="7 5"/>'
    )
    for i, v in enumerate(intact):
        x, y = sx(i), sy(v)
        parts.append(
            f'<polygon points="{x:.1f},{y - 6:.1f} {x + 6:.1f},{y + 5:.1f} {x - 6:.1f},{y + 5:.1f}" '
            f'fill="#6b7280" stroke="#111" stroke-width="1"/>'
        )

    # Thermokarst bog (solid + open circles)
    pts_t = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(thermo))
    parts.append(
        f'<polyline points="{pts_t}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    for i, v in enumerate(thermo):
        x, y = sx(i), sy(v)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#fff" stroke="#111" stroke-width="2"/>'
        )

    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )

    for i, t in enumerate(temps):
        x = sx(i)
        parts.append(
            f'<text x="{x:.1f}" y="{pad_t + plot_h + 22}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="12">{t}°C</text>'
        )

    mid_y = pad_t + plot_h / 2
    parts.append(
        f'<text x="18" y="{mid_y:.1f}" text-anchor="middle" font-family="{ARIAL}" font-size="12" '
        f'transform="rotate(-90 18 {mid_y:.1f})">Methane flux (mg CH₄/m²/day)</text>'
    )
    parts.append(
        f'<text x="{pad_l + plot_w / 2}" y="{H - 18}" text-anchor="middle" '
        f'font-family="{ARIAL}" font-size="13">Soil incubation temperature (°C)</text>'
    )

    # Legend (upper-right of plot)
    lx, ly = pad_l + 168, pad_t + 18
    parts.append(
        f'<rect x="{lx}" y="{ly}" width="300" height="58" fill="#fff" stroke="#111" stroke-width="1"/>'
    )
    parts.append(
        f'<line x1="{lx + 14}" y1="{ly + 20}" x2="{lx + 48}" y2="{ly + 20}" stroke="#111" stroke-width="2.2"/>'
    )
    parts.append(
        f'<circle cx="{lx + 31}" cy="{ly + 20}" r="5" fill="#fff" stroke="#111" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{lx + 58}" y="{ly + 24}" font-family="{ARIAL}" font-size="12">'
        "Thermokarst bog soil (thawed)</text>"
    )
    parts.append(
        f'<line x1="{lx + 14}" y1="{ly + 42}" x2="{lx + 48}" y2="{ly + 42}" stroke="#6b7280" '
        f'stroke-width="2" stroke-dasharray="7 5"/>'
    )
    parts.append(
        f'<polygon points="{lx + 31},{ly + 36} {lx + 37},{ly + 47} {lx + 25},{ly + 47}" '
        f'fill="#6b7280" stroke="#111" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{lx + 58}" y="{ly + 46}" font-family="{ARIAL}" font-size="12">'
        "Intact mineral permafrost soil</text>"
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("eng2-q11-graph.svg", methane_flux_graph())


if __name__ == "__main__":
    main()
