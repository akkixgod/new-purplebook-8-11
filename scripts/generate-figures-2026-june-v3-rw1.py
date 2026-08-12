#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V3 R&W Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v3/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def grouped_bars_svg() -> str:
    # Approximate values from page-12 chart (relative heights sufficient for item).
    cats = ["Direct impact", "Indirect impact", "Induced impact"]
    v2019 = [34, 22, 13]
    v2022 = [38, 33, 16]

    W, H = 640, 420
    left, right, top, bottom = 70, 600, 70, 320
    ymax = 40

    def y_of(v: float) -> float:
        return bottom - (v / ymax) * (bottom - top)

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W / 2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">Value Added to Local Economies by RECs</text>',
        f'<text x="18" y="{(top + bottom) / 2}" text-anchor="middle" font-family="Georgia, serif" font-size="12" transform="rotate(-90 18 {(top + bottom) / 2})">Dollars (billions)</text>',
    ]

    for v in range(0, 41, 5):
        y = y_of(v)
        parts.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{left - 8}" y="{y + 4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{v}</text>'
        )

    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111"/>')
    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#111"/>')

    bar_w = 28
    gap = 8
    group_centers = [160, 330, 500]
    for i, cat in enumerate(cats):
        cx = group_centers[i]
        x1 = cx - bar_w - gap / 2
        y1 = y_of(v2019[i])
        parts.append(
            f'<rect x="{x1}" y="{y1}" width="{bar_w}" height="{bottom - y1}" fill="#4b5563" stroke="#111" stroke-width="1"/>'
        )
        x2 = cx + gap / 2
        y2 = y_of(v2022[i])
        parts.append(
            f'<rect x="{x2}" y="{y2}" width="{bar_w}" height="{bottom - y2}" fill="#d1d5db" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{bottom + 18}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{cat}</text>'
        )

    parts.append(
        f'<text x="{(left + right) / 2}" y="{bottom + 42}" text-anchor="middle" font-family="Georgia, serif" font-size="12">Type of impact</text>'
    )

    lx, ly = 480, 55
    parts.append(f'<rect x="{lx}" y="{ly}" width="14" height="14" fill="#4b5563" stroke="#111"/>')
    parts.append(f'<text x="{lx + 20}" y="{ly + 12}" font-family="Georgia, serif" font-size="12">2019</text>')
    parts.append(f'<rect x="{lx}" y="{ly + 22}" width="14" height="14" fill="#d1d5db" stroke="#111"/>')
    parts.append(f'<text x="{lx + 20}" y="{ly + 34}" font-family="Georgia, serif" font-size="12">2022</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("eng1-q11-rec-impacts.svg", grouped_bars_svg())


if __name__ == "__main__":
    main()
