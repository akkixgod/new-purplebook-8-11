#!/usr/bin/env python3
"""Generate English-section SVG figures for 2025 June US-B."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def eng1_q11_science() -> None:
    W, H = 560, 420
    pad_l, pad_r, pad_t, pad_b = 55, 30, 70, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    years = [2016, 2017, 2018, 2019]
    series = [
        ("cellular and molecular biology", "#111", "triangle", [200, 300, 280, 280]),
        ("physics and space science", "#4b5563", "square", [95, 90, 95, 100]),
        ("medicine and health", "#6b7280", "circle", [220, 220, 225, 285]),
        ("animal science", "#9ca3af", "star", [50, 50, 50, 95]),
    ]
    ymax = 350

    def sx(i: int) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / ymax) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">'
        "Total Science Research Submissions by Topic, 2016–2019</text>",
    ]
    for v in range(0, 351, 50):
        y = sy(v)
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<text x="{pad_l-8}" y="{y+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{v}</text>'
        )
    for i, yr in enumerate(years):
        parts.append(
            f'<text x="{sx(i):.1f}" y="{pad_t+plot_h+20}" text-anchor="middle" font-family="{ARIAL}" font-size="12">{yr}</text>'
        )
    for lab, color, marker, vals in series:
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>'
        )
        for i, v in enumerate(vals):
            x, y = sx(i), sy(v)
            if marker == "triangle":
                parts.append(
                    f'<polygon points="{x},{y-5} {x-5},{y+4} {x+5},{y+4}" fill="{color}"/>'
                )
            elif marker == "square":
                parts.append(
                    f'<rect x="{x-4}" y="{y-4}" width="8" height="8" fill="#fff" stroke="{color}" stroke-width="1.5"/>'
                )
            elif marker == "circle":
                parts.append(
                    f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="{color}" stroke-width="1.5"/>'
                )
            else:
                parts.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{color}"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<text x="14" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="{ARIAL}" font-size="11" '
        f'transform="rotate(-90 14 {pad_t+plot_h/2})">Number of submissions</text>'
    )
    parts.append("</svg>")
    write("eng1-q11-science-submissions.svg", "\n".join(parts))


def eng1_q13_forest() -> None:
    W, H = 560, 420
    pad_l, pad_r, pad_t, pad_b = 55, 30, 70, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    years = [1960, 1979, 1986, 2000]
    series = [
        ("Class VIII", "#111", [125, 125, 35, 60]),
        ("Class VI", "#6b7280", [65, 75, 20, 35]),
        ("Class VII", "#9ca3af", [75, 85, 30, 50]),
    ]
    ymax = 150

    def sx(i: int) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / ymax) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{W/2}" y="24" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">'
        "Annual Mean Forest Patch Size for Three Land Use</text>",
        f'<text x="{W/2}" y="42" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">'
        "Capability Classes in the Chorotega Region, Costa Rica</text>",
    ]
    for v in range(0, 151, 25):
        y = sy(v)
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<text x="{pad_l-8}" y="{y+4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{v}</text>'
        )
    for i, yr in enumerate(years):
        parts.append(
            f'<text x="{sx(i):.1f}" y="{pad_t+plot_h+20}" text-anchor="middle" font-family="{ARIAL}" font-size="12">{yr}</text>'
        )
    for lab, color, vals in series:
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>')
        for i, v in enumerate(vals):
            parts.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="4" fill="{color}"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>'
    )
    parts.append(
        f'<text x="14" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="{ARIAL}" font-size="11" '
        f'transform="rotate(-90 14 {pad_t+plot_h/2})">Mean patch size (hectares)</text>'
    )
    lx = pad_l
    for i, (lab, color, _) in enumerate(series):
        x = lx + i * 120
        parts.append(f'<rect x="{x}" y="{H-28}" width="12" height="12" fill="{color}"/>')
        parts.append(f'<text x="{x+18}" y="{H-18}" font-family="{ARIAL}" font-size="11">{lab}</text>')
    parts.append("</svg>")
    write("eng1-q13-forest-patches.svg", "\n".join(parts))


def eng2_q13_table() -> None:
    headers = [
        "Baseline concentration of annual precipitation",
        "% change in water entering aquifers",
        "% change in surface water used for irrigation",
        "% change in groundwater used for irrigation",
    ]
    rows = [
        ["Somewhat concentrated", "4.9", "0.4", "0.9"],
        ["Evenly distributed", "11.0", "9.0", "7.9"],
    ]
    col_w = [220, 120, 150, 160]
    row_h, header_h = 48, 64
    title = "Simulated Change in Annual Aquifer Input and Irrigation Output\nif Precipitation Concentration Increases as Climate Models Predict"
    title_lines = title.split("\n")
    title_block = 18 + len(title_lines) * 18
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{tw/2}" y="{20 + i * 18}" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x, y, w, h, text, header=False):
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 10 if len(text) > 28 else 12
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111"/>'
        )
        # wrap long header roughly
        if header and len(text) > 28:
            words = text.split()
            mid = len(words) // 2
            t1 = " ".join(words[:mid])
            t2 = " ".join(words[mid:])
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700">{esc(t1)}</text>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2+10}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700">{esc(t2)}</text>'
            )
        else:
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
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
    write("eng2-q13-precipitation-irrigation.svg", "\n".join(parts))


def main() -> None:
    eng1_q11_science()
    eng1_q13_forest()
    eng2_q13_table()


if __name__ == "__main__":
    main()
