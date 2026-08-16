#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-A figures."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-a/figures")
OUT.mkdir(parents=True, exist_ok=True)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    path: Path,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    title_size: int = 13,
) -> None:
    row_h = 40
    header_h = 52 if any(len(h) > 18 for h in headers) else 36
    title_lines = [ln for ln in title.split("\n") if ln]
    title_block = 18 + len(title_lines) * 18 if title_lines else 12
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{tw/2}" y="{20 + i * 18}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="{title_size}" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 11 if len(text) > 28 else 12
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        # wrap long header text
        if header and len(text) > 22:
            words = text.split()
            mid = (len(words) + 1) // 2
            l1 = " ".join(words[:mid])
            l2 = " ".join(words[mid:])
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="11" font-weight="{weight}">{esc(l1)}</text>'
            )
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 12}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="11" font-weight="{weight}">{esc(l2)}</text>'
            )
        else:
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
            )

    x = x0
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True)
        x += col_w[i]
    y += header_h
    for r in rows:
        x = x0
        for i, val in enumerate(r):
            cell(x, y, col_w[i], row_h, val, False)
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main() -> None:
    # --- English tables / chart ---
    table_svg(
        OUT / "eng1-q09-copper-mined.svg",
        "Millions of Metric Tons of Copper Mined\nin 1995 and 2020",
        ["Country", "1995", "2020"],
        [
            ["Indonesia", "0.44", "0.51"],
            ["United States", "1.85", "1.20"],
            ["Kazakhstan", "0.26", "0.55"],
            ["Chile", "2.49", "5.73"],
        ],
        [140, 80, 80],
    )
    table_svg(
        OUT / "eng1-q11-productivity-loss.svg",
        "Average Monetized Productivity Loss at Two Points\nAfter Programs Began, in Australian Dollars",
        ["Type of training", "12 weeks", "12 months"],
        [
            ["EET", "268", "171"],
            ["EHP", "282", "436"],
        ],
        [160, 100, 100],
    )

    # Story rating grouped bars
    stories = [
        ("A Dark Brown Dog", 3.5, 4.6),
        ("Owl Creek Bridge", 4.9, 5.1),
        ("Blitzed", 6.2, 7.1),
        ("A Chess Problem", 6.1, 7.2),
        ("The Calm", 4.3, 5.0),
        ("Plumbing", 4.1, 4.9),
    ]
    tw, th = 720, 420
    left, bottom, top, right = 70, 340, 50, 680
    plot_h = bottom - top
    plot_w = right - left
    ymax = 8
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{(left+right)/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">Story Rating: Spoiled vs. Unspoiled</text>',
        f'<text x="22" y="{(top+bottom)/2}" text-anchor="middle" transform="rotate(-90 22 {(top+bottom)/2})" font-family="Georgia, serif" font-size="11">Average enjoyment rating (1 = lowest; 10 = highest)</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#111"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111"/>',
    ]
    for yv in range(0, 9):
        yy = bottom - (yv / ymax) * plot_h
        parts.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{yv}</text>'
        )
    group_w = plot_w / len(stories)
    bar_w = group_w * 0.32
    for i, (name, unsp, spo) in enumerate(stories):
        cx = left + (i + 0.5) * group_w
        x1 = cx - bar_w - 2
        x2 = cx + 2
        h1 = (unsp / ymax) * plot_h
        h2 = (spo / ymax) * plot_h
        parts.append(
            f'<rect x="{x1}" y="{bottom-h1}" width="{bar_w}" height="{h1}" fill="#d1d5db" stroke="#111"/>'
        )
        parts.append(
            f'<rect x="{x2}" y="{bottom-h2}" width="{bar_w}" height="{h2}" fill="#4b5563" stroke="#111"/>'
        )
        # rotated label
        parts.append(
            f'<text x="{cx}" y="{bottom+12}" text-anchor="end" transform="rotate(-35 {cx} {bottom+12})" '
            f'font-family="Georgia, serif" font-size="10">"{esc(name)}"</text>'
        )
    # legend
    parts.append('<rect x="560" y="48" width="14" height="14" fill="#d1d5db" stroke="#111"/>')
    parts.append('<text x="580" y="60" font-family="Georgia, serif" font-size="12">unspoiled</text>')
    parts.append('<rect x="560" y="70" width="14" height="14" fill="#4b5563" stroke="#111"/>')
    parts.append('<text x="580" y="82" font-family="Georgia, serif" font-size="12">spoiled</text>')
    parts.append('<text x="360" y="400" text-anchor="middle" font-family="Georgia, serif" font-size="12">Story</text>')
    parts.append("</svg>")
    write(OUT / "eng1-q12-story-rating.svg", parts)

    # --- Math1 Q2 right triangle ---
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="280" viewBox="0 0 320 280">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<polygon points="40,220 240,220 240,70" fill="none" stroke="#111" stroke-width="2"/>',
        '<rect x="225" y="205" width="15" height="15" fill="none" stroke="#111" stroke-width="1.5"/>',
        '<text x="255" y="150" font-family="Georgia, serif" font-size="18">8</text>',
        '<text x="130" y="245" font-family="Georgia, serif" font-size="18" font-style="italic">b</text>',
        '<text x="110" y="130" font-family="Georgia, serif" font-size="18">20</text>',
        '<text x="160" y="270" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q02-right-triangle.svg", parts)

    # --- Math1 Q3 histogram ---
    freqs = [5, 3, 4, 3, 5]
    left, bottom, top, right = 60, 280, 30, 460
    plot_h = bottom - top
    plot_w = right - left
    bin_w = plot_w / 5
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="520" height="340" viewBox="0 0 520 340">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#111"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111"/>',
        f'<line x1="{right}" y1="{top}" x2="{right}" y2="{bottom}" stroke="#111"/>',
        f'<text x="{(left+right)/2}" y="325" text-anchor="middle" font-family="Georgia, serif" font-size="13">Length (feet)</text>',
        f'<text x="18" y="{(top+bottom)/2}" text-anchor="middle" transform="rotate(-90 18 {(top+bottom)/2})" font-family="Georgia, serif" font-size="13">Frequency</text>',
    ]
    for yv in range(0, 6):
        yy = bottom - (yv / 5) * plot_h
        parts.append(f'<line x1="{left-4}" y1="{yy}" x2="{left}" y2="{yy}" stroke="#111"/>')
        parts.append(f'<line x1="{right}" y1="{yy}" x2="{right+4}" y2="{yy}" stroke="#111"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="12">{yv}</text>'
        )
    for i, f in enumerate(freqs):
        x = left + i * bin_w
        h = (f / 5) * plot_h
        parts.append(
            f'<rect x="{x}" y="{bottom-h}" width="{bin_w}" height="{h}" fill="#9ca3af" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{x}" y="{bottom+16}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{i*50}</text>'
        )
    parts.append(
        f'<text x="{right}" y="{bottom+16}" text-anchor="middle" font-family="Georgia, serif" font-size="12">250</text>'
    )
    parts.append("</svg>")
    write(OUT / "math1-q03-histogram.svg", parts)

    # --- Math1 Q8 scatter ---
    # map: x in [-14,0] -> plot, y in [0,20]
    def sx(x):
        return 50 + (x + 14) / 14 * 320

    def sy(y):
        return 300 - y / 20 * 260

    pts = [(-14, 16), (-11.8, 14), (-9.8, 12.7), (-8, 11), (-5.8, 9), (-4, 5.4)]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for xv in range(-14, 1, 2):
        parts.append(f'<line x1="{sx(xv)}" y1="{sy(0)}" x2="{sx(xv)}" y2="{sy(20)}" stroke="#e5e7eb"/>')
        if xv < 0:
            parts.append(
                f'<text x="{sx(xv)}" y="{sy(0)+16}" text-anchor="middle" font-family="Georgia, serif" font-size="10">{xv}</text>'
            )
    for yv in range(2, 21, 2):
        parts.append(f'<line x1="{sx(-14)}" y1="{sy(yv)}" x2="{sx(0)}" y2="{sy(yv)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{sx(0)+12}" y="{sy(yv)+4}" font-family="Georgia, serif" font-size="10">{yv}</text>'
        )
    parts.append(f'<line x1="{sx(-14)}" y1="{sy(0)}" x2="{sx(0)+20}" y2="{sy(0)}" stroke="#111"/>')
    parts.append(f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(0)}" y2="{sy(20)+10}" stroke="#111"/>')
    parts.append(f'<text x="{sx(0)+28}" y="{sy(0)+4}" font-family="Georgia, serif" font-size="14" font-style="italic">x</text>')
    parts.append(f'<text x="{sx(0)+8}" y="{sy(20)-8}" font-family="Georgia, serif" font-size="14" font-style="italic">y</text>')
    parts.append(f'<text x="{sx(0)-8}" y="{sy(0)+14}" font-family="Georgia, serif" font-size="11">O</text>')
    parts.append(
        f'<line x1="{sx(-14)}" y1="{sy(16.3)}" x2="{sx(0)}" y2="{sy(2.3)}" stroke="#111" stroke-width="2"/>'
    )
    for x, y in pts:
        parts.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="3.5" fill="#111"/>')
    parts.append("</svg>")
    write(OUT / "math1-q08-scatterplot.svg", parts)

    # --- Math1 Q13 transversal ---
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="380" height="360" viewBox="0 0 380 360">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<line x1="120" y1="30" x2="120" y2="310" stroke="#111" stroke-width="2"/>',
        '<line x1="260" y1="30" x2="260" y2="310" stroke="#111" stroke-width="2"/>',
        '<line x1="50" y1="50" x2="330" y2="300" stroke="#111" stroke-width="2"/>',
        '<text x="112" y="24" font-family="Georgia, serif" font-size="16" font-style="italic">r</text>',
        '<text x="252" y="24" font-family="Georgia, serif" font-size="16" font-style="italic">s</text>',
        '<text x="40" y="48" font-family="Georgia, serif" font-size="16" font-style="italic">k</text>',
        '<text x="128" y="100" font-family="Georgia, serif" font-size="15" font-style="italic">w°</text>',
        '<text x="128" y="145" font-family="Georgia, serif" font-size="15" font-style="italic">x°</text>',
        '<text x="268" y="230" font-family="Georgia, serif" font-size="15" font-style="italic">y°</text>',
        '<text x="268" y="275" font-family="Georgia, serif" font-size="15" font-style="italic">z°</text>',
        '<text x="190" y="345" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q13-transversal.svg", parts)

    # --- Math1 Q21 cone ---
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="300" viewBox="0 0 360 300">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<ellipse cx="180" cy="220" rx="120" ry="28" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>',
        '<path d="M60,220 A120,28 0 0,0 300,220" fill="none" stroke="#111" stroke-width="2"/>',
        '<line x1="180" y1="50" x2="60" y2="220" stroke="#111" stroke-width="2"/>',
        '<line x1="180" y1="50" x2="300" y2="220" stroke="#111" stroke-width="2"/>',
        '<circle cx="180" cy="50" r="3.5" fill="#111"/>',
        '<text x="188" y="45" font-family="Georgia, serif" font-size="16" font-style="italic">A</text>',
        '<circle cx="90" cy="210" r="3.5" fill="#111"/>',
        '<text x="70" y="230" font-family="Georgia, serif" font-size="16" font-style="italic">B</text>',
        '<text x="180" y="285" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q21-cone.svg", parts)

    # --- Math2 Q1 ball height ---
    def bx(x):
        return 70 + x / 3.2 * 280

    def by(y):
        return 300 - y / 7.5 * 250

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="360" viewBox="0 0 400 360">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<line x1="{bx(0)}" y1="{by(0)}" x2="{bx(3.2)}" y2="{by(0)}" stroke="#111"/>',
        f'<line x1="{bx(0)}" y1="{by(0)}" x2="{bx(0)}" y2="{by(7.5)}" stroke="#111"/>',
    ]
    for xv in range(1, 4):
        parts.append(f'<line x1="{bx(xv)}" y1="{by(0)}" x2="{bx(xv)}" y2="{by(7)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{bx(xv)}" y="{by(0)+16}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{xv}</text>'
        )
    for yv in range(1, 8):
        parts.append(f'<line x1="{bx(0)}" y1="{by(yv)}" x2="{bx(3)}" y2="{by(yv)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{bx(0)-8}" y="{by(yv)+4}" text-anchor="end" font-family="Georgia, serif" font-size="12">{yv}</text>'
        )
    # parabola path
    pts = []
    for i in range(0, 50):
        x = i / 49 * 1.55
        y = -7.3 * (x - 0.65) ** 2 + 4.6
        if y < 0:
            break
        pts.append(f"{bx(x):.1f},{by(y):.1f}")
    parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{bx(1.0)}" cy="{by(3.9)}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{(bx(0)+bx(3))/2}" y="340" text-anchor="middle" font-family="Georgia, serif" font-size="12">Time (seconds)</text>'
    )
    parts.append(
        f'<text x="18" y="180" text-anchor="middle" transform="rotate(-90 18 180)" font-family="Georgia, serif" font-size="12">Height above ground (meters)</text>'
    )
    parts.append(f'<text x="{bx(3.2)+8}" y="{by(0)+4}" font-family="Georgia, serif" font-size="14" font-style="italic">x</text>')
    parts.append(f'<text x="{bx(0)+8}" y="{by(7.5)}" font-family="Georgia, serif" font-size="14" font-style="italic">y</text>')
    parts.append("</svg>")
    write(OUT / "math2-q01-ball-height.svg", parts)

    # --- Math2 Q4 similar triangles ---
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 300 360">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<line x1="60" y1="300" x2="230" y2="300" stroke="#111" stroke-width="2"/>',
        '<line x1="230" y1="300" x2="230" y2="40" stroke="#111" stroke-width="2"/>',
        '<line x1="60" y1="300" x2="230" y2="40" stroke="#111" stroke-width="2"/>',
        '<line x1="145" y1="170" x2="230" y2="170" stroke="#111" stroke-width="2"/>',
        '<rect x="215" y="285" width="15" height="15" fill="none" stroke="#111"/>',
        '<rect x="215" y="155" width="15" height="15" fill="none" stroke="#111"/>',
        '<text x="48" y="318" font-family="Georgia, serif" font-size="16" font-style="italic">A</text>',
        '<text x="236" y="318" font-family="Georgia, serif" font-size="16" font-style="italic">E</text>',
        '<text x="236" y="38" font-family="Georgia, serif" font-size="16" font-style="italic">C</text>',
        '<text x="236" y="175" font-family="Georgia, serif" font-size="16" font-style="italic">D</text>',
        '<text x="128" y="168" font-family="Georgia, serif" font-size="16" font-style="italic">B</text>',
        '<text x="150" y="345" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math2-q04-similar-triangles.svg", parts)

    # --- Math2 Q12 shaded inequality ---
    def ix(x):
        return 50 + (x + 10.5) / 11.5 * 280

    def iy(y):
        return 40 + (-y) / 16 * 280  # y from 0.5 to -15.5 mapped

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="360" height="400" viewBox="0 0 360 400">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        # clip shaded region above the line within plot
        '<defs><clipPath id="plot"><rect x="50" y="40" width="280" height="280"/></clipPath></defs>',
    ]
    # grid
    for xv in range(-10, 1):
        parts.append(f'<line x1="{ix(xv)}" y1="{iy(0)}" x2="{ix(xv)}" y2="{iy(-15)}" stroke="#d1d5db"/>')
    for yv in range(0, -16, -1):
        parts.append(f'<line x1="{ix(-10)}" y1="{iy(yv)}" x2="{ix(0)}" y2="{iy(yv)}" stroke="#d1d5db"/>')
    # shade above line: polygon from left to right along line then up
    # line y = -x/4 - 11
    x0, x1 = -10.5, 1
    y0 = -x0 / 4 - 11
    y1 = -x1 / 4 - 11
    parts.append(
        f'<polygon clip-path="url(#plot)" points="{ix(x0)},{iy(y0)} {ix(x1)},{iy(y1)} {ix(x1)},{iy(0.5)} {ix(x0)},{iy(0.5)}" fill="#b8b8b8"/>'
    )
    parts.append(
        f'<line x1="{ix(x0)}" y1="{iy(y0)}" x2="{ix(x1)}" y2="{iy(y1)}" stroke="#111" stroke-width="2.5"/>'
    )
    parts.append(f'<circle cx="{ix(-4)}" cy="{iy(-10)}" r="3.5" fill="#111"/>')
    parts.append(f'<circle cx="{ix(0)}" cy="{iy(-11)}" r="3.5" fill="#111"/>')
    parts.append(f'<line x1="{ix(-10.5)}" y1="{iy(0)}" x2="{ix(1)}" y2="{iy(0)}" stroke="#111"/>')
    parts.append(f'<line x1="{ix(0)}" y1="{iy(0.5)}" x2="{ix(0)}" y2="{iy(-15.5)}" stroke="#111"/>')
    for xv in [-10, -8, -6, -4, -2]:
        parts.append(
            f'<text x="{ix(xv)}" y="{iy(0)-8}" text-anchor="middle" font-family="Georgia, serif" font-size="10">{xv}</text>'
        )
    parts.append(f'<text x="{ix(0)-8}" y="{iy(0)-8}" font-family="Georgia, serif" font-size="11">O</text>')
    for yv in [-2, -4, -6, -8, -10, -12, -14]:
        parts.append(
            f'<text x="{ix(0)+10}" y="{iy(yv)+4}" font-family="Georgia, serif" font-size="10">{yv}</text>'
        )
    parts.append(f'<text x="{ix(1)+8}" y="{iy(0)+4}" font-family="Georgia, serif" font-size="14" font-style="italic">x</text>')
    parts.append(f'<text x="{ix(0)+8}" y="{iy(0.5)-4}" font-family="Georgia, serif" font-size="14" font-style="italic">y</text>')
    parts.append("</svg>")
    write(OUT / "math2-q12-shaded-inequality.svg", parts)

    # --- Math2 Q17 exponential ---
    def ex(x):
        return 80 + (x + 1.5) / 7 * 260

    def ey(y):
        return 280 - (y + 5) / 16 * 240

    pts = []
    x = -1.5
    while x <= 1.6:
        y = -(5**x) + 5
        if -5 <= y <= 11:
            pts.append(f"{ex(x):.1f},{ey(y):.1f}")
        x += 0.05
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="340" viewBox="0 0 400 340">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for xv in range(-1, 6):
        parts.append(f'<line x1="{ex(xv)}" y1="{ey(-5)}" x2="{ex(xv)}" y2="{ey(11)}" stroke="#e5e7eb"/>')
    for yv in range(-4, 12, 2):
        parts.append(f'<line x1="{ex(-1.5)}" y1="{ey(yv)}" x2="{ex(5)}" y2="{ey(yv)}" stroke="#e5e7eb"/>')
    parts.append(f'<line x1="{ex(-1.5)}" y1="{ey(0)}" x2="{ex(5.2)}" y2="{ey(0)}" stroke="#111"/>')
    parts.append(f'<line x1="{ex(0)}" y1="{ey(-5)}" x2="{ex(0)}" y2="{ey(11)}" stroke="#111"/>')
    parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>')
    for xv in [-1, 1, 2, 3, 4, 5]:
        parts.append(
            f'<text x="{ex(xv)}" y="{ey(0)+14}" text-anchor="middle" font-family="Georgia, serif" font-size="11">{xv}</text>'
        )
    parts.append(f'<text x="{ex(0)-10}" y="{ey(0)+14}" font-family="Georgia, serif" font-size="11">O</text>')
    for yv in [-4, -2, 2, 4, 6, 8, 10]:
        parts.append(
            f'<text x="{ex(0)-8}" y="{ey(yv)+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{yv}</text>'
        )
    parts.append(f'<text x="{ex(5.2)+4}" y="{ey(0)+4}" font-family="Georgia, serif" font-size="14" font-style="italic">x</text>')
    parts.append(f'<text x="{ex(0)+8}" y="{ey(11)}" font-family="Georgia, serif" font-size="14" font-style="italic">y</text>')
    parts.append("</svg>")
    write(OUT / "math2-q17-exponential-graph.svg", parts)

    print("done")


if __name__ == "__main__":
    main()
