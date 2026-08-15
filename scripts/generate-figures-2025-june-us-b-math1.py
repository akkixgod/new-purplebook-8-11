#!/usr/bin/env python3
"""Generate clean SVG figures for 2025 June US-B Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def math1_q01_linear() -> None:
    """Line y = -x/4 - 6 on -8..8 grid; y-intercept (0, -6)."""
    W, H = 420, 400
    pad = 40
    plot = 320
    xmin, xmax = -8.0, 8.0
    ymin, ymax = -8.0, 8.0

    def sx(x: float) -> float:
        return pad + ((x - xmin) / (xmax - xmin)) * plot

    def sy(y: float) -> float:
        return pad + ((ymax - y) / (ymax - ymin)) * plot

    def f(x: float) -> float:
        return -x / 4 - 6

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
    x0, x1 = -8.0, 8.0
    parts.append(
        f'<line x1="{sx(x0):.2f}" y1="{sy(f(x0)):.2f}" x2="{sx(x1):.2f}" y2="{sy(f(x1)):.2f}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
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


def math1_q02_rocks() -> None:
    headers = ["Classification", "Frequency"]
    rows = [
        ["igneous", "10"],
        ["metamorphic", "38"],
        ["sedimentary", "22"],
    ]
    col_w = [160, 110]
    row_h = 40
    header_h = 36
    title_block = 12
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    y = title_block
    x0 = 20

    def cell(x: float, yy: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        parts.append(
            f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + w/2}" y="{yy + h/2 + 4}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="13" font-weight="{weight}">{esc(text)}</text>'
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
    write("math1-q02-rock-frequency.svg", "\n".join(parts))


def main() -> None:
    math1_q01_linear()
    math1_q02_rocks()


if __name__ == "__main__":
    main()
