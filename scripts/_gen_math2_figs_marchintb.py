"""Generate Math Module 2 figures for the 2025-march-int-b mock."""
import os

OUT = "public/mocks/2025-march-int-b/figures"
os.makedirs(OUT, exist_ok=True)
SERIF = 'font-family="Georgia, serif"'


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(path)


# ---------------------------------------------------------------- Q15 table
def q15():
    cw, rh = 90, 56
    x0, y0 = 40, 20
    w, h = cw * 2, rh * 4
    rows = [("x", "y", True), ("\u22122s", "28", False),
            ("\u2212s", "23", False), ("s", "13", False)]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 80}" height="{h + 40}" '
         f'viewBox="0 0 {w + 80} {h + 40}">',
         '<rect width="100%" height="100%" fill="#fff"/>']
    for i in range(5):
        y = y0 + i * rh
        p.append(f'<line x1="{x0}" y1="{y}" x2="{x0 + w}" y2="{y}" stroke="#111"/>')
    for j in range(3):
        x = x0 + j * cw
        p.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0 + h}" stroke="#111"/>')
    for i, (left, right, header) in enumerate(rows):
        y = y0 + i * rh + rh / 2 + 7
        style = ' font-style="italic"' if header else ""
        for j, txt in enumerate((left, right)):
            x = x0 + j * cw + cw / 2
            p.append(f'<text x="{x}" y="{y}" text-anchor="middle" {SERIF} '
                     f'font-size="19"{style}>{txt}</text>')
    p.append("</svg>")
    write("math2-q15-linear-table.svg", "\n".join(p))


# ------------------------------------------------------------ Q17 exp graph
def q17():
    W, H = 425, 380
    xmin, xmax, ymin, ymax = -1.5, 5.5, -5.0, 10.5
    L, R, T, B = 55, 385, 20, 360

    def sx(x):
        return L + (x - xmin) / (xmax - xmin) * (R - L)

    def sy(y):
        return B - (y - ymin) / (ymax - ymin) * (B - T)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">',
         '<rect width="100%" height="100%" fill="#fff"/>']
    for gx in range(-1, 6):
        p.append(f'<line x1="{sx(gx):.1f}" y1="{T}" x2="{sx(gx):.1f}" y2="{B}" stroke="#e5e7eb"/>')
    for gy in range(-4, 11):
        p.append(f'<line x1="{L}" y1="{sy(gy):.1f}" x2="{R}" y2="{sy(gy):.1f}" stroke="#e5e7eb"/>')
    # axes with arrowheads
    p.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{R + 8}" y2="{sy(0):.1f}" stroke="#111"/>')
    p.append(f'<line x1="{sx(0):.1f}" y1="{B}" x2="{sx(0):.1f}" y2="{T - 8}" stroke="#111"/>')
    p.append(f'<polygon points="{R + 14},{sy(0):.1f} {R + 6},{sy(0) - 4:.1f} '
             f'{R + 6},{sy(0) + 4:.1f}" fill="#111"/>')
    p.append(f'<polygon points="{sx(0):.1f},{T - 14} {sx(0) - 4:.1f},{T - 6} '
             f'{sx(0) + 4:.1f},{T - 6}" fill="#111"/>')
    # curve y = -6^x + 9, clipped to the plot box
    pts = []
    steps = 400
    for i in range(steps + 1):
        x = xmin + (xmax - xmin) * i / steps
        y = -(6 ** x) + 9
        if y < ymin:
            break
        if y <= ymax:
            pts.append(f"{sx(x):.1f},{sy(y):.1f}")
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>')
    # ticks + labels
    for gx in [-1, 1, 2, 3, 4, 5]:
        p.append(f'<line x1="{sx(gx):.1f}" y1="{sy(0) - 4:.1f}" x2="{sx(gx):.1f}" '
                 f'y2="{sy(0) + 4:.1f}" stroke="#111"/>')
        p.append(f'<text x="{sx(gx):.1f}" y="{sy(0) + 19:.1f}" text-anchor="middle" '
                 f'{SERIF} font-size="12">{gx}</text>')
    for gy in [-4, -2, 2, 4, 6, 8, 10]:
        p.append(f'<line x1="{sx(0) - 4:.1f}" y1="{sy(gy):.1f}" x2="{sx(0) + 4:.1f}" '
                 f'y2="{sy(gy):.1f}" stroke="#111"/>')
        p.append(f'<text x="{sx(0) - 8:.1f}" y="{sy(gy) + 4:.1f}" text-anchor="end" '
                 f'{SERIF} font-size="12">{gy}</text>')
    p.append(f'<text x="{sx(0) - 16:.1f}" y="{sy(0) + 19:.1f}" {SERIF} font-size="12" '
             f'font-style="italic">O</text>')
    p.append(f'<text x="{R + 20}" y="{sy(0) + 5:.1f}" {SERIF} font-size="15" '
             f'font-style="italic">x</text>')
    p.append(f'<text x="{sx(0) + 8:.1f}" y="{T - 10}" {SERIF} font-size="15" '
             f'font-style="italic">y</text>')
    p.append("</svg>")
    write("math2-q17-exponential-graph.svg", "\n".join(p))


# ------------------------------------------------- Q18 intersecting triangles
def q18():
    Lp, M, Rp = (30, 110), (95, 40), (165, 110)
    P, Q = (294.5, 239.5), (414.8, 110)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="460" height="300" '
         'viewBox="0 0 460 300">',
         '<rect width="100%" height="100%" fill="#fff"/>']
    seg = lambda a, b: (f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
                        f'stroke="#111" stroke-width="2"/>')
    p += [seg(Lp, Q), seg(M, P), seg(Lp, M), seg(P, Q)]
    labels = [("L", Lp[0] - 18, Lp[1] + 5), ("M", M[0] - 6, M[1] - 10),
              ("R", Rp[0] - 8, Rp[1] - 10), ("Q", Q[0] + 8, Q[1] + 5),
              ("P", P[0] - 5, P[1] + 22)]
    for txt, x, y in labels:
        p.append(f'<text x="{x}" y="{y}" {SERIF} font-size="17" font-style="italic">{txt}</text>')
    p.append(f'<text x="230" y="288" text-anchor="middle" {SERIF} font-size="13">'
             f'Note: Figure not drawn to scale.</text>')
    p.append("</svg>")
    write("math2-q18-intersecting-triangles.svg", "\n".join(p))


q15()
q17()
q18()
