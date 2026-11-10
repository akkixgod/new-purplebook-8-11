#!/usr/bin/env python3
"""Clean SAT-style SVG figures for 2025 Nov International A Math Module 2 (hard)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-nov-int-a/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, 'Times New Roman', serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table(headers: list[str], rows: list[list[str]], widths: list[int], *, italic: set[tuple[int, int]] | None = None) -> str:
    """headers/rows are plain text. italic holds (row, col) with row -1 for the header."""
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


def scatter() -> str:
    # Axes 0–500. Grid every 50, labels every 100. Line of best fit y = 0.6x.
    left, top, size = 64, 36, 360
    right, bottom = left + size, top + size

    def sx(x: float) -> float:
        return left + (x / 500) * size

    def sy(y: float) -> float:
        return bottom - (y / 500) * size

    points = [
        (50, 30),
        (105, 90),
        (155, 78),
        (200, 120),
        (250, 180),
        (305, 145),
        (360, 216),
        (400, 198),
        (455, 318),
        (490, 294),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="470" viewBox="0 0 480 470">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<defs>',
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">',
        '<path d="M0,0 L7,3 L0,6 Z" fill="#111"/>',
        "</marker>",
        "</defs>",
    ]
    for v in range(50, 501, 50):
        parts.append(
            f'<line x1="{sx(v):.1f}" y1="{top}" x2="{sx(v):.1f}" y2="{bottom}" stroke="#d0d0d0" stroke-width="1"/>'
        )
        parts.append(
            f'<line x1="{left}" y1="{sy(v):.1f}" x2="{right}" y2="{sy(v):.1f}" stroke="#d0d0d0" stroke-width="1"/>'
        )
    for v in range(100, 501, 100):
        parts.append(
            f'<text x="{sx(v):.1f}" y="{bottom + 18}" text-anchor="middle" font-family="{FONT}" font-size="13">{v}</text>'
        )
        parts.append(
            f'<text x="{left - 10}" y="{sy(v) + 4:.1f}" text-anchor="end" font-family="{FONT}" font-size="13">{v}</text>'
        )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{right + 22}" y2="{bottom}" stroke="#111" stroke-width="1.6" marker-end="url(#arrow)"/>'
    )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top - 16}" stroke="#111" stroke-width="1.6" marker-end="url(#arrow)"/>'
    )
    parts.append(
        f'<text x="{left - 12}" y="{bottom + 16}" text-anchor="end" font-family="{FONT}" font-size="14">O</text>'
    )
    parts.append(
        f'<text x="{right + 28}" y="{bottom + 5}" font-family="{FONT}" font-size="16" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{left - 16}" y="{top - 18}" text-anchor="middle" font-family="{FONT}" font-size="16" font-style="italic">y</text>'
    )
    parts.append(
        f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(500):.1f}" y2="{sy(300):.1f}" stroke="#111" stroke-width="2"/>'
    )
    for x, y in points:
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="#111"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("math2-q02-parallel-lines.svg", parallel_lines())
    write(
        "math2-q03-food-tickets.svg",
        table(
            ["Number of food tickets", "Total amount paid"],
            [["10", "$44.00"], ["15", "$51.50"], ["25", "$66.50"]],
            [230, 190],
        ),
    )
    write("math2-q04-germination-scatter.svg", scatter())
    write(
        "math2-q08-line-table.svg",
        table(
            ["x", "y"],
            [["0", "−10"], ["1", "−4"], ["2", "2"]],
            [72, 72],
            italic={(-1, 0), (-1, 1)},
        ),
    )
    write(
        "math2-q17-mail-table.svg",
        table(
            ["Pieces of mail", "Days"],
            [
                ["0", "2"],
                ["3", "2"],
                ["4", "2"],
                ["5", "2"],
                ["6", "1"],
                ["7", "1"],
                ["13", "1"],
            ],
            [170, 90],
        ),
    )
    write(
        "math2-q20-similar-rectangles.svg",
        table(
            ["", "Area (square inches)", "Perimeter (inches)"],
            [["Rectangle A", "630", "210"], ["Rectangle B", "2,520", "n"]],
            [150, 200, 180],
            italic={(1, 2)},
        ),
    )
    print("done")


if __name__ == "__main__":
    main()
