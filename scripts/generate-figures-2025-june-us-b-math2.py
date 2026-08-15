#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 June US-B Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)

ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q09_orbital_dot_plot() -> str:
    """Dot plot: Orbital period (days) for 13 Jupiter moons."""
    # counts at integer days 720..732
    counts = {
        720: 1,
        721: 1,
        722: 0,
        723: 3,
        724: 2,
        725: 0,
        726: 1,
        727: 1,
        728: 1,
        729: 0,
        730: 2,
        731: 0,
        732: 1,
    }
    assert sum(counts.values()) == 13

    W, H = 520, 260
    pad_l, pad_r, pad_t, pad_b = 36, 36, 48, 56
    plot_w = W - pad_l - pad_r
    xmin, xmax = 719.5, 732.5
    baseline = H - pad_b
    r = 6
    gap = 14

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W / 2}" y="28" text-anchor="middle" font-family="{ARIAL}" '
        f'font-size="15" font-weight="700">Orbital period (days)</text>',
        f'<line x1="{pad_l}" y1="{baseline}" x2="{pad_l + plot_w}" y2="{baseline}" '
        f'stroke="#111" stroke-width="1.5"/>',
    ]

    for day in range(720, 733):
        x = sx(day)
        parts.append(
            f'<line x1="{x:.1f}" y1="{baseline}" x2="{x:.1f}" y2="{baseline + 5}" stroke="#111"/>'
        )
        if day % 2 == 0:
            parts.append(
                f'<text x="{x:.1f}" y="{baseline + 20}" text-anchor="middle" '
                f'font-family="{ARIAL}" font-size="12">{day}</text>'
            )
        for i in range(counts[day]):
            cy = baseline - 12 - i * gap
            parts.append(f'<circle cx="{x:.1f}" cy="{cy}" r="{r}" fill="#111"/>')

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("math2-q09-orbital-dot-plot.svg", math2_q09_orbital_dot_plot())
    print("done")


if __name__ == "__main__":
    main()
