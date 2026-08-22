#!/usr/bin/env python3
"""Clean SAT-style SVGs for 2026 August Module 1 (R&W graph + table)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-august-m1/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def nitrogen_bars() -> str:
    W, H = 560, 430
    pad_l, pad_r, pad_t, pad_b = 78, 28, 62, 78
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 70

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / ymax) * plot_h

    grid = []
    ylabels = []
    for i in range(0, 8):
        v = i * 10
        y = sy(v)
        grid.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{pad_l + plot_w}" y2="{y}" stroke="#d1d5db" stroke-width="1" stroke-dasharray="3 3"/>'
        )
        ylabels.append(
            f'<text x="{pad_l - 10}" y="{y + 4}" text-anchor="end" font-family="Arial, sans-serif" font-size="12">{v}</text>'
        )

    cats = [
        ("Low\n(5 mg/kg)", 15),
        ("Moderate\n(20 mg/kg)", 45),
        ("High\n(50 mg/kg)", 65),
    ]
    bw = 70
    gap = 48
    total_w = 3 * bw + 2 * gap
    start_x = pad_l + (plot_w - total_w) / 2
    bars = []
    xlabs = []
    for i, (label, val) in enumerate(cats):
        x = start_x + i * (bw + gap)
        y = sy(val)
        h = pad_t + plot_h - y
        bars.append(
            f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="#93c5fd" stroke="#111" stroke-width="1.4"/>'
        )
        lines = label.split("\n")
        xlabs.append(
            f'<text x="{x + bw / 2}" y="{pad_t + plot_h + 20}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{lines[0]}</text>'
            f'<text x="{x + bw / 2}" y="{pad_t + plot_h + 36}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11">{lines[1]}</text>'
        )

    mid_y = pad_t + plot_h / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W / 2}" y="24" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">Symbiotic Nitrogen Fixation Rate</text>
  <text x="{W / 2}" y="44" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">Under Varying Soil Phosphorus Levels</text>
  {"".join(grid)}
  {"".join(ylabels)}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>
  {"".join(xlabs)}
  <text x="18" y="{mid_y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" transform="rotate(-90 18 {mid_y})">Nitrogen fixation rate (µmol N₂/plant/h)</text>
</svg>'''


def tree_ring_table() -> str:
    title = "Mean Annual Tree-Ring Width Anomalies for Siberian Larch Following Major Volcanic Eruptions"
    headers = [
        "Volcanic Event",
        "Eruption Year",
        "Year +1 Ring Width Anomaly (mm)",
        "Year +2 Ring Width Anomaly (mm)",
        "Year +3 Ring Width Anomaly (mm)",
    ]
    rows = [
        ["Kuwae", "1453", "−0.42", "−0.68", "−0.25"],
        ["Huaynaputina", "1600", "−0.81", "−0.54", "−0.18"],
        ["Tambora", "1815", "−0.95", "−0.72", "−0.31"],
        ["Krakatoa", "1883", "−0.36", "−0.22", "+0.04"],
    ]
    widths = [150, 110, 150, 150, 150]
    width = sum(widths) + 40
    row_h = 44
    header_h = 58
    title_h = 56
    height = title_h + header_h + row_h * len(rows) + 24
    x0 = 20
    y0 = title_h

    def wrap_header(text: str, max_chars: int = 16) -> list[str]:
        words = text.split()
        lines: list[str] = []
        cur = ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if len(trial) > max_chars and cur:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines

    header_cells = []
    x = x0
    for i, h in enumerate(headers):
        header_cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{header_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
        )
        lines = wrap_header(h, 14 if i > 1 else 16)
        start = y0 + 18 if len(lines) == 2 else y0 + 22 if len(lines) == 3 else y0 + 34
        if len(lines) == 3:
            start = y0 + 16
        elif len(lines) == 2:
            start = y0 + 22
        for li, ln in enumerate(lines):
            header_cells.append(
                f'<text x="{x + widths[i] / 2}" y="{start + li * 14}" text-anchor="middle" font-family="Georgia, serif" font-size="11" font-weight="700">{ln}</text>'
            )
        x += widths[i]

    body_cells = []
    for r, row in enumerate(rows):
        y = y0 + header_h + row_h * r
        x = x0
        for i, cell in enumerate(row):
            body_cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 28}" text-anchor="middle" font-family="Georgia, serif" font-size="13">{cell}</text>'
            )
            x += widths[i]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{width / 2}" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Mean Annual Tree-Ring Width Anomalies for Siberian Larch</text>
  <text x="{width / 2}" y="42" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Following Major Volcanic Eruptions</text>
  {"".join(header_cells)}
  {"".join(body_cells)}
</svg>'''


if __name__ == "__main__":
    write("eng1-q11-graph.svg", nitrogen_bars())
    write("eng1-q12-table.svg", tree_ring_table())
