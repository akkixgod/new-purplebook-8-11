#!/usr/bin/env python3
"""Generate Eng M1 graph/table SVGs for 2025 March US-A."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-us-a" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INT_E_TABLE = (
    ROOT / "public" / "mocks" / "2025-march-int-e" / "figures" / "eng1-q12-productivity-loss.svg"
)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fta_bar_chart(path: Path) -> None:
    # Measured from page-13.png on the −10 to 40 grid.
    # Costa Rica Post-FTA is 13.5, matching the value quoted in choice C.
    # Morocco Pre-FTA is the tallest Pre bar (~20); Morocco Post-FTA drops to ~5 —
    # the relationship the correct answer (D) depends on.
    # Jordan Pre-FTA is the only negative bar (axis includes −10 for that reason).
    tw, th = 720, 460
    left, right, top, bottom = 70, 460, 90, 380
    y_min, y_max = -10, 40
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
    for tick in range(-10, 45, 5):
        yy = y_to_px(tick)
        parts.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#ddd" stroke-width="1"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{tick}</text>'
        )

    groups = [
        ("Pre-FTA", [10.0, -5.0, 20.0]),
        ("Post-FTA", [13.5, 37.0, 5.0]),
    ]
    colors = ["#4b5563", "#d1d5db", "#111"]
    labels = ["Costa Rica (CAFTA-DR)", "Jordan (JOFTA)", "Morocco (MAFTA)"]
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
    fta_bar_chart(OUT / "eng1-q14-fta-export-growth.svg")
    dest = OUT / "eng1-q12-productivity-loss.svg"
    shutil.copyfile(INT_E_TABLE, dest)
    print("copied", dest.name)


if __name__ == "__main__":
    main()
