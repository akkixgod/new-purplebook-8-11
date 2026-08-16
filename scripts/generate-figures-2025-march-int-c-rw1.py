#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-C figures (English Module 1).

Q12 bar values come from `scripts/_measure-rw1-q12-march-int-c.py`, which calibrates
page-12.png's y axis from its gridlines and reads each bar's top edge.
"""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-c/figures")
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


def fta_bar_chart(path: Path) -> None:
    tw, th = 720, 470
    left, right, top, bottom = 70, 680, 90, 340
    y_min, y_max = -5, 15
    mid_y = (top + bottom) / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{tw/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Average Total Agricultural Export Growth Rate, Five Years</text>",
        f'<text x="{tw/2}" y="48" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Pre- and Post-FTA with the United States</text>",
        f'<text x="28" y="{mid_y}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
        f'transform="rotate(-90 28 {mid_y})">Growth rate (%)</text>',
        f'<text x="{(left+right)/2}" y="392" text-anchor="middle" font-family="Georgia, serif" font-size="12">'
        "Export growth</text>",
    ]

    def y_to_px(v: float) -> float:
        return bottom - (v - y_min) / (y_max - y_min) * (bottom - top)

    zero = y_to_px(0)
    parts.append(
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111" stroke-width="1.5"/>'
    )
    for tick in range(-5, 20, 5):
        yy = y_to_px(tick)
        parts.append(
            f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#ddd" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{tick}</text>'
        )
    parts.append(
        f'<line x1="{left}" y1="{zero}" x2="{right}" y2="{zero}" stroke="#111" stroke-width="1.5"/>'
    )

    groups = [
        ("Pre-FTA", [4.7, 9.9, -1.5]),
        ("Post-FTA", [3.1, 13.5, 13.7]),
    ]
    colors = ["#4b5563", "#d1d5db", "#111"]
    labels = ["Canada (NAFTA)", "Costa Rica (CAFTA-DR)", "Mexico (NAFTA)"]
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
                f'<rect x="{x}" y="{top_y}" width="{bar_w}" height="{max(h,1)}" '
                f'fill="{colors[bi]}" stroke="#111" stroke-width="0.5"/>'
            )
        parts.append(
            f'<text x="{gx}" y="{bottom+22}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{gname}</text>'
        )

    # Legend sits in a bordered box below the axis label, as on the source page.
    box_w, box_h = 190, 64
    bx = (left + right) / 2 - box_w / 2
    by = 400
    parts.append(
        f'<rect x="{bx}" y="{by}" width="{box_w}" height="{box_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
    )
    for i, lab in enumerate(labels):
        yy = by + 20 + i * 18
        parts.append(
            f'<rect x="{bx+14}" y="{yy-9}" width="11" height="11" fill="{colors[i]}" stroke="#111" stroke-width="0.7"/>'
        )
        parts.append(
            f'<text x="{bx+33}" y="{yy}" font-family="Georgia, serif" font-size="11">{esc(lab)}</text>'
        )

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main() -> None:
    fta_bar_chart(OUT / "eng1-q12-fta-export-growth.svg")

    table_svg(
        OUT / "eng1-q13-productivity-loss.svg",
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
