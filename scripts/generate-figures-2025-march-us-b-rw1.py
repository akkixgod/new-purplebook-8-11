#!/usr/bin/env python3
"""Generate Eng M1 line-graph SVGs for 2025 March US-B.

Values measured from public/mocks/2025-march-us-b/pages/page-11.png (Q10)
and page-12.png (Q11). Style follows generate-figures-2025-march-int-e-rw1.py
and generate-figures-2025-june-us-b-eng.py (Georgia, no watermark).
"""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def marker(kind: str, x: float, y: float, color: str) -> str:
    if kind == "tri":
        return f'<polygon points="{x},{y-6} {x-6},{y+5} {x+6},{y+5}" fill="{color}"/>'
    if kind == "sq":
        return (
            f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="#fff" '
            f'stroke="{color}" stroke-width="1.5"/>'
        )
    return f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{color}" stroke-width="1.5"/>'


def chorotega_forest() -> None:
    """Q10 — measured from page-11.png on the 0–150 hectare grid."""
    W, H = 640, 500
    pad_l, pad_r, pad_t, pad_b = 70, 36, 78, 148
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 150
    years = ["1960", "1979", "1986", "2000"]
    # Class VIII filled triangles; Class VI open squares; Class VII open circles.
    series = [
        ("Class VIII (cannot be used for commercial crops)", "0", "tri", "#111", [125, 125, 38, 61]),
        ("Class VI (severe limitations on use for crops)", "6 4", "sq", "#6b7280", [67, 77, 20, 35]),
        ("Class VII (very severe limitations on use for crops)", "2 3", "circ", "#111", [76, 87, 28, 49]),
    ]

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + ((y_max - v) / y_max) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">'
        "Annual Mean Forest Patch Size for Three Land Use</text>",
        f'<text x="{W/2}" y="40" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">'
        "Capability Classes in the Chorotega Region, Costa Rica</text>",
        f'<text x="16" y="{pad_t + plot_h/2}" text-anchor="middle" font-family="{FONT}" font-size="12" '
        f'transform="rotate(-90 16 {pad_t + plot_h/2})">Mean patch size (hectares)</text>',
    ]
    for v in range(0, 151, 25):
        parts.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    parts.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i, yr in enumerate(years):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t+plot_h+22}" text-anchor="middle" font-family="{FONT}" font-size="12">{yr}</text>'
        )
    parts.append(
        f'<text x="{pad_l+plot_w/2}" y="{pad_t+plot_h+40}" text-anchor="middle" font-family="{FONT}" font-size="12">Year</text>'
    )
    for _name, dash, kind, color, vals in series:
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals))
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"{dashattr}/>')
        for i, v in enumerate(vals):
            parts.append(marker(kind, sx(i), sy(v), color))

    lx, ly = pad_l, H - 92
    for i, (name, dash, kind, color, _vals) in enumerate(series):
        y = ly + i * 28
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(f'<line x1="{lx}" y1="{y}" x2="{lx+28}" y2="{y}" stroke="{color}" stroke-width="2"{dashattr}/>')
        parts.append(marker(kind, lx + 14, y, color))
        parts.append(f'<text x="{lx+36}" y="{y+4}" font-family="{FONT}" font-size="11">{esc(name)}</text>')

    parts.append("</svg>")
    write("eng1-q10-forest-patches.svg", "\n".join(parts))


def taiwan_fish() -> None:
    """Q11 — measured from page-12.png on the 0–65 grid."""
    W, H = 640, 460
    pad_l, pad_r, pad_t, pad_b = 70, 40, 70, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 65
    months = ["January 2001", "April 2001", "July 2001", "October 2001"]
    series = [
        ("combtooth blenny", "0", "tri", "#111", [62, 3, 3, 1]),
        ("barred flagtail", "6 4", "sq", "#6b7280", [14, 9, 7, 16]),
        ("striated rockskipper", "2 3", "circ", "#111", [0, 0, 5, 4]),
    ]

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + ((y_max - v) / y_max) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="24" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">'
        "Fish Population in a Taiwanese Tide Pool,</text>",
        f'<text x="{W/2}" y="44" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">'
        "January 2001 to October 2001</text>",
        f'<text x="18" y="{pad_t + plot_h/2}" text-anchor="middle" font-family="{FONT}" font-size="12" '
        f'transform="rotate(-90 18 {pad_t + plot_h/2})">Number of individual fish observed</text>',
    ]
    for v in range(0, 66, 5):
        parts.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    parts.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i, m in enumerate(months):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t+plot_h+28}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11" transform="rotate(-25 {sx(i)} {pad_t+plot_h+28})">{m}</text>'
        )
    parts.append(
        f'<text x="{pad_l+plot_w/2}" y="{H-14}" text-anchor="middle" font-family="{FONT}" font-size="12">Month</text>'
    )
    for _name, dash, kind, color, vals in series:
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals))
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"{dashattr}/>')
        for i, v in enumerate(vals):
            parts.append(marker(kind, sx(i), sy(v), color))

    lx, ly = pad_l, H - 36
    gap = 195
    for i, (name, dash, kind, color, _vals) in enumerate(series):
        x = lx + i * gap
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(f'<line x1="{x}" y1="{ly}" x2="{x+28}" y2="{ly}" stroke="{color}" stroke-width="2"{dashattr}/>')
        parts.append(marker(kind, x + 14, ly, color))
        parts.append(f'<text x="{x+36}" y="{ly+4}" font-family="{FONT}" font-size="11">{esc(name)}</text>')

    parts.append("</svg>")
    write("eng1-q11-fish-population.svg", "\n".join(parts))


def main() -> None:
    chorotega_forest()
    taiwan_fish()


if __name__ == "__main__":
    main()
