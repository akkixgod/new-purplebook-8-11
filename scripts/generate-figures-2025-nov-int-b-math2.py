#!/usr/bin/env python3
"""Clean SAT-style SVG figures for 2025 Nov International B Math Module 2 (hard)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-nov-int-b/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, 'Times New Roman', serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table(
    headers: list[str],
    rows: list[list[str]],
    widths: list[int],
    *,
    italic: set[tuple[int, int]] | None = None,
) -> str:
    italic = italic or set()
    row_h = 36
    x0, y0 = 8, 8
    height = y0 * 2 + row_h * (1 + len(rows))
    width = x0 * 2 + sum(widths)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]

    def cell(text: str, x: int, y: int, w: int, header: bool, use_italic: bool) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = ' font-weight="700"' if header else ""
        style = ' font-style="italic"' if use_italic else ""
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{row_h}" fill="{fill}" stroke="#111"/>')
        parts.append(
            f'<text x="{x + w / 2}" y="{y + 23}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="15"{weight}{style}>{text}</text>'
        )

    x = x0
    for c, header in enumerate(headers):
        cell(header, x, y0, widths[c], True, (-1, c) in italic)
        x += widths[c]
    for r, row in enumerate(rows):
        x = x0
        y = y0 + row_h * (r + 1)
        for c, value in enumerate(row):
            cell(value, x, y, widths[c], False, (r, c) in italic)
            x += widths[c]
    parts.append("</svg>")
    return "\n".join(parts)


def parallel_lines() -> str:
    # Transversal k falls left-to-right across vertical lines r and s.
    # w and x sit on the right of r (w above k, x below k).
    # y and z sit on the right of s (y above k, z below k).
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="460" viewBox="0 0 420 460">
<rect width="100%" height="100%" fill="#fff"/>
<line x1="150" y1="36" x2="150" y2="390" stroke="#111" stroke-width="1.75"/>
<line x1="290" y1="36" x2="290" y2="390" stroke="#111" stroke-width="1.75"/>
<line x1="36" y1="66" x2="384" y2="414" stroke="#111" stroke-width="1.75"/>
<text x="22" y="58" font-family="{FONT}" font-size="18" font-style="italic">k</text>
<text x="142" y="28" font-family="{FONT}" font-size="18" font-style="italic">r</text>
<text x="282" y="28" font-family="{FONT}" font-size="18" font-style="italic">s</text>
<text x="162" y="158" font-family="{FONT}" font-size="17" font-style="italic">w°</text>
<text x="162" y="214" font-family="{FONT}" font-size="17" font-style="italic">x°</text>
<text x="302" y="298" font-family="{FONT}" font-size="17" font-style="italic">y°</text>
<text x="302" y="354" font-family="{FONT}" font-size="17" font-style="italic">z°</text>
<text x="210" y="442" text-anchor="middle" font-family="{FONT}" font-size="13" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def triangle() -> str:
    # Right angle at R. Leg SR = 23 is the base; QR is the vertical leg, drawn shorter.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="300" viewBox="0 0 420 300">
<rect width="100%" height="100%" fill="#fff"/>
<polygon points="48,210 340,210 340,78" fill="none" stroke="#111" stroke-width="2"/>
<path d="M340 194 H324 V210" fill="none" stroke="#111" stroke-width="1.6"/>
<text x="32" y="228" font-family="{FONT}" font-size="18" font-style="italic">S</text>
<text x="348" y="228" font-family="{FONT}" font-size="18" font-style="italic">R</text>
<text x="348" y="74" font-family="{FONT}" font-size="18" font-style="italic">Q</text>
<text x="194" y="234" text-anchor="middle" font-family="{FONT}" font-size="18">23</text>
<text x="210" y="274" text-anchor="middle" font-family="{FONT}" font-size="13" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def exponential() -> str:
    # y = 5^x - 8. Asymptote y = -8. Grid -10 to 10, labels every 2.
    left, top, size = 58, 28, 420
    right, bottom = left + size, top + size
    unit = size / 20

    def sx(x: float) -> float:
        return left + (x + 10) * unit

    def sy(y: float) -> float:
        return bottom - (y + 10) * unit

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="500" viewBox="0 0 520 500">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        "<defs>",
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">',
        '<path d="M0,0 L7,3 L0,6 Z" fill="#111"/>',
        "</marker>",
        "</defs>",
    ]
    for v in range(-10, 11):
        parts.append(
            f'<line x1="{sx(v):.1f}" y1="{top}" x2="{sx(v):.1f}" y2="{bottom}" stroke="#d4d4d4" stroke-width="1"/>'
        )
        parts.append(
            f'<line x1="{left}" y1="{sy(v):.1f}" x2="{right}" y2="{sy(v):.1f}" stroke="#d4d4d4" stroke-width="1"/>'
        )
    for v in range(-10, 11, 2):
        if v == 0:
            continue
        parts.append(
            f'<text x="{sx(v):.1f}" y="{sy(0) + 16:.1f}" text-anchor="middle" font-family="{FONT}" font-size="13">{v}</text>'
        )
        parts.append(
            f'<text x="{sx(0) - 8:.1f}" y="{sy(v) + 4:.1f}" text-anchor="end" font-family="{FONT}" font-size="13">{v}</text>'
        )
    parts.append(
        f'<line x1="{left}" y1="{sy(0):.1f}" x2="{right + 16}" y2="{sy(0):.1f}" stroke="#111" stroke-width="1.6" marker-end="url(#arrow)"/>'
    )
    parts.append(
        f'<line x1="{sx(0):.1f}" y1="{bottom}" x2="{sx(0):.1f}" y2="{top - 14}" stroke="#111" stroke-width="1.6" marker-end="url(#arrow)"/>'
    )
    parts.append(
        f'<text x="{sx(0) - 12:.1f}" y="{sy(0) + 16:.1f}" text-anchor="end" font-family="{FONT}" font-size="14">O</text>'
    )
    parts.append(
        f'<text x="{right + 22}" y="{sy(0) + 5:.1f}" font-family="{FONT}" font-size="16" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10:.1f}" y="{top - 16}" font-family="{FONT}" font-size="16" font-style="italic">y</text>'
    )

    pts: list[str] = []
    x = -10.0
    while x <= 3:
        y = (5**x) - 8
        if y >= 10:
            # land on the top grid line
            y0 = (5 ** (x - 0.02)) - 8
            t = (10 - y0) / (y - y0) if y != y0 else 1
            xf = (x - 0.02) + t * 0.02
            pts.append(f"{sx(xf):.2f},{sy(10):.2f}")
            break
        pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.02
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("math2-q01-parallel-lines.svg", parallel_lines())
    write("math2-q11-triangle.svg", triangle())
    write("math2-q12-exponential.svg", exponential())
    write(
        "math2-q20-similar-rectangles.svg",
        table(
            ["", "Area (square inches)", "Perimeter (inches)"],
            [["Rectangle A", "660", "220"], ["Rectangle B", "2,640", "n"]],
            [150, 200, 180],
            italic={(1, 2)},
        ),
    )
    print("done")


if __name__ == "__main__":
    main()
