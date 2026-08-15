#!/usr/bin/env python3
"""Generate clean SVG figures for 2025 June US-A (RW + Math1; Math2 has its own script)."""

from __future__ import annotations

import shutil
from pathlib import Path

OUT = Path("public/mocks/2025-june-us-a/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    name: str,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
) -> None:
    row_h = 40
    header_h = 48 if any(len(h) > 18 for h in headers) else 36
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
            f'font-family="{FONT}" font-size="12" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 11 if len(text) > 24 else 13
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
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
    write(name, "\n".join(parts))


def eng1_q13_grape() -> None:
    # Grouped bars: opposite / same side × Amur, frost, riverbank
    W, H = 560, 420
    pad_l, pad_r, pad_t, pad_b = 60, 30, 70, 90
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 650
    cats = ["opposite side", "same side"]
    series = [
        ("Amur grape", "#4b5563", [150, 60]),
        ("frost grape", "#d1d5db", [110, 45]),
        ("riverbank grape", "#111", [650, 200]),
    ]
    n_cat = len(cats)
    group_w = plot_w / n_cat
    bar_w = group_w / (len(series) + 1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">'
        "Orientation of Leaf Pairs in Grapevines</text>",
    ]
    for v in range(0, 651, 50):
        y = pad_t + plot_h - (v / ymax) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<text x="{pad_l-8}" y="{y+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="10">{v}</text>'
        )
    for ci, cat in enumerate(cats):
        gx = pad_l + ci * group_w
        for si, (lab, fill, vals) in enumerate(series):
            h = (vals[ci] / ymax) * plot_h
            x = gx + (si + 0.5) * bar_w
            y = pad_t + plot_h - h
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w*0.9:.1f}" height="{h:.1f}" fill="{fill}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + group_w/2}" y="{pad_t+plot_h+22}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="12">{cat}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<text x="16" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="{ARIAL}" font-size="11" '
        f'transform="rotate(-90 16 {pad_t+plot_h/2})">Number of pairs</text>'
    )
    # legend
    lx = pad_l
    ly = H - 28
    for si, (lab, fill, _) in enumerate(series):
        x = lx + si * 160
        parts.append(f'<rect x="{x}" y="{ly-10}" width="14" height="14" fill="{fill}" stroke="#111"/>')
        parts.append(
            f'<text x="{x+20}" y="{ly+2}" font-family="{ARIAL}" font-size="11">{lab}</text>'
        )
    parts.append("</svg>")
    write("eng1-q13-grape-orientation.svg", "\n".join(parts))


def eng2_q10_painting() -> None:
    W, H = 520, 400
    pad_l, pad_r, pad_t, pad_b = 55, 30, 70, 80
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 0.4
    cats = ["Abstract", "Cubist"]
    series = [
        ("P3", "#4b5563", [0.16, 0.31]),
        ("P5", "#d1d5db", [0.20, 0.34]),
        ("P2", "#111", [0.16, 0.28]),
    ]
    n_cat = len(cats)
    group_w = plot_w / n_cat
    bar_w = group_w / (len(series) + 1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">'
        "Correlation between Model-Predicted and</text>",
        f'<text x="{W/2}" y="40" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">'
        "Participant-Reported Enjoyment Ratings, by Painting Style</text>",
    ]
    for i in range(0, 5):
        v = i * 0.1
        y = pad_t + plot_h - (v / ymax) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<text x="{pad_l-8}" y="{y+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{v:.1f}</text>'
        )
    for ci, cat in enumerate(cats):
        gx = pad_l + ci * group_w
        for si, (lab, fill, vals) in enumerate(series):
            h = (vals[ci] / ymax) * plot_h
            x = gx + (si + 0.5) * bar_w
            y = pad_t + plot_h - h
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w*0.85:.1f}" height="{h:.1f}" fill="{fill}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + group_w/2}" y="{pad_t+plot_h+22}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="13">{cat}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<text x="14" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="{ARIAL}" font-size="11" '
        f'transform="rotate(-90 14 {pad_t+plot_h/2})">Correlation</text>'
    )
    lx = pad_l + 40
    ly = H - 22
    for si, (lab, fill, _) in enumerate(series):
        x = lx + si * 80
        parts.append(f'<rect x="{x}" y="{ly-10}" width="14" height="14" fill="{fill}" stroke="#111"/>')
        parts.append(f'<text x="{x+20}" y="{ly+2}" font-family="{ARIAL}" font-size="12">{lab}</text>')
    parts.append("</svg>")
    write("eng2-q10-painting-style-correlation.svg", "\n".join(parts))


def math1_q01_linear() -> None:
    W, H = 420, 400
    pad = 40
    plot = 320
    xmin, xmax = -8.0, 8.0
    ymin, ymax = -8.0, 8.0

    def sx(x: float) -> float:
        return pad + ((x - xmin) / (xmax - xmin)) * plot

    def sy(y: float) -> float:
        return pad + ((ymax - y) / (ymax - ymin)) * plot

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(-8, 9):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad}" x2="{sx(i):.1f}" y2="{pad+plot}" stroke="#eee"/>'
        )
        parts.append(
            f'<line x1="{pad}" y1="{sy(i):.1f}" x2="{pad+plot}" y2="{sy(i):.1f}" stroke="#eee"/>'
        )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    # y = 2x + 3
    parts.append(
        f'<line x1="{sx(-5.5):.2f}" y1="{sy(2*(-5.5)+3):.2f}" x2="{sx(2.5):.2f}" y2="{sy(2*2.5+3):.2f}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    for x, y in [(-2, -1), (-1, 1), (0, 3), (1, 5)]:
        parts.append(f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="4" fill="#111"/>')
    for i in range(-8, 9, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0)+14}" text-anchor="middle" font-family="{ARIAL}" font-size="11">{i}</text>'
        )
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(i)+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{i}</text>'
        )
    parts.append(
        f'<text x="{sx(0)+6}" y="{sy(0)+16}" font-family="{ARIAL}" font-size="12">O</text>'
    )
    parts.append(
        f'<text x="{pad+plot-6}" y="{sy(0)-8}" text-anchor="end" font-family="{ARIAL}" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0)+8}" y="{pad+14}" font-family="{ARIAL}" font-size="13" font-style="italic">y</text>'
    )
    parts.append("</svg>")
    write("math1-q01-linear-graph.svg", "\n".join(parts))


def math1_q02_seal() -> None:
    W, H = 440, 400
    pad_l, pad_r, pad_t, pad_b = 55, 30, 30, 55
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = 0.0, 6.0
    ymin, ymax = 0.0, 140.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    points = [(1, 78), (2, 97), (4, 103), (5, 122), (6, 125)]
    # LOBF approx through (0,73) and (6,127): y = 73 + 9x
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(0, 7):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad_t}" x2="{sx(i):.1f}" y2="{pad_t+plot_h}" stroke="#eee"/>'
        )
    for j in range(0, 141, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j):.1f}" x2="{pad_l+plot_w}" y2="{sy(j):.1f}" stroke="#eee"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0):.2f}" y1="{sy(73):.2f}" x2="{sx(6):.2f}" y2="{sy(127):.2f}" '
        f'stroke="#111" stroke-width="2"/>'
    )
    for x, y in points:
        parts.append(f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="4.5" fill="#111"/>')
    for i in range(0, 7):
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0)+16}" text-anchor="middle" font-family="{ARIAL}" font-size="11">{i}</text>'
        )
    for j in range(0, 141, 20):
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(j)+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l+plot_w/2}" y="{H-10}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Age (years)</text>'
    )
    parts.append(
        f'<text x="14" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="{ARIAL}" font-size="12" '
        f'transform="rotate(-90 14 {pad_t+plot_h/2})">Body length (cm)</text>'
    )
    parts.append("</svg>")
    write("math1-q02-seal-scatter.svg", "\n".join(parts))


def math1_q22_triangle() -> None:
    # Right triangle: C left with 30°, B right with right angle, A top; hypotenuse AC = 124
    C = (80, 280)
    B = (340, 280)
    A = (340, 80)
    write(
        "math1-q22-triangle.svg",
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="360" viewBox="0 0 440 360">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{B[0]-14}" y="{B[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <text x="{A[0]+10}" y="{A[1]+6}" font-family="{FONT}" font-size="16" font-weight="700">A</text>
  <text x="{B[0]+10}" y="{B[1]+22}" font-family="{FONT}" font-size="16" font-weight="700">B</text>
  <text x="{C[0]-18}" y="{C[1]+22}" font-family="{FONT}" font-size="16" font-weight="700">C</text>
  <text x="{C[0]+28}" y="{C[1]-12}" font-family="{ARIAL}" font-size="14">30°</text>
  <text x="{(A[0]+C[0])/2 - 10}" y="{(A[1]+C[1])/2}" font-family="{ARIAL}" font-size="15">124</text>
  <text x="220" y="340" text-anchor="middle" font-family="{ARIAL}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>''',
    )


def main() -> None:
    table_svg(
        "eng1-q11-non-native-trees.svg",
        "Numbers of the 23 Non-native Tree Species Reported\nand the Insect and Fungus Threats to Them",
        ["Country", "Trees", "Fungi", "Insects"],
        [
            ["Great Britain", "18", "290", "120"],
            ["Hungary", "1", "18", "13"],
            ["Switzerland", "11", "43", "78"],
        ],
        [160, 80, 80, 90],
    )
    eng1_q13_grape()
    eng2_q10_painting()
    math1_q01_linear()
    math1_q02_seal()
    table_svg(
        "math1-q06-task-times.svg",
        "",
        ["Task", "Time (minutes)"],
        [["A", "8"], ["B", "5"], ["C", "12"], ["D", "10"], ["E", "10"]],
        [100, 140],
    )
    # Q9 filler: copy Int-B function table if present
    src = Path("public/mocks/2025-june-int-b/figures/math1-q01-function-table.svg")
    dst = OUT / "math1-q09-function-table.svg"
    if src.exists():
        shutil.copyfile(src, dst)
        print("copied", dst.name)
    else:
        # recreate
        write(
            "math1-q09-function-table.svg",
            '''<svg xmlns="http://www.w3.org/2000/svg" width="220" height="240" viewBox="0 0 220 240">
  <rect width="100%" height="100%" fill="#fff"/>
  <rect x="40" y="20" width="70" height="40" fill="#f3f4f6" stroke="#111"/>
  <text x="75" y="46" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-weight="700">x</text>
  <rect x="110" y="20" width="70" height="40" fill="#f3f4f6" stroke="#111"/>
  <text x="145" y="46" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-weight="700">f(x)</text>
  <rect x="40" y="60" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="75" y="86" text-anchor="middle" font-family="Georgia, serif" font-size="15">-1</text>
  <rect x="110" y="60" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="145" y="78" text-anchor="middle" font-family="Georgia, serif" font-size="13">1</text>
  <line x1="130" y1="84" x2="160" y2="84" stroke="#111"/>
  <text x="145" y="98" text-anchor="middle" font-family="Georgia, serif" font-size="13">50</text>
  <rect x="40" y="100" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="75" y="126" text-anchor="middle" font-family="Georgia, serif" font-size="15">0</text>
  <rect x="110" y="100" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="145" y="126" text-anchor="middle" font-family="Georgia, serif" font-size="15">1</text>
  <rect x="40" y="140" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="75" y="166" text-anchor="middle" font-family="Georgia, serif" font-size="15">1</text>
  <rect x="110" y="140" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="145" y="166" text-anchor="middle" font-family="Georgia, serif" font-size="15">50</text>
  <rect x="40" y="180" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="75" y="206" text-anchor="middle" font-family="Georgia, serif" font-size="15">2</text>
  <rect x="110" y="180" width="70" height="40" fill="#fff" stroke="#111"/>
  <text x="145" y="206" text-anchor="middle" font-family="Georgia, serif" font-size="15">2,500</text>
</svg>''',
        )
    table_svg(
        "math1-q11-h-table.svg",
        "",
        ["x", "h(x)"],
        [["0", "17"], ["1", "18"], ["2", "20"]],
        [80, 80],
    )
    math1_q22_triangle()


if __name__ == "__main__":
    main()
