"""Generate Reading & Writing Module 2 figures for the 2025-march-us-b mock.

    py -3 scripts/generate-figures-2025-march-us-b-rw2.py

Figures:
  Q11 Iigaya grouped bar graph (PDF page 38)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-us-b" / "figures"

FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", path.name)


def iigaya_art_ratings() -> None:
    # Measured from page-38.png. Y-axis 0–0.6, grid every 0.1.
    # Legend below the x-axis: P6 (dark gray), P1 (light gray), P2 (black).
    # Impressionist: P6 0.38, P1 0.58, P2 0.09
    # Cubist:        P6 0.27, P1 0.37, P2 0.22
    W, H = 540, 420
    pad_l, pad_r, pad_t, pad_b = 60, 30, 70, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 0.6
    cats = ["Impressionist", "Cubist"]
    series = [
        ("P6", "#4b5563", [0.38, 0.27]),
        ("P1", "#d1d5db", [0.58, 0.37]),
        ("P2", "#111111", [0.09, 0.22]),
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
    for i in range(0, 7):
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
    parts.append(
        f'<text x="{W/2}" y="{pad_t+plot_h+42}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Painting style</text>'
    )
    lx = pad_l + 80
    ly = H - 22
    for si, (lab, fill, _) in enumerate(series):
        x = lx + si * 90
        parts.append(f'<rect x="{x}" y="{ly-10}" width="14" height="14" fill="{fill}" stroke="#111"/>')
        parts.append(f'<text x="{x+20}" y="{ly+2}" font-family="{ARIAL}" font-size="12">{lab}</text>')
    parts.append("</svg>")
    write(OUT / "eng2-q11-painting-style-correlation.svg", parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    iigaya_art_ratings()


if __name__ == "__main__":
    main()
