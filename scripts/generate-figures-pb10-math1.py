#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 10 Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-10/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math1_q05_population() -> str:
    """Population line: (0, 3) through ~ (2, 4.3) to (5, 6.25); y 0–14, x 0–5."""
    W, H = 480, 460
    pad_l, pad_r, pad_t, pad_b = 56, 28, 24, 56
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = 0.0, 5.0
    ymin, ymax = 0.0, 14.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(0, 6):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 15):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(0, 6):
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in range(0, 15, 2):
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    # Line from (0, 3) to (5, 6.25) → at x=2, y=4.3
    x1, y1, x2, y2 = 0.0, 3.0, 5.0, 6.25
    parts.append(
        f'<line x1="{sx(x1)}" y1="{sy(y1)}" x2="{sx(x2)}" y2="{sy(y2)}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    parts.append(
        f'<text x="{(pad_l + pad_l + plot_w) / 2}" y="{H - 12}" text-anchor="middle" '
        f'font-family="Arial" font-size="13">Years after census was taken</text>'
    )
    parts.append(
        f'<text x="16" y="{(pad_t + pad_t + plot_h) / 2}" text-anchor="middle" '
        f'font-family="Arial" font-size="13" '
        f'transform="rotate(-90 16 {(pad_t + pad_t + plot_h) / 2})">'
        f"Population (in thousands)</text>"
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q17_line_k() -> str:
    """Line k: y = −(3/2)x − 1 on axes from −6 to 6."""
    W, H = 460, 460
    pad_l, pad_r, pad_t, pad_b = 40, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -6.0, 6.0
    ymin, ymax = -6.0, 6.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{sx(xmin)}" y1="{sy(0)}" x2="{sx(xmax)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(ymin)}" x2="{sx(0)}" y2="{sy(ymax)}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(int(xmin), int(xmax) + 1, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(int(ymin), int(ymax) + 1, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{sx(0) - 8}" y="{sy(0) + 14}" text-anchor="end" '
        f'font-family="Arial" font-size="11">0</text>'
    )

    # Clip y = −1.5x − 1 to plot bounds
    def clip_seg(xa: float, ya: float, xb: float, yb: float):
        pts = []
        for t_i in range(401):
            t = t_i / 400
            x = xa + t * (xb - xa)
            y = ya + t * (yb - ya)
            if xmin <= x <= xmax and ymin <= y <= ymax:
                pts.append((x, y))
        if not pts:
            return xa, ya, xb, yb
        return pts[0][0], pts[0][1], pts[-1][0], pts[-1][1]

    cx1, cy1, cx2, cy2 = clip_seg(xmin, -1.5 * xmin - 1, xmax, -1.5 * xmax - 1)
    parts.append(
        f'<line x1="{sx(cx1)}" y1="{sy(cy1)}" x2="{sx(cx2)}" y2="{sy(cy2)}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    parts.append(
        f'<text x="{sx(3.2)}" y="{sy(-5.2)}" font-family="Arial" font-size="16" '
        f'font-style="italic">k</text>'
    )
    parts.append(
        f'<text x="{sx(xmax) + 6}" y="{sy(0) + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 6}" y="{sy(ymax) - 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q19_triangle() -> str:
    """Right triangle RST: right angle at S; hypotenuse RT labeled 67."""
    # T bottom-left, S bottom-right (right angle), R top
    Tx, Ty = 70, 250
    Sx, Sy = 340, 250
    Rx, Ry = 340, 70
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Tx},{Ty} {Sx},{Sy} {Rx},{Ry}" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="{Sx - 20}" y="{Sy - 20}" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{Tx - 18}" y="{Ty + 6}" font-family="Arial" font-size="16" font-style="italic">T</text>
  <text x="{Sx + 10}" y="{Sy + 18}" font-family="Arial" font-size="16" font-style="italic">S</text>
  <text x="{Rx + 10}" y="{Ry + 6}" font-family="Arial" font-size="16" font-style="italic">R</text>
  <text x="{(Tx + Rx) / 2 - 10}" y="{(Ty + Ry) / 2 - 8}" font-family="Arial" font-size="16">67</text>
  <text x="210" y="300" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def main() -> None:
    write("math1-q05-population.svg", math1_q05_population())
    write("math1-q17-line-k.svg", math1_q17_line_k())
    write("math1-q19-triangle.svg", math1_q19_triangle())


if __name__ == "__main__":
    main()
