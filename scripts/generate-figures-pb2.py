#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 2 (ElitePractice X2)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-2/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math1_q01_right_triangle() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="80,260 80,80 340,260" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="80" y="240" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="68" y="70" font-family="Arial" font-size="18" font-weight="700">A</text>
  <text x="62" y="280" font-family="Arial" font-size="18" font-weight="700">B</text>
  <text x="350" y="280" font-family="Arial" font-size="18" font-weight="700">C</text>
  <text x="95" y="150" font-family="Arial" font-size="16">56°</text>
  <text x="210" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q02_isosceles() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="210,50 60,250 360,250" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="200" y="280" font-family="Arial" font-size="18" font-style="italic">x</text>
  <text x="110" y="150" font-family="Arial" font-size="18" font-style="italic">y</text>
  <text x="300" y="150" font-family="Arial" font-size="18" font-style="italic">y</text>
  <text x="210" y="305" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q06_linear_graph() -> str:
    W, H = 440, 400
    pad_l, pad_r, pad_t, pad_b = 40, 30, 20, 30
    # x from -9 to 9, y from -11 to 3
    x0, x1, y0, y1 = -9.0, 9.0, -11.0, 3.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * (W - pad_l - pad_r)

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * (H - pad_t - pad_b)

    parts: list[str] = []
    # grid every 1
    for i in range(-9, 10):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(3)}" x2="{sx(i)}" y2="{sy(-11)}" stroke="#e5e7eb"/>'
        )
    for j in range(-11, 4):
        parts.append(
            f'<line x1="{sx(-9)}" y1="{sy(j)}" x2="{sx(9)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    # axes
    parts.append(
        f'<line x1="{sx(-9)}" y1="{sy(0)}" x2="{sx(9)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(3)}" x2="{sx(0)}" y2="{sy(-11)}" stroke="#111" stroke-width="1.5"/>'
    )
    # arrowheads
    parts.append(
        f'<polygon points="{sx(9)},{sy(0)} {sx(9)-10},{sy(0)-5} {sx(9)-10},{sy(0)+5}" fill="#111"/>'
    )
    parts.append(
        f'<polygon points="{sx(0)},{sy(3)} {sx(0)-5},{sy(3)+10} {sx(0)+5},{sy(3)+10}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{sx(9)+8}" y="{sy(0)+4}" font-family="Arial" font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0)+8}" y="{sy(3)+14}" font-family="Arial" font-size="14" font-style="italic">y</text>'
    )
    for i in range(-8, 9, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(-10, 3, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    # line through (-6,-8) and (6,-6): y = (1/6)x - 7
    # extend across visible x
    xa, xb = -9.0, 9.0
    ya, yb = (1 / 6) * xa - 7, (1 / 6) * xb - 7
    parts.append(
        f'<line x1="{sx(xa)}" y1="{sy(ya)}" x2="{sx(xb)}" y2="{sy(yb)}" stroke="#111" stroke-width="2.5"/>'
    )
    for px, py in [(-6, -8), (6, -6)]:
        parts.append(
            f'<circle cx="{sx(px)}" cy="{sy(py)}" r="4" fill="#111"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q09_parallels() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="320" viewBox="0 0 460 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="90" x2="400" y2="90" stroke="#111" stroke-width="2"/>
  <line x1="40" y1="210" x2="400" y2="210" stroke="#111" stroke-width="2"/>
  <line x1="140" y1="40" x2="300" y2="260" stroke="#111" stroke-width="2"/>
  <text x="410" y="95" font-family="Arial" font-size="16" font-style="italic">r</text>
  <text x="410" y="215" font-family="Arial" font-size="16" font-style="italic">s</text>
  <text x="305" y="250" font-family="Arial" font-size="16" font-style="italic">t</text>
  <text x="250" y="78" font-family="Arial" font-size="15">x°</text>
  <text x="255" y="198" font-family="Arial" font-size="15">44°</text>
  <text x="230" y="300" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q15_histograms() -> str:
    W, H = 420, 520
    pad_l, pad_r = 50, 30
    plot_w = W - pad_l - pad_r
    plot_h = 180
    bins = [15, 20, 25, 30, 35, 40, 45, 50]
    team_a = [10, 15, 30, 50, 30, 15, 10]
    team_b = [30, 25, 15, 10, 15, 25, 30]

    def panel(title: str, freqs: list[int], top: int) -> str:
        parts = [
            f'<text x="{pad_l}" y="{top - 10}" font-family="Arial" font-size="14" font-weight="700">{title}</text>'
        ]
        for v in range(0, 51, 10):
            y = top + plot_h - (v / 50) * plot_h
            parts.append(
                f'<line x1="{pad_l}" y1="{y}" x2="{pad_l + plot_w}" y2="{y}" stroke="#e5e7eb"/>'
                f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
            )
        bw = plot_w / 7
        for i, f in enumerate(freqs):
            h = (f / 50) * plot_h
            x = pad_l + i * bw
            y = top + plot_h - h
            parts.append(
                f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="#fff" stroke="#111" stroke-width="1.5"/>'
            )
        parts.append(
            f'<line x1="{pad_l}" y1="{top}" x2="{pad_l}" y2="{top + plot_h}" stroke="#111"/>'
            f'<line x1="{pad_l}" y1="{top + plot_h}" x2="{pad_l + plot_w}" y2="{top + plot_h}" stroke="#111"/>'
        )
        for i, lab in enumerate(bins):
            x = pad_l + i * (plot_w / 7)
            parts.append(
                f'<text x="{x}" y="{top + plot_h + 16}" text-anchor="middle" font-family="Arial" font-size="11">{lab}</text>'
            )
        parts.append(
            f'<text x="{pad_l + plot_w / 2}" y="{top + plot_h + 32}" text-anchor="middle" font-family="Arial" font-size="12">Score</text>'
            f'<text x="14" y="{top + plot_h / 2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 14 {top + plot_h / 2})">Frequency</text>'
        )
        return "\n".join(parts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {panel("Team A", team_a, 40)}
  {panel("Team B", team_b, 300)}
</svg>'''


def eng1_q10_employment() -> str:
    """Employment line graph Czech Republic vs Austria 1995-2013."""
    W, H = 560, 380
    pad_l, pad_r, pad_t, pad_b = 60, 30, 70, 60
    years = [1995, 1998, 2001, 2004, 2007, 2010, 2013]
    # Approximate from visual: CZ ~225→125 declining; AT flat ~50
    cz = [225, 205, 185, 165, 150, 135, 125]
    at = [50, 50, 50, 50, 50, 50, 50]
    y_max = 250

    def sx(i: int) -> float:
        return pad_l + i / (len(years) - 1) * (W - pad_l - pad_r)

    def sy(v: float) -> float:
        return pad_t + (1 - v / y_max) * (H - pad_t - pad_b)

    parts = [
        f'<text x="{W/2}" y="28" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">Employment in Agriculture, Hunting, and Forestry</text>',
        f'<text x="{W/2}" y="48" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">in the Czech Republic and Austria, 1995–2013</text>',
    ]
    for v in range(0, 251, 25):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{W-pad_r}" y2="{sy(v)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    # CZ solid
    pts_cz = " ".join(f"{sx(i)},{sy(cz[i])}" for i in range(len(years)))
    parts.append(f'<polyline points="{pts_cz}" fill="none" stroke="#111" stroke-width="2"/>')
    for i in range(len(years)):
        parts.append(f'<circle cx="{sx(i)}" cy="{sy(cz[i])}" r="4" fill="#111"/>')
    # AT dashed
    pts_at = " ".join(f"{sx(i)},{sy(at[i])}" for i in range(len(years)))
    parts.append(
        f'<polyline points="{pts_at}" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
    )
    for i in range(len(years)):
        parts.append(
            f'<rect x="{sx(i)-3}" y="{sy(at[i])-3}" width="6" height="6" fill="#fff" stroke="#111"/>'
        )
    for i, y in enumerate(years):
        parts.append(
            f'<text x="{sx(i)}" y="{H-pad_b+18}" text-anchor="middle" font-family="Arial" font-size="11">{y}</text>'
        )
    parts.append(
        f'<text x="{(pad_l+W-pad_r)/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="12">Year</text>'
        f'<text x="16" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 {(pad_t+H-pad_b)/2})">Number of employees (in thousands)</text>'
    )
    # legend
    lx, ly = pad_l + 20, pad_t + 20
    parts.append(
        f'<line x1="{lx}" y1="{ly}" x2="{lx+30}" y2="{ly}" stroke="#111" stroke-width="2"/>'
        f'<circle cx="{lx+15}" cy="{ly}" r="3" fill="#111"/>'
        f'<text x="{lx+38}" y="{ly+4}" font-family="Arial" font-size="12">Czech Republic</text>'
        f'<line x1="{lx}" y1="{ly+20}" x2="{lx+30}" y2="{ly+20}" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
        f'<rect x="{lx+12}" y="{ly+17}" width="6" height="6" fill="#fff" stroke="#111"/>'
        f'<text x="{lx+38}" y="{ly+24}" font-family="Arial" font-size="12">Austria</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q08_orangutan() -> str:
    W, H = 520, 360
    # Categories: MD shared with ID | ID not shared with MD
    # male (17) light, female (5) dark
    # Values from page: MD shared male~18 female~65; ID not shared male~20 female~8
    cats = ["MD shared with ID", "ID not shared with MD"]
    male = [18, 20]
    female = [65, 8]
    pad_l, pad_r, pad_t, pad_b = 60, 30, 70, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 70

    def sy(v: float) -> float:
        return pad_t + (1 - v / y_max) * plot_h

    parts = [
        f'<text x="{W/2}" y="24" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">Average Overlap between Immature Orangutans&#8217; Diets (ID)</text>',
        f'<text x="{W/2}" y="44" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">and Their Mothers&#8217; Diets (MD)</text>',
    ]
    for v in range(0, 71, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{W-pad_r}" y2="{sy(v)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    group_w = plot_w / 2
    bar_w = group_w * 0.28
    for i, cat in enumerate(cats):
        gx = pad_l + i * group_w
        # male light gray
        x1 = gx + group_w * 0.22
        h1 = (male[i] / y_max) * plot_h
        parts.append(
            f'<rect x="{x1}" y="{sy(male[i])}" width="{bar_w}" height="{h1}" fill="#d1d5db" stroke="#111"/>'
        )
        # female black
        x2 = gx + group_w * 0.52
        h2 = (female[i] / y_max) * plot_h
        parts.append(
            f'<rect x="{x2}" y="{sy(female[i])}" width="{bar_w}" height="{h2}" fill="#111" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{gx + group_w/2}" y="{H-pad_b+28}" text-anchor="middle" font-family="Arial" font-size="12">{cat}</text>'
        )
    parts.append(
        f'<text x="16" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 {(pad_t+H-pad_b)/2})">% of diet</text>'
    )
    # legend
    lx, ly = W - 200, pad_t + 10
    parts.append(
        f'<rect x="{lx}" y="{ly}" width="14" height="14" fill="#d1d5db" stroke="#111"/>'
        f'<text x="{lx+20}" y="{ly+12}" font-family="Arial" font-size="12">individual 17 (male)</text>'
        f'<rect x="{lx}" y="{ly+22}" width="14" height="14" fill="#111" stroke="#111"/>'
        f'<text x="{lx+20}" y="{ly+34}" font-family="Arial" font-size="12">individual 5 (female)</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_investors() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="220" viewBox="0 0 520 220">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="260" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Year That Foreign Investors Were First Allowed to Purchase Shares</text>
  <rect x="40" y="50" width="220" height="36" fill="#f3f4f6" stroke="#111"/>
  <rect x="260" y="50" width="220" height="36" fill="#f3f4f6" stroke="#111"/>
  <text x="150" y="74" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">Country</text>
  <text x="370" y="74" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">Year</text>
  <rect x="40" y="86" width="220" height="36" fill="#fff" stroke="#111"/>
  <rect x="260" y="86" width="220" height="36" fill="#fff" stroke="#111"/>
  <text x="150" y="110" text-anchor="middle" font-family="Georgia, serif" font-size="13">India</text>
  <text x="370" y="110" text-anchor="middle" font-family="Georgia, serif" font-size="13">1986</text>
  <rect x="40" y="122" width="220" height="36" fill="#fff" stroke="#111"/>
  <rect x="260" y="122" width="220" height="36" fill="#fff" stroke="#111"/>
  <text x="150" y="146" text-anchor="middle" font-family="Georgia, serif" font-size="13">Morocco</text>
  <text x="370" y="146" text-anchor="middle" font-family="Georgia, serif" font-size="13">1988</text>
  <rect x="40" y="158" width="220" height="36" fill="#fff" stroke="#111"/>
  <rect x="260" y="158" width="220" height="36" fill="#fff" stroke="#111"/>
  <text x="150" y="182" text-anchor="middle" font-family="Georgia, serif" font-size="13">Indonesia</text>
  <text x="370" y="182" text-anchor="middle" font-family="Georgia, serif" font-size="13">1989</text>
</svg>'''


def math2_q06_triangle() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="80,260 80,80 340,260" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="80" y="240" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="68" y="70" font-family="Arial" font-size="18" font-weight="700">X</text>
  <text x="62" y="280" font-family="Arial" font-size="18" font-weight="700">Y</text>
  <text x="350" y="280" font-family="Arial" font-size="18" font-weight="700">Z</text>
  <text x="250" y="245" font-family="Arial" font-size="16">35°</text>
  <text x="210" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q10_pyramid() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <path d="M 80,240 L 260,240 L 320,190 L 140,190 Z" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="140" y1="190" x2="80" y2="240" stroke="#111" stroke-width="1.5" stroke-dasharray="5 4"/>
  <line x1="140" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="320" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="80" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="260" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="200" y1="60" x2="200" y2="215" stroke="#111" stroke-width="1.5" stroke-dasharray="5 4"/>
  <rect x="200" y="201" width="12" height="12" fill="none" stroke="#111"/>
  <text x="165" y="265" font-family="Arial" font-size="16" font-style="italic">l</text>
  <text x="295" y="225" font-family="Arial" font-size="16" font-style="italic">w</text>
  <text x="210" y="140" font-family="Arial" font-size="16" font-style="italic">h</text>
  <text x="210" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q21_freq_tables() -> str:
    def table(title: str, x0: int, rows: list[tuple[str, str]]) -> str:
        parts = [
            f'<text x="{x0 + 120}" y="28" text-anchor="middle" font-family="Arial" font-size="14" font-weight="700">{title}</text>',
            f'<rect x="{x0}" y="44" width="120" height="32" fill="#f3f4f6" stroke="#111"/>',
            f'<rect x="{x0+120}" y="44" width="120" height="32" fill="#f3f4f6" stroke="#111"/>',
            f'<text x="{x0+60}" y="66" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Value</text>',
            f'<text x="{x0+180}" y="66" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Frequency</text>',
        ]
        for i, (val, freq) in enumerate(rows):
            y = 76 + i * 32
            parts.append(f'<rect x="{x0}" y="{y}" width="120" height="32" fill="#fff" stroke="#111"/>')
            parts.append(f'<rect x="{x0+120}" y="{y}" width="120" height="32" fill="#fff" stroke="#111"/>')
            parts.append(f'<text x="{x0+60}" y="{y+22}" text-anchor="middle" font-family="Arial" font-size="13">{val}</text>')
            parts.append(f'<text x="{x0+180}" y="{y+22}" text-anchor="middle" font-family="Arial" font-size="13">{freq}</text>')
        return "\n".join(parts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="220" viewBox="0 0 560 220">
  <rect width="100%" height="100%" fill="#fff"/>
  {table("Data Set A", 20, [("c", "12"), ("2c", "21"), ("3c", "30")])}
  {table("Data Set B", 300, [("c", "30"), ("2c", "21"), ("3c", "12")])}
</svg>'''


def math2_q22_circle() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="400" viewBox="0 0 420 400">
  <rect width="100%" height="100%" fill="#fff"/>
  <circle cx="210" cy="190" r="140" fill="none" stroke="#111" stroke-width="2"/>
  <!-- points approx on circle -->
  <circle cx="120" cy="100" r="3" fill="#111"/><text x="100" y="95" font-family="Arial" font-size="16">B</text>
  <circle cx="100" cy="200" r="3" fill="#111"/><text x="78" y="205" font-family="Arial" font-size="16">A</text>
  <circle cx="140" cy="300" r="3" fill="#111"/><text x="120" y="320" font-family="Arial" font-size="16">E</text>
  <circle cx="340" cy="190" r="3" fill="#111"/><text x="350" y="195" font-family="Arial" font-size="16">C</text>
  <!-- chords AC and BE intersect at D -->
  <line x1="100" y1="200" x2="340" y2="190" stroke="#111" stroke-width="2"/>
  <line x1="120" y1="100" x2="140" y2="300" stroke="#111" stroke-width="2"/>
  <line x1="120" y1="100" x2="100" y2="200" stroke="#111" stroke-width="1.5"/>
  <line x1="120" y1="100" x2="340" y2="190" stroke="#111" stroke-width="1.5"/>
  <circle cx="128" cy="185" r="3" fill="#111"/><text x="138" y="175" font-family="Arial" font-size="16">D</text>
  <rect x="128" y="185" width="12" height="12" fill="none" stroke="#111" transform="rotate(-5 128 185)"/>
  <text x="210" y="380" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def main() -> None:
    write("math1-q01-right-triangle.svg", math1_q01_right_triangle())
    write("math1-q02-isosceles-triangle.svg", math1_q02_isosceles())
    write("math1-q06-linear-graph.svg", math1_q06_linear_graph())
    write("math1-q09-parallel-lines.svg", math1_q09_parallels())
    write("math1-q15-histograms.svg", math1_q15_histograms())
    write("eng1-q10-employment-agriculture.svg", eng1_q10_employment())
    write("eng2-q08-orangutan-diet.svg", eng2_q08_orangutan())
    write("eng2-q11-foreign-investors.svg", eng2_q11_investors())
    write("math2-q06-right-triangle.svg", math2_q06_triangle())
    write("math2-q10-pyramid.svg", math2_q10_pyramid())
    write("math2-q21-frequency-tables.svg", math2_q21_freq_tables())
    write("math2-q22-circle-chords.svg", math2_q22_circle())
    print("done all purplebook-test-2 figures")


if __name__ == "__main__":
    main()

