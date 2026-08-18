#!/usr/bin/env python3
"""Generate Eng M1 table/graph SVGs for 2025 March Int-E."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-e/figures")
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


def fish_line_graph(path: Path) -> None:
    """Line graph from page-09.png. Y-axis 0–30 (not the 0–65 sibling graphs)."""
    W, H = 640, 460
    pad_l, pad_r, pad_t, pad_b = 70, 40, 70, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 30
    months = ["January 2001", "April 2001", "July 2001", "October 2001"]
    series = [
        ("Cocos frillgoby", "0", "tri", "#111", [0, 10, 5, 5]),
        ("wavy-lined blenny", "7 5", "sq", "#6b7280", [0, 0, 0, 4]),
        ("Indo-Pacific sergeant", "2 3", "circ", "#111", [2, 3, 21, 28]),
    ]

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + ((y_max - v) / y_max) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="24" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Fish Population in a Taiwanese Tide Pool,</text>",
        f'<text x="{W/2}" y="44" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "January 2001 to October 2001</text>",
        f'<text x="18" y="{pad_t + plot_h/2}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
        f'transform="rotate(-90 18 {pad_t + plot_h/2})">Number of individual fish observed</text>',
    ]
    for v in range(0, 31, 5):
        parts.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{v}</text>'
        )
    parts.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i, m in enumerate(months):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t+plot_h+28}" text-anchor="middle" font-family="Georgia, serif" '
            f'font-size="11" transform="rotate(-25 {sx(i)} {pad_t+plot_h+28})">{m}</text>'
        )
    parts.append(
        f'<text x="{pad_l+plot_w/2}" y="{H-14}" text-anchor="middle" font-family="Georgia, serif" font-size="12">Month</text>'
    )

    def marker(kind: str, x: float, y: float, color: str) -> str:
        if kind == "tri":
            return f'<polygon points="{x},{y-6} {x-6},{y+5} {x+6},{y+5}" fill="{color}"/>'
        if kind == "sq":
            return (
                f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{color}" '
                f'stroke="#111" stroke-width="0.8"/>'
            )
        return f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{color}" stroke-width="1.5"/>'

    for _name, dash, kind, color, vals in series:
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals))
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"{dashattr}/>'
        )
        for i, v in enumerate(vals):
            parts.append(marker(kind, sx(i), sy(v), color))

    # legend
    lx, ly = pad_l, H - 36
    gap = 195
    for i, (name, dash, kind, color, _vals) in enumerate(series):
        x = lx + i * gap
        dashattr = f' stroke-dasharray="{dash}"' if dash != "0" else ""
        parts.append(f'<line x1="{x}" y1="{ly}" x2="{x+28}" y2="{ly}" stroke="{color}" stroke-width="2"{dashattr}/>')
        parts.append(marker(kind, x + 14, ly, color))
        parts.append(
            f'<text x="{x+36}" y="{ly+4}" font-family="Georgia, serif" font-size="11">{esc(name)}</text>'
        )

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def fta_bar_chart(path: Path) -> None:
    # Measured from page-11.png on the −5 to 25 grid (same College Board figure as int-b).
    # Nicaragua Pre-FTA is the tallest bar (~23.6), not 0%.
    # Mexico Pre-FTA is the only negative bar (axis includes −5 for that reason).
    # El Salvador Post-FTA is 21.8, matching the value quoted in choice C.
    tw, th = 720, 420
    left, right, top, bottom = 70, 460, 90, 340
    y_min, y_max = -5, 25
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{tw/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Average Total Agricultural Export Growth Rate, Five Years</text>",
        f'<text x="{tw/2}" y="48" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Pre- and Post-FTA with the United States</text>",
        f'<text x="28" y="{(top+bottom)/2}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
        f'transform="rotate(-90 28 {(top + bottom) / 2})">Growth rate (%)</text>',
        f'<text x="{(left+right)/2}" y="{th-18}" text-anchor="middle" font-family="Georgia, serif" font-size="12">'
        "Export growth</text>",
    ]

    def y_to_px(v: float) -> float:
        return bottom - (v - y_min) / (y_max - y_min) * (bottom - top)

    zero = y_to_px(0)
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111" stroke-width="1.5"/>')
    parts.append(f'<line x1="{left}" y1="{zero}" x2="{right}" y2="{zero}" stroke="#111" stroke-width="1.5"/>')
    for tick in range(-5, 30, 5):
        yy = y_to_px(tick)
        parts.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#ddd" stroke-width="1"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{tick}</text>'
        )

    groups = [
        ("Pre-FTA", [8.7, -1.4, 23.6]),
        ("Post-FTA", [21.8, 13.8, 17.7]),
    ]
    colors = ["#4b5563", "#d1d5db", "#111"]
    labels = ["El Salvador (CAFTA-DR)", "Mexico (NAFTA)", "Nicaragua (CAFTA-DR)"]
    group_w = (right - left) / 2
    bar_w = 28
    gap = 8

    for gi, (gname, vals) in enumerate(groups):
        gx = left + gi * group_w + group_w / 2
        start = gx - (3 * bar_w + 2 * gap) / 2
        for bi, val in enumerate(vals):
            x = start + bi * (bar_w + gap)
            y2 = y_to_px(val)
            top_y = min(zero, y2)
            h = abs(y2 - zero)
            parts.append(
                f'<rect x="{x}" y="{top_y}" width="{bar_w}" height="{max(h,1)}" fill="{colors[bi]}" '
                f'stroke="#111" stroke-width="0.5"/>'
            )
        parts.append(
            f'<text x="{gx}" y="{bottom+22}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{gname}</text>'
        )

    lx, ly = 490, 70
    for i, lab in enumerate(labels):
        yy = ly + i * 22
        parts.append(f'<rect x="{lx}" y="{yy-10}" width="14" height="14" fill="{colors[i]}" stroke="#111"/>')
        parts.append(
            f'<text x="{lx+20}" y="{yy+2}" font-family="Georgia, serif" font-size="11">{esc(lab)}</text>'
        )

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main() -> None:
    fish_line_graph(OUT / "eng1-q09-fish-population.svg")
    fta_bar_chart(OUT / "eng1-q11-fta-export-growth.svg")
    table_svg(
        OUT / "eng1-q12-productivity-loss.svg",
        "Average Monetized Productivity Loss at Two Points\nAfter Programs Began, in Australian Dollars",
        ["Type of training", "12 weeks", "12 months"],
        [
            ["EET", "268", "171"],
            ["EHP", "282", "436"],
        ],
        [160, 100, 100],
    )


if __name__ == "__main__":
    main()
